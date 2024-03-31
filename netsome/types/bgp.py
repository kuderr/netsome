from netsome.validators import bgp as validators
from netsome.converters import bgp as converters


class ASN:
    def __init__(self, number: int) -> None:
        validators.validate_asplain(number)
        self._number = number

    @classmethod
    def from_asdot(cls, string: str) -> "ASN":
        validators.validate_asdot(string)
        return cls(converters.asdot_to_asplain(string))

    @classmethod
    def from_asdotplus(cls, string: str) -> "ASN":
        validators.validate_asdotplus(string)
        return cls(converters.asdotplus_to_asplain(string))

    @classmethod
    def from_asplain(cls, number: int) -> "ASN":
        validators.validate_asplain(number)
        return cls(number)

    def to_asdot(self):
        return converters.asplain_to_asdot(self._number)

    def to_asdotplus(self):
        return converters.asplain_to_asdotplus(self._number)

    def to_asplain(self):
        return self._number

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._number})"
