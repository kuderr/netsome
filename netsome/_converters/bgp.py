from netsome import constants as c


def asdotplus_to_asplain(string: str) -> int:
    high_order, low_order = map(int, string.split(c.DELIMITERS.DOT, maxsplit=1))
    return high_order * c.BYTES.TWO + low_order


def asdot_to_asplain(string: str) -> int:
    if c.DELIMITERS.DOT in string:
        return asdotplus_to_asplain(string)

    return int(string)


def asplain_to_asdot(number: int) -> str:
    high_order, low_order = divmod(number, c.BYTES.TWO)
    if high_order:
        return c.DELIMITERS.DOT.join_as_str(high_order, low_order)

    return str(low_order)


def asplain_to_asdotplus(number: int) -> str:
    return c.DELIMITERS.DOT.join_as_str(*divmod(number, c.BYTES.TWO))


def asplain_to_community(number: int) -> str:
    return c.DELIMITERS.COLON.join_as_str(*divmod(number, c.BYTES.TWO))


def community_to_asplain(string: str) -> int:
    asn, value = map(int, string.split(c.DELIMITERS.COLON, maxsplit=1))
    return asn * c.BYTES.TWO + value
