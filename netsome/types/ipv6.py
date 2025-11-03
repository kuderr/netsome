# pyright: strict, reportUninitializedInstanceVariable=false, reportUnreachable=false, reportUnnecessaryIsInstance=false

import collections.abc as cabc
import contextlib
import functools
import typing as t

from netsome import constants as c
from netsome._converters import ipv6 as convs
from netsome.validators import ipv6 as valids


class IPv6Address:
    """
    Represents an IPv6 address.

    Class provides a way to store and manipulate individual IPv6 addresses.
    Addresses can be created from strings in standard IPv6 notation or integer values.

    Args:
        address (str): IPv6 address in standard notation (e.g. "2001:db8::1")

    Raises:
        TypeError: If input is not a string
        ValueError: If address format is invalid

    Examples:
        >>> addr = IPv6Address("2001:db8::1")
        >>> str(addr)
        '2001:db8::1'
        >>> int(addr)
        42540766411282592856903984951653826561
    """

    PREFIXLEN_MIN = c.IPV6.PREFIXLEN_MIN
    PREFIXLEN_MAX = c.IPV6.PREFIXLEN_MAX

    ADDRESS_MIN = c.IPV6.ADDRESS_MIN
    ADDRESS_MAX = c.IPV6.ADDRESS_MAX

    GROUP_MIN = c.IPV6.GROUP_MIN
    GROUP_MAX = c.IPV6.GROUP_MAX

    def __init__(self, address: str) -> None:
        valids.validate_address_str(address)
        self._addr = convs.address_to_int(address)

    @classmethod
    def from_int(cls, number: int) -> "IPv6Address":
        valids.validate_address_int(number)
        obj = cls.__new__(cls)
        obj._addr = number
        return obj

    @classmethod
    def from_cidr(cls, string: str) -> "IPv6Address":
        valids.validate_cidr(string)

        addr, prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
        if int(prefixlen) != cls.PREFIXLEN_MAX:
            raise ValueError(
                f"Invalid address prefixlen, expected: {cls.PREFIXLEN_MAX}"
            )

        return cls(addr)

    @functools.cached_property
    def address(self) -> str:
        """Compressed IPv6 address representation."""
        return convs.int_to_address(self._addr)

    @functools.cached_property
    def cidr(self) -> str:
        """IPv6 address in CIDR notation with /128."""
        return c.DELIMITERS.SLASH.join_as_str(self.address, self.PREFIXLEN_MAX.value)

    @functools.cached_property
    def compressed(self) -> str:
        """Compressed IPv6 address (same as address)."""
        return self.address

    @functools.cached_property
    def expanded(self) -> str:
        """Expanded IPv6 address without compression."""
        return convs.expand_address(self.address)

    @functools.cached_property
    def is_multicast(self) -> bool:
        """True if address is multicast (ff00::/8)."""
        return (self._addr >> 120) == 0xFF

    @functools.cached_property
    def is_link_local(self) -> bool:
        """True if address is link-local (fe80::/10)."""
        return (self._addr >> 118) == 0x3FA

    @functools.cached_property
    def is_loopback(self) -> bool:
        """True if address is loopback (::1)."""
        return self._addr == 1

    @functools.cached_property
    def is_unspecified(self) -> bool:
        """True if address is unspecified (::)."""
        return self._addr == 0

    @functools.cached_property
    def is_private(self) -> bool:
        """True if address is private/unique local (fc00::/7)."""
        return (self._addr >> 121) == 0x7E

    @functools.cached_property
    def is_global(self) -> bool:
        """True if address is global unicast."""
        return not (
            self.is_multicast
            or self.is_link_local
            or self.is_loopback
            or self.is_unspecified
            or self.is_private
        )

    def __int__(self) -> int:
        return self._addr

    def __str__(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    def __hash__(self) -> int:
        return hash(self._addr)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._addr == other._addr

    def __lt__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._addr < other._addr

    def __le__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._addr <= other._addr

    def __gt__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._addr > other._addr

    def __ge__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._addr >= other._addr


class IPv6Network:
    """
    Represents an IPv6 network.

    The IPv6Network class represents a network address with a prefix length.
    It provides methods for subnet calculations and address containment checks.

    Args:
        network (str): Network in CIDR notation (e.g. "2001:db8::/32")

    Raises:
        TypeError: If input is not a string
        ValueError: If network format is invalid or has host bits set

    Examples:
        >>> net = IPv6Network("2001:db8::/32")
        >>> net.prefixlen
        32
        >>> list(net.subnets(prefixlen=33))
        [IPv6Network('2001:db8::/33'), IPv6Network('2001:db8:8000::/33')]
    """

    def __init__(self, network: str) -> None:
        valids.validate_cidr(network)

        addr, prefixlen = network.split(c.DELIMITERS.SLASH, maxsplit=1)
        prefixlen = int(prefixlen)
        valids.validate_network_int(convs.address_to_int(addr), prefixlen)

        self._prefixlen = prefixlen
        self._populate(IPv6Address(addr), prefixlen)

    def _populate(self, netaddr: IPv6Address, prefixlen: int) -> None:
        self._prefixlen = prefixlen
        self._netaddr = netaddr

        # Calculate netmask
        if prefixlen == 0:
            netmask_int = 0
        else:
            netmask_int = (
                c.IPV6.ADDRESS_MAX << (c.IPV6.PREFIXLEN_MAX - prefixlen)
            ) & c.IPV6.ADDRESS_MAX

        self._netmask = IPv6Address.from_int(netmask_int)

    @classmethod
    def from_int(cls, int_addr: int, prefixlen: int) -> "IPv6Network":
        valids.validate_address_int(int_addr)
        valids.validate_prefixlen_int(prefixlen)
        valids.validate_network_int(int_addr, prefixlen)

        obj = cls.__new__(cls)
        obj._populate(IPv6Address.from_int(int_addr), prefixlen)
        return obj

    @classmethod
    def from_address(cls, string: str) -> "IPv6Network":
        obj = cls.__new__(cls)
        obj._populate(IPv6Address(string), c.IPV6.PREFIXLEN_MAX.value)
        return obj

    @classmethod
    def parse(cls, string: str) -> "IPv6Network":
        from_fmts = (
            cls,
            cls.from_address,
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
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._netaddr == other._netaddr and self._prefixlen == other._prefixlen

    def __lt__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.as_tuple() < other.as_tuple()

    def __le__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.as_tuple() <= other.as_tuple()

    def __gt__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.as_tuple() > other.as_tuple()

    def __ge__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.as_tuple() >= other.as_tuple()

    @property
    def prefixlen(self) -> int:
        return self._prefixlen

    @property
    def netaddress(self) -> IPv6Address:
        return self._netaddr

    @property
    def netmask(self) -> IPv6Address:
        return self._netmask

    @functools.cached_property
    def address(self) -> str:
        return c.DELIMITERS.SLASH.join_as_str(self._netaddr.address, self._prefixlen)

    @functools.cached_property
    def hostmask(self) -> IPv6Address:
        return IPv6Address.from_int(int(self._netmask) ^ c.IPV6.ADDRESS_MAX)

    def subnets(
        self,
        prefixlen: int | None = None,
    ) -> cabc.Generator["IPv6Network", None, None]:
        new_prefixlen = prefixlen or self._prefixlen + 1
        valids.validate_prefixlen_int(new_prefixlen, min_len=self._prefixlen + 1)

        subnet_size = 1 << (c.IPV6.PREFIXLEN_MAX - new_prefixlen)

        current_addr = int(self._netaddr)
        network_size = 1 << (c.IPV6.PREFIXLEN_MAX - self._prefixlen)
        end_addr = current_addr + network_size

        while current_addr < end_addr:
            yield IPv6Network.from_int(current_addr, new_prefixlen)
            current_addr += subnet_size

    def supernet(
        self,
        prefixlen: int | None = None,
    ) -> "IPv6Network":
        new_prefixlen = prefixlen or self._prefixlen - 1
        valids.validate_prefixlen_int(new_prefixlen, max_len=self._prefixlen - 1)

        # Calculate supernet address by masking host bits
        if new_prefixlen == 0:
            supernet_addr = 0
        else:
            mask = (
                c.IPV6.ADDRESS_MAX << (c.IPV6.PREFIXLEN_MAX - new_prefixlen)
            ) & c.IPV6.ADDRESS_MAX
            supernet_addr = int(self._netaddr) & mask

        return IPv6Network.from_int(supernet_addr, new_prefixlen)

    def hosts(self) -> cabc.Generator["IPv6Address", None, None]:
        """
        Generate all host addresses in the network.

        Note: Unlike IPv4, IPv6 does not have broadcast addresses, so all addresses
        in the subnet are valid host addresses. This can generate extremely large
        numbers of addresses for networks with small prefix lengths.

        WARNING: Be cautious when calling this on large networks (e.g., /64 or smaller).
        A /64 network contains 2^64 (18+ quintillion) addresses. Consider using
        subnets() to break large networks into smaller chunks instead.

        Yields:
            IPv6Address: Each host address in the network
        """
        if self._prefixlen == c.IPV6.PREFIXLEN_MAX:
            # Single address - yield the address itself
            yield self._netaddr
            return

        # Unlike IPv4, IPv6 has no broadcast address concept.
        # All addresses in an IPv6 subnet are valid host addresses.
        network_size = 1 << (c.IPV6.PREFIXLEN_MAX - self._prefixlen)
        start_addr = int(self._netaddr)

        for i in range(network_size):
            yield IPv6Address.from_int(start_addr + i)

    def contains_subnet(self, subnet: "IPv6Network") -> bool:
        if not isinstance(subnet, self.__class__):
            raise TypeError(
                f'Unable to process value "{subnet}" of type "{type(subnet)}"'
            )

        if self == subnet:
            return False

        # For subnet to be contained, it must have a longer prefix
        if subnet.prefixlen <= self.prefixlen:
            return False

        # Check if subnet's network address is within our network
        return self.contains_address(subnet.netaddress)

    def contains_address(self, address: IPv6Address) -> bool:
        if not isinstance(address, IPv6Address):
            raise TypeError(
                f'Unable to process value "{address}" of type "{type(address)}"'
            )

        if self._prefixlen == 0:
            return True  # Network covers all addresses

        # Apply network mask to both addresses and compare
        mask = int(self._netmask)
        return (int(address) & mask) == (int(self._netaddr) & mask)


class IPv6Interface:
    """
    Represents an IPv6 interface.

    The IPv6Interface class combines an IPv6 address with its associated network,
    representing a network interface configuration.

    Args:
        address (str): Interface address in CIDR notation (e.g. "2001:db8::1/64")

    Raises:
        TypeError: If input is not a string
        ValueError: If address or network format is invalid

    Examples:
        >>> iface = IPv6Interface("2001:db8::1/64")
        >>> iface.address
        IPv6Address('2001:db8::1')
        >>> iface.network
        IPv6Network('2001:db8::/64')
    """

    def __init__(self, address: str) -> None:
        valids.validate_cidr(address)
        addr, prefixlen = address.split(c.DELIMITERS.SLASH, maxsplit=1)
        self._populate(addr, prefixlen)

    @classmethod
    def from_simple(cls, address: str, prefixlen: str) -> "IPv6Interface":
        obj = cls.__new__(cls)
        obj._populate(address, prefixlen)
        return obj

    def _populate(self, address: str, prefixlen: str) -> None:
        prefixlen_ = int(prefixlen)
        self._addr = IPv6Address(address)

        # Calculate network address
        if prefixlen_ == 0:
            netaddr = 0
        else:
            mask = (
                c.IPV6.ADDRESS_MAX << (c.IPV6.PREFIXLEN_MAX - prefixlen_)
            ) & c.IPV6.ADDRESS_MAX
            netaddr = int(self._addr) & mask

        self._network = IPv6Network.from_int(netaddr, prefixlen_)

    @classmethod
    def from_objects(
        cls,
        address: IPv6Address,
        network: IPv6Network,
    ) -> "IPv6Interface":
        if not isinstance(address, IPv6Address):
            raise TypeError(f'Unable to create "{cls.__name__}" from "{address=}"')

        if not isinstance(network, IPv6Network):
            raise TypeError(f'Unable to create "{cls.__name__}" from "{network=}"')

        if not network.contains_address(address):
            raise ValueError(f'Provided "{network=}" doesnt contain "{address=}"')

        obj = cls.__new__(cls)
        obj._addr = address
        obj._network = network
        return obj

    def as_tuple(self) -> tuple[IPv6Address, IPv6Network]:
        return self.address, self.network

    def __str__(self) -> str:
        return self.ip

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.ip}")'

    def __hash__(self) -> int:
        return hash((self._addr, self._network))

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._addr == other._addr and self._network == other._network

    @property
    def address(self) -> "IPv6Address":
        return self._addr

    @property
    def network(self) -> "IPv6Network":
        return self._network

    @functools.cached_property
    def ip(self) -> str:
        return c.DELIMITERS.SLASH.join_as_str(
            self._addr.address, self._network.prefixlen
        )
