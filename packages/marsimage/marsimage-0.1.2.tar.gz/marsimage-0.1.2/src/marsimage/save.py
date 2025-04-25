"""Various functions to save images."""

import logging
from contextlib import suppress
from pathlib import Path

import numpy as np
import tifffile

logger = logging.getLogger(__name__)


def save_tiff(img, whitelevel, save_path, scale_factor=1.0, gamma: float = 1.0, dtype=np.uint16):
    """Write the image array as a tiff file.

    The brightness will be normalize between 0 and the whitelevel.
    A gamma correction is applied if specified.

    Parameters
    ----------
    img : ndarray
        The image array to save.
    whitelevel : int
        The whitelevel of the image.
    save_path : str | Path
        The path to save the image to.
    scale_factor : float, optional
        The brightness scale factor to apply to the image. Default is 1.0.
    gamma : float, optional
        The gamma correction to apply to the image. Default is 1.0.
    dtype : numpy.dtype, optional
        The data type to save the image as. Default is np.uint16.
        Can be np.uint8 or np.uint16.

    Returns
    -------
    str
        The path to the saved TIFF image.
    """
    if dtype not in {np.uint8, np.uint16, 'uint8', 'uint16'}:
        raise ValueError(f'dtype must be np.uint8 or np.uint16, not {dtype}')
    dtype_max = np.iinfo(dtype).max

    if scale_factor != 1.0 or gamma != 1.0:
        # normalize the image between 0 and the whitepoint and apply gamma correction
        img = np.float32(img * scale_factor / whitelevel)
        if gamma == 'sRGB':
            img = np.where(img <= 0.0031308, 12.92 * img, 1.055 * img ** (1 / 2.4) - 0.055)
        else:
            img **= gamma
        img = np.clip(img * dtype_max, 0, dtype_max).astype(dtype)

    save_path = Path(save_path)

    # parrallel CI tests caused a race condition when creating the directory
    with suppress(FileExistsError):
        save_path.parent.mkdir(parents=True, exist_ok=True)

    tifffile.imwrite(
        save_path,
        img,
        compression='zlib',
        compressionargs={'level': 3},
        predictor=False,
    )
    logger.debug(f'Saved image to {save_path}')
    return str(save_path)
