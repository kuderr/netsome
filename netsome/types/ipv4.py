from netsome import constants as c
from netsome.validators import ipv4 as validators


def _address_to_int(string: str) -> int:
    octets = map(int, string.split(c.DOT, maxsplit=3))
    return int.from_bytes(octets, byteorder="big")


def _int_to_address(number: int) -> str:
    octets = map(str, number.to_bytes(length=4, byteorder="big"))
    return c.DOT.join(octets)


class IPv4Address:
    def __init__(self, address: str) -> None:
        validators.validate_address(address)
        self._address = _address_to_int(address)

    # TODO: cache?
    def __str__(self) -> str:
        return _int_to_address(self._address)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self)})"


# TODO:
class IPv4Network:
    def __init__(self) -> None:
        pass
