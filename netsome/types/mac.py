import contextlib
import functools
import re
import typing as t

from netsome import constants as c


# TODO: make common
def validate_hex_string(string: str, size: int) -> None:

    # TODO: make common
    if not isinstance(string, str):
        raise TypeError

    if not re.fullmatch(r"^[0-9a-fA-F]{%s}$" % size, string):
        raise ValueError


# TODO: make common
def validate_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError()

    if not (c.MAC.ADDRESS_MIN <= number <= c.MAC.ADDRESS_MAX):
        raise ValueError()


class MacAddress:
    # MAC-48/EUI-48

    MIN = c.MAC.ADDRESS_MIN
    MAX = c.MAC.ADDRESS_MAX

    OUI_MAX = c.MAC.OUI_MAX
    NIC_MAX = c.MAC.NIC_MAX

    # can be calculated from const above
    ADDR_STRING_SIZE = 12
    OUI_PART_STRING_SIZE = 6

    def __init__(self, addr: str) -> None:
        validate_hex_string(addr, self.ADDR_STRING_SIZE)
        self._addr = int(addr, base=c.NUMERALSYSTEMS.HEX)

    @functools.cached_property
    def address(self):
        addr = hex(self._addr)[2:]  # ignore 0x part
        leading_zeros = "0" * (self.ADDR_STRING_SIZE - len(addr))
        return leading_zeros + addr

    @functools.cached_property
    def oui(self):
        return self.address[: self.OUI_PART_STRING_SIZE]

    @functools.cached_property
    def nic(self):
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
        validate_int(number)
        obj = cls.__new__(cls)
        obj._addr = number
        return obj

    @classmethod
    def parse(cls, addr: str | int) -> "MacAddress":
        # TODO: can collect all this from cls attrs?
        from_fmts = (
            cls.from_dashed,
            cls.from_coloned,
            cls.from_dotted,
            # cls.from_bit_reversed,
            cls.from_int,
        )

        for fmt in from_fmts:
            with contextlib.suppress(Exception):
                return fmt(addr)

        raise ValueError

    @functools.lru_cache
    def to_str(
        self,
        delimiter: c.DELIMITERS = c.DELIMITERS.DASH,
        group_len: int = 2,
    ) -> str:
        addr = self.address
        groups = (addr[i : i + group_len] for i in range(0, len(addr), group_len))

        return delimiter.join(groups)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.address}")'

    def __hash__(self) -> int:
        return hash(self._addr)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and self._addr < other._addr

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and self._addr == other._addr


class Mac64Address:
    # EUI-64

    MIN = c.MAC.ADDRESS_MIN
    MAX = c.MAC.ADDRESS64_MAX

    OUI_MAX = c.MAC.OUI_MAX
    NIC_MAX = c.MAC.NIC64_MAX
