import contextlib
import typing as t

from netsome import constants as c
from netsome._converters import bgp as convs
from netsome.validators import bgp as valids


# TODO(kuderr): can move some common stuff to Base class


class ASN:
    """
    Represents a BGP Autonomous System Number.

    An ASN can be represented in different formats:
    - asplain: decimal number (e.g. 65000)
    - asdot: hybrid decimal/dot notation for 4-byte ASNs (e.g. 65000 or 64512.1)
    - asdotplus: mandatory dot notation for all ASNs (e.g. 0.65000 or 1.10)

    Args:
        number (int): ASN value in asplain format (0 to 4294967295)

    Raises:
        TypeError: If input is not an integer
        ValueError: If input is outside valid range

    Examples:
        >>> asn = ASN(65000)
        >>> str(asn)
        '65000'
        >>> asn.to_asdot()
        '65000'
        >>> asn.to_asdotplus()
        '0.65000'
    """

    MIN = c.BGP.ASN_MIN
    MAX = c.BGP.ASN_MAX
    ORDER_MAX = c.BGP.ASN_ORDER_MAX

    def __init__(self, number: int) -> None:
        valids.validate_asplain(number)
        self._number = number

    @property
    def number(self) -> int:
        return self._number

    @classmethod
    def from_asdot(cls, string: str) -> "ASN":
        valids.validate_asdot(string)
        return cls(convs.asdot_to_asplain(string))

    @classmethod
    def from_asdotplus(cls, string: str) -> "ASN":
        valids.validate_asdotplus(string)
        return cls(convs.asdotplus_to_asplain(string))

    @classmethod
    def from_asplain(cls, string: str) -> "ASN":
        return cls(int(string))

    @classmethod
    def parse(cls, value: str | int) -> "ASN":
        from_fmts = (
            cls,
            cls.from_asdot,
            cls.from_asdotplus,
            cls.from_asplain,
        )

        for fmt in from_fmts:
            with contextlib.suppress(Exception):
                return fmt(value)

        raise ValueError(f'Unable to parse "{value}" of type "{type(value)}"')

    def to_asdot(self) -> str:
        return convs.asplain_to_asdot(self._number)

    def to_asdotplus(self) -> str:
        return convs.asplain_to_asdotplus(self._number)

    def to_asplain(self) -> str:
        return str(self._number)

    def __int__(self) -> int:
        return self._number

    def __str__(self) -> str:
        return self.to_asplain()

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number == other._number)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number < other._number)

    def __le__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number <= other._number)

    def __gt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number > other._number)

    def __ge__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number >= other._number)

    def __hash__(self) -> int:
        return hash(self._number)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"


class Community:
    """
    Represents a BGP community value.

    BGP communities are represented as ASN:VALUE pairs where both ASN and VALUE
    are 16-bit numbers.

    Args:
        number (int): Community value as 32-bit integer

    Raises:
        TypeError: If input is not an integer
        ValueError: If input is outside valid range

    Examples:
        >>> comm = Community.from_str('65000:100')
        >>> str(comm)
        '65000:100'
        >>> int(comm)
        4259840100
    """

    def __init__(self, number: int) -> None:
        valids.validate_asplain(number)
        self._number = number

    @property
    def number(self) -> int:
        return self._number

    @classmethod
    def from_str(cls, string: str) -> "Community":
        valids.validate_community(string)
        return cls(convs.community_to_asplain(string))

    def __int__(self) -> int:
        return self._number

    def __str__(self) -> str:
        return convs.asplain_to_community(self._number)

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number == other._number)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number < other._number)

    def __le__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number <= other._number)

    def __gt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number > other._number)

    def __ge__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number >= other._number)

    def __hash__(self) -> int:
        return hash(self._number)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"
