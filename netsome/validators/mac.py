import re

from netsome import constants as c


# TODO: make common
def validate_hex_string(string: str, size: int) -> None:
    # TODO: make common
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string}" of type "{type(string)}", str expected'
        )

    if not re.fullmatch(r"^[0-9a-fA-F]{%s}$" % size, string):
        raise ValueError(f'Provided value "{string}" has invalid mac format')


# TODO: make common
def validate_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number}" of type "{type(number)}", int expected'
        )

    if not (c.MAC.ADDRESS_MIN <= number <= c.MAC.ADDRESS_MAX):
        raise ValueError(
            f'Value "{number}" must be in range {c.MAC.ADDRESS_MIN}-{c.MAC.ADDRESS_MAX}'
        )
