import pytest

from netsome import types


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("::/0", types.IPv6Network("::/0")),
        ("2001:db8::/32", types.IPv6Network("2001:db8::/32")),
        ("ffff:ffff:ffff:ffff::/64", types.IPv6Network("ffff:ffff:ffff:ffff::/64")),
    ),
)
def test_init_ok(string, expected):
    assert types.IPv6Network(string) == expected


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Network(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "zzxxccvvbbnn",
        "aabbcc",
        "-::1",
        "ffff:ffff:ffff:ffff::1/",
        "ffff:ffff:ffff:ffff::1/129",
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Network(test_input)


@pytest.mark.parametrize(
    ("int_addr", "prefixlen", "expected"),
    (
        (
            0,
            128,
            types.IPv6Network("::/128"),
        ),
        (
            1,
            128,
            types.IPv6Network("::1/128"),
        ),
    ),
)
def test_from_int_ok(int_addr, prefixlen, expected):
    assert types.IPv6Network.from_int(int_addr, prefixlen) == expected


@pytest.mark.parametrize("test_input", (("::1", 128), (0, 1.1), ([], 64), object()))
def test_from_int_type_error(test_input):
    addr, prefix = test_input if isinstance(test_input, tuple) else (test_input, 128)
    with pytest.raises(TypeError):
        types.IPv6Network.from_int(addr, prefix)


@pytest.mark.parametrize(
    ("int_addr", "prefixlen"),
    ((-1, 64), (0, 129)),
)
def test_from_int_value_error(int_addr, prefixlen):
    with pytest.raises(ValueError):
        types.IPv6Network.from_int(int_addr, prefixlen)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("2001:db8::/32", types.IPv6Network("2001:db8::/32")),
        ("ffff:ffff:ffff:ffff::/64", types.IPv6Network("ffff:ffff:ffff:ffff::/64")),
    ),
)
def test_from_cidr_ok(string, expected):
    assert types.IPv6Network.from_cidr(string) == expected


@pytest.mark.parametrize("test_input", (1, 1.1, [], object()))
def test_from_cidr_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Network.from_cidr(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "ffff:ffff:ffff:ffff::/129",
        "::1/127",  # might fail if not a valid boundary
    ),
)
def test_from_cidr_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv6Network.from_cidr(test_input)


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("::", types.IPv6Network("::/128")),
        ("2001:db8::1", types.IPv6Network("2001:db8::1/128")),
    ),
)
def test_from_address_ok(string, expected):
    assert types.IPv6Network.from_address(string) == expected


@pytest.mark.parametrize(
    "test_input",
    (1, 1.1, [], object()),
)
def test_from_address_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv6Network.from_address(test_input)


@pytest.mark.parametrize(
    ("ipv6net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv6_net"),
            (1, 128),  # example from fixture
        ),
    ),
)
def test_as_tuple(ipv6net, expected):
    assert ipv6net.as_tuple() == expected


@pytest.mark.parametrize(
    ("ipv6net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv6_net"),
            "::1/128",
        ),
    ),
)
def test_str(ipv6net, expected):
    assert str(ipv6net) == expected


@pytest.mark.parametrize(
    ("ipv6net", "expected"),
    (
        (
            pytest.lazy_fixture("ipv6_net"),
            'IPv6Network("::1/128")',
        ),
    ),
)
def test_repr(ipv6net, expected):
    assert repr(ipv6net) == expected


@pytest.mark.parametrize(
    "ipv6net",
    (pytest.lazy_fixture("ipv6_net"),),
)
def test_hash(ipv6net):
    assert hash(ipv6net) == hash(ipv6net.as_tuple())


@pytest.mark.parametrize(
    "ipv6net",
    (pytest.lazy_fixture("ipv6_net"),),
)
def test_eq(ipv6net):
    assert ipv6net == types.IPv6Network.from_int(
        ipv6net.as_tuple()[0], ipv6net.prefixlen
    )


@pytest.mark.parametrize(
    ("ipv6net", "expected_prefixlen"),
    ((pytest.lazy_fixture("ipv6_net"), 128),),
)
def test_property_prefixlen(ipv6net, expected_prefixlen):
    assert ipv6net.prefixlen == expected_prefixlen


@pytest.mark.parametrize(
    "ipv6net",
    (pytest.lazy_fixture("ipv6_net"),),
)
def test_property_netaddress(ipv6net):
    # fixture might have netaddress "::1"
    assert ipv6net.netaddress


@pytest.mark.parametrize(
    "ipv6net",
    (pytest.lazy_fixture("ipv6_net"),),
)
def test_property_netmask(ipv6net):
    assert ipv6net.netmask


@pytest.mark.parametrize(
    ("ipv6net", "prefixlen"),
    (
        (pytest.lazy_fixture("ipv6_net"), None),
        (pytest.lazy_fixture("ipv6_net"), 120),
    ),
)
def test_subnets(ipv6net, prefixlen):
    # Just ensure no exceptions here; subnets is a generator
    list(ipv6net.subnets(prefixlen))


@pytest.mark.parametrize(
    ("ipv6net", "prefixlen"),
    (
        (pytest.lazy_fixture("ipv6_net"), None),
        (pytest.lazy_fixture("ipv6_net"), 64),
    ),
)
def test_supernet(ipv6net, prefixlen):
    ipv6net.supernet(prefixlen)


@pytest.mark.parametrize(
    "ipv6net",
    (pytest.lazy_fixture("ipv6_net"),),
)
def test_hosts(ipv6net):
    list(ipv6net.hosts())


@pytest.mark.parametrize(
    ("ipv6net", "other"),
    ((pytest.lazy_fixture("ipv6_net"), pytest.lazy_fixture("ipv6_net")),),
)
def test_contains_subnet(ipv6net, other):
    ipv6net.contains_subnet(other)


@pytest.mark.parametrize(
    ("ipv6net", "address"),
    ((pytest.lazy_fixture("ipv6_net"), pytest.lazy_fixture("ipv6_addr")),),
)
def test_contains_address(ipv6net, address):
    ipv6net.contains_address(address)
