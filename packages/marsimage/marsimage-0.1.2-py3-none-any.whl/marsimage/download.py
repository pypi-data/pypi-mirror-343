"""Download images from the PDS archive."""

import concurrent.futures
import logging
import os
import re
import time
from pathlib import Path
from time import sleep

import pandas as pd
import requests
from tqdm.auto import tqdm

from .filename import Filename

logger = logging.getLogger(__name__)

# url
PDS3_URL = 'https://planetarydata.jpl.nasa.gov/w10n/msl/'  # The MSL PDS3 archive
PDS4_URL = (
    'https://planetarydata.jpl.nasa.gov/w10n/msl/msl_mmm/'  # New MMM PDS4 bundle since release 33
)

PDS3_END = 3644  # PDS3 was used until Sol 3644
PDS4_START = 3570  # PDS4 was used from Sol 3570

# check if directories exists, if not create them
CAM_LIST = ['mastcam', 'mahli', 'navcam', 'mardi', 'hazcam']
CAM_IDS = {
    'mastcam': 'MSLMST',
    'mahli': 'MSLMHL',
    'navcam': 'MSLNAV_1',
    'mardi': 'MSLMRD',
    'hazcam': 'MSLHAZ_1',
}

MSL_PROD_FILTER = ['DRXX', 'RAD_', 'MXY_']  # radiometrically calibrated, non linearized images

TIMEOUT = 600  # 10 minutes


def _urljoin(*args):
    """Join given arguments into an url.

    Trailing but not leading slashes are stripped for each argument.
    """
    # https://stackoverflow.com/questions/1793261/how-to-join-components-of-a-path-when-you-are-constructing-a-url-in-python
    return '/'.join(str(x).rstrip('/') for x in args)


def _get_json(url, retries=3):
    """Fetch JSON data from a PDS W10N url with retries.

    Parameters
    ----------
    url : str
        The URL to fetch JSON data from.
    retries : int, optional
        The number of retry attempts in case of a timeout, by default 3.

    Returns
    -------
    dict
        The JSON data fetched from the URL.
    """
    for attempt in range(retries):
        try:
            response = requests.get(url + '/?output=json', timeout=TIMEOUT)
            response.raise_for_status()
            return response.json()
        except (
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
        ) as e:
            # if not a timeout, log the error and return an empty dictionary
            if response.status_code not in {408, 504, 502}:  # timeout status codes
                logger.debug(f'Error {response.status_code} occurred for URL: {url}. Skipping...')
                return {'nodes': {}, 'leaves': {}}
            logger.debug(
                f'Error occurred for URL: {url}. Retrying {attempt + 1}/{retries}... Error: {e}'
            )
            sleep(4**attempt)  # exponential backoff to avoid overloading the server
            if attempt == retries - 1:
                logger.error(f'Failed to fetch data from URL: {url}. {e}')
    return {'nodes': {}, 'leaves': {}}


def _msl_index_pds3_folders(camera, sol_list=None):
    """Build PDS3 folder index for the selected instrument ID.

    PDS3 was used until release 32, or Sol 3644. Since Sol 3570, PDS4 is used for MMM cameras.

    Parameters
    ----------
    camera : str
        Instrument name
    sol_list : dict, optional
        Existing dictionary of sols and their URLs, by default None
    """
    try:
        mission_node = _get_json(PDS3_URL)  # get mission root page
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout occurred for URL: {PDS3_URL}. {e}')
        mission_node = {}
    if sol_list is None:
        sol_list = {}
    cam_id = CAM_IDS[camera]
    bundle_nodes = [node for node in mission_node['nodes'] if cam_id in node['name']]
    for bundle_node in tqdm(
        bundle_nodes, desc='PDS3 Sol index', leave=False
    ):  # iterate over each folder and append instrument specific data urls  # noqa: PLR1702
        bundle_name = bundle_node['name']
        if 'MSLHAZ' in cam_id:
            data_urls = [_urljoin(PDS3_URL, bundle_name + '/DATA/')]
        elif 'MSLNAV' in cam_id:
            data_urls = [
                _urljoin(PDS3_URL, bundle_name + '/DATA/'),
                _urljoin(PDS3_URL, bundle_name + '/DATA_V1/'),
            ]
        else:
            data_urls = [_urljoin(PDS3_URL, bundle_name + '/DATA/RDR/SURFACE/')]

        for data_url in data_urls:
            logger.debug(f'Indexing {data_url}')
            data_node = _get_json(data_url)
            for sol_node in data_node['nodes']:
                sol_name = sol_node['name']
                # get sol number with regex expression \d+ (one or more digits)
                nsol = re.search(r'\d+', sol_name).group()
                nsol = nsol.zfill(5)  # pad sol number with zeros
                sol_url = _urljoin(data_url, sol_name)  # get full SOL folder url
                if nsol not in sol_list:  # check that sol is not already in list and add url
                    sol_list[nsol] = [sol_url]
                elif (
                    sol_url not in sol_list[nsol]
                ):  # otherwise add new url to existing sol (in case of data updates)
                    sol_list[nsol].append(sol_url)
    return sol_list


# sort the PDS by sol number for a given image product
def _mmm_index_pds4_folders(camera, sol_list=None):
    """Build PDS4 folder index for the selected instrument ID.

    PDS3 was used until release 32, or Sol 3644. Since Sol 3570, PDS4 is used for MMM cameras.

    Parameters
    ----------
    camera : str
        Instrument name
    sol_list : dict, optional
        Existing dictionary of sols and their URLs, by default None
    """
    try:
        mmm_node = _get_json(PDS4_URL)  # get mission root page
    except requests.exceptions.Timeout as e:
        logger.error(f'Timeout occurred for URL: {PDS3_URL}. {e}')
        mmm_node = {}
    if sol_list is None:
        sol_list = {}
    cam_id = CAM_IDS[camera]
    collection_nodes = [node for node in mmm_node['nodes'] if f'data_{cam_id}' in node['name']]
    for collection in (
        collection_nodes
    ):  # iterate over each folder and append instrument specific data urls  # noqa: PLR1702
        collection_name = collection['name']
        collection_url = _urljoin(PDS4_URL, collection_name)
        logger.debug(f'Indexing {collection_url}')
        collection_node = _get_json(collection_url)
        volume_list = [
            volume for volume in collection_node['nodes'] if 'calibrated' in volume['name']
        ]
        for volume in tqdm(volume_list, desc='PDS4 Sol index', leave=False):
            data_url = _urljoin(collection_url, volume['name'] + '/SURFACE/')
            logger.debug(f'Indexing {data_url}')
            data_node = _get_json(data_url)
            for sol_node in data_node['nodes']:
                sol_name = sol_node['name']
                # get sol number with regex expression \d+ (one or more digits)
                nsol = re.search(r'\d+', sol_name).group()
                nsol = nsol.zfill(5)  # pad sol number with zeros
                sol_url = _urljoin(data_url, sol_name)  # get full SOL folder url
                if nsol not in sol_list:  # check that sol is not already in list and add url
                    sol_list[nsol] = [sol_url]
                elif (
                    sol_url not in sol_list[nsol]
                ):  # otherwise add new url to existing sol (in case of data updates)
                    sol_list[nsol].append(sol_url)
    return sol_list


def _msl_index_pds_folders(camera, sol_start=None, sol_end=None):
    """Build PDS folder index for the selected instrument ID.

    Will index PDS3, PDS4, or both, depending on the sol range and camera.
    If no sol range is given, it will index both PDS3 and PDS4.

    Parameters
    ----------
    camera : str
        Instrument name
    sol_start : int
        Starting sol number
    sol_end : int
        Ending sol number
    """
    # for MMM cameras possibly check both PDS3 and PDS4 bundles
    if camera in {'mastcam', 'mahli', 'mardi'}:
        if sol_end < PDS4_START and sol_end is not None:
            return _msl_index_pds3_folders(camera)
        if sol_start >= PDS3_END and sol_start is not None:
            return _mmm_index_pds4_folders(camera)
        return _mmm_index_pds4_folders(camera, _msl_index_pds3_folders(camera))
    # for HAZCAM and NAVCAM only check PDS3
    return _msl_index_pds3_folders(camera)


def _msl_index_singlesol_products(
    camera,
    folder_urls,
    sol,
    product_filter=MSL_PROD_FILTER,
    remove_thumbnails=True,
    find_best=True,
):
    """Index folders from a single sol for a given camera.

    Parameters
    ----------
    camera : str
        The camera to download images from. Options are 'mastcam
    folder_urls : list of str
        The URLs to the folders to index.
    sol : int
        The sol number.
    product_filter : list, optional
    remove_thumbnails : bool, optional
        If True, remove thumbnails from the index, by default True.
    find_best : bool, optional
        If True, only download the highest quality version of each product, by default True.
        This will also non unique thumbnails.
    """
    if isinstance(folder_urls, str):
        folder_urls = [folder_urls]

    file_index = pd.Index([], name='productid')
    df = pd.DataFrame(
        index=file_index,
        columns=[
            'observation',
            'image',
            'pds3_label',
            'pds4_label',
            'sol',
            'camera',
            'desirability',
            'thumbnail',
        ],
    )

    for folder_url in folder_urls:
        logger.debug(f'Indexing {folder_url}')
        folder_node = _get_json(folder_url)
        for file_leaf in folder_node['leaves']:
            file_name = file_leaf['name']
            fname = Filename(file_name)
            if '.IMG' in file_name:
                df.loc[
                    fname.product_id,
                    ['observation', 'image', 'sol', 'camera', 'desirability', 'thumbnail'],
                ] = (
                    fname._product,
                    _urljoin(folder_url, file_name),
                    sol,
                    camera,
                    fname._desirability,
                    fname.is_thumbnail,
                )
            if '.LBL' in file_name:
                df.loc[fname.product_id, 'pds3_label'] = _urljoin(folder_url, file_name)
            if '.xml' in file_name:
                df.loc[fname.product_id, 'pds4_label'] = _urljoin(folder_url, file_name)

    # only keep rows with highest desirability for each observation
    if find_best:
        df = df.loc[df.groupby('observation')['desirability'].idxmax()]

    # Remove thumbnails
    if remove_thumbnails:
        df = df.loc[df['thumbnail'] == False]  # noqa: E712 Pandas doesn't work with 'is False'

    # filter out products who's productid index does not contain any of the product_filter strings
    if product_filter:
        if isinstance(product_filter, str):
            product_filter = [product_filter]
        df = df.loc[
            df.index.get_level_values('productid').str.contains(
                '|'.join(product_filter), regex=True
            )
        ]

    return df


# download products
def msl_index_products(
    camera,
    sol_start,
    sol_end,
    product_filter=MSL_PROD_FILTER,
    remove_thumbnails=True,
    find_best=True,
):
    """Index products from the PDS archive.

    Warning: This function may fail for very large sol folders (like MSL Navcam),
    because the PDS takes very long to reply to many of these reqests.

    Parameters
    ----------
    camera : str
        The camera to download images from. Options are 'mastcam', 'mahli', 'mardi', 'navcam', 'hazcam'.
    sol_start : int
        The starting sol number.
    sol_end : int
        The ending sol number.
    product_filter : list, optional
        A whitelist of strings to filter the product ids, by default `['DRXX', 'RAD_', 'MXY_']`.
        Only products containing these strings will be downloaded.
        If None, all products will be downloaded.
        TODO implemet regex filtering
    find_best : bool, optional
        If True, only download the highest quality version of each product, by default True.
        This will also remove non unique thumbnails.
    """
    camera = camera.lower()
    if camera not in CAM_LIST:
        raise ValueError(f'Camera incorrect. Available cameras are: {", ".join(CAM_LIST)}')

    # Index data for each folder from sol sol_start to sol sol_end
    sol_list = _msl_index_pds_folders(
        camera, sol_start=sol_start, sol_end=sol_end
    )  # build PDS index for instrument and sol range
    sol_subset = {
        k: v for k, v in sol_list.items() if sol_end >= int(k) >= sol_start
    }  # generate subset of sols to download

    file_index = pd.Index([], name='productid')
    df = pd.DataFrame(
        index=file_index,
        columns=[
            'observation',
            'image',
            'pds3_label',
            'pds4_label',
            'sol',
            'camera',
            'desirability',
            'thumbnail',
        ],
    )

    # iterate over each sol and add image and label files to the dataframe
    for sol in tqdm(sorted(sol_subset), desc='Indexing Products', total=len(sol_subset)):
        sol_df = _msl_index_singlesol_products(
            camera,
            sol_subset[sol],
            sol,
            product_filter=product_filter,
            remove_thumbnails=remove_thumbnails,
            find_best=find_best,
        )
        df = pd.concat([df, sol_df])

        sleep(4)  # sleep between requests to reduce server load

    return df


def download(url, path, skip_existing=True, session=None):
    """Download a file from a URL.

    Parameters
    ----------
    url : str
        The URL to download the file from.
    path : str
        The path to save the file to.
        If a directory is provided, the file will be saved with the same name as the URL.
    skip_existing : bool, optional
        If True, skip downloading if the file already exists, by default True.
    session : requests.Session, optional
        A requests session to use for the download.
        This allows for reusing the same connection for multiple downloads, by default None.

    Returns
    -------
    pathlib.Path
        The path to the downloaded file.
    """
    if session is None:
        session = requests.Session()

    path = Path(path)
    if path.is_dir():
        path = path / Path(url).name

    if skip_existing and path.exists():
        logger.debug(f'Skipping existing file: {path}')
        return path.absolute()
    r = session.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        logger.error(f'Error downloading file: {url}. Status code: {r.status_code}')
    return path.absolute()


def download_pds3(product_url, path, skip_existing=True, session=None):
    """Download a PDS3 product and label from a URL.

    Parameters
    ----------
    product_url : str
        The URL to download the product from.
    path : str
        The path to save the product to.
    skip_existing : bool, optional
        If True, skip downloading if the file already exists, by default True.
    session : requests.Session, optional
        A requests session to use for the download.
        This allows for reusing the same connection for multiple downloads, by default None.

    Returns
    -------
    pathlib.Path
        The path to the downloaded product.
    """
    if session is None:
        session = requests.Session()
        _internal_session = True
    else:
        _internal_session = False

    product = Path(product_url).stem + '.IMG'
    product_url = _urljoin(*product_url.split('/')[:-1], product)
    label = Path(product_url).stem + '.LBL'
    label_url = _urljoin(*product_url.split('/')[:-1], label)

    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)

    if path.suffix == '':
        product_path = path / product
        label_path = path / label
    else:
        raise ValueError('Path must be a directory.')

    try:
        download(label_url, label_path, skip_existing=skip_existing, session=session)
    except requests.exceptions.HTTPError:
        logger.debug(f'Label not found: {label_url}')

    download(product_url, product_path, skip_existing=skip_existing, session=session)

    if _internal_session:
        session.close()
    return product_path


def download_products(
    products_df,
    output_dir='.',
    groupby='sol/camera',
    skip_existing=True,
    pbar=None,
    num_threads=None,
):
    """Download products from the DataFrame.

    Parameters
    ----------
    products_df : pd.DataFrame
        The DataFrame containing the product index created by msl_index_products or msl_index_pds_folders.
    output_dir : str, optional
        The output directory to save the products to, by default '.'.
    groupby : str, optional
        The column to group by, by default 'sol'.
    num_threads : int, optional
        The number of threads to use for downloading, by default number of CPUs.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the paths to the downloaded files.
    """
    download_index = pd.Index([], name='productid')
    files_downloaded = pd.DataFrame(
        index=download_index,
        columns=[
            'observation',
            'image',
            'pds3_label',
            'pds4_label',
            'sol',
            'camera',
            'desirability',
            'thumbnail',
        ],
    )

    session = requests.Session()

    def download2(url, path):
        sleep(0.1)  # sleep to increase interval between requests
        return download(url, path, skip_existing=skip_existing, session=session)

    def download_row(row):
        match groupby:
            case 'sol':
                group = row['sol'].zfill(5)
            case 'sol/camera':
                group = f'{row["sol"].zfill(5)}/{row["camera"].upper()}'
            case 'camera':
                group = row['camera'].upper()
            case 'site':
                raise NotImplementedError('Grouping by site is not yet implemented.')
            case None:
                group = ''
            case _:
                raise ValueError(f'Invalid groupby value: {groupby}')

        folder = Path(output_dir) / group
        folder.mkdir(parents=True, exist_ok=True)

        if pd.notna(row['image']):
            file = download2(row['image'], folder / Path(row['image']).name)
            files_downloaded.loc[
                row.name, ['observation', 'image', 'sol', 'camera', 'desirability', 'thumbnail']
            ] = (
                row['observation'],
                file,
                row['sol'],
                row['camera'],
                row['desirability'],
                row['thumbnail'],
            )

            # if the image exists, also try to download the label
            if pd.notna(row['pds3_label']):
                file = download2(row['pds3_label'], folder / Path(row['pds3_label']).name)
                files_downloaded.loc[row.name, 'pds3_label'] = file
            if pd.notna(row['pds4_label']):
                file = download2(row['pds4_label'], folder / Path(row['pds4_label']).name)
                files_downloaded.loc[row.name, 'pds4_label'] = file

    if num_threads is None:
        num_threads = min(os.cpu_count(), 8)

    if pbar is None:
        pbar = tqdm(total=len(products_df), desc='Downloading Sol')

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_url = {
            executor.submit(download_row, row): row for _, row in products_df.iterrows()
        }
        for future in concurrent.futures.as_completed(future_to_url):
            future_to_url[future]
            pbar.update(1)

    session.close()

    return files_downloaded


def download_msl(
    cameras,
    sol_start,
    sol_end,
    output_dir='.',
    groupby='sol/camera',
    product_filter=MSL_PROD_FILTER,
    skip_existing=True,
    **kwargs,
):
    """Download images from the PDS archive.

    Parameters
    ----------
    cameras : str | list of str
        The cameras to download images from. Options are 'mastcam', 'mahli', 'mardi', 'navcam', 'hazcam'.
        If a list is provided, images from all cameras in the list will be downloaded.
        If 'all' is provided, images from all cameras will be downloaded.
    sol_start : int
        The starting sol number.
    sol_end : int
        The ending sol number.
    output_dir : str, optional
        The output directory to save the products to, by default '.'.
    product_filter : list, optional
        A whitelist of strings to filter the product ids, by default `['DRXX', 'RAD_', 'MXY_']`.
        Only products containing these strings will be downloaded.
        If None, all products will be downloaded.
        TODO implemet regex filtering
    find_best : bool, optional
        If True, only download the highest quality version of each product, by default True.
        This will also remove most thumbnails.
    num_threads : int, optional
        The number of threads to use for downloading, by default number of CPUs.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the paths to the downloaded files.
    """
    start_time = time.time()

    if sol_end < sol_start:
        logger.warning('sol_end is less than sol_start. Swapping values.')
        sol_start, sol_end = sol_end, sol_start

    # pre parse cameras list
    if isinstance(cameras, str) and cameras.lower() == 'all':
        cameras = CAM_LIST
    if isinstance(cameras, str):
        cameras = [cameras]
    for i, camera in enumerate(cameras):
        cameras[i] = camera.lower()

    print(  # noqa: T201
        f'Downloading images from Sol {sol_start} to Sol {sol_end} for {", ".join(cameras).upper()}.'
    )

    for camera in cameras:
        if camera not in CAM_LIST:
            raise ValueError(f'Camera incorrect. Available cameras are: {", ".join(CAM_LIST)}')

    total_downloaded = dict.fromkeys(cameras, 0)
    download_df = pd.DataFrame()

    try:
        for camera in cameras:
            with tqdm(
                total=1,
                desc=f'Downloading {camera.upper()} Products (Sol {sol_start}-{sol_end})',
                smoothing=0.05,
            ) as pbar_camera:
                # Index data for each folder from sol sol_start to sol sol_end
                sol_list = _msl_index_pds_folders(
                    camera, sol_start=sol_start, sol_end=sol_end
                )  # build PDS index for instrument and sol range
                sol_subset = {
                    k: v for k, v in sol_list.items() if sol_end >= int(k) >= sol_start
                }  # generate subset of sols to download
                pbar_camera.reset(total=len(sol_subset))

                # iterate over each sol and add image and label files to the dataframe
                for sol in sorted(sol_subset):
                    pbar_camera.set_description(
                        f'Downloading {camera.upper()} (Sol {int(sol)} of {sol_start}-{sol_end})'
                    )
                    with tqdm(total=1, desc=f'Indexing Sol {int(sol)}', leave=False) as pbar_sol:
                        sol_df = _msl_index_singlesol_products(
                            camera, sol_subset[sol], sol, product_filter=product_filter, **kwargs
                        )
                        pbar_sol.reset(total=len(sol_df))
                        pbar_sol.set_description(f'Downloading Sol {int(sol)} products')
                        files = download_products(
                            sol_df,
                            output_dir=output_dir,
                            groupby=groupby,
                            skip_existing=skip_existing,
                            pbar=pbar_sol,
                        )
                        total_downloaded[camera] += len(files)
                        download_df = pd.concat([download_df, files])
                    pbar_camera.update(1)

        elapsed_time = time.time() - start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        for camera in cameras:
            pass
        return download_df
    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return download_df
