import pytest

from netsome import types


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0.0.0.0/32", types.IPv4Interface("0.0.0.0/32")),
        ("1.1.1.1/16", types.IPv4Interface("1.1.1.1/16")),
        ("255.255.255.255/24", types.IPv4Interface("255.255.255.255/24")),
    ),
)
def test_init_ok(string, expected):
    assert types.IPv4Interface(string) == expected


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv4Interface(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "zzxxccvvbbnn",
        "aabbcc",
        "-1.1.1.1",
        "255.255.255.256",
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv4Interface(test_input)


@pytest.mark.parametrize(
    ("address", "prefixlen", "expected"),
    (
        ("0.0.0.0", 32, types.IPv4Interface("0.0.0.0/32")),
        ("1.1.1.1", 16, types.IPv4Interface("1.1.1.1/16")),
        ("255.255.255.255", 24, types.IPv4Interface("255.255.255.255/24")),
    ),
)
def test_from_simple(address, prefixlen, expected):
    assert types.IPv4Interface.from_simple(address, prefixlen) == expected


@pytest.mark.parametrize(
    ("address", "network", "expected"),
    (
        (
            types.IPv4Address("0.0.0.0"),
            types.IPv4Network("0.0.0.0/32"),
            types.IPv4Interface("0.0.0.0/32"),
        ),
        (
            types.IPv4Address("1.1.1.1"),
            types.IPv4Network("1.1.0.0/16"),
            types.IPv4Interface("1.1.1.1/16"),
        ),
        (
            types.IPv4Address("255.255.255.255"),
            types.IPv4Network("255.255.255.0/24"),
            types.IPv4Interface("255.255.255.255/24"),
        ),
    ),
)
def test_from_objects_ok(address, network, expected):
    assert types.IPv4Interface.from_objects(address, network) == expected


@pytest.mark.parametrize(
    ("address", "network"),
    (
        (
            "0.0.0.0",
            types.IPv4Network("0.0.0.0/32"),
        ),
        (
            types.IPv4Address("1.1.1.1"),
            "1.1.0.0/16",
        ),
        (
            types.IPv4Address("255.255.255.255"),
            1_000,
        ),
        (
            1_000,
            types.IPv4Network("255.255.255.0/24"),
        ),
    ),
)
def test_from_objects_type_error(address, network):
    with pytest.raises(TypeError):
        types.IPv4Interface.from_objects(address, network)


@pytest.mark.parametrize(
    ("address", "network"),
    (
        (
            types.IPv4Address("1.0.0.0"),
            types.IPv4Network("0.0.0.0/32"),
        ),
        (
            types.IPv4Address("1.2.1.1"),
            types.IPv4Network("1.1.0.0/16"),
        ),
        (
            types.IPv4Address("255.255.254.255"),
            types.IPv4Network("255.255.255.0/24"),
        ),
    ),
)
def test_from_objects_value_error(address, network):
    with pytest.raises(ValueError):
        types.IPv4Interface.from_objects(address, network)


@pytest.mark.parametrize(
    ("ipv4_iface", "expected"),
    (
        (
            types.IPv4Interface("0.0.0.0/32"),
            (
                types.IPv4Address("0.0.0.0"),
                types.IPv4Network("0.0.0.0/32"),
            ),
        ),
        (
            types.IPv4Interface("1.1.1.1/16"),
            (
                types.IPv4Address("1.1.1.1"),
                types.IPv4Network("1.1.0.0/16"),
            ),
        ),
        (
            types.IPv4Interface("255.255.255.255/24"),
            (
                types.IPv4Address("255.255.255.255"),
                types.IPv4Network("255.255.255.0/24"),
            ),
        ),
    ),
)
def test_as_tuple(ipv4_iface, expected):
    assert ipv4_iface.as_tuple() == expected


@pytest.mark.parametrize(
    ("ipv4_iface", "expected"),
    (
        (types.IPv4Interface("0.0.0.0/32"), "0.0.0.0/32"),
        (types.IPv4Interface("1.1.1.1/16"), "1.1.1.1/16"),
        (types.IPv4Interface("255.255.255.255/24"), "255.255.255.255/24"),
    ),
)
def test_str(ipv4_iface, expected):
    assert str(ipv4_iface) == expected
    assert ipv4_iface.ip == expected


@pytest.mark.parametrize(
    ("ipv4_iface", "expected"),
    (
        (types.IPv4Interface("0.0.0.0/32"), 'IPv4Interface("0.0.0.0/32")'),
        (types.IPv4Interface("1.1.1.1/16"), 'IPv4Interface("1.1.1.1/16")'),
        (
            types.IPv4Interface("255.255.255.255/24"),
            'IPv4Interface("255.255.255.255/24")',
        ),
    ),
)
def test_repr(ipv4_iface, expected):
    assert repr(ipv4_iface) == expected


@pytest.mark.parametrize(
    "ipv4_iface",
    (
        types.IPv4Interface("0.0.0.0/32"),
        types.IPv4Interface("1.1.1.1/16"),
        types.IPv4Interface("255.255.255.255/24"),
    ),
)
def test_hash(ipv4_iface):
    assert hash(ipv4_iface) == hash((ipv4_iface._addr, ipv4_iface._network))
