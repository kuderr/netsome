import pytest

from netsome import constants as c
from netsome import types


@pytest.mark.parametrize(
    "test_input",
    (
        "::",
        "::1",
        "2001:db8::1",
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "fe80::1",
        "ff02::1",
        "::ffff:192.0.2.1",
    ),
)
def test_init_ok(test_input):
    assert types.IPv6Address(test_input)


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Address(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "",
        "invalid",
        "2001:db8::1::2",  # Multiple ::
        "2001:db8:gggg::1",  # Invalid hex
        "2001:db8::12345",  # Group too long
        "2001:db8:1:2:3:4:5:6:7:8:9",  # Too many groups
        "2001:db8::1/64",  # CIDR not allowed in address
        "::ffff:256.1.1.1",  # Invalid IPv4 in mapped address
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Address(test_input)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        (0, "::"),
        (1, "::1"),
        (0x20010DB8000000000000000000000001, "2001:db8::1"),
        (c.IPV6.ADDRESS_MAX, "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
    ),
)
def test_from_int_ok(test_input, expected):
    addr = types.IPv6Address.from_int(test_input)
    assert str(addr) == expected


@pytest.mark.parametrize("test_input", (-1, c.IPV6.ADDRESS_MAX + 1, 1.1, "string"))
def test_from_int_error(test_input):
    with pytest.raises((TypeError, ValueError)):
        types.IPv6Address.from_int(test_input)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("::1/128", "::1"),
        ("2001:db8::1/128", "2001:db8::1"),
    ),
)
def test_from_cidr_ok(test_input, expected):
    addr = types.IPv6Address.from_cidr(test_input)
    assert str(addr) == expected


@pytest.mark.parametrize(
    "test_input",
    (
        "::1/127",  # Not /128
        "::1/64",  # Not /128
        "invalid/128",  # Invalid address
        "::1",  # Missing prefix
    ),
)
def test_from_cidr_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Address.from_cidr(test_input)


def test_int_conversion():
    addr = types.IPv6Address("2001:db8::1")
    assert int(addr) == 0x20010DB8000000000000000000000001


def test_str_representation():
    addr = types.IPv6Address("2001:0db8:0000:0000:0000:0000:0000:0001")
    assert str(addr) == "2001:db8::1"  # Should be compressed


def test_repr():
    addr = types.IPv6Address("2001:db8::1")
    assert repr(addr) == 'IPv6Address("2001:db8::1")'


def test_compressed_property():
    addr = types.IPv6Address("2001:0db8:0000:0000:0000:0000:0000:0001")
    assert addr.compressed == "2001:db8::1"


def test_expanded_property():
    addr = types.IPv6Address("2001:db8::1")
    assert addr.expanded == "2001:0db8:0000:0000:0000:0000:0000:0001"


def test_cidr_property():
    addr = types.IPv6Address("2001:db8::1")
    assert addr.cidr == "2001:db8::1/128"


@pytest.mark.parametrize(
    ("address", "is_multicast"),
    (
        ("ff02::1", True),
        ("ff00::1", True),
        ("2001:db8::1", False),
        ("::", False),
    ),
)
def test_is_multicast(address, is_multicast):
    addr = types.IPv6Address(address)
    assert addr.is_multicast == is_multicast


@pytest.mark.parametrize(
    ("address", "is_link_local"),
    (
        ("fe80::1", True),
        ("fe80::", True),
        ("2001:db8::1", False),
        ("fec0::1", False),  # Site-local (deprecated)
    ),
)
def test_is_link_local(address, is_link_local):
    addr = types.IPv6Address(address)
    assert addr.is_link_local == is_link_local


@pytest.mark.parametrize(
    ("address", "is_loopback"),
    (
        ("::1", True),
        ("::", False),
        ("2001:db8::1", False),
    ),
)
def test_is_loopback(address, is_loopback):
    addr = types.IPv6Address(address)
    assert addr.is_loopback == is_loopback


@pytest.mark.parametrize(
    ("address", "is_unspecified"),
    (
        ("::", True),
        ("::1", False),
        ("2001:db8::1", False),
    ),
)
def test_is_unspecified(address, is_unspecified):
    addr = types.IPv6Address(address)
    assert addr.is_unspecified == is_unspecified


@pytest.mark.parametrize(
    ("address", "is_private"),
    (
        ("fc00::1", True),
        ("fd00::1", True),
        ("fe00::1", False),
        ("2001:db8::1", False),
    ),
)
def test_is_private(address, is_private):
    addr = types.IPv6Address(address)
    assert addr.is_private == is_private


def test_is_global():
    global_addr = types.IPv6Address("2001:db8::1")
    assert global_addr.is_global

    private_addr = types.IPv6Address("fc00::1")
    assert not private_addr.is_global

    loopback_addr = types.IPv6Address("::1")
    assert not loopback_addr.is_global


def test_hash():
    addr1 = types.IPv6Address("2001:db8::1")
    addr2 = types.IPv6Address("2001:0db8:0000:0000:0000:0000:0000:0001")
    addr3 = types.IPv6Address("2001:db8::2")

    assert hash(addr1) == hash(addr2)  # Same address, different representation
    assert hash(addr1) != hash(addr3)  # Different addresses


def test_equality():
    addr1 = types.IPv6Address("2001:db8::1")
    addr2 = types.IPv6Address("2001:0db8:0000:0000:0000:0000:0000:0001")
    addr3 = types.IPv6Address("2001:db8::2")

    assert addr1 == addr2  # Same address, different representation
    assert addr1 != addr3  # Different addresses
    assert addr1 != "not an address"  # Different type


def test_comparison():
    addr1 = types.IPv6Address("2001:db8::1")
    addr2 = types.IPv6Address("2001:db8::2")
    addr3 = types.IPv6Address("2001:db8::1")

    assert addr1 < addr2
    assert addr2 > addr1
    assert addr1 <= addr3
    assert addr1 >= addr3
    assert not (addr1 > addr2)
    assert not (addr2 < addr1)


def test_comparison_with_different_types():
    addr = types.IPv6Address("2001:db8::1")

    # __eq__ returns NotImplemented, which Python converts to False for !=
    assert addr != "string"  # This should be True

    # Other comparison operators should return NotImplemented which raises TypeError
    with pytest.raises(TypeError):
        addr < "string"
    with pytest.raises(TypeError):
        addr <= "string"
    with pytest.raises(TypeError):
        addr > "string"
    with pytest.raises(TypeError):
        addr >= "string"
