from netsome import constants as c


def address_to_int(string: str) -> int:
    """Convert IPv6 address string to 128-bit integer."""
    string = string.lower()

    # Handle IPv4-mapped IPv6 addresses (::ffff:192.0.2.1)
    if "." in string:
        return _handle_ipv4_mapped(string)

    # Handle :: compression or regular format
    groups = _parse_address_groups(string)

    # Convert groups to integer
    return _groups_to_int(groups)


def _handle_ipv4_mapped(string: str) -> int:
    """Handle IPv4-mapped IPv6 addresses."""
    if string.startswith("::ffff:"):
        ipv4_part = string[7:]  # Remove '::ffff:'
        ipv4_octets = ipv4_part.split(".")
        if len(ipv4_octets) == 4:
            ipv4_int = int.from_bytes(
                bytes(int(octet) for octet in ipv4_octets), byteorder="big"
            )
            return (0xFFFF << 32) + ipv4_int
    raise ValueError(
        f"Unsupported IPv4-mapped format: {string}. "
        + "Only '::ffff:x.x.x.x' format is supported (e.g., '::ffff:192.0.2.1')"
    )


def _parse_address_groups(string: str) -> list[str]:
    """Parse IPv6 address string into groups."""
    if "::" in string:
        return _handle_compression(string)
    else:
        return _handle_regular_format(string)


def _handle_compression(string: str) -> list[str]:
    """Handle :: compression in IPv6 address."""
    if string.count("::") > 1:
        raise ValueError(
            f"Invalid address '{string}': multiple '::' compressions found. "
            + "Only one '::' is allowed per address"
        )

    parts = string.split("::")
    left_groups = parts[0].split(":") if parts[0] else []
    right_groups = parts[1].split(":") if parts[1] else []

    # Remove empty strings from splitting
    left_groups = [g for g in left_groups if g]
    right_groups = [g for g in right_groups if g]

    # Calculate missing groups
    missing_groups = c.IPV6.GROUPS_COUNT - len(left_groups) - len(right_groups)
    if missing_groups < 0:
        raise ValueError(
            f"Invalid address '{string}': too many groups. "
            + f"Expected at most {c.IPV6.GROUPS_COUNT} groups"
        )

    # Reconstruct full groups list
    return left_groups + ["0"] * missing_groups + right_groups


def _handle_regular_format(string: str) -> list[str]:
    """Handle regular IPv6 address format without compression."""
    groups = string.split(":")
    if len(groups) != c.IPV6.GROUPS_COUNT:
        raise ValueError(
            f"Invalid number of groups: {len(groups)}, "
            + f"expected: {c.IPV6.GROUPS_COUNT}"
        )
    return groups


def _groups_to_int(groups: list[str]) -> int:
    """Convert list of hex groups to integer."""
    result = 0
    for i, group in enumerate(groups):
        if not group:
            group = "0"
        if len(group) > 4:
            raise ValueError(
                f"Invalid IPv6 group '{group}': groups must be 1-4 hexadecimal digits"
            )

        try:
            group_int = int(group, 16)
        except ValueError:
            raise ValueError(
                f"Invalid IPv6 group '{group}': "
                + "must contain only hexadecimal digits (0-9, a-f)"
            )

        if not (c.IPV6.GROUP_MIN <= group_int <= c.IPV6.GROUP_MAX):
            raise ValueError(
                f"Invalid IPv6 group value {group_int}: "
                + f"must be between {c.IPV6.GROUP_MIN} and {c.IPV6.GROUP_MAX}"
            )

        result |= group_int << ((c.IPV6.GROUPS_COUNT - 1 - i) * c.IPV6.BITS_PER_GROUP)

    return result


def int_to_address(number: int) -> str:
    """Convert 128-bit integer to IPv6 address string."""
    if not (c.IPV6.ADDRESS_MIN <= number <= c.IPV6.ADDRESS_MAX):
        raise ValueError(f"Address integer out of range: {number}")

    # Extract groups
    groups: list[str] = []
    for i in range(c.IPV6.GROUPS_COUNT):
        shift = (c.IPV6.GROUPS_COUNT - 1 - i) * c.IPV6.BITS_PER_GROUP
        group = (number >> shift) & c.IPV6.GROUP_MAX
        groups.append(f"{group:x}")

    # Apply compression rules
    return _compress_address(":".join(groups))


def _compress_address(address: str) -> str:
    """Apply IPv6 compression rules to address string."""
    groups = address.split(":")

    # Find the longest sequence of consecutive zero groups
    max_zero_start = -1
    max_zero_length = 0
    current_zero_start = -1
    current_zero_length = 0

    for i, group in enumerate(groups):
        if group == "0":
            if current_zero_start == -1:
                current_zero_start = i
                current_zero_length = 1
            else:
                current_zero_length += 1
        else:
            if current_zero_length > max_zero_length:
                max_zero_start = current_zero_start
                max_zero_length = current_zero_length
            current_zero_start = -1
            current_zero_length = 0

    # Check final sequence
    if current_zero_length > max_zero_length:
        max_zero_start = current_zero_start
        max_zero_length = current_zero_length

    # Apply compression if we found a sequence of 2 or more zeros
    if max_zero_length >= 2:
        left = groups[:max_zero_start]
        right = groups[max_zero_start + max_zero_length :]

        if not left and not right:
            return "::"
        elif not left:
            return "::" + ":".join(right)
        elif not right:
            return ":".join(left) + "::"
        else:
            return ":".join(left) + "::" + ":".join(right)

    return address


def expand_address(address: str) -> str:
    """Expand IPv6 address to full form without compression."""
    # Convert to int and back to get standardized form
    addr_int = address_to_int(address)

    # Extract groups and format with leading zeros
    groups: list[str] = []
    for i in range(c.IPV6.GROUPS_COUNT):
        shift = (c.IPV6.GROUPS_COUNT - 1 - i) * c.IPV6.BITS_PER_GROUP
        group = (addr_int >> shift) & c.IPV6.GROUP_MAX
        groups.append(f"{group:04x}")

    return ":".join(groups)
