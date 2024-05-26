import pytest

from netsome import constants as c
from netsome import types


@pytest.fixture
def default_vid():
    return types.VID(c.VLAN.VID_DEFAULT)


@pytest.fixture
def mid_vid():
    return types.VID(c.VLAN.VID_MAX // 2)
