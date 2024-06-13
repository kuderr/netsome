import pytest

from netsome import constants as c
from netsome import types


@pytest.mark.parametrize("test_input", ("aabbccddeeff", "ffffffffffff"))
def test_init_ok(test_input):
    assert types.MacAddress(test_input)


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.MacAddress(test_input)


@pytest.mark.parametrize("test_input", ("zzxxccvvbbnn", "aabbcc"))
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.MacAddress(test_input)


@pytest.mark.parametrize(
    ("mac", "address"),
    (
        (pytest.lazy_fixture("some_mac"), "aabbccddeeff"),
        (pytest.lazy_fixture("multicast_mac"), "010000ddeeff"),
    ),
)
def test_property_address(mac, address):
    assert mac.address == address


@pytest.mark.parametrize(
    ("mac", "oui"),
    (
        (pytest.lazy_fixture("some_mac"), "aabbcc"),
        (pytest.lazy_fixture("multicast_mac"), "010000"),
    ),
)
def test_property_oui(mac, oui):
    assert mac.oui == oui


@pytest.mark.parametrize(
    ("mac", "nic"),
    (
        (pytest.lazy_fixture("some_mac"), "ddeeff"),
        (pytest.lazy_fixture("multicast_mac"), "ddeeff"),
    ),
)
def test_property_nic(mac, nic):
    assert mac.nic == nic


@pytest.mark.parametrize(
    ("mac", "is_multicast"),
    (
        (pytest.lazy_fixture("some_mac"), False),
        (pytest.lazy_fixture("multicast_mac"), True),
    ),
)
def test_is_multicast_unicast(mac, is_multicast):
    assert mac.is_multicast() == is_multicast
    assert mac.is_unicast() != is_multicast


@pytest.mark.parametrize(
    ("mac", "is_local"),
    (
        (pytest.lazy_fixture("some_mac"), True),
        (pytest.lazy_fixture("multicast_mac"), False),
    ),
)
def test_is_local_global(mac, is_local):
    assert mac.is_local() == is_local
    assert mac.is_global() != is_local


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("a-a-b-b-c-c-d-d-e-e-f-f", pytest.lazy_fixture("some_mac")),
        ("aabb-cc-dd-e-e-f-f", pytest.lazy_fixture("some_mac")),
        ("aa-bb-cc-dd-ee-ff", pytest.lazy_fixture("some_mac")),
        ("aabb-ccdd-eeff", pytest.lazy_fixture("some_mac")),
        ("aabbccddeeff", pytest.lazy_fixture("some_mac")),
        ("0-1-0-0-0-0-d-d-e-e-f-f", pytest.lazy_fixture("multicast_mac")),
        ("0100-00-dd-e-e-f-f", pytest.lazy_fixture("multicast_mac")),
        ("01-00-00-dd-ee-ff", pytest.lazy_fixture("multicast_mac")),
        ("0100-00dd-eeff", pytest.lazy_fixture("multicast_mac")),
        ("010000ddeeff", pytest.lazy_fixture("multicast_mac")),
    ),
)
def test_from_dashed(string, expected):
    assert types.MacAddress.from_dashed(string) == expected


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("a:a:b:b:c:c:d:d:e:e:f:f", pytest.lazy_fixture("some_mac")),
        ("aabb:cc:dd:e:e:f:f", pytest.lazy_fixture("some_mac")),
        ("aa:bb:cc:dd:ee:ff", pytest.lazy_fixture("some_mac")),
        ("aabb:ccdd:eeff", pytest.lazy_fixture("some_mac")),
        ("aabbccddeeff", pytest.lazy_fixture("some_mac")),
        ("0:1:0:0:0:0:d:d:e:e:f:f", pytest.lazy_fixture("multicast_mac")),
        ("0100:00:dd:e:e:f:f", pytest.lazy_fixture("multicast_mac")),
        ("01:00:00:dd:ee:ff", pytest.lazy_fixture("multicast_mac")),
        ("0100:00dd:eeff", pytest.lazy_fixture("multicast_mac")),
        ("010000ddeeff", pytest.lazy_fixture("multicast_mac")),
    ),
)
def test_from_coloned(string, expected):
    assert types.MacAddress.from_coloned(string) == expected


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("a.a.b.b.c.c.d.d.e.e.f.f", pytest.lazy_fixture("some_mac")),
        ("aabb.cc.dd.e.e.f.f", pytest.lazy_fixture("some_mac")),
        ("aa.bb.cc.dd.ee.ff", pytest.lazy_fixture("some_mac")),
        ("aabb.ccdd.eeff", pytest.lazy_fixture("some_mac")),
        ("aabbccddeeff", pytest.lazy_fixture("some_mac")),
        ("0.1.0.0.0.0.d.d.e.e.f.f", pytest.lazy_fixture("multicast_mac")),
        ("0100.00.dd.e.e.f.f", pytest.lazy_fixture("multicast_mac")),
        ("01.00.00.dd.ee.ff", pytest.lazy_fixture("multicast_mac")),
        ("0100.00dd.eeff", pytest.lazy_fixture("multicast_mac")),
        ("010000ddeeff", pytest.lazy_fixture("multicast_mac")),
    ),
)
def test_from_dotted(string, expected):
    assert types.MacAddress.from_dotted(string) == expected


@pytest.mark.parametrize(
    ("number", "expected"),
    (
        (187723572702975, pytest.lazy_fixture("some_mac")),
        (1099526172415, pytest.lazy_fixture("multicast_mac")),
    ),
)
def test_from_int_ok(number, expected):
    assert types.MacAddress.from_int(number) == expected


@pytest.mark.parametrize("number", ("0", 1.1, [], object()))
def test_from_int_type_error(number):
    with pytest.raises(TypeError):
        types.MacAddress.from_int(number)


@pytest.mark.parametrize("number", (-c.MAC.ADDRESS_MAX, -1, c.MAC.ADDRESS_MAX + 1))
def test_from_int_value_error(number):
    with pytest.raises(ValueError):
        types.MacAddress.from_int(number)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("a-a-b-b-c-c-d-d-e-e-f-f", pytest.lazy_fixture("some_mac")),
        ("aabb-cc-dd-e-e-f-f", pytest.lazy_fixture("some_mac")),
        ("aa-bb-cc-dd-ee-ff", pytest.lazy_fixture("some_mac")),
        ("aabb-ccdd-eeff", pytest.lazy_fixture("some_mac")),
        ("aabbccddeeff", pytest.lazy_fixture("some_mac")),
        ("0-1-0-0-0-0-d-d-e-e-f-f", pytest.lazy_fixture("multicast_mac")),
        ("0100-00-dd-e-e-f-f", pytest.lazy_fixture("multicast_mac")),
        ("01-00-00-dd-ee-ff", pytest.lazy_fixture("multicast_mac")),
        ("0100-00dd-eeff", pytest.lazy_fixture("multicast_mac")),
        ("010000ddeeff", pytest.lazy_fixture("multicast_mac")),
        ("a:a:b:b:c:c:d:d:e:e:f:f", pytest.lazy_fixture("some_mac")),
        ("aabb:cc:dd:e:e:f:f", pytest.lazy_fixture("some_mac")),
        ("aa:bb:cc:dd:ee:ff", pytest.lazy_fixture("some_mac")),
        ("aabb:ccdd:eeff", pytest.lazy_fixture("some_mac")),
        ("aabbccddeeff", pytest.lazy_fixture("some_mac")),
        ("0:1:0:0:0:0:d:d:e:e:f:f", pytest.lazy_fixture("multicast_mac")),
        ("0100:00:dd:e:e:f:f", pytest.lazy_fixture("multicast_mac")),
        ("01:00:00:dd:ee:ff", pytest.lazy_fixture("multicast_mac")),
        ("0100:00dd:eeff", pytest.lazy_fixture("multicast_mac")),
        ("010000ddeeff", pytest.lazy_fixture("multicast_mac")),
        ("a.a.b.b.c.c.d.d.e.e.f.f", pytest.lazy_fixture("some_mac")),
        ("aabb.cc.dd.e.e.f.f", pytest.lazy_fixture("some_mac")),
        ("aa.bb.cc.dd.ee.ff", pytest.lazy_fixture("some_mac")),
        ("aabb.ccdd.eeff", pytest.lazy_fixture("some_mac")),
        ("aabbccddeeff", pytest.lazy_fixture("some_mac")),
        ("0.1.0.0.0.0.d.d.e.e.f.f", pytest.lazy_fixture("multicast_mac")),
        ("0100.00.dd.e.e.f.f", pytest.lazy_fixture("multicast_mac")),
        ("01.00.00.dd.ee.ff", pytest.lazy_fixture("multicast_mac")),
        ("0100.00dd.eeff", pytest.lazy_fixture("multicast_mac")),
        ("010000ddeeff", pytest.lazy_fixture("multicast_mac")),
        (187723572702975, pytest.lazy_fixture("some_mac")),
        (1099526172415, pytest.lazy_fixture("multicast_mac")),
    ),
)
def test_parse_ok(string, expected):
    assert types.MacAddress.parse(string) == expected


@pytest.mark.parametrize(
    "string",
    ("0", 1.1, [], object(), -c.MAC.ADDRESS_MAX, -1, c.MAC.ADDRESS_MAX + 1),
)
def test_parse_value_error(string):
    with pytest.raises(ValueError):
        types.MacAddress.parse(string)


@pytest.mark.parametrize(
    ("mac", "params", "expected"),
    (
        (pytest.lazy_fixture("some_mac"), {}, "aa-bb-cc-dd-ee-ff"),
        (pytest.lazy_fixture("multicast_mac"), {}, "01-00-00-dd-ee-ff"),
        (pytest.lazy_fixture("some_mac"), dict(delimiter="."), "aa.bb.cc.dd.ee.ff"),
        (
            pytest.lazy_fixture("multicast_mac"),
            dict(delimiter="."),
            "01.00.00.dd.ee.ff",
        ),
        (pytest.lazy_fixture("some_mac"), dict(group_len=4), "aabb-ccdd-eeff"),
        (pytest.lazy_fixture("multicast_mac"), dict(group_len=4), "0100-00dd-eeff"),
        (
            pytest.lazy_fixture("some_mac"),
            dict(group_len=6, delimiter=":"),
            "aabbcc:ddeeff",
        ),
        (
            pytest.lazy_fixture("multicast_mac"),
            dict(group_len=6, delimiter=":"),
            "010000:ddeeff",
        ),
        # no one will stop u from expressing urself
        (
            pytest.lazy_fixture("some_mac"),
            dict(group_len=5, delimiter="@"),
            "aabbc@cddee@ff",
        ),
        (
            pytest.lazy_fixture("multicast_mac"),
            dict(group_len=5, delimiter="@"),
            "01000@0ddee@ff",
        ),
    ),
)
def test_to_str(mac, params, expected):
    assert mac.to_str(**params) == expected


@pytest.mark.parametrize(
    ("mac", "expected"),
    (
        (pytest.lazy_fixture("some_mac"), 'MacAddress("aabbccddeeff")'),
        (pytest.lazy_fixture("multicast_mac"), 'MacAddress("010000ddeeff")'),
    ),
)
def test_repr(mac, expected):
    assert repr(mac) == expected


@pytest.mark.parametrize(
    "mac",
    (
        pytest.lazy_fixture("some_mac"),
        pytest.lazy_fixture("multicast_mac"),
    ),
)
def test_hash(mac):
    assert hash(mac) == hash(mac._addr)


@pytest.mark.parametrize(
    "mac",
    (
        pytest.lazy_fixture("some_mac"),
        pytest.lazy_fixture("multicast_mac"),
    ),
)
def test_eq(mac):
    assert mac == types.MacAddress.from_int(mac._addr)


@pytest.mark.parametrize(
    "mac",
    (
        pytest.lazy_fixture("some_mac"),
        pytest.lazy_fixture("multicast_mac"),
    ),
)
def test_lt(mac):
    assert mac < types.MacAddress.from_int(mac._addr + 1)


@pytest.mark.parametrize(
    "mac",
    (
        pytest.lazy_fixture("some_mac"),
        pytest.lazy_fixture("multicast_mac"),
    ),
)
def test_le(mac):
    assert mac <= types.MacAddress.from_int(mac._addr + 1)
    assert mac <= types.MacAddress.from_int(mac._addr)


@pytest.mark.parametrize(
    "mac",
    (
        pytest.lazy_fixture("some_mac"),
        pytest.lazy_fixture("multicast_mac"),
    ),
)
def test_gt(mac):
    assert types.MacAddress.from_int(mac._addr + 1) > mac


@pytest.mark.parametrize(
    "mac",
    (
        pytest.lazy_fixture("some_mac"),
        pytest.lazy_fixture("multicast_mac"),
    ),
)
def test_ge(mac):
    assert types.MacAddress.from_int(mac._addr + 1) >= mac
    assert types.MacAddress.from_int(mac._addr) >= mac
