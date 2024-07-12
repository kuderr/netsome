import contextlib
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

        raise ValueError

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
