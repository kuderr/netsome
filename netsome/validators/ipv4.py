from netsome import constants as c


def validate_address(string: str):
    if not isinstance(string, str):
        raise TypeError("Invalid type")

    octets = string.split(c.DOT, maxsplit=3)
    for octet in octets:
        validate_octet(octet)


def validate_octet(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid type")

    if not (string.isascii() and string.isdigit()):
        raise ValueError("Invalid octet format")

    if string != "0" and string.startswith("0"):
        raise ValueError("Invalid octet format")

    validate_octet_int(int(string))


def validate_octet_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid type")

    if number < c.ZERO or number > c.IPV4_OCTET_MAX:
        raise ValueError("Invalid value")


def validate_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid type")

    if number < c.ZERO or number > c.IPV4_MAX:
        raise ValueError("Invalid value")


def validate_mask(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError()

    if not (string.isascii() and string.isdigit()):
        raise ValueError()

    validate_prefixlen(int(string))


def validate_prefixlen(
    number: int,
    min_len: int = c.ZERO,
    max_len: int = c.IPV4_PREFIXLEN_MAX,
) -> None:
    if not isinstance(number, int):
        raise TypeError()

    if not (min_len <= number <= max_len):
        raise ValueError()
