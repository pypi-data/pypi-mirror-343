"""
Module containing microSWIFT sensor type and variable definitions.
"""

__all__ = [
    "get_sensor_type_definition",
    "get_variable_definitions",
]

import struct
from typing import List, Tuple


def get_sensor_type_definition(sensor_type: str, file_size: int) -> str:
    """
    Dictionary of microSWIFT sensor type definitions;
    see https://github.com/alexdeklerk/microSWIFT.

    Arguments:
        - sensor_type (str), sensor type definition to return
        - file_size (int), size of the SBD file in bytes

    Raises:
        - ValueError, raise error if the sensor type is not one of the
                types defined in microSWIFT.py and configured to be
                parsed on the sever.

    Returns:
        - (str), sensor type definition in Python's struct module format
            * See: https://docs.python.org/3/library/struct.html
    """

    # Define the sensor type using Python's struct module format
    PAYLOAD_DEFINITIONS = {
        '50': '<sbbhfff42f42f42f42f42f42f42ffffffffiiiiii',
        '51': '<sbbhfff42fffffffffffiiiiii',
        '52': '<sbBheee42eee42b42b42b42b42Bffeeef',  # original v1 has `b` in third pos
        '52-2': '<sbbheee42eee42b42b42b42b42BffeeefI',  # Phil Mar 2025 edits
        '53': '<sbbH' + 3 * 'iiiiIIHH',
        '54': '<sbbH' + 6 * 'iiiiII13H',
    }

    # Accommodate modified sensor type 52 definition past Nov 2024
    if sensor_type == '52' and file_size == struct.calcsize(PAYLOAD_DEFINITIONS['52-2']):
        sensor_type = '52-2'

    if sensor_type not in PAYLOAD_DEFINITIONS.keys():
        raise ValueError((f'sensor_type not defined - can only be value in:'
                          f'{list(PAYLOAD_DEFINITIONS.keys())}'))

    return PAYLOAD_DEFINITIONS[sensor_type]


def get_variable_definitions() -> List[Tuple]:
    """
    microSWIFT variable definitions.

    Returns:
        - (List[Tuple]), microSWIFT variable definitions with format:
            [
            (variable name, description, units)
                :             :          :
            ]
    """
    VARIABLE_DEFINITIONS = [
        ('datetime', "native Python datetime.datetime", "(datetime)"),
        ('significant_height', "significant wave height", "(m)"),
        ('peak_period', "peak period", "(s) "),
        ('peak_direction', "peak ave direction", "(deg)"),
        ('energy_density', "energy density", "(m^2/Hz)"),
        ('frequency' , "frequency", "(Hz)"),
        ('a1', "first directional moment, positive E", "(-)"),
        ('b1', "second directional moment, positive N", "(-)"),
        ('a2', "third directional moment, positive E-W", "(-)"),
        ('b2', "fourth directional moment, positive NE-SW", "(-)"),
        ('check', "check factor", "(-)"),
        ('u_mean', "mean GPS E-W velocity, positive E", "(m/s)"),
        ('v_mean', "mean GPS N-S velocity, positive N", "(m/s)"),
        ('z_mean', "mean GPS altitude, positive up", "(m)"),
        ('latitude', "mean GPS latitude", "(decimal degrees)"),
        ('longitude', "mean GPS longitude", "(decimal degrees)"),
        ('temperature', "mean temperature", "(C)"),
        ('salinity', "mean salinity", "(psu)"),
        ('voltage', "mean battery voltage", "(V)"),
        ('sensor_type', "Iridium sensor type definition", "(-)"),
        ('com_port', "Iridium com port or # of replaced values", "(-)"),
        ('payload_size', "Iridium message size", "(bytes)"),
    ]

    return VARIABLE_DEFINITIONS
