import contextlib
import functools
import typing as t

from netsome import constants as c
from netsome._converters import ipv4 as convs
from netsome.validators import ipv4 as valids


class IPv4Address:
    """
    Represents an IPv4 address.

    Class provides a way to store and manipulate individual IPv4 addresses.
    Addresses can be created from strings in dotted decimal notation or integer values.

    Args:
        address (str): IPv4 address in dotted decimal notation (e.g. "192.168.1.1")

    Raises:
        TypeError: If input is not a string
        ValueError: If address format is invalid

    Examples:
        >>> addr = IPv4Address("192.168.1.1")
        >>> str(addr)
        '192.168.1.1'
        >>> int(addr)
        3232235777
    """

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
    def from_cidr(cls, string: str) -> "IPv4Address":
        valids.validate_cidr(string)

        addr, prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
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

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    def __hash__(self) -> int:
        return hash(self._addr)

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._addr == other._addr)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._addr < other._addr)

    def __le__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._addr <= other._addr)

    def __gt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._addr > other._addr)

    def __ge__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._addr >= other._addr)


class IPv4Network:
    """
    Represents an IPv4 network.

    The IPv4Network class represents a network address with a prefix length.
    It provides methods for subnet calculations and address containment checks.

    Args:
        network (str): Network in CIDR notation (e.g. "192.168.1.0/24")

    Raises:
        TypeError: If input is not a string
        ValueError: If network format is invalid or has host bits set

    Examples:
        >>> net = IPv4Network("192.168.1.0/24")
        >>> net.broadcast
        IPv4Address('192.168.1.255')
        >>> list(net.subnets(prefixlen=25))
        [IPv4Network('192.168.1.0/25'), IPv4Network('192.168.1.128/25')]
    """

    def __init__(self, network: str) -> None:
        valids.validate_cidr(network)

        addr, prefixlen = network.split(c.DELIMITERS.SLASH, maxsplit=1)
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

    @classmethod
    def from_cidr(cls, string: str) -> "IPv4Network":
        addr, *prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
        obj = cls.from_octets(addr)

        if prefixlen:
            prefixlen = prefixlen[0]
            valids.validate_prefixlen_str(prefixlen)
            if obj.prefixlen != int(prefixlen):
                raise ValueError(
                    f'Provided prefixlen "{prefixlen}" is invalid for network "{addr}",'
                    f' should be "{obj.prefixlen}"'
                )

        return obj

    @classmethod
    def from_address(cls, string: str) -> "IPv4Network":
        obj = cls.__new__(cls)
        obj._populate(IPv4Address(string), c.IPV4.PREFIXLEN_MAX.value)
        return obj

    @classmethod
    def from_octets(cls, string: str) -> "IPv4Network":
        octets = string.split(c.DELIMITERS.DOT)
        if len(octets) > c.IPV4.OCTETS_COUNT:
            raise ValueError(
                f'Provided value "{string}" should have'
                f' less than "{c.IPV4.OCTETS_COUNT}" octets'
            )

        for octet in octets:
            valids.validate_octet_str(octet)

        prefixlen = len(octets) * 8
        octets += ["0"] * (c.IPV4.OCTETS_COUNT - len(octets))
        addr = c.DELIMITERS.DOT.join(octets)

        obj = cls.__new__(cls)
        obj._populate(IPv4Address(addr), prefixlen)

        return obj

    @classmethod
    def parse(cls, string: str) -> "IPv4Network":
        from_fmts = (
            cls,
            cls.from_address,
            cls.from_cidr,
            cls.from_octets,
        )

        for fmt in from_fmts:
            with contextlib.suppress(Exception):
                return fmt(string)

        raise ValueError(f'Unable to parse "{string}" of type "{type(string)}"')

    def as_tuple(self) -> tuple[int, int]:
        return int(self.netaddress), self._prefixlen

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def __eq__(self, other: t.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and (self._netaddr == other._netaddr)
            and (self._prefixlen == other._prefixlen)
        )

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
        new_prefixlen = prefixlen or self._prefixlen + 1
        valids.validate_prefixlen_int(new_prefixlen, min_len=self._prefixlen + 1)

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
        new_prefixlen = prefixlen or self._prefixlen - 1
        valids.validate_prefixlen_int(new_prefixlen, max_len=self._prefixlen - 1)

        prefixlen_diff = self._prefixlen - new_prefixlen
        addr = int(self._netaddr) & (int(self._netmask) << prefixlen_diff)

        return IPv4Network.from_int(addr, new_prefixlen)

    def hosts(self) -> t.Generator["IPv4Address", None, None]:
        start = int(self._netaddr) + 1
        end = int(self.broadcast)

        # TODO(kuderr): make it prettier?
        # /31 and /32 prefixlens
        if self._prefixlen + 2 > c.IPV4.PREFIXLEN_MAX:
            start -= 1
            end += 1

        for addr in range(start, end):
            yield IPv4Address.from_int(addr)

    def contains_subnet(self, subnet: "IPv4Network") -> bool:
        if not isinstance(subnet, self.__class__):
            raise TypeError(
                f'Unable to process value "{subnet}" of type "{type(subnet)}"'
            )

        return (
            self != subnet
            and self.netaddress <= subnet.netaddress
            and self.broadcast >= subnet.broadcast
        )

    def contains_address(self, address: IPv4Address) -> bool:
        if not isinstance(address, IPv4Address):
            raise TypeError(
                f'Unable to process value "{address}" of type "{type(address)}"'
            )

        return self.netaddress <= address <= self.broadcast


class IPv4Interface:
    """
    Represents an IPv4 interface.

    The IPv4Interface class combines an IPv4 address with its associated network,
    representing a network interface configuration.

    Args:
        address (str): Interface address in CIDR notation (e.g. "192.168.1.1/24")

    Raises:
        TypeError: If input is not a string
        ValueError: If address or network format is invalid

    Examples:
        >>> iface = IPv4Interface("192.168.1.1/24")
        >>> iface.address
        IPv4Address('192.168.1.1')
        >>> iface.network
        IPv4Network('192.168.1.0/24')
    """

    def __init__(self, address: str) -> None:
        valids.validate_cidr(address)
        addr, prefixlen = address.split(c.DELIMITERS.SLASH, maxsplit=1)
        self._populate(addr, prefixlen)

    @classmethod
    def from_simple(cls, address: str, prefixlen: str) -> "IPv4Interface":
        obj = cls.__new__(cls)
        obj._populate(address, prefixlen)
        return obj

    def _populate(self, address: str, prefixlen: str) -> None:
        prefixlen = int(prefixlen)
        self._addr = IPv4Address(address)
        netmask = c.IPV4.ADDRESS_MAX ^ (c.IPV4.ADDRESS_MAX >> prefixlen)
        netaddr = int(self._addr) & netmask
        self._network = IPv4Network.from_int(netaddr, prefixlen)

    @classmethod
    def from_objects(
        cls,
        address: IPv4Address,
        network: IPv4Network,
    ) -> "IPv4Interface":
        if not isinstance(address, IPv4Address):
            raise TypeError(f'Unable to create "{cls.__name__}" from "{address=}"')

        if not isinstance(network, IPv4Network):
            raise TypeError(f'Unable to create "{cls.__name__}" from "{network=}"')

        if not network.contains_address(address):
            raise ValueError(f'Provided "{network=}" doesnt contain "{address=}"')

        obj = cls.__new__(cls)
        obj._addr = address
        obj._network = network
        return obj

    def as_tuple(self) -> tuple[IPv4Address, IPv4Network]:
        return self.address, self.network

    def __str__(self) -> str:
        return self.ip

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.ip}")'

    def __hash__(self) -> int:
        return hash((self._addr, self._network))

    def __eq__(self, other: t.Any) -> bool:
        return (
            isinstance(other, self.__class__)
            and self._addr == other._addr
            and self._network == other._network
        )

    @property
    def address(self) -> "IPv4Address":
        return self._addr

    @property
    def network(self) -> "IPv4Network":
        return self._network

    @functools.cached_property
    def ip(self) -> str:
        return c.DELIMITERS.SLASH.join_as_str(
            self._addr.address, self._network.prefixlen
        )
