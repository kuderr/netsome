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
    ("ipv6_addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), "::1"),),
)
def test_property_address(ipv6_addr, expected):
    assert ipv6_addr.address == expected


@pytest.mark.parametrize(
    ("ipv6_addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), "::1/128"),),
)
def test_property_cidr(ipv6_addr, expected):
    assert ipv6_addr.cidr == expected


@pytest.mark.parametrize(
    ("ipv6_addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), 1),),
)
def test_int(ipv6_addr, expected):
    assert int(ipv6_addr) == expected


@pytest.mark.parametrize(
    ("ipv6_addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), "::1"),),
)
def test_str(ipv6_addr, expected):
    assert str(ipv6_addr) == expected


@pytest.mark.parametrize(
    ("ipv6_addr", "expected"),
    ((pytest.lazy_fixture("ipv6_addr"), 'IPv6Address("::1")'),),
)
def test_repr(ipv6_addr, expected):
    assert repr(ipv6_addr) == expected


@pytest.mark.parametrize(
    "ipv6_addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_hash(ipv6_addr):
    assert hash(ipv6_addr) == hash(ipv6_addr._addr)


@pytest.mark.parametrize(
    "ipv6_addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_eq(ipv6_addr):
    assert ipv6_addr == types.IPv6Address.from_int(int(ipv6_addr))


@pytest.mark.parametrize(
    "ipv6_addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_lt(ipv6_addr):
    assert ipv6_addr < types.IPv6Address.from_int(int(ipv6_addr) + 1)


@pytest.mark.parametrize(
    "ipv6_addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_le(ipv6_addr):
    assert ipv6_addr <= types.IPv6Address.from_int(int(ipv6_addr))
    assert ipv6_addr <= types.IPv6Address.from_int(int(ipv6_addr) + 1)


@pytest.mark.parametrize(
    "ipv6_addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_gt(ipv6_addr):
    assert ipv6_addr > types.IPv6Address.from_int(int(ipv6_addr) - 1)


@pytest.mark.parametrize(
    "ipv6_addr",
    (pytest.lazy_fixture("ipv6_addr"),),
)
def test_ge(ipv6_addr):
    assert ipv6_addr >= types.IPv6Address.from_int(int(ipv6_addr))
    assert ipv6_addr >= types.IPv6Address.from_int(int(ipv6_addr) - 1)
