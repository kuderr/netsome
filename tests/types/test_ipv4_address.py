import pytest

from netsome import constants as c
from netsome import types


@pytest.mark.parametrize(
    "test_input",
    (
        "0.0.0.0",
        "1.1.1.1",
        "255.255.255.255",
    ),
)
def test_init_ok(test_input):
    assert types.IPv4Address(test_input)


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv4Address(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "zzxxccvvbbnn",
        "aabbcc",
        "-1.1.1.1",
        "1.1.1.1/32",
        "1.1.1.1/24",
        "255.255.255.256",
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv4Address(test_input)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        (0, "0.0.0.0"),
        (256**0, "0.0.0.1"),
        (256**1, "0.0.1.0"),
        (256**2, "0.1.0.0"),
        (256**3, "1.0.0.0"),
        (256**3 + 256**2 + 256**1 + 256**0, "1.1.1.1"),
        (c.IPV4.ADDRESS_MAX, "255.255.255.255"),
    ),
)
def test_from_int_ok(test_input, expected):
    assert types.IPv4Address.from_int(test_input) == types.IPv4Address(expected)


@pytest.mark.parametrize("test_input", ("1.1.1.1", "aabbccddeeff", 1.1, [], object()))
def test_from_int_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv4Address.from_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-c.IPV4.ADDRESS_MAX, -1, c.IPV4.ADDRESS_MAX + 1),
)
def test_from_int_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv4Address.from_int(test_input)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("0.0.0.0/32", "0.0.0.0"),
        ("0.0.0.1/32", "0.0.0.1"),
        ("0.0.1.0/32", "0.0.1.0"),
        ("0.1.0.0/32", "0.1.0.0"),
        ("1.0.0.0/32", "1.0.0.0"),
        ("1.1.1.1/32", "1.1.1.1"),
        ("255.255.255.255/32", "255.255.255.255"),
    ),
)
def test_from_cidr_ok(test_input, expected):
    assert types.IPv4Address.from_cidr(test_input) == types.IPv4Address(expected)


@pytest.mark.parametrize("test_input", (1, 1.1, [], object()))
def test_from_cidr_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv4Address.from_cidr(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("1.1.1.1/31", "1.1.1.1"),
)
def test_from_cidr_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv4Address.from_cidr(test_input)


@pytest.mark.parametrize(
    ("addr", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_addr"),
            "1.1.1.1",
        ),
    ),
)
def test_property_address(addr, expected):
    assert addr.address == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_addr"),
            "1.1.1.1/32",
        ),
    ),
)
def test_property_cidr(addr, expected):
    assert addr.cidr == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_addr"),
            256**3 + 256**2 + 256**1 + 256**0,
        ),
    ),
)
def test_int(addr, expected):
    assert int(addr) == expected


@pytest.mark.parametrize(
    ("addr", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_addr"),
            'IPv4Address("1.1.1.1")',
        ),
    ),
)
def test_repr(addr, expected):
    assert repr(addr) == expected


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv4_addr"),),
)
def test_hash(addr):
    assert hash(addr) == hash(addr._addr)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv4_addr"),),
)
def test_eq(addr):
    assert addr == types.IPv4Address.from_int(int(addr))


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv4_addr"),),
)
def test_lt(addr):
    assert addr < types.IPv4Address.from_int(int(addr) + 1)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv4_addr"),),
)
def test_le(addr):
    assert addr <= types.IPv4Address.from_int(int(addr))
    assert addr <= types.IPv4Address.from_int(int(addr) + 1)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv4_addr"),),
)
def test_gt(addr):
    assert addr > types.IPv4Address.from_int(int(addr) - 1)


@pytest.mark.parametrize(
    "addr",
    (pytest.lazy_fixture("ipv4_addr"),),
)
def test_ge(addr):
    assert addr >= types.IPv4Address.from_int(int(addr))
    assert addr >= types.IPv4Address.from_int(int(addr) - 1)
