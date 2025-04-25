"""RawTherapee module."""

import os
import shutil
import sys
from pathlib import Path


def get_rawtherapee() -> str:
    """Get rawtherapee bundled library absolute path for a given platform."""
    # Use global environment variable.
    if cli := os.environ.get('RAWTHERAPEE_CLI'):
        return cli

    # Try to locate RawTherapee from the $PATH
    if cli := shutil.which('rawtherapee-cli'):
        return cli

    # Try default platform locations
    match sys.platform:
        # `linux` case should always be covered with `which`
        case 'win32':
            if cli := _windows():
                return cli

        case 'darwin':
            if cli := _macos():
                return cli

    raise RuntimeError(
        '`rawtherapee-cli` not found on your system. '
        'Make sure you have installed it (https://www.rawtherapee.com). '
        'You can also provide a global environment variable '
        '`$RAWTHERAPEE_CLI` to point to its location'
    )


def _windows() -> str | None:
    """Try to get windows default location of RawTherapee."""
    default = Path('C:\\Program Files\\RawTherapee')

    if default.exists():
        cli = list(default.glob('*/rawtherapee-cli.exe'))

        if len(cli) > 1:
            raise RuntimeError(
                'Multiple version of RawTherapee detected. '
                'Provide an explicit path in `$RAWTHERAPEE_CLI`.'
            )

        return str(cli[0])

    return None


def _macos() -> str | None:
    """Try to get macOS default location of RawTherapee."""
    # Try `/usr/local/bin` folder (as recommended by RawTherapee)
    default = '/usr/local/bin/rawtherapee-cli'

    if Path(default).exists():
        return default

    return None
