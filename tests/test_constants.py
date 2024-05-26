import pytest
from netsome import constants as c


# Ensure constants to never change unexpectedly
@pytest.mark.parametrize(
    ("constant", "value"),
    (
        # NUMERALSYSTEMS
        (c.NUMERALSYSTEMS.BIN, 2),
        (c.NUMERALSYSTEMS.DEC, 10),
        (c.NUMERALSYSTEMS.HEX, 16),
        # BYTES
        (c.BYTES.ZERO, 0),
        (c.BYTES.ONE, 2**8),
        (c.BYTES.TWO, 2 ** (8 * 2)),
        (c.BYTES.THREE, 2 ** (8 * 3)),
        (c.BYTES.FOUR, 2 ** (8 * 4)),
        (c.BYTES.FIVE, 2 ** (8 * 5)),
        (c.BYTES.SIX, 2 ** (8 * 6)),
        (c.BYTES.EIGHT, 2 ** (8 * 8)),
        # DELIMITERS
        (c.DELIMITERS.DASH, "-"),
        (c.DELIMITERS.DOT, "."),
        (c.DELIMITERS.COLON, ":"),
        (c.DELIMITERS.SLASH, "/"),
        # IPV4
        (c.IPV4.PREFIXLEN_MIN, 0),
        (c.IPV4.PREFIXLEN_MAX, 32),
        (c.IPV4.ADDRESS_MIN, 0),
        (c.IPV4.ADDRESS_MAX, 2 ** (8 * 4) - 1),
        (c.IPV4.OCTET_MIN, 0),
        (c.IPV4.OCTET_MAX, 2**8 - 1),
        # VLAN
        (c.VLAN.VID_MIN, 0),
        (c.VLAN.VID_MAX, 2**12 - 1),
        (c.VLAN.VID_DEFAULT, 1),
        # BGP
        (c.BGP.ASN_MIN, 0),
        (c.BGP.ASN_MAX, 2 ** (8 * 4) - 1),
        (c.BGP.ASN_ORDER_MAX, 2 ** (8 * 2) - 1),
        # MAC
        (c.MAC.ADDRESS_MIN, 0),
        (c.MAC.ADDRESS_MAX, 2 ** (8 * 6) - 1),
        (c.MAC.OUI_MAX, 2 ** (8 * 3) - 1),
        (c.MAC.NIC_MAX, 2 ** (8 * 3) - 1),
        (c.MAC.NIC64_MAX, 2 ** (8 * 5) - 1),
        (c.MAC.ADDRESS64_MAX, 2 ** (8 * 8) - 1),
    ),
)
def test_constant(constant, value):
    assert constant == value
