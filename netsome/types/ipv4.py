import typing as t

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

    # TODO: cache
    def __str__(self) -> str:
        return _int_to_address(self._address)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{str(self)}")'


class IPv4Network:
    # Is /32 network valid?
    def __init__(self, network: str) -> None:
        validators.validate_network(network)

        address, mask = network.split("/")
        self._address = _address_to_int(address)
        self._mask = int(mask)

    # TODO: cache
    def __str__(self) -> str:
        return f"{_int_to_address(self._address)}/{self._mask}"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{str(self)}")'

    def subnets(
        self,
        mask: int | None = None,
    ) -> t.Generator["IPv4Network", None, None]:
        new_mask = self._mask + 1
        if mask:
            validators.validate_mask_len(mask, min_len=self._mask + 1)
            new_mask = mask
