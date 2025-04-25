"""Module that handles dng metadata and saving to the dng format."""

import logging
import subprocess
import time
from pathlib import Path

import numpy as np

from .imgutils import generate_badpixellist
from .lib import get_exiftool, get_rawtherapee
from .lib.pidng.core import RAW2DNG, DNGTags, Tag
from .lib.pidng.defs import (
    CalibrationIlluminant,
    CFAPattern,
    Orientation,
    PhotometricInterpretation,
    PreviewColorSpace,
)
from .metautils import PP3

logger = logging.getLogger(__name__)


def format_matrix(matrix, shape=(3, 3), precision=3):
    """Format a numpy array into a list of integer formatted floats for pidng.

    Parameters
    ----------
    matrix : numpy.ndarray
        The input numpy array to be formatted.
    shape : tuple of int, optional
        The desired shape of the matrix, by default (3, 3).
    precision : int, optional
        The number of decimal places to round to, by default 3.

    Returns
    -------
    list of list of int
        The formatted matrix as a list of lists of integers.
    """
    length = shape[0] * shape[1]
    # split numpy array with shape (3,3) into an array of shape (9,1)
    matrix = np.reshape(matrix, (length, 1))
    # for each element in the array, append 1
    matrix = np.append(matrix, np.ones((length, 1)), axis=1)
    # muliplay each element by 1000 and convert to int
    matrix = np.int32(matrix * np.power(10, precision))
    # convert to list
    return matrix.tolist()


def format_float(value, precision=3):
    """Format a float into a list of integer formatted floats for pidng.

    Parameters
    ----------
    value : float or array-like
        The float or array of floats to be formatted.
    precision : int, optional
        The number of decimal places to keep (default is 3).

    Returns
    -------
    list
        A list of integer formatted floats.
    """
    value = np.append(value, 1)
    value = np.int32(value * np.power(10, precision))
    value = np.expand_dims(value, axis=0)
    return value.tolist()


def save_dng(
    marsimage, save_path, compress=False, pp3=False, rawtherapee_convert=False, remove_dng=False
):
    """Save a marsimage object as a calibrated DNG file.

    Optionally converts the DNG to a TIFF file using RawTherapee.

    Parameters
    ----------
    marsimage : MarsImage
        The MarsImage object containing image data and metadata.
    save_path : str | Path
        The path where the DNG file will be saved.
    compress : bool, optional
        Whether to compress the DNG file lossless, by default False.
    rawtherapee_convert : bool, optional
        Whether to convert the DNG to a TIFF file in place using RawTherapee, by default False.
        Ensure that the RAWTHERAPEE_CLI environment variable is set
        to the path of the RawTherapee CLI executable.
    pp3 : bool, optional
        Whether to write a pp3 processing profile for RawTherapee, by default False.
    remove_dng : bool, optional
        Whether to remove the DNG and pp3 file after conversion to TIFF, by default False

    Returns
    -------
    str
        The path to the saved DNG file.
    """
    camdefs = marsimage.defs

    # create DNGTags object
    logger.debug('Creating DNG tags')
    t = DNGTags()

    # set camera tags
    t.set(Tag.Make, camdefs['make'])
    t.set(Tag.Model, camdefs['model'])
    t.set(Tag.EXIFPhotoLensModel, camdefs['model'])
    t.set(Tag.FocalLength, format_float(marsimage.cm.f_mm, precision=2))
    t.set(
        Tag.FocalLengthIn35mmFilm,
        int(marsimage.cm.f_35),
    )  # unfortunately this has to be an integer
    t.set(Tag.FocalPlaneXResolution, format_float(10 / marsimage.cm.pixel_size, precision=1))
    t.set(Tag.FocalPlaneYResolution, format_float(10 / marsimage.cm.pixel_size, precision=1))
    t.set(Tag.FocalPlaneResolutionUnit, 3)  # set to cm (default is 2 (inches))
    t.set(Tag.FNumber, format_float(camdefs['aperture_value']))  # F-Number
    t.set(
        Tag.ApertureValue,
        format_float(2 * np.log2(camdefs['aperture_value'])),
    )  # APEX aperture value 2log2(F-Number)
    t.set(Tag.ExposureTime, format_float(marsimage.exposure_time))  # Exposure time in seconds

    t.set(
        Tag.DateTimeOriginal,
        time.strftime('%Y:%m:%d %H:%M:%S', marsimage.start_time),
    )  # if marsimage.start_time is not None else None

    # set xmp metadata
    logger.debug('Setting XMP metadata')
    t.set(Tag.XMP_Metadata, marsimage.xmp.tag)

    # set color sensor specific tags
    if camdefs['color'] is True:
        # if image is a Bayer image
        if marsimage.img.ndim == 2:
            logger.debug('Setting Bayer sensor tags')
            t.set(Tag.BayerGreenSplit, 500) if camdefs['green_split'] else None
            t.set(Tag.CFAPattern, getattr(CFAPattern, camdefs['cfa']))
            t.set(Tag.CFARepeatPatternDim, [2, 2])

            logger.debug('Generating bad pixel list')
            OpcodeList1 = generate_badpixellist(
                marsimage.subframe,
                **camdefs['badpixels'],
            )
            t.set(Tag.OpcodeList1, OpcodeList1)

        logger.debug('Setting color calibration tags')
        t.set(Tag.ColorMatrix1, format_matrix(camdefs['ColorMatrix1']))
        t.set(
            Tag.ForwardMatrix1,
            format_matrix(camdefs['ForwardMatrix1']),
        ) if 'ForwardMatrix1' in camdefs else None
        t.set(Tag.CalibrationIlluminant1, CalibrationIlluminant.Other)

        # # if image has responsivity scaling applied to it
        responsivity = (
            marsimage.meta.responsivity if 'responsivity' in marsimage.meta else [1, 1, 1]
        )

        # # normalize rad scaling to median value
        # responsivity = [x / np.median(responsivity) for x in responsivity]
        # # dng_logger.debug("responsivity normalized: ", responsivity)

        # # set AnalogBalance tag to responsivity scaling
        # if t.get(Tag.AnalogBalance) is None:
        #     t.set(Tag.AnalogBalance, format_matrix(responsivity, (3, 1)))

        # set as shot neutral to forward matrix white balance and multiply by radiance scaling parameters
        as_shot_neutral = (
            np.multiply(camdefs['ForwardMatrixWhitebalance1'], responsivity)
            if 'ForwardMatrixWhitebalance1' in camdefs
            else responsivity
        )
        t.set(Tag.AsShotNeutral, format_matrix(as_shot_neutral, (3, 1)))

    # # set active area to maximum avallable light sensitive area of the potentially subframed image
    # active_area = marsimage.active_area
    # t.set(
    #     Tag.ActiveArea, [active_area[1], active_area[0], active_area[3], active_area[2]]
    # )

    # set image data specific tags
    logger.debug('Setting image data tags')
    t.set(Tag.ImageWidth, marsimage.width)
    t.set(Tag.ImageLength, marsimage.height)
    t.set(Tag.TileWidth, marsimage.width)
    t.set(Tag.TileLength, marsimage.height)
    t.set(Tag.Orientation, Orientation.Horizontal)

    bit_depth = marsimage.img.dtype.itemsize * 8  # calculates the bit depth of the img array
    if marsimage.img.ndim == 2:  # if image is monochrome
        logger.debug('Setting monochrome image tags')
        t.set(Tag.SamplesPerPixel, 1)
        t.set(Tag.BitsPerSample, bit_depth)
        t.set(Tag.WhiteLevel, marsimage.whitelevel)
        t.set(Tag.BlackLevel, marsimage.blacklevel)
    elif marsimage.img.ndim == 3:  # if image is color
        logger.debug('Setting color image tags')
        t.set(Tag.SamplesPerPixel, 3)
        t.set(Tag.BitsPerSample, [bit_depth, bit_depth, bit_depth])
        t.set(
            Tag.WhiteLevel,
            [marsimage.whitelevel, marsimage.whitelevel, marsimage.whitelevel],
        )
        t.set(
            Tag.BlackLevel,
            [marsimage.blacklevel, marsimage.blacklevel, marsimage.blacklevel],
        )

    # set baseline exposure stops
    logger.debug(f'Setting baseline exposure stops to {marsimage.baseline_exposure_stops}')
    t.set(Tag.BaselineExposure, [[int(marsimage.baseline_exposure_stops * 100), 100]])

    # ensure that no additional black level correction is applied by CameraRaw
    t.set(Tag.DefaultBlackRender, 1)

    # set profile curve
    logger.debug('Setting linear profile tone curve')
    t.set(Tag.ProfileToneCurve, [0, 0, 1.0, 1.0])
    # t.set(Tag.ProfileToneCurve, [0, 0, 0.1, 0.09, 0.32, 0.43, 0.66, 0.87, 1, 1])

    # set photometric interpretation to color filter array if image is color and has one band, else set to linear raw
    if camdefs['color'] is True and marsimage.img.ndim == 2:
        t.set(Tag.PhotometricInterpretation, PhotometricInterpretation.Color_Filter_Array)
    else:
        t.set(Tag.PhotometricInterpretation, PhotometricInterpretation.Linear_Raw)

    # set color space
    t.set(Tag.PreviewColorSpace, PreviewColorSpace.sRGB)

    r = RAW2DNG()
    r.options(t, path='', compress=compress)

    # if output_dir == None:
    #     output_dir = marsimage.dirname + "//"
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    save_path = Path(save_path)
    if save_path.is_dir():
        save_path = save_path / (marsimage.basename + '.dng')  # noqa: PLR6104
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # convert to 16 bit and save
    logger.debug('Converting to 16 bit and saving DNG')
    img = np.uint16(np.clip(marsimage.img, 0, 65535))
    r.convert(np.uint16(np.clip(img, 0, 65535)), filename=save_path.as_posix())
    logger.debug(f'Saved DNG to {save_path}')

    # rewrite tags with exiftool because PiDNG writes everything to IFD0 which causes issues
    # with some software like RawTherapee and Metashape
    # TODO this needs to be rewritten to a python native version, or ideally PiDNG should be fixed
    logger.debug('Rewriting tags with exiftool')
    subprocess.run(
        [
            get_exiftool(),
            '-overwrite_original',
            '-exif:all<ifd0:all',
            '-exif:all<exififd:all',
            save_path,
        ],
        check=True,
        capture_output=True,
    )

    # write pp3 processing profile
    pp3_path = save_path.parent / (save_path.stem + '.dng.pp3')
    if pp3 or rawtherapee_convert:
        PP3(
            marsimage.baseline_exposure_stops,
            marsimage.pixel_averaging,
        ).write(pp3_path)
        logger.debug('Wrote pp3 processing profile')

    # process file with rawtherapee-cli
    if rawtherapee_convert:
        source_dng = save_path.absolute()
        output_file = source_dng.parent / (source_dng.stem + '.tif')
        subprocess.run(
            [
                get_rawtherapee(),
                '-o',
                str(output_file),
                '-Y',
                '-S',
                '-b8',
                '-t',
                '-c',
                str(source_dng),
            ],
            check=True,
            capture_output=True,
        )
        logger.debug('Converted to TIFF with RawTherapee CLI')

        # remove DNG and pp3 file
        if remove_dng:
            for i in range(5):  # retry up to 5 times
                try:
                    save_path.unlink(missing_ok=True)
                    pp3_path.unlink(missing_ok=True)
                    break
                except PermissionError:
                    logger.debug(f'Retrying to remove DNG file... Attempt {i + 1}/5')
                    time.sleep((i + 1) ** 2)
            else:
                logger.error(f'Failed to remove DNG file {save_path}')
            logger.debug('Removed DNG and pp3 file')

        save_path = output_file

    return save_path
