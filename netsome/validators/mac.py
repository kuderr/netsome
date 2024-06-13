import re

from netsome import constants as c


# TODO: make common
def validate_hex_string(string: str, size: int) -> None:
    # TODO: make common
    if not isinstance(string, str):
        raise TypeError

    if not re.fullmatch(r"^[0-9a-fA-F]{%s}$" % size, string):
        raise ValueError


# TODO: make common
def validate_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError()

    if not (c.MAC.ADDRESS_MIN <= number <= c.MAC.ADDRESS_MAX):
        raise ValueError()
