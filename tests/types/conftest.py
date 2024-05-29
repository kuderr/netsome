import pytest

from netsome import constants as c
from netsome import types


@pytest.fixture
def default_vid():
    return types.VID(c.VLAN.VID_DEFAULT)


@pytest.fixture
def mid_vid():
    return types.VID(c.VLAN.VID_MAX // 2)


@pytest.fixture
def some_mac():
    return types.MacAddress("aabbccddeeff")


@pytest.fixture
def multicast_mac():
    return types.MacAddress("010000ddeeff")
