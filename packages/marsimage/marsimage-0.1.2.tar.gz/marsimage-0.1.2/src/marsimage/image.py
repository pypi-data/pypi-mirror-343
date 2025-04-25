"""The MarsImage class, which is the main class for handling all image types."""

from .imagebase import MarsImageBase
from .msl.mahliimage import MAHLIZstackImage
from .msl.mastimage import MASTCAMRadfixImage

PARENTS = [
    MAHLIZstackImage,
    MASTCAMRadfixImage,
]


class MarsImage(MarsImageBase):
    """Marsimage class, handles image loading and processing for all cameras.

    This class is the main class for handling all image types.
    It creates the appropriate image class based on the input image file.
    It is also the main class that should be used to load and process images.

    Parameters
    ----------
    path : str | pathlib.Path
        The path to the image file.

    Returns
    -------
    MarsImageBase | MAHLIZstackImage
        The appropriate MarsImage subclass object based on the input image file.
        Please see the subclasses for more information on the interface.

        - :class:`.MarsImageBase`
        - :class:`.MAHLIZstackImage`

    Examples
    --------
    >>> from marsimage import MarsImage
    >>> img = MarsImage('./3048ML0159170400407724C00_DRXX.IMG')
    """

    def __new__(cls, *args, **kwargs):  # noqa: D102
        img = MarsImageBase(*args, **kwargs)

        for parent in PARENTS:
            if parent._promote(img):
                img.__class__ = parent
                img.__post_init__()
                break

        return img
