from netsome import constants as c


def validate_cidr(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid type")

    addr, prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
    validate_address_str(addr)
    validate_prefixlen_str(prefixlen)


def validate_address_str(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid type")

    octets = tuple(map(int, string.split(c.DELIMITERS.DOT)))
    if len(octets) != c.IPV4.OCTETS_COUNT:
        raise ValueError()

    for octet in octets:
        validate_octet_int(octet)


def validate_address_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid type")

    if not (c.IPV4.ADDRESS_MIN <= number <= c.IPV4.ADDRESS_MAX):
        raise ValueError("Invalid value")


def validate_octet_str(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError("Invalid type")

    if not (string.isascii() and string.isdigit()):
        raise ValueError("Invalid octet format")

    if string != "0" and string.startswith("0"):
        raise ValueError("Invalid octet format")

    validate_octet_int(int(string))


def validate_octet_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError("Invalid type")

    if not (c.IPV4.OCTET_MIN <= number <= c.IPV4.OCTET_MAX):
        raise ValueError("Invalid value")


def validate_prefixlen_str(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError()

    # TODO(dm.a.kudryavtsev): можно вынести в валидатор строки на проверку что внутри число
    if not (string.isascii() and string.isdigit()):
        raise ValueError()

    validate_prefixlen_int(int(string))


# TODO(dm.a.kudryavtsev): можно сделать общим валидатором на значение
def validate_prefixlen_int(
    number: int,
    min_len: int = c.IPV4.PREFIXLEN_MIN,
    max_len: int = c.IPV4.PREFIXLEN_MAX,
) -> None:
    if not isinstance(number, int):
        raise TypeError()

    if not (min_len <= number <= max_len):
        raise ValueError()


def validate_network_int(address: int, prefixlen: int) -> None:
    netmask = c.IPV4.ADDRESS_MAX ^ (c.IPV4.ADDRESS_MAX >> prefixlen)
    if address & netmask != address:
        raise ValueError("host bits set")
