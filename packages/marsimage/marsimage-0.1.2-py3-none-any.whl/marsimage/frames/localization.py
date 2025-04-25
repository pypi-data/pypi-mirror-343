"""Module to handle and parse localization data for Mars rovers."""

import logging
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas
import requests
from scipy.spatial.transform import Rotation

from .coordinate_frames import CoordinateFrame

# Set up logging
logger = logging.getLogger(__name__)

# Localization data urls
LOCALIZATION_URLS = {
    'MSL_PLACES_URL': 'https://planetarydata.jpl.nasa.gov/img/data/msl/MSLPLC_1XXX/data_localizations/localized_interp.csv',
    'M20_PLACES_URL': 'https://pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_rover_places/data_localizations/best_interp.csv',
    # "M20_waypoints": "https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json",
    # "MSL_waypoints": "https://mars.nasa.gov/mmgis-maps/MSL/Layers/json/MSL_waypoints.json",
}

localization_files = {}

# Standard parallels for the equirectangular projections used by the rovers
MSL_STADARD_PARALLEL = 0
M20_STADARD_PARALLEL = 18.4663


# Download or refresh Localization data #########################################

# Generate a temporary file path using tempfile
temp_dir = tempfile.gettempdir()
# make new subdirectory for marsimage data
temp_dir = Path(temp_dir) / 'marsimage'
temp_dir.mkdir(exist_ok=True)


# Download the files and store them in the temporary location
def get_localization_files(force_download=False):
    """Download the localization files from the URLs in the LOCALIZATION_URLS dictionary.

    The files are stored in a temporary directory and the URLs
    are updated to the local file paths after function execution.
    Files are only downloaded if they do not exist locally or if they are out of date.

    Parameters
    ----------
    force_download : bool, optional
        If True, the files are downloaded even if they are up to date. Default is False.
    """
    for key, url in LOCALIZATION_URLS.items():
        filename = url.split('/')[-1]
        temp_file_path = temp_dir / filename

        if temp_file_path.exists() and not force_download:
            logger.debug(f'Localization file already exists: {temp_file_path.name}')
            # update the dictionary with the new file path
            localization_files[key] = temp_file_path

        elif not OrbitalCoordinateFrame.places_updated:
            logger.debug(f'Checking for updates for {url}')
            # get remote file modification date
            response = requests.head(url, timeout=10)
            try:
                remote_last_update = datetime.strptime(
                    response.headers['Last-Modified'],
                    '%a, %d %b %Y %H:%M:%S %Z',
                )
            except KeyError:
                logging.warning(f'Last-Modified header not found in the response for {url}')
                remote_last_update = datetime.now()

            # check if the file already exists in the temporary location and if it is up to date
            if (temp_dir / filename).exists():
                local_last_update = datetime.fromtimestamp((temp_dir / filename).stat().st_mtime)

                if remote_last_update < local_last_update:
                    logger.debug(f'Local file is up to date: {temp_file_path.name}')
                    localization_files[key] = temp_file_path
                    continue

            # download the file since it is out of date
            logger.info(f'Downloading {url} to {temp_file_path}')
            response = requests.get(url)
            if response.status_code == 200:
                with open(temp_file_path, 'wb') as file:
                    file.write(response.content)

            # update the dictionary with the new file path
            localization_files[key] = temp_file_path


class OrbitalCoordinateFrame(CoordinateFrame):
    """Localization class to parse the Rover localization data from different sources."""

    # override the constructor
    def __init__(self):
        # download json files
        if not localization_files:
            get_localization_files()

    # cache the PLACES data
    _MSL_PLACES_cache = None
    _M20_PLACES_cache = None

    places_updated = False

    @classmethod
    def from_places(cls, mission, site, drive):
        """
        Create a Localization object from the PLACES data.

        Parameters
        ----------
        mission : str
            The mission name, either "MSL" or "M20".
        site : int
            The site number.
        drive : int
            The drive number.

        Returns
        -------
        OrbitalCoordinateFrame
            The Localization object describing the coordinate frame of the rover
            at a specific site and drive in the orbital frame.
        """
        self = cls()
        if mission == 'MSL':
            # Load the DataFrame if not already cached
            if OrbitalCoordinateFrame._MSL_PLACES_cache is None:
                OrbitalCoordinateFrame._MSL_PLACES_cache = pandas.read_csv(
                    localization_files['MSL_PLACES_URL'],
                    delimiter=',',
                    # temp_dir / "localized_interp.csv", delimiter=","
                )
            places = OrbitalCoordinateFrame._MSL_PLACES_cache
        elif mission == 'M20':
            # Load the DataFrame if not already cached
            if OrbitalCoordinateFrame._M20_PLACES_cache is None:
                OrbitalCoordinateFrame._M20_PLACES_cache = pandas.read_csv(
                    localization_files['M20_PLACES_URL'],
                    delimiter=',',
                )
            places = OrbitalCoordinateFrame._M20_PLACES_cache

        # check if localization data is available in PLACES
        try:
            self.localization = places.loc[
                (places['site'] == site) & (places['drive'] == drive)
            ].iloc[0]
        except IndexError as e:
            if not OrbitalCoordinateFrame.places_updated:
                logger.info(
                    'Localization not found in local PLACES data. Downloading the latest data.'
                )
                get_localization_files(force_download=True)
                OrbitalCoordinateFrame.places_updated = True
                try:
                    self.localization = places.loc[
                        (places['site'] == site) & (places['drive'] == drive)
                    ].iloc[0]
                except IndexError as e:
                    raise KeyError(
                        f'Localization not found in updated PLACES for mission: {mission}, site: {site} and drive: {drive}'
                    ) from e
            else:
                raise KeyError(
                    f'Localization not found in updated PLACES for mission: {mission}, site: {site} and drive: {drive}'
                ) from e

        self.site = site
        self.drive = drive
        self.mission = mission
        self.standard_parallel = MSL_STADARD_PARALLEL if mission == 'MSL' else M20_STADARD_PARALLEL
        self.coordinate_system_name = 'ROVER_NAV_FRAME'
        self.coordinate_system_index = (self.localization['site'], self.localization['drive'])
        self.reference_coordinate_system_name = 'ORBITAL'
        self.reference_coordinate_system_index = 0
        self.variant = 'NED'

        self.origin_offset_vector = np.array(
            [
                self.localization['northing'],
                self.localization['easting'],
                -self.localization['elevation'],
            ],
        )

        self.origin_rotation = Rotation.from_euler(
            'ZYX',
            self.localization[['yaw', 'pitch', 'roll']],
            degrees=True,
        )

        return self

    @classmethod
    def from_mmgis(cls, mission, site, drive):
        """
        TODO Create a Localization object from the MMGIS json files.

        Parameters
        ----------
        mission : str
            The mission name, either "MSL" or "M20".
        site : str
            The site name.
        drive : int
            The drive number.

        Returns
        -------
        OrbitalCoordinateFrame
            The Localization object describing the coordinate frame of the rover
            at a specific site and drive in the orbital frame.
        """
        raise NotImplementedError('Method not implemented yet. Please use .from_places() instead.')

    @classmethod
    def from_spice(cls, mission, sclk):
        """
        TODO Create a Localization object from SPICE data.

        Parameters
        ----------
        mission : str
            The mission name, either "MSL" or "M20".
        sclk : str
            The spacecraft clock time.

        Returns
        -------
        OrbitalCoordinateFrame
            The Localization object describing the coordinate frame of the rover
            at a specific site and drive in the orbital frame.
        """
        raise NotImplementedError('Method not implemented yet. Please use .from_places() instead.')

    @property
    def longitude(self):
        """The longitude of the rover in degrees."""
        return lon_from_easting(self.easting, self.standard_parallel)

    @property
    def planetocentric_latitude(self):
        """The planetocentric latitude of the rover in degrees. I.e. no ellipsoidal correction."""
        return planetocentric_lat_from_northing(self.northing)

    @property
    def planetodetic_latitude(self):
        """The planetodetic latitude of the rover in degrees. I.e. with ellipsoidal correction."""
        return planetodetic_lat_from_lat(self.planetocentric_latitude)


# COORDINATE CONVERSIONS #########################################
# use formulas from https://pds-geosciences.wustl.edu/m2020/urn-nasa-pds-mars2020_rover_places/document/Mars2020_Rover_PLACES_PDS_SIS.pdf


def lon_from_easting(easting, standard_parallel=0):
    """
    Calculate longitude from easting.

    Parameters
    ----------
    easting : float
        Easting coordinate in meters.
    standard_parallel : float, optional
        Latitude of the standard parallel in degrees. Default is 0.

    Returns
    -------
    float
        Longitude in degrees.
    """
    return easting / (3396190.0 * np.cos(np.deg2rad(standard_parallel))) * (180 / np.pi)


def planetocentric_lat_from_northing(northing):
    """Calculate planetocentric latitude from northing."""
    return northing / 3396190.0 * (180 / np.pi)


def planetodetic_lat_from_lat(lat):
    """Calculate planetographic latitude from planetocentric latitude."""
    return np.arctan(np.tan(np.deg2rad(lat)) * (3396190.0 / 3376200.0) ** 2) * (180 / np.pi)


# calculate easting from longitude
def easting_from_lon(lon, standard_parallel=0):
    """
    Calculate easting from longitude.

    Parameters
    ----------
    lon : float
        Longitude in degrees.
    standard_parallel : float, optional
        Latitude of the standard parallel in degrees. Default is 0.

    Returns
    -------
    float
        Easting coordinate in meters.
    """
    return lon * (3396190.0 * np.cos(np.deg2rad(standard_parallel))) / (180 / np.pi)


# calculate northing from planetocentric latitude
def northing_from_planetocentric_lat(lat):
    """Calculate northing from planetocentric latitude."""
    return lat * 3396190.0 / (180 / np.pi)
