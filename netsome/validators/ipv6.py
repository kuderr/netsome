# pyright: strict, reportUnnecessaryIsInstance=false, reportUnreachable=false
from netsome import constants as c


def validate_cidr(string: str) -> None:
    """Validate IPv6 CIDR notation string."""
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string=}" of type "{type(string)}", str expected'
        )

    parts = string.split(c.DELIMITERS.SLASH)
    if len(parts) != 2:
        raise ValueError(
            f'Invalid CIDR format "{string}", expected format: address/prefixlen'
        )

    addr, prefixlen = parts
    validate_address_str(addr)
    validate_prefixlen_str(prefixlen)


def validate_address_str(string: str) -> None:
    """Validate IPv6 address string format."""
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string=}" of type "{type(string)}", str expected'
        )

    if not string:
        raise ValueError("IPv6 address cannot be empty")

    string = string.lower()

    # Check for IPv4-mapped IPv6 addresses
    if "." in string:
        _validate_ipv4_mapped_format(string)
        return

    # Validate regular IPv6 format
    _validate_regular_ipv6_format(string)


def _validate_ipv4_mapped_format(string: str) -> None:
    """Validate IPv4-mapped IPv6 address format."""
    if not string.startswith("::ffff:"):
        raise ValueError(f"Invalid IPv4-mapped IPv6 format: {string}")
    ipv4_part = string[7:]
    _validate_ipv4_in_ipv6(ipv4_part)


def _validate_regular_ipv6_format(string: str) -> None:
    """Validate regular IPv6 address format."""
    # Check for multiple :: occurrences
    if string.count("::") > 1:
        raise ValueError(f'Multiple "::" found in address: {string}')

    # Handle :: compression
    if "::" in string:
        _validate_compressed_format(string)
    else:
        _validate_full_format(string)


def _validate_compressed_format(string: str) -> None:
    """Validate IPv6 address with :: compression."""
    parts = string.split("::")
    left_groups = parts[0].split(":") if parts[0] else []
    right_groups = parts[1].split(":") if parts[1] else []

    # Remove empty strings
    left_groups = [g for g in left_groups if g]
    right_groups = [g for g in right_groups if g]

    total_groups = len(left_groups) + len(right_groups)
    if total_groups >= c.IPV6.GROUPS_COUNT:
        raise ValueError(f"Too many groups in compressed address: {string}")

    # Validate each group
    for group in left_groups + right_groups:
        validate_group_str(group)


def _validate_full_format(string: str) -> None:
    """Validate IPv6 address without compression."""
    groups = string.split(":")
    if len(groups) != c.IPV6.GROUPS_COUNT:
        raise ValueError(
            f"Invalid number of groups: {len(groups)}, "
            + f"expected: {c.IPV6.GROUPS_COUNT}"
        )

    for group in groups:
        validate_group_str(group)


def validate_address_int(number: int) -> None:
    """Validate IPv6 address as 128-bit integer."""
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number=}" of type "{type(number)}", '
            + "int expected"
        )

    if not (c.IPV6.ADDRESS_MIN <= number <= c.IPV6.ADDRESS_MAX):
        raise ValueError(
            f'Value "{number}" must be in range '
            + f"{c.IPV6.ADDRESS_MIN}-{c.IPV6.ADDRESS_MAX}"
        )


def validate_group_str(string: str) -> None:
    """Validate IPv6 hexadecimal group string."""
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string=}" of type "{type(string)}", str expected'
        )

    if not string:
        raise ValueError("IPv6 group cannot be empty")

    if len(string) > 4:
        raise ValueError(f'IPv6 group too long: "{string}", max 4 characters')

    # Check if valid hexadecimal
    try:
        group_int = int(string, 16)
    except ValueError:
        raise ValueError(f'Invalid hexadecimal group: "{string}"')

    validate_group_int(group_int)


def validate_group_int(number: int) -> None:
    """Validate IPv6 group as integer."""
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number=}" of type "{type(number)}", int expected'
        )

    if not (c.IPV6.GROUP_MIN <= number <= c.IPV6.GROUP_MAX):
        raise ValueError(
            f'IPv6 group value "{number}" must be in range '
            + f"{c.IPV6.GROUP_MIN}-{c.IPV6.GROUP_MAX}"
        )


def validate_prefixlen_str(string: str) -> None:
    """Validate IPv6 prefix length string."""
    if not isinstance(string, str):
        raise TypeError(
            f'Provided invalid value "{string=}" of type "{type(string)}", str expected'
        )

    if not (string.isascii() and string.isdigit()):
        raise ValueError(f'Provided value "{string}" is invalid prefixlen')

    validate_prefixlen_int(int(string))


def validate_prefixlen_int(
    number: int,
    min_len: int = c.IPV6.PREFIXLEN_MIN,
    max_len: int = c.IPV6.PREFIXLEN_MAX,
) -> None:
    """Validate IPv6 prefix length as integer."""
    if not isinstance(number, int):
        raise TypeError(
            f'Provided invalid value "{number=}" of type "{type(number)}", int expected'
        )

    if not (isinstance(min_len, int) and isinstance(max_len, int)):
        raise TypeError(
            f'One of provided len borders "{min_len=}", "{max_len=}" is not of type int'
        )

    if not (min_len <= number <= max_len):
        raise ValueError(f'Value "{number}" must be in range {min_len}-{max_len}')


def validate_network_int(address: int, prefixlen: int) -> None:
    """Validate that network address has no host bits set."""
    if prefixlen == 0:
        return  # All bits are network bits

    host_bits = c.IPV6.PREFIXLEN_MAX - prefixlen
    if host_bits == 0:
        return  # No host bits to check

    # Create mask with host bits set
    host_mask = (1 << host_bits) - 1

    if address & host_mask != 0:
        raise ValueError("Host bits set in network address")


def _validate_ipv4_in_ipv6(ipv4_str: str) -> None:
    """Validate IPv4 part of IPv4-mapped IPv6 address."""
    octets = ipv4_str.split(".")
    if len(octets) != 4:
        raise ValueError(f"Invalid IPv4 format in IPv6: {ipv4_str}")

    for octet in octets:
        if not octet.isdigit():
            raise ValueError(f"Invalid IPv4 octet: {octet}")

        octet_int = int(octet)
        if not (0 <= octet_int <= 255):
            raise ValueError(f"IPv4 octet out of range: {octet_int}")

        # Check for leading zeros (except for '0' itself)
        if octet != "0" and octet.startswith("0"):
            raise ValueError(f"Invalid IPv4 octet format: {octet}")
