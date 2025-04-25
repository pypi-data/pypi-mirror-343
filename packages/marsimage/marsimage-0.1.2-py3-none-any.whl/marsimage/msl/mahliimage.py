"""MAHLI submodule to handle edcases for MAHLI images."""

import re

from ..imagebase import MarsImageBase
from ..imgutils import read_pds3

"""Keywords that need to be updated from the MAHLI source image in a zstack image."""
KEYWORDS = [
    'MSL:LOCAL_MEAN_SOLAR_TIME',
    'LOCAL_TRUE_SOLAR_TIME',
    'ROVER_MOTION_COUNTER',
    'SOLAR_LONGITUDE',
    'SPACECRAFT_CLOCK_START_COUNT',
    'SPACECRAFT_CLOCK_STOP_COUNT',
    'IMAGE_TIME',
    'START_TIME',
    'STOP_TIME',
    'GEOMETRIC_CAMERA_MODEL_PARMS',
    'ROVER_COORDINATE_SYSTEM_PARMS',
    'RSM_COORDINATE_SYSTEM_PARMS',
    'ARM_COORDINATE_SYSTEM_PARMS',
    'RSM_ARTICULATION_STATE_PARMS',
    'ARM_ARTICULATION_STATE_PARMS',
    'CHASSIS_ARTICULATION_STATE_PARMS',
    'HGA_ARTICULATION_STATE_PARMS',
    'SITE_COORDINATE_SYSTEM_PARMS',
    'INSTRUMENT_STATE_PARMS',
    'DERIVED_IMAGE_PARMS',
]


class MAHLIZstackImage(MarsImageBase):
    """Mahli image class to handle non standard MAHLI images."""

    @classmethod
    def _promote(cls, self):
        """Return True if the `self` object should be processed by this class."""
        return self.metafind(('APPLICATION_PROCESS_NAME'), None) == 'MhliZstack'

    def __post_init__(self):
        """Run automatically after the normal __init__ from MarsImageBase."""
        # replace metadata with source image metadata, but initialize from PDS3 label!
        source_image = self.find_source_image_from_zstack_rationale()
        metadata = read_pds3(source_image).metadata
        self.zstack_merge_label(metadata)

    def find_source_image_from_zstack_rationale(self):
        """Find a source image of the MAHLI zstack.

        MAHLI Z-STACK images labels contain the rover state during stack generation,
        so we need to find the source images to get valid metadata.
        Currently this method only tries to load the middle image of the sequence.
        """
        rationale = self.meta['OBSERVATION_REQUEST_PARMS']['RATIONALE_DESC']
        # example: "target Daglan - stereo-2 - standoff near 5 cm - focus stack acquired sol 3047
        #           with MSL CAMERA_PRODUCT_IDs 1007-1014 - best focus image product"
        pattern = r'CAMERA_PRODUCT_IDs\s(\d+)-(\d+)'

        # find the first and last image in the stack
        result = re.search(pattern, rationale)
        if result:
            source_numbers = [int(result.group(1)), int(result.group(2))]
            # take middle image as representative of the stack
            source_number = source_numbers[0] + (source_numbers[1] - source_numbers[0]) // 2
            source_name_pattern = (
                f'*{self.fname.stem[4:6]}*{source_number}???{self.fname.stem[-5:]}.IMG'
            )

            folder = self.fname
            for _i in range(3):
                folder = folder.parent
                possible_matches = list(folder.rglob(source_name_pattern))
                if len(possible_matches) > 0:
                    continue

            if len(possible_matches) == 1:
                return possible_matches[0]
            if len(possible_matches) > 0:
                # find image with closest, but smaller sol number
                possible_matches.sort()
                possible_matches = reversed(possible_matches)
                sol = int(self.fname.stem[0:4])
                for match in possible_matches:
                    match_sol = int(match.stem[0:4])
                    if match_sol <= sol:
                        return match
            raise ValueError(
                f'Could not find source images of MAHLI ZSTACK with pattern {source_name_pattern}',
            )

        raise ValueError(
            f'Could not find source images of MAHLI ZSTACK in RATIONALE_DESC:{rationale}',
        )

    def zstack_merge_label(self, source_label):
        """Merge the relevant values from the source image into the zstack image label."""
        ...
        for key in KEYWORDS:
            self.meta[key] = source_label[key]
