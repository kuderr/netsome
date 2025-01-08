import pytest

from netsome import types


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("::/128", types.IPv6Interface("::/128")),
        ("2001:db8::1/64", types.IPv6Interface("2001:db8::1/64")),
        ("ffff:ffff:ffff:ffff::/64", types.IPv6Interface("ffff:ffff:ffff:ffff::/64")),
    ),
)
def test_init_ok(string, expected):
    assert types.IPv6Interface(string) == expected


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Interface(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "gggg::/128",
        "-::1/128",
        "ffff:ffff:ffff:ffff::/129",
        "::1",
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Interface(test_input)


@pytest.mark.parametrize(
    ("address", "prefixlen", "expected"),
    (
        ("::", 128, types.IPv6Interface("::/128")),
        ("2001:db8::1", 64, types.IPv6Interface("2001:db8::1/64")),
    ),
)
def test_from_simple(address, prefixlen, expected):
    assert types.IPv6Interface.from_simple(address, prefixlen) == expected


@pytest.mark.parametrize(
    ("address", "network", "expected"),
    (
        (
            types.IPv6Address("::"),
            types.IPv6Network("::/128"),
            types.IPv6Interface("::/128"),
        ),
        (
            types.IPv6Address("2001:db8::1"),
            types.IPv6Network("2001:db8::/64"),
            types.IPv6Interface("2001:db8::1/64"),
        ),
    ),
)
def test_from_objects_ok(address, network, expected):
    assert types.IPv6Interface.from_objects(address, network) == expected


@pytest.mark.parametrize(
    ("address", "network"),
    (
        ("::", types.IPv6Network("::/128")),
        (
            types.IPv6Address("2001:db8::1"),
            "::/64",
        ),
        (
            1_000,
            types.IPv6Network("ffff:ffff:ffff:ffff::/64"),
        ),
        (
            types.IPv6Address("::"),
            64,
        ),
    ),
)
def test_from_objects_type_error(address, network):
    with pytest.raises(TypeError):
        types.IPv6Interface.from_objects(address, network)


@pytest.mark.parametrize(
    ("address", "network"),
    (
        (
            types.IPv6Address("2001:db8::2"),
            types.IPv6Network("2001:db8:1::/64"),
        ),
        (
            types.IPv6Address("::1"),
            types.IPv6Network("::/127"),
        ),
    ),
)
def test_from_objects_value_error(address, network):
    with pytest.raises(ValueError):
        types.IPv6Interface.from_objects(address, network)


@pytest.mark.parametrize(
    ("ipv6_iface", "expected"),
    (
        (
            types.IPv6Interface("::/128"),
            (types.IPv6Address("::"), types.IPv6Network("::/128")),
        ),
        (
            types.IPv6Interface("2001:db8::1/64"),
            (
                types.IPv6Address("2001:db8::1"),
                types.IPv6Network("2001:db8::/64"),
            ),
        ),
    ),
)
def test_as_tuple(ipv6_iface, expected):
    assert ipv6_iface.as_tuple() == expected


@pytest.mark.parametrize(
    ("ipv6_iface", "expected"),
    (
        (types.IPv6Interface("::/128"), "::/128"),
        (types.IPv6Interface("2001:db8::1/64"), "2001:db8::1/64"),
    ),
)
def test_str(ipv6_iface, expected):
    assert str(ipv6_iface) == expected
    assert ipv6_iface.ip == expected


@pytest.mark.parametrize(
    ("ipv6_iface", "expected"),
    (
        (types.IPv6Interface("::/128"), 'IPv6Interface("::/128")'),
        (types.IPv6Interface("2001:db8::1/64"), 'IPv6Interface("2001:db8::1/64")'),
    ),
)
def test_repr(ipv6_iface, expected):
    assert repr(ipv6_iface) == expected


@pytest.mark.parametrize(
    "ipv6_iface",
    (
        types.IPv6Interface("::/128"),
        types.IPv6Interface("2001:db8::1/64"),
    ),
)
def test_hash(ipv6_iface):
    assert hash(ipv6_iface) == hash((ipv6_iface._addr, ipv6_iface._network))
