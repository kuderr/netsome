from netsome import constants as c


def address_to_int(string: str) -> int:
    octets = map(int, string.split(c.DELIMITERS.DOT, maxsplit=3))
    return int.from_bytes(octets, byteorder="big")


def int_to_address(number: int) -> str:
    octets = map(str, number.to_bytes(length=4, byteorder="big"))
    return c.DELIMITERS.DOT.join(octets)
