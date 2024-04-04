import typing as t
import functools
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


def _validate_network_int(address: int, prefixlen: int):
    netmask = c.IPV4_MAX ^ (c.IPV4_MAX >> prefixlen)
    if address & netmask != address:
        raise ValueError("host bits set")


class IPv4Network:
    def __init__(self, network: str) -> None:
        address, mask = network.split(c.SLASH, maxsplit=1)
        validators.validate_address(address)
        validators.validate_mask(mask)

        _validate_network_int(_address_to_int(address), int(mask))

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
        return f"{_int_to_address(int(self._address))}/{self._prefixlen}"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{str(self)}")'

    @classmethod
    def from_int(cls, int_address: int, prefixlen: int) -> "IPv4Network":
        validators.validate_int(int_address)
        validators.validate_prefixlen(prefixlen)

        _validate_network_int(int_address, prefixlen)

        address = f"{_int_to_address(int_address)}{c.SLASH}{prefixlen}"
        return cls(address)

    @property
    def prefixlen(self):
        return self._prefixlen

    @property
    def address(self):
        return self._address

    @property
    def netmask(self):
        return self._netmask

    @functools.cached_property
    def hostmask(self):
        return IPv4Address.from_int(int(self._netmask) ^ c.IPV4_MAX)

    @functools.cached_property
    def broadcast(self):
        return IPv4Address.from_int(int(self._address) | int(self.hostmask))

    def subnets(
        self,
        prefixlen: int | None = None,
    ) -> t.Generator["IPv4Network", None, None]:
        new_prefixlen = self._prefixlen + 1
        if prefixlen:
            validators.validate_prefixlen(prefixlen, min_len=new_prefixlen)
            new_prefixlen = prefixlen

        prefixlen_diff = new_prefixlen - self._prefixlen

        start = int(self._address)
        end = int(self.broadcast) + 1
        step = (int(self.hostmask) + 1) >> prefixlen_diff
        for addr in range(start, end, step):
            yield IPv4Network.from_int(addr, new_prefixlen)

    def supernet(
        self,
        prefixlen: int | None = None,
    ) -> "IPv4Network":
        new_prefixlen = self._prefixlen - 1
        if prefixlen:
            validators.validate_prefixlen(prefixlen, max_len=new_prefixlen)
            new_prefixlen = prefixlen

        prefixlen_diff = self._prefixlen - new_prefixlen

        return IPv4Network.from_int(
            int(self._address) & (int(self._netmask) << prefixlen_diff),
            new_prefixlen,
        )

    def hosts(self):
        start = int(self._address) + 1
        end = int(self.broadcast)

        for addr in range(start, end):
            yield IPv4Address.from_int(addr)
