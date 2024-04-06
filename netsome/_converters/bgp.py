from netsome import constants as c


def asdotplus_to_asplain(string: str) -> int:
    high_order, low_order = map(int, string.split(c.DOT, maxsplit=1))
    return high_order * c.TWO_BYTES + low_order


def asdot_to_asplain(string: str) -> int:
    if c.DOT in string:
        return asdotplus_to_asplain(string)

    return int(string)


def asplain_to_asdot(number: int) -> str:
    high_order, low_order = divmod(number, c.TWO_BYTES)
    return f"{high_order}{c.DOT}{low_order}" if high_order else str(low_order)


def asplain_to_asdotplus(number: int) -> str:
    high_order, low_order = divmod(number, c.TWO_BYTES)
    return f"{high_order}{c.DOT}{low_order}"
