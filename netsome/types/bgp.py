from netsome import constants as c
from netsome.validators import bgp as validators


def _asdotplus_to_asplain(string: str) -> int:
    high_order, low_order = map(int, string.split(c.DOT, maxsplit=1))
    return high_order * c.TWO_BYTES + low_order


def _asdot_to_asplain(string: str) -> int:
    if c.DOT in string:
        return _asdotplus_to_asplain(string)

    return int(string)


def _asplain_to_asdot(number: int) -> str:
    high_order, low_order = divmod(number, c.TWO_BYTES)
    return f"{high_order}{c.DOT}{low_order}" if high_order else str(low_order)


def _asplain_to_asdotplus(number: int) -> str:
    high_order, low_order = divmod(number, c.TWO_BYTES)
    return f"{high_order}{c.DOT}{low_order}"


class ASN:
    def __init__(self, number: int) -> None:
        validators.validate_asplain(number)
        self._number = number

    @classmethod
    def from_asdot(cls, string: str) -> "ASN":
        validators.validate_asdot(string)
        return cls(_asdot_to_asplain(string))

    @classmethod
    def from_asdotplus(cls, string: str) -> "ASN":
        validators.validate_asdotplus(string)
        return cls(_asdotplus_to_asplain(string))

    @classmethod
    def from_asplain(cls, number: int) -> "ASN":
        validators.validate_asplain(number)
        return cls(number)

    def to_asdot(self):
        return _asplain_to_asdot(self._number)

    def to_asdotplus(self):
        return _asplain_to_asdotplus(self._number)

    def to_asplain(self):
        return self._number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"
