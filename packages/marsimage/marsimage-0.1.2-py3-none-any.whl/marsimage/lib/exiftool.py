"""Exiftool module."""

import sys
from pathlib import Path

DIR = Path(__file__).parent.absolute()


def get_exiftool(platform: str = sys.platform) -> Path:
    """Get exiftool bundled library absolute path for a given platform."""
    match platform:
        case 'win32':
            return DIR / 'exiftool' / 'win' / 'exiftool.exe'

        case 'linux' | 'darwin':
            return DIR / 'exiftool' / 'unix' / 'exiftool'

    raise RuntimeError(f'Platform not supported with exiftool: {platform}')
