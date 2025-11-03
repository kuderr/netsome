import pytest

from netsome import types


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0.0.0.0/0", types.IPv4Network("0.0.0.0/0")),
        ("1.1.1.1/32", types.IPv4Network("1.1.1.1/32")),
        ("255.255.255.0/24", types.IPv4Network("255.255.255.0/24")),
    ),
)
def test_init_ok(string, expected):
    assert types.IPv4Network(string) == expected


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv4Network(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "zzxxccvvbbnn",
        "aabbcc",
        "-1.1.1.1",
        "1.1.1.1",
        "255.255.255.256/24",
        "255.255.255.255/24",
        "255.255.255.255/error",
        "255.255.255.255/-32",
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv4Network(test_input)


@pytest.mark.parametrize(
    ("int_addr", "prefixlen", "expected"),
    (
        (
            256**3,
            24,
            types.IPv4Network("1.0.0.0/24"),
        ),
    ),
)
def test_from_int_ok(int_addr, prefixlen, expected):
    assert types.IPv4Network.from_int(int_addr, prefixlen) == expected


@pytest.mark.parametrize(
    ("int_addr", "prefixlen"),
    (
        (256**3, 2),
        (256**3 + 256**2 + 256**1, 16),
    ),
)
def test_from_int_value_error(int_addr, prefixlen):
    with pytest.raises(ValueError):
        types.IPv4Network.from_int(int_addr, prefixlen)


@pytest.mark.parametrize(
    ("int_addr", "prefixlen"),
    (
        (256**3, "24"),
        (256**3 + 256**2 + 256**1, "foobar"),
        ("1.1.1.0", 24),
    ),
)
def test_from_int_type_error(int_addr, prefixlen):
    with pytest.raises(TypeError):
        types.IPv4Network.from_int(int_addr, prefixlen)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("10", types.IPv4Network("10.0.0.0/8")),
        ("10.0", types.IPv4Network("10.0.0.0/16")),
        ("10.0.0", types.IPv4Network("10.0.0.0/24")),
        ("10.0.0.0", types.IPv4Network("10.0.0.0/32")),
    ),
)
def test_from_octets_ok(string, expected):
    assert types.IPv4Network.from_octets(string) == expected


@pytest.mark.parametrize(
    "string",
    (
        "10.0.0.0.0.0.0.0",
        "10.foo.1.1",
    ),
)
def test_from_octets_value_error(string):
    with pytest.raises(ValueError):
        types.IPv4Network.from_octets(string)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("10", types.IPv4Network("10.0.0.0/8")),
        ("10.0", types.IPv4Network("10.0.0.0/16")),
        ("10.0.0", types.IPv4Network("10.0.0.0/24")),
        ("10.0.0.0", types.IPv4Network("10.0.0.0/32")),
        ("10/8", types.IPv4Network("10.0.0.0/8")),
        ("10.0/16", types.IPv4Network("10.0.0.0/16")),
        ("10.0.0/24", types.IPv4Network("10.0.0.0/24")),
        ("10.0.0.0/32", types.IPv4Network("10.0.0.0/32")),
    ),
)
def test_from_cidr_ok(string, expected):
    assert types.IPv4Network.from_cidr(string) == expected


@pytest.mark.parametrize(
    "string",
    (
        "10.0.0.0.0.0.0.0",
        "10.foo.1.1",
        "10/16",
        "10.0/24",
    ),
)
def test_from_cidr_value_error(string):
    with pytest.raises(ValueError):
        types.IPv4Network.from_cidr(string)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("10.0.0.0", types.IPv4Network("10.0.0.0/32")),
        ("10.0.0.1", types.IPv4Network("10.0.0.1/32")),
        ("10.10.10.10", types.IPv4Network("10.10.10.10/32")),
    ),
)
def test_from_address_ok(string, expected):
    assert types.IPv4Network.from_address(string) == expected


@pytest.mark.parametrize(
    "string",
    (
        "10.0.0.0.0.0.0.0",
        "10.foo.1.1",
        "10/16",
        "10.0/24",
        "10.0.0.0/24",
    ),
)
def test_from_address_value_error(string):
    with pytest.raises(ValueError):
        types.IPv4Network.from_address(string)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0.0.0.0/0", types.IPv4Network("0.0.0.0/0")),
        ("1.1.1.1/32", types.IPv4Network("1.1.1.1/32")),
        ("255.255.255.0/24", types.IPv4Network("255.255.255.0/24")),
        ("10", types.IPv4Network("10.0.0.0/8")),
        ("10.0", types.IPv4Network("10.0.0.0/16")),
        ("10.0.0", types.IPv4Network("10.0.0.0/24")),
        ("10", types.IPv4Network("10.0.0.0/8")),
        ("10.0", types.IPv4Network("10.0.0.0/16")),
        ("10.0.0", types.IPv4Network("10.0.0.0/24")),
        ("10.0.0.0", types.IPv4Network("10.0.0.0/32")),
        ("10/8", types.IPv4Network("10.0.0.0/8")),
        ("10.0/16", types.IPv4Network("10.0.0.0/16")),
        ("10.0.0/24", types.IPv4Network("10.0.0.0/24")),
        ("10.0.0.0/32", types.IPv4Network("10.0.0.0/32")),
        ("10.0.0.0", types.IPv4Network("10.0.0.0/32")),
        ("10.0.0.0", types.IPv4Network("10.0.0.0/32")),
        ("10.0.0.1", types.IPv4Network("10.0.0.1/32")),
        ("10.10.10.10", types.IPv4Network("10.10.10.10/32")),
    ),
)
def test_parse_ok(string, expected):
    assert types.IPv4Network.parse(string) == expected


@pytest.mark.parametrize(
    "string",
    (
        "10.0.0.0.0.0.0.0",
        "10.foo.1.1",
        "10/16",
        "10.0/24",
        256,
    ),
)
def test_parse_value_error(string):
    with pytest.raises(ValueError):
        types.IPv4Network.parse(string)


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            (256**3 + 256**2 + 256**1, 24),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            (256**3, 16),
        ),
    ),
)
def test_as_tuple(ipv4net, expected):
    assert ipv4net.as_tuple() == expected


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            "1.1.1.0/24",
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            "1.0.0.0/16",
        ),
    ),
)
def test_str(ipv4net, expected):
    assert str(ipv4net) == expected
    assert ipv4net.address == expected


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            'IPv4Network("1.1.1.0/24")',
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            'IPv4Network("1.0.0.0/16")',
        ),
    ),
)
def test_repr(ipv4net, expected):
    assert repr(ipv4net) == expected


@pytest.mark.parametrize(
    "ipv4net",
    (
        pytest.lazy_fixture("ipv4_net"),
        types.IPv4Network("1.0.0.0/16"),
    ),
)
def test_hash(ipv4net):
    assert hash(ipv4net) == hash(ipv4net.as_tuple())


@pytest.mark.parametrize(
    ("ipv4net", "other"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            pytest.lazy_fixture("ipv4_net"),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            types.IPv4Network("1.0.0.0/16"),
        ),
    ),
)
def test_eq(ipv4net, other):
    assert ipv4net == other


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            24,
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            16,
        ),
    ),
)
def test_prefixlen(ipv4net, expected):
    assert ipv4net.prefixlen == expected


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            types.IPv4Address("1.1.1.0"),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            types.IPv4Address("1.0.0.0"),
        ),
    ),
)
def test_netaddress(ipv4net, expected):
    assert ipv4net.netaddress == expected


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            types.IPv4Address("255.255.255.0"),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            types.IPv4Address("255.255.0.0"),
        ),
    ),
)
def test_netmask(ipv4net, expected):
    assert ipv4net.netmask == expected


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            types.IPv4Address("0.0.0.255"),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            types.IPv4Address("0.0.255.255"),
        ),
    ),
)
def test_hostmask(ipv4net, expected):
    assert ipv4net.hostmask == expected


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            types.IPv4Address("1.1.1.255"),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            types.IPv4Address("1.0.255.255"),
        ),
    ),
)
def test_broadcast(ipv4net, expected):
    assert ipv4net.broadcast == expected


@pytest.mark.parametrize(
    ("ipv4net", "prefixlen", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            None,
            (types.IPv4Network("1.1.1.0/25"), types.IPv4Network("1.1.1.128/25")),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            18,
            (
                types.IPv4Network("1.0.0.0/18"),
                types.IPv4Network("1.0.64.0/18"),
                types.IPv4Network("1.0.128.0/18"),
                types.IPv4Network("1.0.192.0/18"),
            ),
        ),
    ),
)
def test_subnets_ok(ipv4net, prefixlen, expected):
    assert tuple(ipv4net.subnets(prefixlen)) == expected


@pytest.mark.parametrize(
    ("ipv4net", "prefixlen"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            "dasda",
        ),
    ),
)
def test_subnets_type_error(ipv4net, prefixlen):
    with pytest.raises(TypeError):
        tuple(ipv4net.subnets(prefixlen))


@pytest.mark.parametrize(
    ("ipv4net", "prefixlen"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            1_000,
        ),
        (
            pytest.lazy_fixture("ipv4_net"),
            -1,
        ),
    ),
)
def test_subnets_value_error(ipv4net, prefixlen):
    with pytest.raises(ValueError):
        tuple(ipv4net.subnets(prefixlen))


@pytest.mark.parametrize(
    ("ipv4net", "prefixlen", "expected"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            None,
            types.IPv4Network("1.1.0.0/23"),
        ),
        (
            types.IPv4Network("1.0.0.0/16"),
            8,
            types.IPv4Network("1.0.0.0/8"),
        ),
    ),
)
def test_supernet_ok(ipv4net, prefixlen, expected):
    assert ipv4net.supernet(prefixlen) == expected


@pytest.mark.parametrize(
    ("ipv4net", "prefixlen"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            "dasda",
        ),
    ),
)
def test_supernet_type_error(ipv4net, prefixlen):
    with pytest.raises(TypeError):
        tuple(ipv4net.supernet(prefixlen))


@pytest.mark.parametrize(
    ("ipv4net", "prefixlen"),
    (
        (
            pytest.lazy_fixture("ipv4_net"),
            1_000,
        ),
        (
            pytest.lazy_fixture("ipv4_net"),
            -1,
        ),
    ),
)
def test_supernet_value_error(ipv4net, prefixlen):
    with pytest.raises(ValueError):
        tuple(ipv4net.supernet(prefixlen))


@pytest.mark.parametrize(
    ("ipv4net", "expected"),
    (
        (
            types.IPv4Network("1.1.1.0/32"),
            (types.IPv4Address("1.1.1.0"),),
        ),
        (
            types.IPv4Network("1.1.1.0/31"),
            (
                types.IPv4Address("1.1.1.0"),
                types.IPv4Address("1.1.1.1"),
            ),
        ),
        (
            types.IPv4Network("1.1.1.0/30"),
            (
                types.IPv4Address("1.1.1.1"),
                types.IPv4Address("1.1.1.2"),
            ),
        ),
        (
            types.IPv4Network("1.1.1.0/29"),
            (
                types.IPv4Address("1.1.1.1"),
                types.IPv4Address("1.1.1.2"),
                types.IPv4Address("1.1.1.3"),
                types.IPv4Address("1.1.1.4"),
                types.IPv4Address("1.1.1.5"),
                types.IPv4Address("1.1.1.6"),
            ),
        ),
    ),
)
def test_hosts(ipv4net, expected):
    assert tuple(ipv4net.hosts()) == expected


@pytest.mark.parametrize(
    ("ipv4net", "subnet", "expected"),
    (
        (types.IPv4Network("1.1.1.0/29"), types.IPv4Network("1.1.1.0/32"), True),
        (types.IPv4Network("1.1.1.0/29"), types.IPv4Network("1.1.0.0/32"), False),
        (types.IPv4Network("1.1.1.0/29"), types.IPv4Network("1.1.1.0/28"), False),
    ),
)
def test_contains_subnet_ok(ipv4net, subnet, expected):
    assert ipv4net.contains_subnet(subnet) == expected


@pytest.mark.parametrize(
    ("ipv4net", "subnet"),
    (
        (types.IPv4Network("1.1.1.0/29"), 5),
        (types.IPv4Network("1.1.1.0/29"), "foobar"),
    ),
)
def test_contains_subnet_type_error(ipv4net, subnet):
    with pytest.raises(TypeError):
        ipv4net.contains_subnet(subnet)


@pytest.mark.parametrize(
    ("ipv4net", "subnet", "expected"),
    (
        (types.IPv4Network("1.1.1.0/29"), types.IPv4Address("1.1.1.0"), True),
        (types.IPv4Network("1.1.1.0/29"), types.IPv4Address("1.1.1.1"), True),
        (types.IPv4Network("1.1.1.0/29"), types.IPv4Address("1.1.0.0"), False),
    ),
)
def test_contains_address_ok(ipv4net, subnet, expected):
    assert ipv4net.contains_address(subnet) == expected


@pytest.mark.parametrize(
    ("ipv4net", "subnet"),
    (
        (types.IPv4Network("1.1.1.0/29"), 5),
        (types.IPv4Network("1.1.1.0/29"), "foobar"),
    ),
)
def test_contains_address_type_error(ipv4net, subnet):
    with pytest.raises(TypeError):
        ipv4net.contains_address(subnet)


def test_comparison():
    """Test comparison operators for IPv4Network."""
    # Different networks with same prefix length
    net1 = types.IPv4Network("10.0.0.0/24")
    net2 = types.IPv4Network("10.0.1.0/24")
    net3 = types.IPv4Network("10.0.0.0/24")  # Same as net1

    # Test less than
    assert net1 < net2
    assert not (net2 < net1)
    assert not (net1 < net3)

    # Test less than or equal
    assert net1 <= net2
    assert net1 <= net3
    assert not (net2 <= net1)

    # Test greater than
    assert net2 > net1
    assert not (net1 > net2)
    assert not (net1 > net3)

    # Test greater than or equal
    assert net2 >= net1
    assert net1 >= net3
    assert not (net1 >= net2)


def test_comparison_different_prefix_lengths():
    """Test comparison with different prefix lengths."""
    # Same network address, different prefix lengths
    net1 = types.IPv4Network("10.0.0.0/16")
    net2 = types.IPv4Network("10.0.0.0/24")

    # Shorter prefix (larger network) should be "less than" longer prefix
    # This is based on (netaddress_int, prefixlen) tuple comparison
    assert net1 < net2
    assert net1 <= net2
    assert net2 > net1
    assert net2 >= net1


def test_comparison_with_different_types():
    """Test comparison operators with non-network types."""
    net = types.IPv4Network("10.0.0.0/24")

    # __eq__ returns NotImplemented, which Python converts to False for !=
    assert net != "string"

    # Other comparison operators should raise TypeError
    with pytest.raises(TypeError):
        net < "string"
    with pytest.raises(TypeError):
        net <= "string"
    with pytest.raises(TypeError):
        net > "string"
    with pytest.raises(TypeError):
        net >= "string"


def test_comparison_sorting():
    """Test that networks can be sorted."""
    networks = [
        types.IPv4Network("10.0.3.0/24"),
        types.IPv4Network("10.0.1.0/24"),
        types.IPv4Network("10.0.2.0/24"),
        types.IPv4Network("10.0.0.0/16"),
        types.IPv4Network("10.0.0.0/20"),
    ]

    sorted_networks = sorted(networks)

    expected = [
        types.IPv4Network("10.0.0.0/16"),
        types.IPv4Network("10.0.0.0/20"),
        types.IPv4Network("10.0.1.0/24"),
        types.IPv4Network("10.0.2.0/24"),
        types.IPv4Network("10.0.3.0/24"),
    ]

    assert sorted_networks == expected
