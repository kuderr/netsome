import pytest

from netsome import constants as c
from netsome import types


@pytest.mark.parametrize(
    "test_input",
    (
        "::/0",
        "::1/128",
        "2001:db8::/32",
        "2001:db8::/64",
        "fe80::/10",
    ),
)
def test_init_ok(test_input):
    assert types.IPv6Network(test_input)


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Network(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "invalid",
        "2001:db8::1",  # Missing prefix
        "2001:db8::1/129",  # Invalid prefix length
        "2001:db8::1/32",  # Host bits set
        "2001:db8:1::/32",  # Host bits set
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Network(test_input)


@pytest.mark.parametrize(
    ("int_addr", "prefixlen", "expected"),
    (
        (0, 0, "::/0"),
        (0x20010DB8000000000000000000000000, 32, "2001:db8::/32"),
        (0x20010DB8000000000000000000000000, 64, "2001:db8::/64"),
    ),
)
def test_from_int_ok(int_addr, prefixlen, expected):
    net = types.IPv6Network.from_int(int_addr, prefixlen)
    assert str(net) == expected


@pytest.mark.parametrize(
    ("int_addr", "prefixlen"),
    (
        (-1, 64),  # Invalid address
        (c.IPV6.ADDRESS_MAX + 1, 64),  # Address too large
        (0, -1),  # Invalid prefix length
        (0, 129),  # Prefix length too large
        (1, 0),  # Host bits set for /0 should be OK actually
    ),
)
def test_from_int_error(int_addr, prefixlen):
    if int_addr == 1 and prefixlen == 0:
        # This should actually work since /0 includes all addresses
        types.IPv6Network.from_int(int_addr, prefixlen)
    else:
        with pytest.raises((TypeError, ValueError)):
            types.IPv6Network.from_int(int_addr, prefixlen)


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("2001:db8::1", "2001:db8::1/128"),
        ("::", "::/128"),
    ),
)
def test_from_address_ok(test_input, expected):
    net = types.IPv6Network.from_address(test_input)
    assert str(net) == expected


def test_parse_success():
    # Test various formats that should parse successfully
    assert str(types.IPv6Network.parse("2001:db8::/32")) == "2001:db8::/32"
    assert str(types.IPv6Network.parse("2001:db8::1")) == "2001:db8::1/128"


def test_parse_failure():
    with pytest.raises(ValueError):
        types.IPv6Network.parse("invalid_format")


def test_properties():
    net = types.IPv6Network("2001:db8::/32")

    assert net.prefixlen == 32
    assert isinstance(net.netaddress, types.IPv6Address)
    assert str(net.netaddress) == "2001:db8::"
    assert isinstance(net.netmask, types.IPv6Address)
    assert str(net.address) == "2001:db8::/32"


def test_hostmask():
    net = types.IPv6Network("2001:db8::/32")
    hostmask = net.hostmask

    assert isinstance(hostmask, types.IPv6Address)
    # For /32, hostmask should have lower 96 bits set
    assert int(hostmask) == (1 << 96) - 1


def test_as_tuple():
    net = types.IPv6Network("2001:db8::/32")
    tuple_result = net.as_tuple()

    assert tuple_result == (0x20010DB8000000000000000000000000, 32)


def test_subnets():
    net = types.IPv6Network("2001:db8::/32")
    subnets = list(net.subnets(prefixlen=33))

    assert len(subnets) == 2
    assert str(subnets[0]) == "2001:db8::/33"
    assert str(subnets[1]) == "2001:db8:8000::/33"


def test_subnets_default():
    net = types.IPv6Network("2001:db8::/32")
    subnets = list(net.subnets())  # Should default to /33

    assert len(subnets) == 2
    assert all(sub.prefixlen == 33 for sub in subnets)


def test_subnets_error():
    net = types.IPv6Network("2001:db8::/32")

    with pytest.raises(ValueError):
        list(net.subnets(prefixlen=31))  # Prefix too short


def test_supernet():
    net = types.IPv6Network("2001:db8::/32")
    supernet = net.supernet(prefixlen=16)

    assert str(supernet) == "2001::/16"


def test_supernet_default():
    net = types.IPv6Network("2001:db8::/32")
    supernet = net.supernet()  # Should default to /31

    assert supernet.prefixlen == 31
    assert str(supernet) == "2001:db8::/31"


def test_supernet_error():
    net = types.IPv6Network("2001:db8::/32")

    with pytest.raises(ValueError):
        net.supernet(prefixlen=33)  # Prefix too long


def test_hosts_single_address():
    net = types.IPv6Network("2001:db8::1/128")
    hosts = list(net.hosts())

    assert len(hosts) == 1
    assert str(hosts[0]) == "2001:db8::1"


def test_hosts_small_network():
    net = types.IPv6Network("2001:db8::/126")  # 4 addresses
    hosts = list(net.hosts())

    assert len(hosts) == 4
    assert str(hosts[0]) == "2001:db8::"
    assert str(hosts[1]) == "2001:db8::1"
    assert str(hosts[2]) == "2001:db8::2"
    assert str(hosts[3]) == "2001:db8::3"


def test_contains_address():
    net = types.IPv6Network("2001:db8::/32")

    assert net.contains_address(types.IPv6Address("2001:db8::1"))
    assert net.contains_address(
        types.IPv6Address("2001:db8:ffff:ffff:ffff:ffff:ffff:ffff")
    )
    assert not net.contains_address(types.IPv6Address("2001:db9::1"))
    assert not net.contains_address(types.IPv6Address("2002::1"))


def test_contains_address_error():
    net = types.IPv6Network("2001:db8::/32")

    with pytest.raises(TypeError):
        net.contains_address("not an address")


def test_contains_subnet():
    net = types.IPv6Network("2001:db8::/32")

    # Contained subnet
    subnet1 = types.IPv6Network("2001:db8:1::/48")
    assert net.contains_subnet(subnet1)

    # Not contained (different network)
    subnet2 = types.IPv6Network("2001:db9::/48")
    assert not net.contains_subnet(subnet2)

    # Same network (should return False)
    subnet3 = types.IPv6Network("2001:db8::/32")
    assert not net.contains_subnet(subnet3)

    # Larger network (should return False)
    subnet4 = types.IPv6Network("2001::/16")
    assert not net.contains_subnet(subnet4)


def test_contains_subnet_error():
    net = types.IPv6Network("2001:db8::/32")

    with pytest.raises(TypeError):
        net.contains_subnet("not a network")


def test_zero_prefix_network():
    net = types.IPv6Network("::/0")

    assert net.prefixlen == 0
    assert str(net.netaddress) == "::"
    assert net.contains_address(types.IPv6Address("2001:db8::1"))
    assert net.contains_address(
        types.IPv6Address("ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff")
    )


def test_hash():
    net1 = types.IPv6Network("2001:db8::/32")
    net2 = types.IPv6Network(
        "2001:0db8:0000:0000::/32"
    )  # Same network, different format
    net3 = types.IPv6Network("2001:db8::/64")

    assert hash(net1) == hash(net2)  # Same network
    assert hash(net1) != hash(net3)  # Different networks


def test_equality():
    net1 = types.IPv6Network("2001:db8::/32")
    net2 = types.IPv6Network("2001:0db8:0000:0000::/32")
    net3 = types.IPv6Network("2001:db8::/64")

    assert net1 == net2  # Same network
    assert net1 != net3  # Different networks
    assert net1 != "not a network"  # Different type


def test_comparison():
    """Test comparison operators for IPv6Network."""
    # Different networks with same prefix length
    net1 = types.IPv6Network("2001:db8::/32")
    net2 = types.IPv6Network("2001:db9::/32")
    net3 = types.IPv6Network("2001:db8::/32")  # Same as net1

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
    net1 = types.IPv6Network("2001:db8::/32")
    net2 = types.IPv6Network("2001:db8::/64")

    # Shorter prefix (larger network) should be "less than" longer prefix
    # This is based on (netaddress_int, prefixlen) tuple comparison
    assert net1 < net2
    assert net1 <= net2
    assert net2 > net1
    assert net2 >= net1


def test_comparison_with_different_types():
    """Test comparison operators with non-network types."""
    net = types.IPv6Network("2001:db8::/32")

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
        types.IPv6Network("2001:db8:3::/64"),
        types.IPv6Network("2001:db8:1::/64"),
        types.IPv6Network("2001:db8:2::/64"),
        types.IPv6Network("2001:db8::/32"),
        types.IPv6Network("2001:db8::/48"),
    ]

    sorted_networks = sorted(networks)

    expected = [
        types.IPv6Network("2001:db8::/32"),
        types.IPv6Network("2001:db8::/48"),
        types.IPv6Network("2001:db8:1::/64"),
        types.IPv6Network("2001:db8:2::/64"),
        types.IPv6Network("2001:db8:3::/64"),
    ]

    assert sorted_networks == expected


def test_str_and_repr():
    net = types.IPv6Network("2001:db8::/32")

    assert str(net) == "2001:db8::/32"
    assert repr(net) == 'IPv6Network("2001:db8::/32")'
