import pytest

from netsome import types


@pytest.mark.parametrize(
    "test_input",
    (
        "2001:db8::1/64",
        "::1/128",
        "::/0",
        "fe80::1/64",
    ),
)
def test_init_ok(test_input):
    assert types.IPv6Interface(test_input)


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Interface(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "invalid",
        "2001:db8::1",  # Missing prefix
        "2001:db8::1/129",  # Invalid prefix length
        "invalid::1/64",  # Invalid address
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Interface(test_input)


def test_from_simple():
    iface = types.IPv6Interface.from_simple("2001:db8::1", "64")

    assert str(iface.address) == "2001:db8::1"
    assert str(iface.network) == "2001:db8::/64"
    assert str(iface) == "2001:db8::1/64"


def test_from_objects():
    addr = types.IPv6Address("2001:db8::1")
    net = types.IPv6Network("2001:db8::/64")

    iface = types.IPv6Interface.from_objects(addr, net)

    assert iface.address == addr
    assert iface.network == net
    assert str(iface) == "2001:db8::1/64"


def test_from_objects_error_wrong_types():
    with pytest.raises(TypeError):
        types.IPv6Interface.from_objects(
            "not an address", types.IPv6Network("2001:db8::/64")
        )

    with pytest.raises(TypeError):
        types.IPv6Interface.from_objects(
            types.IPv6Address("2001:db8::1"), "not a network"
        )


def test_from_objects_error_address_not_in_network():
    addr = types.IPv6Address("2001:db8::1")
    net = types.IPv6Network("2001:db9::/64")  # Different network

    with pytest.raises(ValueError):
        types.IPv6Interface.from_objects(addr, net)


def test_properties():
    iface = types.IPv6Interface("2001:db8::1/64")

    assert isinstance(iface.address, types.IPv6Address)
    assert str(iface.address) == "2001:db8::1"

    assert isinstance(iface.network, types.IPv6Network)
    assert str(iface.network) == "2001:db8::/64"

    assert iface.ip == "2001:db8::1/64"


def test_as_tuple():
    iface = types.IPv6Interface("2001:db8::1/64")
    addr, net = iface.as_tuple()

    assert isinstance(addr, types.IPv6Address)
    assert isinstance(net, types.IPv6Network)
    assert str(addr) == "2001:db8::1"
    assert str(net) == "2001:db8::/64"


def test_str_representation():
    iface = types.IPv6Interface("2001:db8::1/64")
    assert str(iface) == "2001:db8::1/64"


def test_repr():
    iface = types.IPv6Interface("2001:db8::1/64")
    assert repr(iface) == 'IPv6Interface("2001:db8::1/64")'


def test_hash():
    iface1 = types.IPv6Interface("2001:db8::1/64")
    iface2 = types.IPv6Interface("2001:0db8:0000:0000:0000:0000:0000:0001/64")
    iface3 = types.IPv6Interface("2001:db8::2/64")

    assert hash(iface1) == hash(iface2)  # Same interface, different representation
    assert hash(iface1) != hash(iface3)  # Different interfaces


def test_equality():
    iface1 = types.IPv6Interface("2001:db8::1/64")
    iface2 = types.IPv6Interface("2001:0db8:0000:0000:0000:0000:0000:0001/64")
    iface3 = types.IPv6Interface("2001:db8::2/64")
    iface4 = types.IPv6Interface("2001:db8::1/48")  # Same address, different network

    assert iface1 == iface2  # Same interface
    assert iface1 != iface3  # Different address
    assert iface1 != iface4  # Different network
    assert iface1 != "not an interface"  # Different type


def test_edge_cases():
    # Test with /128 (single address)
    iface_single = types.IPv6Interface("2001:db8::1/128")
    assert str(iface_single.network) == "2001:db8::1/128"
    assert iface_single.network.contains_address(iface_single.address)

    # Test with /0 (all addresses)
    iface_all = types.IPv6Interface("2001:db8::1/0")
    assert str(iface_all.network) == "::/0"
    assert iface_all.network.contains_address(iface_all.address)


def test_network_calculation():
    # Test that network is calculated correctly
    iface = types.IPv6Interface("2001:db8:1:2:3:4:5:6/64")

    # For /64, network should be 2001:db8:1:2::/64
    assert str(iface.network) == "2001:db8:1:2::/64"
    assert iface.network.contains_address(iface.address)
