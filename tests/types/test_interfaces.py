import pytest

from netsome import constants as c
from netsome.types.interfaces import Interface


@pytest.fixture
def basic_interface():
    return Interface("GigabitEthernet0/1")


def test_interface_properties(basic_interface):
    """Test basic interface properties."""
    assert basic_interface.type == c.IFACE_TYPES.GIGABIT_ETHERNET
    assert basic_interface.value == "0/1"
    assert basic_interface.sub is None
    assert basic_interface.canonical_name == "GigabitEthernet0/1"
    assert basic_interface.abbreviated_name == "GE0/1"


def test_interface_string_representations(basic_interface):
    assert str(basic_interface) == "GigabitEthernet0/1"
    assert repr(basic_interface) == 'Interface("GigabitEthernet0/1")'


def test_interface_equality(basic_interface):
    same_interface = Interface("GigabitEthernet0/1")
    different_interface = Interface("FastEthernet0/1")

    assert basic_interface == same_interface
    assert basic_interface != different_interface
    assert hash(basic_interface) == hash(same_interface)
    assert hash(basic_interface) != hash(different_interface)


@pytest.mark.parametrize(
    "test_case",
    (
        {
            "input": "GigabitEthernet0/1",
            "type": c.IFACE_TYPES.GIGABIT_ETHERNET,
            "value": "0/1",
            "sub": None,
            "canonical": "GigabitEthernet0/1",
            "abbreviated": "GE0/1",
        },
        {
            "input": "Gi0/1",
            "type": c.IFACE_TYPES.GIGABIT_ETHERNET,
            "value": "0/1",
            "sub": None,
            "canonical": "GigabitEthernet0/1",
            "abbreviated": "GE0/1",
        },
        {
            "input": "FastEthernet1/0",
            "type": c.IFACE_TYPES.FAST_ETHERNET,
            "value": "1/0",
            "sub": None,
            "canonical": "FastEthernet1/0",
            "abbreviated": "FE1/0",
        },
        {
            "input": "Fa0/1.100",
            "type": c.IFACE_TYPES.FAST_ETHERNET,
            "value": "0/1.100",
            "sub": "100",
            "canonical": "FastEthernet0/1.100",
            "abbreviated": "FE0/1.100",
        },
        {
            "input": "Loopback0",
            "type": c.IFACE_TYPES.LOOPBACK,
            "value": "0",
            "sub": None,
            "canonical": "Loopback0",
            "abbreviated": "lo0",
        },
        {
            "input": "Vlan100",
            "type": c.IFACE_TYPES.VLAN,
            "value": "100",
            "sub": None,
            "canonical": "Vlan100",
            "abbreviated": "Vlan100",
        },
        {
            "input": "Vlan100.1337",
            "type": c.IFACE_TYPES.VLAN,
            "value": "100.1337",
            "sub": "1337",
            "canonical": "Vlan100.1337",
            "abbreviated": "Vlan100.1337",
        },
        {
            "input": "Management0",
            "type": c.IFACE_TYPES.MANAGEMENT,
            "value": "0",
            "sub": None,
            "canonical": "Management0",
            "abbreviated": "Mgmt0",
        },
        {
            "input": "PortChannel1",
            "type": c.IFACE_TYPES.PORT_CHANNEL,
            "value": "1",
            "sub": None,
            "canonical": "PortChannel1",
            "abbreviated": "Po1",
        },
        {
            "input": "xe0",
            "type": c.IFACE_TYPES.XE,
            "value": "0",
            "sub": None,
            "canonical": "xe0",
            "abbreviated": "xe0",
        },
        {
            "input": "ce1",
            "type": c.IFACE_TYPES.CE,
            "value": "1",
            "sub": None,
            "canonical": "ce1",
            "abbreviated": "ce1",
        },
    ),
)
def test_interface_variations_extended(test_case):
    iface = Interface(test_case["input"])
    assert iface.type == test_case["type"]
    assert iface.value == test_case["value"]
    assert iface.sub == test_case["sub"]
    assert iface.canonical_name == test_case["canonical"]
    assert iface.abbreviated_name == test_case["abbreviated"]


@pytest.mark.parametrize(
    "invalid_input,expected_exception",
    (
        ("InvalidInterface0/1", ValueError),
        (123, TypeError),
        (None, TypeError),
        ("", ValueError),
        ("Gi0/1/1/1", ValueError),
        ("Fa0//1", ValueError),
        ("GigabitEthernet", ValueError),
        ("PortChannel-1", ValueError),
        ("Mgmt0/1", ValueError),
        ("Mgmt0.123", ValueError),
    ),
)
def test_invalid_interfaces(invalid_input, expected_exception):
    with pytest.raises(expected_exception):
        Interface(invalid_input)


def test_interface_hash_consistency(basic_interface):
    """Test that interface hash remains consistent."""
    initial_hash = hash(basic_interface)

    # Hash should remain the same for multiple calls
    assert hash(basic_interface) == initial_hash
    assert hash(basic_interface) == initial_hash

    # Same interface created again should have same hash
    same_interface = Interface("GigabitEthernet0/1")
    assert hash(same_interface) == initial_hash


def test_interface_comparison_with_other_types(basic_interface):
    assert basic_interface != "GigabitEthernet0/1"
    assert basic_interface != 123
    assert basic_interface is not None
