"""Module that contains various image calibration and utility functions."""

import logging
import struct
import subprocess
from pathlib import Path

import numpy as np
import pdr
import tifffile

from .lib import get_exiftool

logger = logging.getLogger(__name__)


def read_pds3(fp):
    """Read a file with PDR and initialize from PDS3 label.

    The function will try to find an external .lbl file associated with the product.
    Otherwise it will initialize the metadata from the internal PDS3 label.

    Parameters
    ----------
    fp : str | Path

    Returns
    -------
    PDR Data object with PDS3 label
    """
    # ensure that the image is initialized with the PDS3 label
    fp = Path(fp)

    if fp.with_suffix('.LBL').exists():
        data = pdr.fastread(fp.with_suffix('.LBL'))
    else:
        data = pdr.fastread(fp)
    if 'PDS_VERSION_ID' in data.metadata and data.metadata['PDS_VERSION_ID'] == 'PDS3':
        return data
    raise Exception(f'{fp.name} could not be initialized from a PDS3 label')


def calculate_active_area(  # noqa: PLR0914
    subframe,
    max_active_area,
    subframe_orig=None,
    additional_crop=None,
):
    """Calculate the maximum active area of the image in image coordinates.

    The active area is determined based on the subframing of the image array
    and the maximum active area of the sensor.

    Parameters
    ----------
    subframe : list
        The current subframe in the format [first_line_sample, first_line, line_samples, lines].
        The first line sample and first line coordinates start at 1.
    max_active_area : list
        The maximum active area of the sensor in the format [x1, y1, x2, y2]. Starts at [0,0].
    subframe_orig : list
        The original subframe of the image in the format [first_line_sample, first_line, line_samples, lines].
        The first line sample and first line coordinates start at 1.
    additional_crop : list, optional
        Additional cropping values in the format [left, top, right, bottom].
        Default is [0, 0, 0, 0].

    Returns
    -------
    list
        The active area in the image coordinates [x1, y1, x2, y2] and start at [0,0].

    Raises
    ------
    ValueError
        If there is no intersection between subframe and max active area.
    """
    if additional_crop is None:
        additional_crop = [0, 0, 0, 0]

    # JPL image coordinates start at 1, Adobe counts from 0
    # subframing of the image in x1, y1, x2, y2
    sub_rect = [
        subframe[0] - 1,
        subframe[1] - 1,
        subframe[0] + subframe[2] - 1,
        subframe[1] + subframe[3] - 1,
    ]

    # original subframing of the image in x1, y1, x2, y2
    if subframe_orig is not None:
        sub_rect_orig = [
            subframe_orig[0] - 1,
            subframe_orig[1] - 1,
            subframe_orig[0] + subframe_orig[2] - 1,
            subframe_orig[1] + subframe_orig[3] - 1,
        ]
    else:
        sub_rect_orig = sub_rect

    default_rect = [
        additional_crop[0] + sub_rect_orig[0],
        additional_crop[1] + sub_rect_orig[1],
        sub_rect_orig[2] - additional_crop[2],
        sub_rect_orig[3] - additional_crop[3],
    ]

    # corner coordinates
    x1_1, y1_1, x2_1, y2_1 = sub_rect
    x1_2, y1_2, x2_2, y2_2 = max_active_area
    x1_3, y1_3, x2_3, y2_3 = sub_rect_orig
    x1_4, y1_4, x2_4, y2_4 = default_rect

    # Calculate the top-left corner of the intersection
    x1 = max(x1_1, x1_2, x1_3, x1_4)
    y1 = max(y1_1, y1_2, y1_3, y1_4)

    # Calculate the bottom-right corner of the intersection
    x2 = min(x2_1, x2_2, x2_3, x2_4)
    y2 = min(y2_1, y2_2, y2_3, y2_4)

    # Check for no intersection
    if x1 < x2 and y1 < y2:
        # active area in y,x,h,w in image coordinates
        return [
            x1 - sub_rect[0],
            y1 - sub_rect[1],
            x2 - sub_rect[0],
            y2 - sub_rect[1],
        ]
    raise ValueError('No intersection between subframe and max active area')


# undebayer image with specified pattern and mode
def undebayer(rgbimg, pattern='RGGB'):
    """Undebayer a color image array to a monochrome bayer array using the specified pattern.

    Parameters
    ----------
    rgbimg : ndarray
        The color image array.
    pattern : str, optional
        The bayer pattern of the color image. Default is "RGGB".
        Other available patterns are "GRBG", "BGGR", and "GBRG".

    Returns
    -------
    ndarray
        The monochrome bayer array.
    """
    r, g, b = rgbimg[:, :, 0], rgbimg[:, :, 1], rgbimg[:, :, 2]

    # slice RGB image up into RGGB bayer array
    bayered = np.zeros(rgbimg.shape[:2], rgbimg.dtype)
    match pattern:
        case 'RGGB':
            bayered[0::2, 0::2] = r[0::2, 0::2]  # top left
            bayered[0::2, 1::2] = g[0::2, 1::2]  # top right
            bayered[1::2, 0::2] = g[1::2, 0::2]  # bottom left
            bayered[1::2, 1::2] = b[1::2, 1::2]  # bottom right
        case 'GRBG':
            bayered[0::2, 0::2] = g[0::2, 0::2]  # top left
            bayered[0::2, 1::2] = r[0::2, 1::2]  # top right
            bayered[1::2, 0::2] = b[1::2, 0::2]  # bottom left
            bayered[1::2, 1::2] = g[1::2, 1::2]  # bottom right
        case 'BGGR':
            bayered[0::2, 0::2] = b[0::2, 0::2]  # top left
            bayered[0::2, 1::2] = g[0::2, 1::2]  # top right
            bayered[1::2, 0::2] = g[1::2, 0::2]  # bottom left
            bayered[1::2, 1::2] = r[1::2, 1::2]  # bottom right
        case 'GBRG':
            bayered[0::2, 0::2] = g[0::2, 0::2]  # top left
            bayered[0::2, 1::2] = b[0::2, 1::2]  # top right
            bayered[1::2, 0::2] = r[1::2, 0::2]  # bottom left
            bayered[1::2, 1::2] = g[1::2, 1::2]  # bottom right
        case _:
            raise ValueError(f'Unsupported bayer pattern: {pattern}')

    return bayered


def calculate_zenith_scale(solar_elevation, tau=0.6, tau_ref=0.3, min_solar_elevation=5):
    """Calculate the zenith scaling factor from the solar elevation and atmospheric optical depth.

    TODO modify formula to use the path optical depth instead of the normal optical depth.
    https://doi.org/10.1016/j.icarus.2023.115821

    Parameters
    ----------
    solar_elevation : float
        The solar elevation angle in degrees.
    tau : float, optional
        The atmospheric optical depth. Default is 0.6.
    tau_ref : float, optional
        The reference atmospheric optical depth. Default is 0.3.
    min_solar_elevation : float, optional
        The minimum solar elevation for zenith scaling. Default is 5 degrees.

    Returns
    -------
    float
        The zenith scaling factor.
    """
    solar_elevation_limited = max(
        solar_elevation,
        min_solar_elevation,
        0.1,
    )  # minimum solar elevation, because mu => 0 at 0 degrees
    logger.debug(
        f'Calculating Zenith scale with solar_elevation: {solar_elevation_limited}(actual:{solar_elevation}), tau: {tau}, tau_ref: {tau_ref}'
    )
    mu = np.sin(np.deg2rad(solar_elevation_limited))
    return mu * np.exp(-(tau - tau_ref) / 6 / mu)


def calculate_baseline_exposure_factor(
    whitelevel,
    rad_scaling,
    zenith_scaling,
    exposure_equalization=1,
    exp_scale=3.5,
):
    """
    Calculate the baseline exposure factor for an image.

    Parameters
    ----------
    whitelevel : int
        The whitelevel of the image.
    rad_scaling : float or tuple of float
        The radiance scaling factor of the image. If a tuple, the second element is used.
    zenith_scaling : float
        The zenith scaling factor of the image.
    exposure_equalization : float, optional
        The exposure equalization factor to correct for camera differences. Default is 1.
    exp_scale : float, optional
        The exposure scaling factor to adjust the global exposure of the algorithm. Default is 3.5.

    Returns
    -------
    float
        The baseline exposure factor.
    """
    if isinstance(rad_scaling, tuple):
        rad_scaling = rad_scaling[1]  # use the green channel scaling factor
    return float(whitelevel * rad_scaling / zenith_scaling * exposure_equalization * exp_scale)


# find mask image for PDS images
def findmask(file, mission_id):
    """
    Locate a mask image for a PDS image file in the same directory.

    Parameters
    ----------
    file : str
        The PDS image file path.
    mission_id : str
        The mission ID of the image.

    Returns
    -------
    ndarray or None
        The mask image array if found, otherwise None.
    """
    dirname, filename = Path(file).parent, Path(file).name

    mask_name = None
    if mission_id == 'MSL':
        if filename[0:2] in {'NL', 'NR', 'FL', 'FR', 'RL', 'RR'}:
            mask_name = filename[:13] + 'MXY' + filename[16:]
    elif mission_id == 'M20':
        mask_name = filename[:23] + 'MXY' + filename[26:]
    else:
        mask_name = None

    if mask_name is not None:
        mask_path = Path(dirname) / mask_name
        if mask_path.exists():
            mask = np.uint8(read_pds3(mask_path)['IMAGE'])
            return np.invert(mask)
        return None
    return None


# This code was heavily referenced from m9tools by Ben Dyer https://github.com/bendyer/m9tools/
def generate_badpixellist(
    subframe,
    pixels=None,
    columns=None,
    rectangles=None,
):
    """Generate a BadPixelList opcode for a DNG file.

    Computes the binary opcode data for the FixBadPixels opcode in the DNG file.

    Parameters
    ----------
    subframe : list
        The subframe of the image in the format [first_line_sample, first_line, line_samples, lines].
        The first line sample and first line coordinates start at 1.

    width : int
        Width of the image.
    height : int
        Height of the image.
    first_line : int, optional
        First line of the image. Default is 1.
    first_line_sample : int, optional
        First line sample of the image. Default is 1.

    pixels : list, optional
        List of bad pixels. Default is [].
    columns : list, optional
        List of bad columns. Default is [].
    rectangles : list, optional
        List of bad rectangles. Default is [].

    Returns
    -------
    bytes
        Opcode data.
    """
    bad_pixel_data = []
    bad_rect_data = []
    _width, height = subframe[2], subframe[3]
    subframe_rect = [
        subframe[0] - 1,
        subframe[1] - 1,
        subframe[0] + subframe[2] - 1,
        subframe[1] + subframe[3] - 1,
    ]

    # logger.debug(subframe_rect[0], subframe_rect[1])

    # coordinates in sensor coordinates before possible cropping is applied
    if pixels is not None:
        for bad_pixel in pixels:
            logger.debug(f'bad_pixel sensor: {bad_pixel}')
            x, y = bad_pixel
            x, y = int(x - subframe_rect[0]), int(y - subframe_rect[1])
            if not (
                subframe_rect[0] <= x < subframe_rect[2]
                and subframe_rect[1] <= y < subframe_rect[3]
            ):
                logger.debug(f'Bad pixel coordinate ({x}, {y}) out of bounds ({subframe_rect})')
            else:
                logger.debug(f'bad pixel image: {x}, {y}')
                packed_data = struct.pack('>2L', y, x)
                bad_pixel_data.append(packed_data)

    if columns is not None:
        for x in columns:
            logger.debug(f'bad column sensor: {x}')
            if not (subframe_rect[0] <= x < subframe_rect[2]):
                logger.debug(f'Bad column ({x}) out of bounds ({subframe_rect})')
            else:
                x_start = x - subframe_rect[0]
                x_end = x - subframe_rect[0] + 1
                logger.debug(f'bad column image: {x_start}, {height}, {x_end}')
                packed_data = struct.pack('>4L', 0, x_start, height, x_end)
                bad_rect_data.append(packed_data)

    if rectangles is not None:
        for rectangle in rectangles:
            logger.debug(f'Bad rectangle sensor: {rectangle}')
            x1_1, y1_1, x1_2, y1_2 = rectangle
            x2_1, y2_1, x2_2, y2_2 = subframe_rect

            # find the intersection of the rectangle with the subframe
            x1 = max(x1_1, x2_1)
            y1 = max(y1_1, y2_1)
            x2 = min(x1_2, x2_2)
            y2 = min(y1_2, y2_2)

            x1, y1 = int(x1 - subframe_rect[0]), int(y1 - subframe_rect[1])
            x2, y2 = int(x2 - subframe_rect[0] + 1), int(y2 - subframe_rect[1] + 1)

            # don't add rectangles where the intersection is empty
            if x1 >= x2 + 1 or y1 >= y2 + 1:
                logger.debug(f'Bad rectangle ({x1}, {y1}, {x2}, {y2}) out of bounds')
            else:
                logger.debug(f'bad rectangle image: {x1}, {y1}, {x2}, {y2}')
                packed_data = struct.pack('>4L', y1, x1, y2, x2)
                bad_rect_data.append(packed_data)

    # logger.debug("bad_rect_data:", bad_rect_data)

    # Pack parameter data area
    param_data = b''.join(bad_pixel_data) + b''.join(bad_rect_data)
    # logger.debug("param_data:", param_data)

    # Opcode list setup -- one opcode
    opcode_list_header = struct.pack('>L', 1)

    # FixBadPixels opcode setup -- OpcodeID, OpcodeVersion, FlagBits,
    # VariableParamLength, BayerPhase, BadPixelCount, BadRectCount
    opcode_header = struct.pack(
        '>L4B5L',
        5,
        1,
        3,
        0,
        0,
        1,
        len(param_data) + 12,
        1,
        len(bad_pixel_data),
        len(bad_rect_data),
    )

    # return complete opcode
    return opcode_list_header + opcode_header + param_data


def apply_mask(tiff_image, mask, output_path=None):
    """Apply a mask array to a TIFF image.

    Parameters
    ----------
    tiff_image : str | Path
        The TIFF image
    mask : ndarray
        The mask array
    output_path : str | Path, optional
        The output path for the masked image
        If none, the old image is overwritten

    Returns
    -------
    Path
        The path to the masked image
    """
    tiff_image = Path(tiff_image)
    if output_path is None or output_path == tiff_image:
        # rename the original image so it is not overwritten
        output_path = tiff_image
        renamed = tiff_image.with_suffix('.orig.tif')
        if renamed.exists():
            renamed.unlink()
        tiff_image.rename(renamed)
        tiff_image = renamed

    # read image and apply mask, then save
    img = tifffile.imread(tiff_image)
    if img.shape[:2] != mask.shape:
        raise ValueError('Image and mask shapes do not match')

    mask = np.expand_dims(mask, axis=2)
    if len(img.shape) == 2:
        img = np.expand_dims(img, axis=2)
        img = np.concatenate([img, mask], axis=2)
        tifffile.imwrite(
            output_path,
            img,
            photometric='minisblack',
            extrasamples=['unassalpha'],
            compression='zlib',
            compressionargs={'level': 2},
            predictor=False,
        )
    elif img.shape[2] == 3:
        img = np.concatenate([img, mask], axis=2)
        tifffile.imwrite(
            output_path,
            img,
            photometric='rgb',
            extrasamples=['unassalpha'],
            compression='zlib',
            compressionargs={'level': 2},
            predictor=False,
        )

        # rewrite tags with exiftool
        # exiftool -TagsFromFile input.tif -all:all output.tif
        logger.debug('Rewriting tags with exiftool')
    try:
        subprocess.run(
            [
                get_exiftool(),
                '-TagsFromFile',
                tiff_image,
                '-overwrite_original',
                '-exif:all',
                '-xmp:all',
                '-ImageDescription=',
                output_path,
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f'Error rewriting tags with exiftool: {e.stderr.decode()}')

    # delete the original image
    tiff_image.unlink()

    return output_path
