from netsome import constants as c
from netsome._converters import bgp as convs


def validate_asplain(
    number: int,
    min_len: int = c.BGP.ASN_MIN,
    max_len: int = c.BGP.ASN_MAX,
) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid asplain type, must be int")

    if not (min_len <= number <= max_len):
        msg = (
            "Invalid asplain number. Must be in range "
            + c.DELIMITERS.DASH.join_as_str(min_len, max_len)
        )
        raise ValueError(msg)


def validate_asdotplus(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid asdot+ type, must be str")

    if c.DELIMITERS.DOT not in string:
        raise ValueError("Invalid asdot+ format, must be HIGH_ORDER.LOW_ORDER")

    validate_asplain(convs.asdotplus_to_asplain(string))


def validate_asdot(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid asdot type, must be str")

    if c.DELIMITERS.DOT in string:
        validate_asdotplus(string)
    else:
        validate_asplain(int(string), max_len=c.BGP.ASN_ORDER_MAX)


def validate_community(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid Community type, must be str")

    asn, value, *unexpected = string.split(c.DELIMITERS.COLON)

    if unexpected:
        msg = "Invalid Community format, delimiter must be colon – ASN:VALUE"
        raise ValueError(msg)

    asn, value = int(asn), int(value)
    if not (c.BGP.ASN_MIN <= asn <= c.BGP.ASN_ORDER_MAX):
        msg = (
            "Invalid ASN in Community. Must be in range "
            + c.DELIMITERS.DASH.join_as_str(c.BGP.ASN_MIN, c.BGP.ASN_ORDER_MAX)
        )
        raise ValueError(msg)
    if not (c.BGP.ASN_MIN <= value <= c.BGP.ASN_ORDER_MAX):
        msg = (
            "Invalid VALUE number in Community. Must be in range "
            + c.DELIMITERS.DASH.join_as_str(c.BGP.ASN_MIN, c.BGP.ASN_ORDER_MAX)
        )
        raise ValueError(msg)
