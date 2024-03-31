from netsome import constants as c

# TODO(kuderr): подумать над алгоритмами


def address_to_int(string: str) -> int:
    octets = map(int, string.split(c.DOT, maxsplit=3))
    return int.from_bytes(octets)


def int_to_address(number: int) -> str:
    return ".".join(map(str, number.to_bytes(4)))
