# pyright: strict, reportUnnecessaryIsInstance=false, reportUnreachable=false

from netsome import constants as c


def validate_cidr(string: str) -> None:
    """
    Validates that the input is a valid IPv6 CIDR string.
    E.g., '::1/128' or '2001:db8::/64'.
    """
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string=}" of type "{type(string)}", str expected'
        )

    if c.DELIMITERS.SLASH not in string:
        raise ValueError(f'CIDR format required, got "{string}"')

    addr, prefixlen = string.split(c.DELIMITERS.SLASH, maxsplit=1)
    validate_address_str(addr)
    validate_prefixlen_str(prefixlen)


def validate_address_str(address: str) -> None:
    """
    Validates that the input is a valid IPv6 address string.
    This basic check ensures it's a string with at least one colon.
    For robust validation, consider expanding or using ipaddress.
    """
    if not isinstance(address, str):
        raise TypeError(
            f'Provided invalid value "{address=}" of type "{type(address)}",'
            + " str expected"
        )

    if c.DELIMITERS.COLON not in address:
        raise ValueError(f'Invalid IPv6 address format: "{address}"')


def validate_address_int(number: int) -> None:
    """
    Validates that the integer is in the allowed IPv6 range.
    """
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number=}" of type "{type(number)}", int expected'
        )

    if not (c.IPV6.ADDRESS_MIN <= number <= c.IPV6.ADDRESS_MAX):
        raise ValueError(
            f'Value "{number=}" must be in IPv6 range '
            + f"{c.IPV6.ADDRESS_MIN}-{c.IPV6.ADDRESS_MAX}"
        )


def validate_prefixlen_str(string: str) -> None:
    """
    Validates that the prefix length is a valid integer string,
    then checks if it's within the IPv6 prefix length range.
    """
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string=}" of type "{type(string)}", str expected'
        )

    if not (string.isascii() and string.isdigit()):
        raise ValueError(f'Provided value "{string=}" is invalid prefixlen')

    validate_prefixlen_int(int(string))


def validate_prefixlen_int(
    number: int,
    min_len: int = c.IPV6.PREFIXLEN_MIN,
    max_len: int = c.IPV6.PREFIXLEN_MAX,
) -> None:
    """
    Validates that the prefix length integer is within the allowed IPv6 range.
    """
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number=}" of type "{type(number)}", int expected'
        )

    if not isinstance(min_len, int) or not isinstance(max_len, int):
        raise TypeError(
            f'One of provided len borders "{min_len=}", "{max_len=}" is not of type int'
        )

    if not (min_len <= number <= max_len):
        raise ValueError(f'Value "{number}" must be in range {min_len}-{max_len}')


def validate_network_int(address: int, prefixlen: int) -> None:
    """
    Validates that the address/prefix combination represents
    a valid IPv6 network boundary.
    Raises an error if any host bits are set outside the network mask.
    """
    validate_address_int(address)
    validate_prefixlen_int(prefixlen)

    netmask = c.IPV6.ADDRESS_MAX ^ (c.IPV6.ADDRESS_MAX >> prefixlen)
    if address & netmask != address:
        raise ValueError("Host bits set outside of network mask")
