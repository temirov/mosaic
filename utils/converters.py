import argparse
import datetime
import json
import logging
import os

import numpy as np

from dimming_direction import DimmingDirection


def strip_quotes(origin: str) -> str:
    return origin.strip('\"').strip('\'')


def string_to_path(origin: str) -> str:
    expanded_origin = os.path.expanduser(origin)
    return strip_quotes(expanded_origin)


def string_to_dimming_direction(origin: str) -> DimmingDirection:
    if isinstance(origin, DimmingDirection):
        return origin
    if origin.lower() in ('uni', 'uniformed', '6'):
        return DimmingDirection.UNIFORMED
    elif origin.lower() in ('ltr', 'left_to_right', '0'):
        return DimmingDirection.LEFT_TO_RIGHT
    elif origin.lower() in ('rtl', 'right_to_left', '1'):
        return DimmingDirection.RIGHT_TO_LEFT
    elif origin.lower() in ('ttb', 'top_to_bottom', '2'):
        return DimmingDirection.TOP_TO_BOTTOM
    elif origin.lower() in ('btt', 'bottom_to_top', '3'):
        return DimmingDirection.BOTTOM_TO_TOP
    elif origin.lower() in ('lbctrtc', 'left_bottom_corner_to_right_top_corner', '4'):
        return DimmingDirection.LEFT_BOTTOM_CORNER_TO_RIGHT_TOP_CORNER
    elif origin.lower() in ('ltctrbc', 'left_top_corner_to_right_bottom_corner', '5'):
        return DimmingDirection.LEFT_TOP_CORNER_TO_RIGHT_BOTTOM_CORNER
    else:
        raise argparse.ArgumentTypeError(f'Unrecognized value: {origin}.')


def string_to_bool(origin: str) -> bool:
    if isinstance(origin, bool):
        return origin
    if origin.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif origin.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def string_to_int(origin: str) -> int:
    if isinstance(origin, int):
        return origin
    try:
        return int(origin)
    except TypeError as err:
        raise argparse.ArgumentTypeError(f"Integer value expected.\n{err}")


def string_to_float(origin: str) -> float:
    if isinstance(origin, float):
        return origin
    try:
        return float(origin)
    except TypeError as err:
        raise argparse.ArgumentTypeError(f"Float value expected.\n{err}")


def string_to_loglevel(origin: str) -> int:
    string = origin.upper()
    if string == "WARN" or string == "WARNING":
        value = logging.WARN
    elif string == "INFO":
        value = logging.INFO
    elif string == "DEBUG":
        value = logging.DEBUG
    elif string == "ERROR" or string == "ERR":
        value = logging.ERROR
    else:
        raise argparse.ArgumentTypeError(f'Unknown {origin}, known values are WARN, INFO, DEBUG, ERROR')
    return value


def filebytes_to_human_size(size: int) -> str:
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    # bytes pretty-printing
    units_mapping = [
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'b'),
    ]
    for factor, suffix in units_mapping:
        if size >= factor:
            amount = int(size / factor)
            return str(amount) + suffix


def float_to_date(seconds: float) -> datetime:
    return datetime.datetime.utcfromtimestamp(seconds)


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """

    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, np.ndarray):
            return obj.tolist()

        elif isinstance(obj, np.bool_):
            return bool(obj)

        elif isinstance(obj, np.void):
            return None

        return json.JSONEncoder.default(self, obj)
