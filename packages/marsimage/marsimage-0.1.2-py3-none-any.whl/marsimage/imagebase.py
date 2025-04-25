"""Base class for MarsImage data."""

import logging
import textwrap
import time
from base64 import b64encode
from functools import cached_property
from io import BytesIO
from pathlib import Path

import numpy as np
from matplotlib.figure import Figure

from . import imgutils
from .dng import save_dng
from .filename import Filename
from .frames import CAHVORE, CameraModel, OrbitalCoordinateFrame
from .instrument_defs import INSTRUMENT_DEFS
from .metautils import XMP
from .save import save_tiff

# Used in parser getters to indicate the default behaviour when a specific
# option is not found it to raise an exception. Created to enable `None` as
# a valid fallback value.
_UNSET = object()

SUPPORTED_PRODUCT_TYPES = {'DRXX', 'RAD_'}  # supported image types

MIN_SOLAR_ELEVATION = 3  # minimum solar elevation for zenith scaling, below this, the image will not be radiometrically corrected
COLOR_CHANNELS = 3  # number of color channels in a color image

DEFAULT_EXPOSURE_SCALE = 2.5  # default brightness scale for baseline exposure factor

logger = logging.getLogger(__name__)


class MarsImageBase:  # noqa: PLR0904
    """Base class for MarsImage data."""

    def __init__(self, filename):
        """Initialize MarsImage object with image path."""
        self.fname = Path(filename)
        self.parsed_fname = Filename(self.fname)

        # check if the image is a supported type
        if self.parsed_fname.prod_code not in SUPPORTED_PRODUCT_TYPES:
            choices = ' or '.join(SUPPORTED_PRODUCT_TYPES)
            raise ValueError(
                'Attempted to load unsupported image type: '
                f"'{self.parsed_fname.prod_code}', only "
                f'{choices} are supported'
            )

        # ensure that the image is initialized with the PDS3 label
        self._data = imgutils.read_pds3(self.fname)
        self.meta = self._data.metadata  # the PDR metadata object

        self.defs = INSTRUMENT_DEFS[self.meta['INSTRUMENT_ID']]  # instrument definitions from toml
        self._img = None  # Lazy loading
        self._mask = None
        self.blacklevel = 0

        self.first_line = self.metafind(
            [
                ('IMAGE', 'FIRST_LINE'),
                ('SUBFRAME_REQUEST_PARMS', 'FIRST_LINE'),
            ],
            1,
        )
        self.first_line_sample = self.metafind(
            [
                ('IMAGE', 'FIRST_LINE_SAMPLE'),
                ('SUBFRAME_REQUEST_PARMS', 'FIRST_LINE_SAMPLE'),
            ],
            1,
        )
        self.subframe_orig = self.subframe  # store original subframe in case image gets uncropped

        self.__post_init__()

    def _text_summary(self):
        return textwrap.dedent(f"""
            MarsImage
            ---------
            Filename:\t{self.fname.name}
            Mission:\t{self.mission_name}
            Instrument:\t{self.instrument_name}
            Filter:\t{self.metafind(('INSTRUMENT_STATE_PARMS', 'FILTER_NAME'), 'N/A')}
            Image Size:\t{self.width} x {self.height}
            Image Subframe:\t{self.subframe}
            Target:\t{self.target}
            Date UTC:\t{time.strftime('%Y-%m-%d %H:%M:%S', self.start_time)}
            Mission Date:\t{self.mean_solar_time}
            Solar Elevation:\t{round(self.solar_elevation, 1)}°
            Solar Azimuth:\t{round(self.solar_azimuth, 1)}°
            Exposure Time:\t{self.exposure_time}s
            Site, Drive:\t{self.localization.site}, {self.localization.drive}
            Camera Position:\t{np.round(self.localization.longitude, 4)}°E, {np.round(self.localization.planetocentric_latitude, 4)}°N
            Yaw, Pitch, Roll:\t{'°, '.join(map(str, np.round(self.localization.ypr_dji, 1)))}°
            Rationale:\t{self.rationale}""")

    def __str__(self):
        return f'{self._text_summary()}'

    def _repr_html_(self):
        """Produce an HTML summary with image preview for use in Jupyter notebooks."""

        def _figure_to_base64(fig):
            # Converts a matplotlib Figure to a base64 UTF-8 string
            # from https://github.com/sunpy/sunpy/blob/main/sunpy/util/util.py
            buf = BytesIO()
            fig.savefig(buf, format='png')  # works better than transparent=True
            return b64encode(buf.getvalue()).decode('utf-8')

        # Convert the text repr to an HTML table
        partial_html = (
            self._text_summary()[21:]
            .replace('\n', '</td></tr><tr><th>')
            .replace(':\t', '</th><td style="word-wrap:break-word;width:400px;">')
        )
        text_to_table = textwrap.dedent(f"""\
            <table style='text-align:left'>
                <tr><th>{partial_html}</td></tr>
            </table>""").replace('\n', '')

        # make a gamma corrected preview of the image
        img_gamma = np.clip((np.float32(self.img) / self.img.max()) ** (1 / 2.2), 0, 1)

        # Plot the image and convert it to a base64 string
        fig = Figure(figsize=(5.2, 4))
        ax = fig.subplots()
        ax.imshow(img_gamma, cmap='gray', vmin=0, vmax=1)
        ax.set_title('Image preview')
        pixel_src = _figure_to_base64(fig)

        # Plot the mask and convert it to a base64 string
        fig = Figure(figsize=(5.2, 4))
        ax = fig.subplots()
        ax.imshow(self.mask, cmap='gray', vmin=0, vmax=1)
        ax.set_title('Mask preview')
        mask_src = _figure_to_base64(fig)

        return textwrap.dedent(f"""\
            <table>
                <tr>
                    <td>{text_to_table}</td>
                    <td rowspan=3>
                        <img src='data:image/png;base64,{pixel_src}'
                             src2='data:image/png;base64,{mask_src}'
                             onClick='var temp = this.src;
                                      this.src = this.getAttribute("src2");
                                      this.setAttribute("src2", temp)'
                        />
                    </td>
                </tr>
            </table>""")

    @classmethod
    def _promote(cls, _) -> bool:
        return False

    def __post_init__(self):
        pass

    @property
    def img(self):
        """The image array of the image.

        PDR loads the image array lazily, so this poperty is used to prevent preemtive loading.
        The image is loaded and converted to the appropriate dtype on first access.
        """
        if self._img is None:
            self._img = self._data['IMAGE']
            if self._img.ndim == 3:
                # original axes: bands, lines, samples -> new axes: lines, samples, bands
                self._img = self._img.transpose(1, 2, 0)
        return self._img

    @img.setter
    def img(self, img):
        self._img = img

    @property
    def mask(self):
        """The mask array of the image.

        Lazy loading of mask image, if not found, a blank mask is returned.
        """
        # locate mask next to image file
        if self._mask is None:
            self._mask = imgutils.findmask(self.fname, self.mission_id)
            # if mask is not found, return a blank mask with value 255
            if self._mask is None:
                self._mask = np.ones(self.img.shape[:2], dtype=np.uint8) * 255
            # apply active_area to mask
            x1, y1, x2, y2 = self.active_area
            self._mask[:y1, :] = 0
            self._mask[y2:, :] = 0
            self._mask[:, :x1] = 0
            self._mask[:, x2:] = 0

        return self._mask

    @mask.setter
    def mask(self, mask):
        self._mask = mask

    def process(self, undebayer=False, uncrop=False, crop=False):
        """Calibrates the image according to the calibration settings specified in the kwargs.

        This modifies the image in place.

        Parameters
        ----------
        undebayer : bool
            If True, and the image is color, it will be undebayered using the CFA pattern
            specified in the instrument_defs.

        Returns
        -------
        None
        """
        if (
            undebayer
            and self.defs['color']
            and self.defs['cfa']
            and self.img.ndim == COLOR_CHANNELS
            and self.pixel_averaging == 1
        ):
            self.img = imgutils.undebayer(self.img, pattern=self.defs['cfa'])
        if uncrop:
            self.uncrop()
        if crop:
            self.crop_active_area()

    def crop(self, rect):
        """Crop the image and mask to the specified rectangle.

        This modifies the image and mask in place.
        TODO update camera model!

        Parameters
        ----------
        rect : list of int
            The rectangle to crop the image to in the format [x1, y1, x2, y2].
        """
        self.mask = self.mask[rect[1] : rect[3], rect[0] : rect[2]]
        self.img = self.img[rect[1] : rect[3], rect[0] : rect[2]]
        self.first_line += rect[1]
        self.first_line_sample += rect[0]

    def crop_active_area(self):
        """Crop the image and mask to the max active area.

        TODO update camera model!
        """
        self.crop(self.active_area)

    def uncrop(self):
        """Revert image to the full sensor size.

        This modifies the image and mask in place, padding them with zeros to the full sensor size.

        TODO update camera model!
        """
        full_width = self.defs['line_samples'] // self.pixel_averaging
        full_height = self.defs['lines'] // self.pixel_averaging

        padding = [
            (self.first_line - 1, full_height - self.height - self.first_line + 1),
            (self.first_line_sample - 1, full_width - self.width - self.first_line_sample + 1),
        ]
        # Pad the mask with zeros to the full sensor size, mask needs to be first,
        # otherwise it might get initialized with the uncropped image size
        self.mask = np.pad(
            self.mask,
            padding,
            mode='constant',
            constant_values=0,
        )
        # Pad the image with zeros to the full sensor size
        self.img = np.pad(
            self.img,
            padding,
            mode='constant',
            constant_values=0,
        )

        # Update image geometry.
        # width and height are automatically determined from the image array
        self.first_line = 1
        self.first_line_sample = 1

    def to_subframe(self, subframe):
        """Crop/pad the image and mask to the specified subframe.

        This modifies the image and mask in place.

        Parameters
        ----------
        subframe : list of int
            The subframe to crop/pad the image to in the format [first_line_sample, first_line, line_samples, lines].
        """
        # uncrop the the image and mask to the full sensor size in case the new subframe is larger
        self.uncrop()
        # crop the image and mask to the new subframe
        rect = [
            subframe[0] - 1,
            subframe[1] - 1,
            subframe[0] + subframe[2] - 1,
            subframe[1] + subframe[3] - 1,
        ]
        self.crop(rect)

    def save(self, save_path, *args, **kwargs):
        """Save the image to the specified path, with optional arguments for metadata etc.

        The file format is determined by the file extension of the save_path.
        Currently supported formats are TIFF and DNG.

        Parameters
        ----------
        save_path : str
            The path to save the image to. The file extension determines the file format.

        See Also
        --------
        marsimage.save.save_tiff : Save the image as a TIFF file.
        marsimage.dng.save_dng : Save the image as a DNG file.
        """
        save_path = Path(save_path)

        match save_path.suffix.lower():
            case '.tiff' | '.tif':
                save_tiff(
                    self.img,
                    self.whitelevel,
                    save_path,
                    self.baseline_exposure_factor,
                    *args,
                    **kwargs,
                )
            case '.dng':
                save_dng(
                    self,
                    save_path,
                    *args,
                    **kwargs,
                )
            case _:
                raise ValueError(f'Unsupported file format: {save_path.suffix}')

    def rawtherapee_convert(self, save_path, apply_mask=True, remove_dng=True):
        """Convert the image to a TIFF file using RawTherapee and save it to the specified path.

        Parameters
        ----------
        save_path : str
            The path to save the image to. The file extension determines the file format.
        apply_mask : bool
            Whether to apply mask layer as an alpha channel.
        remove_dng : bool
            Whether to clean up and delete the dng.

        Returns
        -------
        str
            The path to the saved image.
        """
        dng_path = Path(save_path).with_suffix('.dng')
        tiff_path = save_dng(self, dng_path, rawtherapee_convert=True, remove_dng=remove_dng)

        if apply_mask:
            imgutils.apply_mask(tiff_path, self.mask)
        return tiff_path

    def save_mask(self, save_path, ignore_empty=True):
        """Save the mask to the specified path.

        Parameters
        ----------
        save_path : str
            The path to save the mask to. The file extension determines the file format.
        ignore_empty : bool
            If True, do not save the mask if it is empty (all 255).
        """
        save_path = Path(save_path)
        if np.min(self.mask) == np.iinfo(np.uint8).max and ignore_empty:
            ...
        else:
            match save_path.suffix:
                case '.tiff' | '.tif':
                    save_tiff(
                        self.mask,
                        255,
                        save_path,
                        dtype=np.uint8,
                    )
                case _:
                    raise ValueError(f'Unsupported file format: {save_path.suffix}')

    @property
    def xmp(self):
        """Generates an XMP object from the image metadata.

        Returns
        -------
        XMP: The XMP object.

        See Also
        --------
        XMP : The XMP class.
        """
        return XMP(self)

    # def metaget(self, key):
    #     """Calls the PDR metaget method on the metadata object:
    #     Get the first value from this object whose key exactly matches `text`,
    #     even if it is nested inside a mapping. optionally evaluate it using
    #     `self.formatter`. raise a warning if there are multiple keys matching
    #     this.

    #     Warning:
    #         This function's return values are memoized for performance.
    #         Updating elements of a `Metadata` object's underlying mapping
    #         that have already been accessed with this function will not update
    #         future calls to this function."""
    #     return self.meta.metaget(key)

    # def metaget_fuzzy(self):
    #     """Calls the PDR metaget method with fuzzy matching on the metadata object.
    #     Like `metaget()`, but fuzzy-matches key names."""
    #     return self.meta.metaget_fuzzy()

    def metafind(self, keys, fallback=_UNSET):
        """Find a value from the metadata object using a list of possible keys.

        Nested keys can be accessed by passing a tuple of keys.
        If the key is not found, return a default value, else raise a KeyError.

        Parameters
        ----------
        keys : list or tuple
            A list of possible keys to search for in the metadata.
        fallback : any, optional
            The value to return if the key is not found. A fallback value of None is valid.
            Default is the sentry value _UNSET.

        Raises
        ------
        KeyError
            If the key is not found in the metadata and no fallback value was provided.
        """
        # if keys is not a list, make it a list for iteration
        if not isinstance(keys, list):
            keys = [keys]

        for key in keys:
            # if key is a string, check if it is in the metadata
            if isinstance(key, str) and key in self.meta:
                return self.meta[key]

            # if key is a tuple, check if the first key is in the metadata
            _meta = self.meta
            for k in key:
                if k in _meta:
                    _meta = _meta[k]
                else:
                    break
            else:
                return _meta

        if fallback is not _UNSET:
            return fallback

        raise KeyError(f'Key {keys} not found in metadata and no fallback value was provided')

    # mission and instrument properties from metadata
    @property
    def mission_id(self):
        """The mission ID of the image. e.g. 'MSL' or 'M20'."""
        return self.metafind('INSTRUMENT_HOST_ID')

    @property
    def mission_name(self):
        """The mission name of the image. e.g. 'MARS SCIENCE LABORATORY'."""
        return self.metafind('INSTRUMENT_HOST_NAME')

    @property
    def instrument_id(self):
        """The instrument ID of the image. e.g. 'MAHLI' or 'MARDI'."""
        return self.metafind('INSTRUMENT_ID')

    @property
    def instrument_name(self):
        """The instrument name of the image. e.g. 'MARS HAND LENS IMAGER CAMERA'."""
        return self.metafind('INSTRUMENT_NAME')

    # rationale property from metadata
    @property
    def rationale(self):
        """The rationale for the image acquisition."""
        return self.metafind(('OBSERVATION_REQUEST_PARMS', 'RATIONALE_DESC'), '')

    # Time properties from metadata
    @property
    def start_time(self):
        """The start time of the image acquisition as a time.struct_time object."""
        start_time = self.metafind(('START_TIME'), None)
        if start_time is not type(time.struct_time):
            start_time = time.strptime(start_time[:23], '%Y-%m-%dT%H:%M:%S.%f')
        return start_time

    @property
    def mean_solar_time(self):
        """The mean solar time of the image acquisition as a string."""
        return self.metafind(['LOCAL_MEAN_SOLAR_TIME', 'MSL:LOCAL_MEAN_SOLAR_TIME'], None)

    @property
    def sol(self):
        """The sol of the image acquisition."""
        return self.metafind('PLANET_DAY_NUMBER')

    @property
    def sclk(self):
        """The spacecraft clock counter (sclk) of the image acquisition."""
        return self.metafind('SPACECRAFT_CLOCK_START_COUNT')

    # Image geometry properties from metadata
    @property
    def width(self):
        """The width of the image array."""
        if self._img is None:
            return self.metafind(('IMAGE', 'LINE_SAMPLES'))
        return self.img.shape[1]

    @property
    def height(self):
        """The height of the image array."""
        if self._img is None:
            return self.metafind(('IMAGE', 'LINES'))
        return self.img.shape[0]

    @property
    def subframe(self):
        """
        The subframe of the image.

        Returns
        -------
        list of int
            The subframe in the format [first_line_sample, first_line, line_samples, lines].
            Coordinates start at [1,1] of the image.
        """
        return [
            self.first_line_sample,
            self.first_line,
            self.width,
            self.height,
        ]

    @property
    def subframe_rect(self):
        """
        The subframe of the image as a rectangle.

        Returns
        -------
        list of int
            The subframe in the format [x1, y1, x2, y2].
            Coordinates start at [0,0] of the image.
        """
        return [
            self.first_line_sample - 1,
            self.first_line - 1,
            self.first_line_sample + self.width - 1,
            self.first_line + self.height - 1,
        ]

    @property
    def pixel_averaging(self):
        """
        The downsample factor of an image.

        Returns
        -------
        int
            The pixel averaging width and height of the image.

        Raises
        ------
        Exception
            If non-square pixel averaging is detected.
        """
        w = self.metafind(
            [
                ('IMAGE_REQUEST_PARMS', 'PIXEL_AVERAGING_WIDTH'),
                ('IMAGE_PARMS', 'PIXEL_AVERAGING_WIDTH'),
            ],
            1,
        )
        h = self.metafind(
            [
                ('IMAGE_REQUEST_PARMS', 'PIXEL_AVERAGING_HEIGHT'),
                ('IMAGE_PARMS', 'PIXEL_AVERAGING_HEIGHT'),
            ],
            1,
        )

        if w == h:
            return w
        raise Exception(f'Non-square pixel averaging ({w, h}) not supported')

    @property
    def active_area(self):
        """
        Returns the active area of the image.

        The active area in the image coordinates [x1, y1, x2, y2] and start at [0,0] of the image.

        Returns
        -------
        list of int
            The active area in the format [x1, y1, x2, y2].
        """
        return imgutils.calculate_active_area(
            self.subframe,  # use original subframe in case image gets uncropped
            max_active_area=np.uint16(
                np.round(np.divide(self.defs['active_area'], self.pixel_averaging)),
            ),
            subframe_orig=self.subframe_orig,
            additional_crop=self.defs['additional_crop'],
        )

    # geometric properties from metadata
    @cached_property
    def localization(self):
        """
        Get the localization object containing the rover position and orientation.

        Returns
        -------
        OrbitalCoordinateFrame
            An instance of OrbitalCoordinateFrame representing the rover position and orientation.
        """
        return OrbitalCoordinateFrame.from_places(
            self.mission_id,
            *self.metafind(['ROVER_MOTION_COUNTER'])[:2],
        )

    @property
    def cahvore(self):
        """
        CAHVORE camera model object for the image.

        Returns
        -------
        CAHVORE
            A CAHVORE camera model object created from the image metadata.
        """
        return CAHVORE.from_odl(
            self.metafind(
                [
                    'GEOMETRIC_CAMERA_MODEL',
                    'GEOMETRIC_CAMERA_MODEL_PARMS',
                ],
            ),
        )

    @property
    def cm(self):
        """
        Generate a CameraModel object for the image in the rover frame.

        Returns
        -------
        CameraModel
            The camera model object for the image.

        Notes
        -----
        The CameraModel is created using the CAHVORE model parameters, image width,
        image height, and pixel size adjusted by pixel averaging.

        See Also
        --------
        CameraModel.from_cahvore : Method to create a CameraModel from CAHVORE parameters.
        """
        return CameraModel.from_cahvore(
            self.cahvore,
            self.width,
            self.height,
            self.defs['pixel_size'] * self.pixel_averaging,
        )

    @property
    def cm_global(self):
        """Camera model object for the image in the global frame.

        Returns
        -------
        CameraModel
            The camera model object for the image in the global frame.
        """
        return self.cm.transform_to(self.localization)

    @property
    def solar_elevation(self):
        """The solar elevation angle at image acquisition."""
        solar_elevation = self.metafind(
            [
                ('SITE_DERIVED_GEOMETRY_PARMS', 'SOLAR_ELEVATION'),
                ('DERIVED_IMAGE_PARMS', 'SOLAR_ELEVATION'),
            ],
        )
        if isinstance(solar_elevation, dict):
            return solar_elevation['value']  # sometimes the value is stored in a dict with units
        return solar_elevation

    @property
    def solar_azimuth(self):
        """The solar azimuth angle at image acquisition."""
        solar_azimuth = self.metafind(
            [
                ('SITE_DERIVED_GEOMETRY_PARMS', 'SOLAR_AZIMUTH'),
                ('DERIVED_IMAGE_PARMS', 'SOLAR_AZIMUTH'),
            ],
        )
        if isinstance(solar_azimuth, dict):  # sometimes the value is stored in a dict with units
            return solar_azimuth['value']
        return solar_azimuth

    @property
    def target(self):
        """The specified target from the label."""
        return self.metafind('TARGET_NAME')

    # Radiometric properties from metadata
    @property
    def zenith_scaling(self):
        """The zenith scaling factor for the image.

        Note
        ----
        The zenith scaling factor is currently only calculated based on the solar elevation angle
        and ignores the atmospheric optical depth.
        """
        return imgutils.calculate_zenith_scale(
            self.solar_elevation, min_solar_elevation=MIN_SOLAR_ELEVATION
        )

    @property
    def baseline_exposure_factor(self):
        """Calculate the baseline exposure factor based on solar elevation.

        The baseline exposure factor is only calculated if the solar elevation is above 5 degrees.
        At night, the image would get too dark, so a default value of 1.0 is returned.

        Returns
        -------
        float
            The calculated baseline exposure factor if solar elevation
            is above 5 degrees, otherwise 1.0.
        """
        return imgutils.calculate_baseline_exposure_factor(
            self.whitelevel,
            self.radiance_scaling_factor,
            self.zenith_scaling,
            self.defs['exposure_equalization'],
            exp_scale=DEFAULT_EXPOSURE_SCALE,
        )

    @property
    def baseline_exposure_stops(self):
        """The baseline exposure factor in EV stops.

        See Also
        --------
        baseline_exposure_factor : The baseline exposure factor.
        """
        return np.log2(self.baseline_exposure_factor)

    # Image scaling properties from metadata
    @property
    def whitelevel(self):
        """The white level of the image.

        The white level is initialized with the maximum valid value from the image label.
        If the value is not found in the label, the maximum value for the image array's
        data type is used.

        Returns
        -------
        int
            The white level value for the image.
        """
        # initialize with maximum valid value from label
        whitelevel = self.metafind(
            ('IMAGE', 'SAMPLE_BIT_MASK'),
            None,
        )
        # if not in label, use maximum value for image array
        if whitelevel is None:
            whitelevel = np.iinfo(self.img.dtype).max
        return whitelevel

    @property
    def radiance_scaling_factor(self):
        """Retrieve the radiance scaling factor from the metadata.

        This method searches for the radiance scaling factor in the metadata using
        different possible keys. The keys are specific to different missions and
        instruments.

        Returns
        -------
        float or list of float
            The radiance scaling factor(s) found in the metadata. If multiple
            factors are found, a list of floats is returned.
        """
        factor = self.metafind(
            [
                ('IMAGE', 'SCALING_FACTOR'),  # M20
                ('DERIVED_IMAGE_PARMS', 'RADIANCE_SCALING_FACTOR'),  # M20
                ('PROCESSING_PARMS', 'RADIANCE_SCALING_FACTOR'),  # MSL MSSS, is a list
                ('DERIVED_IMAGE_PARMS', 'MSL:RADIANCE_SCALING_FACTOR', 'value'),  # MSL ECAM
            ],
        )
        if isinstance(factor, dict):
            return factor['value']
        if factor in {'NULL', 'N/A', ('NULL', 'NULL', 'NULL'), ('N/A', 'N/A', 'N/A')}:
            raise ValueError('Radiance scaling factor is NULL')
        return factor

    @property
    def radiance_offset(self):
        """Float value of the radiance offset of the image.

        Returns
        -------
        float | list of float
            The radiance offset value for the image.
        """
        offset = self.metafind(
            [
                ('IMAGE', 'OFFSET'),  # M20
                ('DERIVED_IMAGE_PARMS', 'RADIANCE_OFFSET'),  # M20
                ('PROCESSING_PARMS', 'RADIANCE_OFFSET'),  # MSL MSSS, is a list
                ('DERIVED_IMAGE_PARMS', 'MSL:RADIANCE_OFFSET', 'value'),  # MSL ECAM
            ],
        )
        if isinstance(offset, dict):
            return offset['value']
        return offset

    @property
    def exposure_time(self):
        """Get the exposure time of the image.

        Returns
        -------
        float
            The exposure time in seconds.
        """
        exp_time = self.metafind(
            [
                ('INSTRUMENT_STATE_PARMS', 'EXPOSURE_DURATION'),  # MSL
            ],
            None,
        )
        if exp_time['units'] == 's':
            return exp_time['value']
        if exp_time['units'] == 'ms':
            return exp_time['value'] / 1000
        raise ValueError(f'Exposure time could not be found in metadata: {exp_time}')
