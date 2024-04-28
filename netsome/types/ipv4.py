import functools
import typing as t

from netsome import constants as c
from netsome._converters import ipv4 as convs
from netsome.validators import ipv4 as valids


class IPv4Address:

    PREFIXLEN_MIN = c.IPV4.PREFIXLEN_MIN
    PREFIXLEN_MAX = c.IPV4.PREFIXLEN_MAX

    ADDRESS_MIN = c.IPV4.ADDRESS_MIN
    ADDRESS_MAX = c.IPV4.PREFIXLEN_MAX

    OCTET_MIN = c.IPV4.OCTET_MIN
    OCTET_MAX = c.IPV4.OCTET_MAX

    def __init__(self, address: str) -> None:
        valids.validate_address_str(address)
        self._addr = convs.address_to_int(address)

    @classmethod
    def from_int(cls, number: int) -> "IPv4Address":
        valids.validate_address_int(number)
        obj = cls.__new__(cls)
        obj._addr = number
        return obj

    @classmethod
    def from_cidr(cls, address: str) -> "IPv4Address":
        addr, prefixlen = address.split(c.DELIMITERS.SLASH, maxsplit=1)
        if int(prefixlen) != cls.PREFIXLEN_MAX:
            raise ValueError(
                f"Invalid address prefixlen, expected: {cls.PREFIXLEN_MAX}"
            )

        return cls(addr)

    @functools.cached_property
    def address(self) -> str:
        return convs.int_to_address(self._addr)

    @functools.cached_property
    def cidr(self) -> str:
        return c.DELIMITERS.SLASH.join_as_str(self.address, self.PREFIXLEN_MAX.value)

    def __int__(self) -> int:
        return self._addr

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    def __hash__(self) -> int:
        return hash(self._addr)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and self._addr < other._addr

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and self._addr == other._addr


class IPv4Network:
    def __init__(self, network: str) -> None:
        # TODO(d.burmistrov): move this block into util? (validate + convert)
        addr, prefixlen = network.split(c.DELIMITERS.SLASH, maxsplit=1)
        valids.validate_address_str(addr)
        valids.validate_prefixlen_str(prefixlen)
        prefixlen = int(prefixlen)
        valids.validate_network_int(convs.address_to_int(addr), prefixlen)

        self._populate(IPv4Address(addr), prefixlen)

    def _populate(self, netaddr: IPv4Address, prefixlen: int) -> None:
        self._prefixlen = prefixlen
        self._netaddr = netaddr
        m = c.IPV4.ADDRESS_MAX
        self._netmask = IPv4Address.from_int(m ^ (m >> prefixlen))

    @classmethod
    def from_int(cls, int_addr: int, prefixlen: int) -> "IPv4Network":
        valids.validate_address_int(int_addr)
        valids.validate_prefixlen_int(prefixlen)
        valids.validate_network_int(int_addr, prefixlen)

        obj = cls.__new__(cls)
        obj._populate(IPv4Address.from_int(int_addr), prefixlen)
        return obj

    def as_tuple(self) -> tuple[int, int]:
        return int(self.netaddress), self._prefixlen

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    def __hash__(self) -> int:
        return hash(self.as_tuple())

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
        return c.DELIMITERS.SLASH.join_as_str(self._netaddr.address, self._prefixlen)

    @functools.cached_property
    def hostmask(self) -> IPv4Address:
        return IPv4Address.from_int(int(self._netmask) ^ c.IPV4.ADDRESS_MAX)

    @functools.cached_property
    def broadcast(self) -> IPv4Address:
        return IPv4Address.from_int(int(self._netaddr) | int(self.hostmask))

    def subnets(
        self,
        prefixlen: int | None = None,
    ) -> t.Generator["IPv4Network", None, None]:
        new_prefixlen = self._prefixlen + 1
        if prefixlen:
            valids.validate_prefixlen_int(prefixlen, min_len=new_prefixlen)
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
            valids.validate_prefixlen_int(prefixlen, max_len=new_prefixlen)
            new_prefixlen = prefixlen

        prefixlen_diff = self._prefixlen - new_prefixlen
        addr = int(self._netaddr) & (int(self._netmask) << prefixlen_diff)

        return IPv4Network.from_int(addr, new_prefixlen)

    def hosts(self):
        start = int(self._netaddr) + 1
        end = int(self.broadcast)

        for addr in range(start, end):
            yield IPv4Address.from_int(addr)


class IPv4Interface:
    def __init__(self, address: str) -> None:
        addr, prefixlen = address.split(c.DELIMITERS.SLASH, maxsplit=1)
        self._addr = IPv4Address(addr)

        prefixlen = int(prefixlen)
        netmask = c.IPV4.ADDRESS_MAX ^ (c.IPV4.ADDRESS_MAX >> prefixlen)
        netaddr = int(self._addr) & netmask
        self._network = IPv4Network.from_int(netaddr, prefixlen)

    def __repr__(self) -> str:
        ip = c.DELIMITERS.SLASH.join_as_str(self._addr.address, self._network.prefixlen)
        return f'{self.__class__.__name__}("{ip}")'

    def __hash__(self) -> int:
        return hash((self._addr, self._network))

    def __eq__(self, other: t.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._addr == other._addr
            and self._network == other._network
        )

    @property
    def network(self) -> "IPv4Network":
        return self._network

    @property
    def address(self) -> "IPv4Address":
        return self._addr
