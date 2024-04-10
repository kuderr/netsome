from netsome import constants as c
from netsome._converters import bgp as converters


def validate_asplain(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid asplain type, must be int")

    if not (c.ZERO <= number <= c.ASN_MAX):
        raise ValueError(
            f"Invalid asplain number. Must be in range {c.ZERO}-{c.ASN_MAX}"
        )


def validate_asdotplus(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid asdot+ type, must be str")

    if c.DOT not in string:
        raise ValueError("Invalid asdot+ format, must be HIGH_ORDER.LOW_ORDER")

    validate_asplain(converters.asdotplus_to_asplain(string))


def validate_asdot(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid asdot type, must be str")

    if c.DOT in string:
        validate_asdotplus(string)
        return

    validate_asplain(int(string))


def validate_community(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid Community type, must be str")

    if string.count(c.COLON) != 1:
        raise ValueError(
            "Invalid Community format, delimiter must be colon – ASN:VALUE"
        )

    asn, value = map(int, string.split(c.COLON, maxsplit=1))
    if not (c.ZERO <= asn <= c.ASN_ORDER_MAX):
        raise ValueError(
            f"Invalid ASN in Community. Must be in range {c.ZERO}-{c.ASN_ORDER_MAX}"
        )
    if not (c.ZERO <= value <= c.ASN_ORDER_MAX):
        raise ValueError(
            f"Invalid VALUE number in Community. Must be in range {c.ZERO}-{c.ASN_ORDER_MAX }"
        )
