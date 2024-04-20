import typing as t

from netsome import constants as c
from netsome._converters import bgp as convs
from netsome.validators import bgp as valids

# TODO(kuderr): can move some common stuff to Base class


class ASN:

    MIN = c.BGP.ASN_MIN
    MAX = c.BGP.ASN_MAX
    ORDER_MAX = c.BGP.ASN_ORDER_MAX

    def __init__(self, number: int) -> None:
        valids.validate_asplain(number)
        self._number = number

    @classmethod
    def from_asdot(cls, string: str) -> "ASN":
        valids.validate_asdot(string)
        return cls(convs.asdot_to_asplain(string))

    @classmethod
    def from_asdotplus(cls, string: str) -> "ASN":
        valids.validate_asdotplus(string)
        return cls(convs.asdotplus_to_asplain(string))

    @classmethod
    def from_asplain(cls, number: int) -> "ASN":
        valids.validate_asplain(number)
        return cls(number)

    def to_asdot(self):
        return convs.asplain_to_asdot(self._number)

    def to_asdotplus(self):
        return convs.asplain_to_asdotplus(self._number)

    def to_asplain(self):
        return self._number

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number == other._number)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number < other._number)

    def __hash__(self) -> int:
        return hash(self._number)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"


class Community:
    def __init__(self, number: int) -> None:
        valids.validate_asplain(number)
        self._number = number

    @classmethod
    def from_str(cls, value: str) -> "Community":
        valids.validate_community(value)
        return cls(convs.community_to_asplain(value))

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number == other._number)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._number < other._number)

    def __hash__(self) -> int:
        return hash(self._number)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"
