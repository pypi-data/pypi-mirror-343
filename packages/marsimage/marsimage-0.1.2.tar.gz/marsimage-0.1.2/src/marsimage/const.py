"""Some constant values used in the package."""

import logging
import os
from pathlib import Path

if not (MARS_DATA := os.getenv('MARS_DATA')):
    logging.debug(
        '`$MARS_DATA` environment variable not set. Defaulting to the data in the package.'
    )

    MARS_DATA = Path(__file__).parent / 'data'
