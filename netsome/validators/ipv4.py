from netsome import constants as c


def validate_cidr(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string}" of type "{type(string)}", str expected'
        )

    addr, prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
    validate_address_str(addr)
    validate_prefixlen_str(prefixlen)


# TODO: regexp?
def validate_address_str(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string}" of type "{type(string)}",'
            " str expected"
        )

    octets = string.split(c.DELIMITERS.DOT)
    if len(octets) != c.IPV4.OCTETS_COUNT:
        raise ValueError(
            f'Provided value "{string}" has invalid octets count,'
            f' must be "{c.IPV4.OCTETS_COUNT}"'
        )

    for octet in octets:
        validate_octet_str(octet)


def validate_address_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number}" of type "{type(number)}",'
            " int expected"
        )

    if not (c.IPV4.ADDRESS_MIN <= number <= c.IPV4.ADDRESS_MAX):
        raise ValueError(
            f'Value "{number}" must be in range'
            f" {c.IPV4.ADDRESS_MIN}-{c.IPV4.ADDRESS_MAX}"
        )


def validate_octet_str(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string}" of type "{type(string)}", str expected'
        )

    if not (string.isascii() and string.isdigit()):
        raise ValueError(f'Provided value "{string}" has invalid octet format')

    if string != "0" and string.startswith("0"):
        raise ValueError(f'Provided value "{string}" has invalid octet format')

    validate_octet_int(int(string))


def validate_octet_int(number: int) -> None:
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number}" of type "{type(number)}", int expected'
        )

    if not (c.IPV4.OCTET_MIN <= number <= c.IPV4.OCTET_MAX):
        raise ValueError(
            f'Value "{number}" must be in range {c.IPV4.OCTET_MIN}-{c.IPV4.OCTET_MAX}'
        )


def validate_prefixlen_str(string: str) -> None:
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string}" of type "{type(string)}", str expected'
        )

    # TODO(dm.a.kudryavtsev): можно вынести в валидатор строки на проверку что внутри число
    if not (string.isascii() and string.isdigit()):
        raise ValueError(f'Provided value "{string}" is invalid prefixlen')

    validate_prefixlen_int(int(string))


# TODO(dm.a.kudryavtsev): можно сделать общим валидатором на значение
def validate_prefixlen_int(
    number: int,
    min_len: int = c.IPV4.PREFIXLEN_MIN,
    max_len: int = c.IPV4.PREFIXLEN_MAX,
) -> None:
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number}" of type "{type(number)}", int expected'
        )

    if not (min_len <= number <= max_len):
        raise ValueError(f'Value "{number}" must be in range {min_len}-{max_len}')


def validate_network_int(address: int, prefixlen: int) -> None:
    netmask = c.IPV4.ADDRESS_MAX ^ (c.IPV4.ADDRESS_MAX >> prefixlen)
    if address & netmask != address:
        raise ValueError("Host bits set")
