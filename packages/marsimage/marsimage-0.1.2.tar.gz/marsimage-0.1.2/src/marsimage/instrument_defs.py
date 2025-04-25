"""Module that loads instrument properties and calibration values from the instrument_defs.toml."""

import tomllib as tl
from pathlib import Path

from .const import MARS_DATA


def _is_group(value):
    """Check if a value is a table or an actual value."""
    return bool(
        isinstance(value, dict) and value.get('type') in {'mission', 'group', 'instrument'},
    )


def _get_values(input_dict):
    """Get the values from a dictionary that are not tables."""
    out_dict = {}
    for k, v in input_dict.items():
        if not _is_group(v):
            out_dict[k] = v
    return out_dict


class InstrumentDefs:
    """Class that loads the instrument definitions from the instrument_defs.toml file.

    The definitions file is a TOML file that contains the properties and calibration values
    for the instruments. The instrument groups are flattened while propagating parent values
    to the children.

    Attributes
    ----------
    instruments_def : dict
        The raw instrument definitions loaded from the TOML file.
    instruments : dict
        The flattened instrument definitions with propagated parent values.

    Returns
    -------
    Dict like object
        The instrument definitions as a dictionary.

    Examples
    --------
    >>> from marsimage.instrument_defs import INSTRUMENT_DEFS
    >>> INSTRUMENT_DEFS['MAST_LEFT']
    {'type': 'instrument',
    'MISSION_NAME': 'MARS SCIENCE LABORATORY',
    'make': 'JPL-Caltech/MSSS',
    'pixel_size': 0.0074,
    'lines': 1200,
    'line_samples': 1648,
    'active_area': [24, 2, 1630, 1200],
    'additional_crop': [0, 2, 0, 0],
    'color': True,
    'cfa': 'RGGB',
    'green_split': True,
    'exposure_equalization': 0.582,
    'model': 'MSL Left Mastcam 34mm',
    'focal_length': 34,
    'aperture_value': 8,
    'badpixels': {'columns': [1069, 653],
    'rectangles': [[859, 1082, 859, 1200], [739, 620, 739, 1200]]},
    'ColorMatrix1': [[2.32533, -1.219946, -0.208088],
    [-0.523358, 1.389468, 0.144668],
    [-0.17526, 0.284039, 0.891039]],
    'ForwardMatrixWhitebalance1': [0.88347, 1.0, 0.775735],
    'ForwardMatrix1': [[0.467471, 0.445046, 0.051702],
    [0.167172, 0.91784, -0.085012],
    [0.048347, -0.198833, 0.975687]]}
    """

    def __init__(self):
        with Path(MARS_DATA / 'instrument_defs.toml').open(mode='rb') as fp:
            self.instruments_def = tl.load(fp)

        # flatten the dictionary to the second level
        self.instruments = {}
        for k1, v1 in self.instruments_def.items():  # k1 is the mission name  # noqa: PLR1702
            if v1.get('type') == 'mission':
                self.instruments[k1] = {}
                for _k2, v2 in v1.items():  # k2 is the group name or instrument name
                    if _is_group(v2):
                        for (
                            k3,
                            v3,
                        ) in v2.items():  # k3 is the instrument name if k2 is a group name
                            if _is_group(v3):
                                self.instruments[k1][k3] = _get_values(
                                    v1
                                )  # add the mission level get_values
                                self.instruments[k1][k3].update(
                                    _get_values(v2)
                                )  # add the group level get_values
                                self.instruments[k1][k3].update(
                                    _get_values(v3)
                                )  # add the instrument level get_values

    def __getitem__(self, key):
        if key in self.instruments:
            return self.instruments[key]
        for v in self.instruments.values():
            return v.get(key)
        raise KeyError(f'Key {key} not found in instrument definitions')


INSTRUMENT_DEFS = InstrumentDefs()
"""
Global dictionary variable that holds the instrument definitions
"""
