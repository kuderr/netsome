import pytest

from netsome.validators import ipv4 as valids


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0.0", "1.1.1.1", "127.0.0.1", "255.255.255.255"),
)
def test_validate_address_str_ok(test_input):
    valids.validate_address_str(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (0, 1.0, [], tuple(), object),
)
def test_validate_address_str_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_address_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0", "1", "255.255.255.255.0"),
)
def test_validate_address_str_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_address_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 4294967295),
)
def test_validate_address_int_ok(test_input):
    valids.validate_address_int(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0", 1.0, [], tuple(), object),
)
def test_validate_address_int_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_address_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, 4294967296),
)
def test_validate_address_int_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_address_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0", "1", "255"),
)
def test_validate_octet_str_ok(test_input):
    valids.validate_octet_str(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    # TODO(kuderr): move to fixture
    (0, 1.0, [], tuple(), object),
)
def test_validate_octet_str_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_octet_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("-1", "lala", "027", "256"),
)
def test_validate_octet_str_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_octet_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 255),
)
def test_validate_octet_int_ok(test_input):
    valids.validate_octet_int(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0", 1.0, [], tuple(), object),
)
def test_validate_octet_int_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_octet_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, 256),
)
def test_validate_octet_int_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_octet_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0", "1", "32"),
)
def test_validate_prefixlen_str_ok(test_input):
    valids.validate_prefixlen_str(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (0, 1.0, [], tuple(), object),
)
def test_validate_prefixlen_str_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_prefixlen_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("-1", "lala"),
)
def test_validate_prefixlen_str_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_prefixlen_str(test_input)


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 32),
)
def test_validate_prefixlen_int_ok(test_input):
    valids.validate_prefixlen_int(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0", 1.0, [], tuple(), object),
)
def test_validate_prefixlen_int_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_prefixlen_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, 33),
)
def test_validate_prefixlen_int_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_prefixlen_int(test_input)


@pytest.mark.parametrize(
    ("address", "prefixlen"),
    ((65536, 16), (256, 24)),
)
def test_validate_network_int_ok(address, prefixlen):
    valids.validate_network_int(address, prefixlen) is None


@pytest.mark.parametrize(
    ("address", "prefixlen"),
    ((255, 24),),
)
def test_validate_network_int_value_error(address, prefixlen):
    with pytest.raises(ValueError):
        valids.validate_network_int(address, prefixlen)
