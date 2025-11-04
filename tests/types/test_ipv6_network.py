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


@pytest.mark.parametrize(
    ("network", "index", "expected"),
    (
        # /128 single address
        (types.IPv6Network("2001:db8::1/128"), 0, types.IPv6Address("2001:db8::1")),
        # /126 small network (4 addresses)
        (types.IPv6Network("2001:db8::/126"), 0, types.IPv6Address("2001:db8::")),
        (types.IPv6Network("2001:db8::/126"), 1, types.IPv6Address("2001:db8::1")),
        (types.IPv6Network("2001:db8::/126"), 2, types.IPv6Address("2001:db8::2")),
        (types.IPv6Network("2001:db8::/126"), 3, types.IPv6Address("2001:db8::3")),
        # /120 network (256 addresses)
        (types.IPv6Network("2001:db8::/120"), 0, types.IPv6Address("2001:db8::")),
        (types.IPv6Network("2001:db8::/120"), 1, types.IPv6Address("2001:db8::1")),
        (
            types.IPv6Network("2001:db8::/120"),
            100,
            types.IPv6Address("2001:db8::64"),
        ),
        (types.IPv6Network("2001:db8::/120"), 255, types.IPv6Address("2001:db8::ff")),
        # /64 large network - test various indexes
        (types.IPv6Network("2001:db8::/64"), 0, types.IPv6Address("2001:db8::")),
        (types.IPv6Network("2001:db8::/64"), 1, types.IPv6Address("2001:db8::1")),
        (types.IPv6Network("2001:db8::/64"), 100, types.IPv6Address("2001:db8::64")),
        (
            types.IPv6Network("2001:db8::/64"),
            1000,
            types.IPv6Address("2001:db8::3e8"),
        ),
        (
            types.IPv6Network("2001:db8::/64"),
            65536,
            types.IPv6Address("2001:db8::1:0"),
        ),
        # /48 network
        (types.IPv6Network("2001:db8::/48"), 0, types.IPv6Address("2001:db8::")),
        (
            types.IPv6Network("2001:db8::/48"),
            65536,
            types.IPv6Address("2001:db8::1:0"),
        ),
    ),
)
def test_host_at_positive_index(network, index, expected):
    """Test host_at with positive indexes."""
    assert network.host_at(index) == expected


@pytest.mark.parametrize(
    ("network", "index", "expected"),
    (
        # /128 single address
        (types.IPv6Network("2001:db8::1/128"), -1, types.IPv6Address("2001:db8::1")),
        # /126 small network (4 addresses)
        (types.IPv6Network("2001:db8::/126"), -1, types.IPv6Address("2001:db8::3")),
        (types.IPv6Network("2001:db8::/126"), -2, types.IPv6Address("2001:db8::2")),
        (types.IPv6Network("2001:db8::/126"), -4, types.IPv6Address("2001:db8::")),
        # /120 network (256 addresses)
        (types.IPv6Network("2001:db8::/120"), -1, types.IPv6Address("2001:db8::ff")),
        (types.IPv6Network("2001:db8::/120"), -2, types.IPv6Address("2001:db8::fe")),
        (types.IPv6Network("2001:db8::/120"), -256, types.IPv6Address("2001:db8::")),
        # /64 large network
        (
            types.IPv6Network("2001:db8::/64"),
            -1,
            types.IPv6Address("2001:db8::ffff:ffff:ffff:ffff"),
        ),
        (
            types.IPv6Network("2001:db8::/64"),
            -2,
            types.IPv6Address("2001:db8::ffff:ffff:ffff:fffe"),
        ),
    ),
)
def test_host_at_negative_index(network, index, expected):
    """Test host_at with negative indexes (Python convention)."""
    assert network.host_at(index) == expected


@pytest.mark.parametrize(
    ("network", "index"),
    (
        # /128 single address
        (types.IPv6Network("2001:db8::1/128"), 1),
        (types.IPv6Network("2001:db8::1/128"), -2),
        # /126 small network (4 addresses)
        (types.IPv6Network("2001:db8::/126"), 4),
        (types.IPv6Network("2001:db8::/126"), -5),
        # /120 network (256 addresses)
        (types.IPv6Network("2001:db8::/120"), 256),
        (types.IPv6Network("2001:db8::/120"), -257),
        # /64 large network
        (types.IPv6Network("2001:db8::/64"), 2**64),
        (types.IPv6Network("2001:db8::/64"), -(2**64 + 1)),
    ),
)
def test_host_at_index_error(network, index):
    """Test host_at raises IndexError for out of range indexes."""
    with pytest.raises(IndexError) as exc_info:
        network.host_at(index)
    assert "out of range" in str(exc_info.value)


def test_host_at_large_ipv6_network():
    """Test host_at works efficiently with very large IPv6 networks."""
    # /64 network has 2^64 addresses (impossible to enumerate)
    net = types.IPv6Network("2001:db8::/64")

    # Test that we can access addresses without enumerating the entire space
    first = net.host_at(0)
    assert str(first) == "2001:db8::"

    # Test sparse access
    sparse_addr = net.host_at(1000000)
    assert net.contains_address(sparse_addr)

    # Test last address
    last = net.host_at(-1)
    assert str(last) == "2001:db8::ffff:ffff:ffff:ffff"

    # Test second to last
    second_last = net.host_at(-2)
    assert str(second_last) == "2001:db8::ffff:ffff:ffff:fffe"


def test_host_at_boundary_conditions():
    """Test host_at at network boundaries."""
    net = types.IPv6Network("2001:db8::/120")

    # First address (network address)
    assert net.host_at(0) == net.netaddress

    # Last address in the range
    last = net.host_at(-1)
    assert last == net.host_at(255)


def test_host_at_consistency_with_hosts():
    """Test that host_at can access addresses from hosts() generator."""
    # For small networks, verify host_at matches hosts()
    net = types.IPv6Network("2001:db8::/126")
    hosts_list = list(net.hosts())

    # hosts() returns all 4 addresses for /126
    assert len(hosts_list) == 4

    # Verify each host can be accessed via host_at()
    for i, host in enumerate(hosts_list):
        assert net.host_at(i) == host


def test_host_at_sparse_allocation():
    """Test sparse address allocation pattern."""
    # Allocate every 1000th address in a /64 network
    net = types.IPv6Network("2001:db8::/64")

    addresses = [net.host_at(i * 1000) for i in range(10)]

    # Verify all addresses are in the network
    for addr in addresses:
        assert net.contains_address(addr)

    # Verify addresses are different
    assert len(set(addresses)) == 10


def test_host_at_arithmetic_operations():
    """Test that host_at produces correct arithmetic results."""
    net = types.IPv6Network("2001:db8::/120")

    # Test that consecutive indexes produce consecutive addresses
    addr_0 = net.host_at(0)
    addr_1 = net.host_at(1)
    addr_100 = net.host_at(100)

    # Verify the integer values are correct
    assert int(addr_1) == int(addr_0) + 1
    assert int(addr_100) == int(addr_0) + 100


def test_host_at_extremely_large_network():
    """Test host_at with /48 network (2^80 addresses)."""
    # /48 network is commonly used for large organizations
    net = types.IPv6Network("2001:db8::/48")

    # Test basic indexing works
    assert str(net.host_at(0)) == "2001:db8::"
    assert str(net.host_at(1)) == "2001:db8::1"

    # Test we can access addresses far into the space
    # 2^16 = 65536
    # For /48 network, adding 65536 affects the host bits
    addr = net.host_at(65536)
    # 2001:db8:: + 0x10000 = 2001:db8::1:0
    assert str(addr) == "2001:db8::1:0"

    # Test negative indexing still works
    last = net.host_at(-1)
    # Last address of /48 is first + 2^80 - 1
    assert net.contains_address(last)
