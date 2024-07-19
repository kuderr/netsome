import pytest

from netsome import types


@pytest.mark.parametrize("test_input", (0, 2_147_483_648, 4_294_967_295))
def test_init_ok(test_input):
    assert types.Community(test_input)


@pytest.mark.parametrize("test_input", ("community", 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.Community(test_input)


@pytest.mark.parametrize("test_input", (-1, 4_294_967_296))
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.Community(test_input)


@pytest.mark.parametrize(
    ("community", "number"), ((pytest.lazy_fixture("min_community"), 0),)
)
def test_property_number(community, number):
    assert community.number == number


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0:0", pytest.lazy_fixture("min_community")),
        ("65535:65535", pytest.lazy_fixture("max_community")),
    ),
)
def test_from_str(string, expected):
    assert types.Community.from_str(string) == expected


@pytest.mark.parametrize(
    ("community", "expected"),
    (
        (pytest.lazy_fixture("min_community"), 0),
        (pytest.lazy_fixture("max_community"), 4_294_967_295),
    ),
)
def test_int(community, expected):
    assert int(community) == expected


@pytest.mark.parametrize(
    ("community", "expected"),
    (
        (pytest.lazy_fixture("min_community"), "0:0"),
        (pytest.lazy_fixture("max_community"), "65535:65535"),
    ),
)
def test_str(community, expected):
    assert str(community) == expected


@pytest.mark.parametrize(
    "community",
    (
        pytest.lazy_fixture("min_community"),
        pytest.lazy_fixture("max_community"),
    ),
)
def test_eq(community):
    assert community == types.Community(int(community))


@pytest.mark.parametrize(
    "community",
    (pytest.lazy_fixture("min_community"),),
)
def test_lt(community):
    assert community < types.Community(int(community) + 1)


@pytest.mark.parametrize(
    "community",
    (pytest.lazy_fixture("min_community"),),
)
def test_le(community):
    assert community <= types.Community(int(community))
    assert community <= types.Community(int(community) + 1)


@pytest.mark.parametrize(
    "community",
    (pytest.lazy_fixture("max_community"),),
)
def test_gt(community):
    assert community > types.Community(int(community) - 1)


@pytest.mark.parametrize(
    "community",
    (pytest.lazy_fixture("max_community"),),
)
def test_ge(community):
    assert community >= types.Community(int(community))
    assert community >= types.Community(int(community) - 1)


@pytest.mark.parametrize(
    "community",
    (
        pytest.lazy_fixture("min_community"),
        pytest.lazy_fixture("max_community"),
    ),
)
def test_hash(community):
    assert hash(community) == hash(community._number)


@pytest.mark.parametrize(
    ("community", "expected"),
    (
        (pytest.lazy_fixture("min_community"), "Community(0)"),
        (pytest.lazy_fixture("max_community"), "Community(4294967295)"),
    ),
)
def test_repr(community, expected):
    assert repr(community) == expected
