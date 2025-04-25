"""MAHLI submodule to handle edcases for MAHLI images."""

import logging

from ..imagebase import MarsImageBase

logger = logging.getLogger(__name__)


class MASTCAMRadfixImage(MarsImageBase):
    """Image class to handle bad radioemtric correction in PDS4 Mastcam images."""

    @classmethod
    def _promote(cls, self):
        """Return True if the `self` object should be processed by this class."""
        return self.metafind(('PROCESSING_PARMS', 'RADIOMETRIC_CORRECTION_TYPE'), None) == 'MMMRAD'

    def __post_init__(self):
        """Run automatically after the normal __init__ from MarsImageBase."""
        # apply a correction to the radiance scaling factor
        # Not sure if this is a problem of how PDR is reading the data or if the label is wrong
        if not isinstance(self.meta['PROCESSING_PARMS']['RADIANCE_SCALING_FACTOR'][0], str):
            try:
                radscale = tuple(
                    x / 16 for x in self.meta['PROCESSING_PARMS']['RADIANCE_SCALING_FACTOR']
                )
                self.meta['PROCESSING_PARMS']['RADIANCE_SCALING_FACTOR'] = radscale
            except:
                logger.debug('Could not correct radiance scaling factor')
                pass
