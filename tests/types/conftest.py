import pytest

from netsome import constants as c
from netsome import types


@pytest.fixture
def default_vid():
    return types.VID(1)


@pytest.fixture
def mid_vid():
    return types.VID(c.VLAN.VID_MAX // 2)


@pytest.fixture
def some_mac():
    return types.MacAddress("aabbccddeeff")


@pytest.fixture
def multicast_mac():
    return types.MacAddress("010000ddeeff")


@pytest.fixture
def ipv4_addr():
    return types.IPv4Address("1.1.1.1")


@pytest.fixture
def ipv4_net():
    return types.IPv4Network("1.1.1.0/24")


@pytest.fixture
def min_asn():
    return types.ASN(0)


@pytest.fixture
def max_asn():
    return types.ASN(4_294_967_295)


@pytest.fixture
def min_community():
    return types.Community(0)


@pytest.fixture
def max_community():
    return types.Community(4_294_967_295)
