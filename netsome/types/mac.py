import contextlib
import functools
import typing as t

from netsome import constants as c
from netsome.validators import mac as valids


class MacAddress:
    """
    Represents a MAC-48/EUI-48 address.

    The MacAddress class handles MAC addresses in various formats and provides
    methods to check address properties and format conversions.

    Args:
        addr (str): MAC address as 12 hex digits (e.g. "001122334455")

    Raises:
        TypeError: If input is not a string
        ValueError: If MAC address format is invalid

    Examples:
        >>> mac = MacAddress("001122334455")
        >>> mac.to_str(delimiter=":")
        '00:11:22:33:44:55'
        >>> mac.oui
        '001122'
        >>> mac.is_unicast()
        True
    """

    MIN = c.MAC.ADDRESS_MIN
    MAX = c.MAC.ADDRESS_MAX

    OUI_MAX = c.MAC.OUI_MAX
    NIC_MAX = c.MAC.NIC_MAX

    # can be calculated from const above
    ADDR_STRING_SIZE = 12
    OUI_PART_STRING_SIZE = 6

    def __init__(self, addr: str) -> None:
        valids.validate_hex_string(addr, self.ADDR_STRING_SIZE)
        self._addr = int(addr, base=c.NUMERALSYSTEMS.HEX)

    @functools.cached_property
    def address(self) -> str:
        addr = hex(self._addr)[2:]  # ignore 0x part
        leading_zeros = "0" * (self.ADDR_STRING_SIZE - len(addr))
        return leading_zeros + addr

    @functools.cached_property
    def oui(self) -> str:
        return self.address[: self.OUI_PART_STRING_SIZE]

    @functools.cached_property
    def nic(self) -> str:
        return self.address[self.OUI_PART_STRING_SIZE :]

    def is_multicast(self) -> bool:
        # TODO: 40 to const, calculate from cls consts
        return bool(self._addr & 1 << 40)

    def is_unicast(self) -> bool:
        return not self.is_multicast()

    def is_local(self) -> bool:
        return bool(self._addr & 2 << 40)

    def is_global(self) -> bool:
        return not self.is_local()

    @classmethod
    def from_dashed(cls, string: str) -> "MacAddress":
        return cls(string.replace(c.DELIMITERS.DASH, ""))

    @classmethod
    def from_coloned(cls, string: str) -> "MacAddress":
        return cls(string.replace(c.DELIMITERS.COLON, ""))

    @classmethod
    def from_dotted(cls, string: str) -> "MacAddress":
        return cls(string.replace(c.DELIMITERS.DOT, ""))

    @classmethod
    def from_int(cls, number: int) -> "MacAddress":
        valids.validate_int(number)
        obj = cls.__new__(cls)
        obj._addr = number
        return obj

    @classmethod
    def parse(cls, addr: str | int) -> "MacAddress":
        # TODO: can collect all this from cls attrs?
        from_fmts = (
            cls,
            cls.from_dashed,
            cls.from_coloned,
            cls.from_dotted,
            cls.from_int,
        )

        for fmt in from_fmts:
            with contextlib.suppress(Exception):
                return fmt(addr)

        raise ValueError(f'Unable to parse "{addr}" of type "{type(addr)}"')

    @functools.lru_cache
    def to_str(
        self,
        delimiter: c.DELIMITERS = c.DELIMITERS.DASH,
        group_len: int = 2,
    ) -> str:
        addr = self.address
        groups = (addr[i : i + group_len] for i in range(0, len(addr), group_len))

        return delimiter.join(groups)

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


# TBD
class Mac64Address:
    """
    Represents an EUI-64 address.

    The Mac64Address class handles 64-bit extended unique identifiers used in
    IPv6 address generation and other contexts.

    Note:
        This class is currently a placeholder and needs implementation.

    Args:
        addr (str): 64-bit MAC address as 16 hex digits

    Raises:
        TypeError: If input is not a string
        ValueError: If address format is invalid
    """

    MIN = c.MAC.ADDRESS_MIN
    MAX = c.MAC.ADDRESS64_MAX

    OUI_MAX = c.MAC.OUI_MAX
    NIC_MAX = c.MAC.NIC64_MAX
