from netsome import constants as c


def address_to_int(string: str) -> int:
    """
    Converts a (possibly compressed) IPv6 address string to a 128-bit integer.
    This implementation does not rely on any external libraries.
    """
    # Split on '::' if present
    if c.DELIMITERS.DOUBLE_COLON in string:
        parts = string.split(c.DELIMITERS.DOUBLE_COLON)
        if len(parts) > 2:
            raise ValueError(f'Invalid IPv6 address: "{string}"')

        left = parts[0].split(c.DELIMITERS.COLON) if parts[0] else []
        right = (
            parts[1].split(c.DELIMITERS.COLON) if len(parts) == 2 and parts[1] else []
        )

        # Calculate how many zero-blocks we need
        missing = 8 - (len(left) + len(right))
        if missing < 1:
            raise ValueError(f'Invalid IPv6 address: "{string}"')

        blocks: list[int] = []
        for block in left:
            blocks.append(int(block, 16) if block else 0)
        blocks.extend([0] * missing)
        for block in right:
            blocks.append(int(block, 16) if block else 0)
    else:
        # No '::', just split and parse normally
        raw_blocks = string.split(c.DELIMITERS.COLON)
        if len(raw_blocks) != 8:
            raise ValueError(f'Invalid IPv6 address: "{string}"')
        blocks = [int(block, 16) if block else 0 for block in raw_blocks]

    # Each block is 16 bits, build a 128-bit integer
    for b in blocks:
        if not (0 <= b <= 0xFFFF):
            raise ValueError(f'Invalid block in IPv6 address: "{b}"')

    raw_bytes: list[int] = []
    for b in blocks:
        raw_bytes.append((b >> 8) & 0xFF)
        raw_bytes.append(b & 0xFF)

    return int.from_bytes(bytes(raw_bytes), byteorder="big")


def int_to_address(number: int) -> str:
    """
    Converts a 128-bit integer to its full (uncompressed) IPv6 address string.
    Example: 1 -> '0:0:0:0:0:0:0:1'
    """
    if not (0 <= number <= c.IPV6.ADDRESS_MAX):
        raise ValueError(f'Integer "{number}" out of IPv6 range')

    raw_bytes = number.to_bytes(16, byteorder="big")
    blocks: list[int] = []
    for i in range(0, 16, 2):
        block = (raw_bytes[i] << 8) | raw_bytes[i + 1]
        blocks.append(block)

    # Convert each 16-bit block back to hex (no compression performed)
    hex_blocks = [f"{block:x}" for block in blocks]
    return c.DELIMITERS.COLON.join(hex_blocks)
