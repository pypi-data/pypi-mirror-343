from typing import Final
from dataclasses import dataclass


@dataclass
class Conversion:
    """
    A dataclass to hold conversion information
    """

    src_unit: str
    dest_unit: str
    factor: float


CONVERSIONS: Final[list[Conversion]] = [
    # length
    Conversion("metre", "centimetre", 100.0),
    Conversion("metre", "millimetre", 1000.0),
    Conversion("metre", "kilometre", 0.001),
    Conversion("metre", "foot", 3.28084),
    Conversion("foot", "inch", 12),
    Conversion("inch", "centimetre", 2.54),
    Conversion("mile", "kilometre", 1.609344),
    # time
    Conversion("second", "millisecond", 1000),
    Conversion("minute", "second", 60),
    Conversion("hour", "minute", 60),
    Conversion("day", "hour", 24),
    # speed
    # TODO: should just be a distance and time conversion
    # so don't need separate conversions technically
    Conversion("miles per hour", "kilometres per hour", 1.609344),
    Conversion("metres per second", "miles per hour", 2.236936),
]

ABBREVIATIONS: Final[dict[str, str]] = {
    # length
    "km": "kilometre",
    "m": "metre",
    "cm": "centimetre",
    "mm": "millimetre",
    "ft": "foot",
    "in": "inch",
    "mi": "mile",
    # time
    "s": "second",
    "ms": "millisecond",
    "min": "minute",
    "h": "hour",
    "d": "day",
    # speed
    "mph": "miles per hour",
    "mi/h": "miles per hour",
    "km/h": "kilometres per hour",
    "m/s": "metres per second",
}
