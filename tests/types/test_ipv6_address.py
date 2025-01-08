import pytest

from netsome import constants as c
from netsome import types


@pytest.mark.parametrize(
    "test_input",
    (
        "::",
        "::1",
        "2001:db8::",
        "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
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
        "gggg::",
        "-::1",
        "2001:db8::/64",  # slash is invalid for the address constructor
        "ffff:ffff:ffff:ffff:ffff:ffff:ffff:10000",
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
        (c.IPV6.ADDRESS_MAX, "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
    ),
)
def test_from_int_ok(test_input, expected):
    assert types.IPv6Address.from_int(test_input) == types.IPv6Address(expected)


@pytest.mark.parametrize("test_input", ("::1", 1.1, [], object()))
def test_from_int_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Address.from_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, c.IPV6.ADDRESS_MAX + 1),
)
def test_from_int_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Address.from_int(test_input)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("::/128", "::"),
        ("2001:db8::FF/128", "2001:db8::ff"),
    ),
)
def test_from_cidr_ok(test_input, expected):
    assert types.IPv6Address.from_cidr(test_input) == types.IPv6Address(expected)


@pytest.mark.parametrize("test_input", (1, 1.1, [], object()))
def test_from_cidr_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Address.from_cidr(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("::/127", "2001:db8::/64", "ffff::/129"),
)
def test_from_cidr_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Address.from_cidr(test_input)


@pytest.mark.parametrize(
    ("addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), "::1"),),
)
def test_property_address(addr, expected):
    assert addr.address == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), "::1/128"),),
)
def test_property_cidr(addr, expected):
    assert addr.cidr == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), 1),),
)
def test_int(addr, expected):
    assert int(addr) == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), "::1"),),
)
def test_str(addr, expected):
    assert str(addr) == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), 'IPv6Address("::1")'),),
)
def test_repr(addr, expected):
    assert repr(addr) == expected


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_hash(addr):
    assert hash(addr) == hash(addr._addr)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_eq(addr):
    assert addr == types.IPv6Address.from_int(int(addr))


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_lt(addr):
    assert addr < types.IPv6Address.from_int(int(addr) + 1)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_le(addr):
    assert addr <= types.IPv6Address.from_int(int(addr))
    assert addr <= types.IPv6Address.from_int(int(addr) + 1)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_gt(addr):
    assert addr > types.IPv6Address.from_int(int(addr) - 1)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_ge(addr):
    assert addr >= types.IPv6Address.from_int(int(addr))
    assert addr >= types.IPv6Address.from_int(int(addr) - 1)
