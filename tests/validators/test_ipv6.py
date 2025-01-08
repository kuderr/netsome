import pytest

from netsome.validators import ipv6 as valids


@pytest.mark.parametrize(
    "test_input",
    ("::", "::1", "2001:db8::", "fe80::42", "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"),
)
def test_validate_address_str_ok(test_input):
    assert valids.validate_address_str(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (0, 1.0, [], tuple(), object),
)
def test_validate_address_str_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_address_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "2001.db8::",
        ":",  # incomplete address
        "2001;db8::",
        "2001:db8::/64",  # includes slash
    ),
)
def test_validate_address_str_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_address_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        0,
        1,
        (2**128) - 1,
    ),
)
def test_validate_address_int_ok(test_input):
    assert valids.validate_address_int(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0", 1.0, [], tuple(), object),
)
def test_validate_address_int_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_address_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, 2**128),
)
def test_validate_address_int_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_address_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0", "64", "128"),
)
def test_validate_prefixlen_str_ok(test_input):
    assert valids.validate_prefixlen_str(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (0, 1.0, [], tuple(), object),
)
def test_validate_prefixlen_str_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_prefixlen_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("-1", "129", "abc"),
)
def test_validate_prefixlen_str_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_prefixlen_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    (0, 64, 128),
)
def test_validate_prefixlen_int_ok(test_input):
    assert valids.validate_prefixlen_int(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0", 1.0, [], tuple(), object),
)
def test_validate_prefixlen_int_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_prefixlen_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, 129),
)
def test_validate_prefixlen_int_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_prefixlen_int(test_input)


@pytest.mark.parametrize(
    ("address", "prefixlen"),
    (
        (0, 128),  # /128 at the lowest possible address
        (0, 64),
        ((2**128) - 1, 128),
    ),
)
def test_validate_network_int_ok(address, prefixlen):
    assert valids.validate_network_int(address, prefixlen) is None


@pytest.mark.parametrize(
    ("address", "prefixlen"),
    [
        # This address has bits set outside /127, so it fails
        (1, 127),
        # Out of address range is handled earlier, but let's keep an example
        ((2**128), 64),
    ],
)
def test_validate_network_int_value_error(address, prefixlen):
    with pytest.raises(ValueError):
        valids.validate_network_int(address, prefixlen)


@pytest.mark.parametrize(
    "test_input",
    (
        "::/128",
        "2001:db8::/64",
        "ffff:ffff:ffff:ffff::/64",
    ),
)
def test_validate_cidr_ok(test_input):
    assert valids.validate_cidr(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (0, 1.0, [], tuple(), object),
)
def test_validate_cidr_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_cidr(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "::",  # Missing slash and prefix
        "2001:db8::",  # Missing prefix
        "2001.db8::/64",  # Invalid address
    ),
)
def test_validate_cidr_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_cidr(test_input)
