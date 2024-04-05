import functools
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
        validators.validate_address_str(address)
        self._addr = _address_to_int(address)

    @classmethod
    def from_int(cls, number: int) -> "IPv4Address":
        validators.validate_address_int(number)
        return cls(_int_to_address(number))

    @functools.cached_property
    def address(self) -> str:
        return _int_to_address(self._addr)

    def __int__(self) -> int:
        return self._addr

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'


def _validate_network_int(address: int, prefixlen: int):
    netmask = c.IPV4_MAX ^ (c.IPV4_MAX >> prefixlen)
    if address & netmask != address:
        raise ValueError("host bits set")


class IPv4Network:
    def __init__(self, network: str) -> None:
        address, prefixlen = network.split(c.SLASH, maxsplit=1)
        validators.validate_address_str(address)
        validators.validate_prefixlen_str(prefixlen)

        _validate_network_int(_address_to_int(address), int(prefixlen))

        self._prefixlen = int(prefixlen)
        self._netaddr = IPv4Address(address)
        self._netmask = IPv4Address.from_int(
            c.IPV4_MAX ^ (c.IPV4_MAX >> self._prefixlen)
        )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    @classmethod
    def from_int(cls, int_address: int, prefixlen: int) -> "IPv4Network":
        validators.validate_address_int(int_address)
        validators.validate_prefixlen_int(prefixlen)

        _validate_network_int(int_address, prefixlen)

        address = f"{_int_to_address(int_address)}{c.SLASH}{prefixlen}"
        return cls(address)

    @property
    def prefixlen(self) -> int:
        return self._prefixlen

    @property
    def netaddress(self) -> IPv4Address:
        return self._netaddr

    @property
    def netmask(self) -> IPv4Address:
        return self._netmask

    @functools.cached_property
    def address(self) -> str:
        return f"{self._netaddr.address}/{self._prefixlen}"

    @functools.cached_property
    def hostmask(self) -> IPv4Address:
        return IPv4Address.from_int(int(self._netmask) ^ c.IPV4_MAX)

    @functools.cached_property
    def broadcast(self) -> IPv4Address:
        return IPv4Address.from_int(int(self._netaddr) | int(self.hostmask))

    def subnets(
        self,
        prefixlen: int | None = None,
    ) -> t.Generator["IPv4Network", None, None]:
        new_prefixlen = self._prefixlen + 1
        if prefixlen:
            validators.validate_prefixlen_int(prefixlen, min_len=new_prefixlen)
            new_prefixlen = prefixlen

        prefixlen_diff = new_prefixlen - self._prefixlen

        start = int(self._netaddr)
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
            validators.validate_prefixlen_int(prefixlen, max_len=new_prefixlen)
            new_prefixlen = prefixlen

        prefixlen_diff = self._prefixlen - new_prefixlen
        addr = int(self._netaddr) & (int(self._netmask) << prefixlen_diff)

        return IPv4Network.from_int(addr, new_prefixlen)

    def hosts(self):
        start = int(self._netaddr) + 1
        end = int(self.broadcast)

        for addr in range(start, end):
            yield IPv4Address.from_int(addr)
