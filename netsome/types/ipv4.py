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

    @classmethod
    def from_int(cls, number: int) -> "IPv4Address":
        validators.validate_int(number)
        return cls(_int_to_address(number))

    # TODO: cache
    def __str__(self) -> str:
        return _int_to_address(self._address)

    def __int__(self) -> int:
        return self._address

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{str(self)}")'


class IPv4Network:
    def __init__(self, network: str) -> None:
        address, mask = network.split(c.SLASH, maxsplit=1)
        validators.validate_address(address)
        validators.validate_mask(mask)

        self._prefixlen = int(mask)
        self._address = IPv4Address(address)
        self._netmask = IPv4Address.from_int(
            c.IPV4_MAX ^ (c.IPV4_MAX >> self._prefixlen)
        )

        int_address = int(self._address)
        int_netmask = int(self._netmask)

        if int_address & int_netmask != int_address:
            raise ValueError("host bits set")

    # TODO: cache
    def __str__(self) -> str:
        return f"{_int_to_address(self._address)}/{self._mask}"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{str(self)}")'

    def subnets(
        self,
        prefixlen: int | None = None,
    ) -> t.Generator["IPv4Network", None, None]:
        new_prefixlen = self._prefixlen + 1
        if prefixlen:
            validators.validate_prefixlen(prefixlen, min_len=self._prefixlen + 1)
            new_prefixlen = prefixlen
