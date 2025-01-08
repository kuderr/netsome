# pyright: strict, reportUninitializedInstanceVariable=false, reportUnreachable=false, reportUnnecessaryIsInstance=false

import collections.abc as cabc
import functools
import typing as t

from netsome import constants as c
from netsome._converters import ipv6 as convs
from netsome.validators import ipv6 as valids


def _compress_ipv6_address(addr_str: str) -> str:
    """
    Naive IPv6 compression:
      1) Remove leading zeros from each block.
      2) Replace longest run of zero-blocks with "::".
    """
    blocks = addr_str.split(c.DELIMITERS.COLON)
    # Remove leading zeros in each block
    blocks = [block.lstrip("0") or "0" for block in blocks]

    # Find longest sequence of consecutive "0" blocks
    best_start = -1
    best_length = 0
    current_start = -1
    current_length = 0
    for i, block in enumerate(blocks):
        if block == "0":
            if current_start == -1:
                current_start = i
                current_length = 1
            else:
                current_length += 1
        else:
            if current_length > best_length:
                best_length = current_length
                best_start = current_start
            current_start = -1
            current_length = 0
    # Edge case: check at the end
    if current_length > best_length:
        best_length = current_length
        best_start = current_start

    # Replace sequence with "::"
    if best_length > 1:
        blocks = (
            blocks[:best_start]
            + [""]  # placeholder for "::"
            + blocks[best_start + best_length :]
        )

    compressed = c.DELIMITERS.COLON.join(blocks)
    # Handle edge cases like all-zero "::"
    compressed = compressed.replace(":::", "::")
    if compressed == "":
        compressed = "::"
    elif compressed.startswith(":") and not compressed.startswith("::"):
        compressed = ":" + compressed
    elif compressed.endswith(":") and not compressed.endswith("::"):
        compressed = compressed + ":"
    return compressed


class IPv6Address:
    """
    Represents an IPv6 address.

    Stores and manipulates individual IPv6 addresses. They can be created from
    standard IPv6 notation or integer values.

    Args:
        address (str): IPv6 address (e.g. "2001:db8::1")

    Raises:
        TypeError: If input is not a string
        ValueError: If address format is invalid
    """

    PREFIXLEN_MIN = c.IPV6.PREFIXLEN_MIN
    PREFIXLEN_MAX = c.IPV6.PREFIXLEN_MAX

    ADDRESS_MIN = c.IPV6.ADDRESS_MIN
    ADDRESS_MAX = c.IPV6.ADDRESS_MAX

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
    def uncompressed(self) -> str:
        return convs.int_to_address(self._addr)

    @functools.cached_property
    def address(self) -> str:
        return _compress_ipv6_address(self.uncompressed)

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

    A network address with a prefix length, supporting subnet calculations
    and containment checks.

    Args:
        network (str): Network in CIDR notation (e.g. "2001:db8::/32")

    Raises:
        TypeError: If input is not a string
        ValueError: If network format is invalid
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
        m = c.IPV6.ADDRESS_MAX
        self._netmask = IPv6Address.from_int(m ^ (m >> prefixlen))

    @classmethod
    def from_int(cls, int_addr: int, prefixlen: int) -> "IPv6Network":
        valids.validate_address_int(int_addr)
        valids.validate_prefixlen_int(prefixlen)
        valids.validate_network_int(int_addr, prefixlen)
        obj = cls.__new__(cls)
        obj._populate(IPv6Address.from_int(int_addr), prefixlen)
        return obj

    @classmethod
    def from_cidr(cls, string: str) -> "IPv6Network":
        addr, *prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
        obj = cls.from_address(addr)
        if prefixlen:
            p = prefixlen[0]
            valids.validate_prefixlen_str(p)
            if obj.prefixlen != int(p):
                raise ValueError(
                    f'Provided prefixlen "{p}" is invalid for network "{addr}",'
                    + f' should be "{obj.prefixlen}"'
                )
        return obj

    @classmethod
    def from_address(cls, string: str) -> "IPv6Network":
        obj = cls.__new__(cls)
        obj._populate(IPv6Address(string), c.IPV6.PREFIXLEN_MAX.value)
        return obj

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
        return _compress_ipv6_address(self.uncompressed)

    @functools.cached_property
    def uncompressed(self) -> str:
        return c.DELIMITERS.SLASH.join_as_str(self._netaddr.address, self._prefixlen)

    @functools.cached_property
    def hostmask(self) -> IPv6Address:
        return IPv6Address.from_int(int(self._netmask) ^ c.IPV6.ADDRESS_MAX)

    @functools.cached_property
    def broadcast(self) -> IPv6Address:
        return IPv6Address.from_int(int(self._netaddr) | int(self.hostmask))

    def subnets(
        self,
        prefixlen: int | None = None,
    ) -> cabc.Generator["IPv6Network", None, None]:
        new_prefixlen = prefixlen or self._prefixlen + 1
        valids.validate_prefixlen_int(new_prefixlen, min_len=self._prefixlen + 1)
        prefixlen_diff = new_prefixlen - self._prefixlen
        start = int(self._netaddr)
        end = int(self.broadcast) + 1
        step = (int(self.hostmask) + 1) >> prefixlen_diff
        for addr in range(start, end, step):
            yield IPv6Network.from_int(addr, new_prefixlen)

    def supernet(
        self,
        prefixlen: int | None = None,
    ) -> "IPv6Network":
        new_prefixlen = prefixlen or self._prefixlen - 1
        valids.validate_prefixlen_int(new_prefixlen, max_len=self._prefixlen - 1)
        diff = self._prefixlen - new_prefixlen
        addr = int(self._netaddr) & (int(self._netmask) << diff)
        return IPv6Network.from_int(addr, new_prefixlen)

    def hosts(self) -> cabc.Generator["IPv6Address", None, None]:
        start = int(self._netaddr) + 1
        end = int(self.broadcast)
        if self._prefixlen + 2 > c.IPV6.PREFIXLEN_MAX:
            start -= 1
            end += 1
        for addr in range(start, end):
            yield IPv6Address.from_int(addr)

    def contains_subnet(self, subnet: "IPv6Network") -> bool:
        if not isinstance(subnet, self.__class__):
            raise TypeError(
                f'Unable to process value "{subnet}" of type "{type(subnet)}"'
            )
        return (
            self != subnet
            and self.netaddress <= subnet.netaddress
            and self.broadcast >= subnet.broadcast
        )

    def contains_address(self, address: IPv6Address) -> bool:
        if not isinstance(address, IPv6Address):
            raise TypeError(
                f'Unable to process value "{address}" of type "{type(address)}"'
            )
        return self.netaddress <= address <= self.broadcast


class IPv6Interface:
    """
    Represents an IPv6 interface.

    Combines an IPv6 address with its associated network, representing
    a network interface configuration.

    Args:
        address (str): Interface address in CIDR notation (e.g. "2001:db8::1/64")

    Raises:
        TypeError: If input is not a string
        ValueError: If address or network format is invalid
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
        netmask = c.IPV6.ADDRESS_MAX ^ (c.IPV6.ADDRESS_MAX >> prefixlen_)
        netaddr = int(self._addr) & netmask
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
    def address(self) -> IPv6Address:
        return self._addr

    @property
    def network(self) -> IPv6Network:
        return self._network

    @functools.cached_property
    def ip(self) -> str:
        return _compress_ipv6_address(self.uncompressed)

    @functools.cached_property
    def uncompressed(self) -> str:
        return c.DELIMITERS.SLASH.join_as_str(
            self._addr.address, self._network.prefixlen
        )
