import pytest

from netsome import types


@pytest.mark.parametrize("test_input", (0, 2_147_483_648, 4_294_967_295))
def test_init_ok(test_input):
    assert types.ASN(test_input)


@pytest.mark.parametrize("test_input", ("asn", 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.ASN(test_input)


@pytest.mark.parametrize("test_input", (-1, 4_294_967_296))
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.ASN(test_input)


@pytest.mark.parametrize(("asn", "number"), ((pytest.lazy_fixture("min_asn"), 0),))
def test_property_number(asn, number):
    assert asn.number == number


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0", pytest.lazy_fixture("min_asn")),
        ("65535.65535", pytest.lazy_fixture("max_asn")),
    ),
)
def test_from_asdot(string, expected):
    assert types.ASN.from_asdot(string) == expected


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0.0", pytest.lazy_fixture("min_asn")),
        ("65535.65535", pytest.lazy_fixture("max_asn")),
    ),
)
def test_from_asdotplus(string, expected):
    assert types.ASN.from_asdotplus(string) == expected


@pytest.mark.parametrize(
    ("string", "expected"),
    (
        ("0", pytest.lazy_fixture("min_asn")),
        ("4294967295", pytest.lazy_fixture("max_asn")),
    ),
)
def test_from_asplain(string, expected):
    assert types.ASN.from_asplain(string) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    (
        (0, pytest.lazy_fixture("min_asn")),
        (4_294_967_295, pytest.lazy_fixture("max_asn")),
        ("0", pytest.lazy_fixture("min_asn")),
        ("65535.65535", pytest.lazy_fixture("max_asn")),
        ("0.0", pytest.lazy_fixture("min_asn")),
        ("65535.65535", pytest.lazy_fixture("max_asn")),
        ("0", pytest.lazy_fixture("min_asn")),
        ("4294967295", pytest.lazy_fixture("max_asn")),
    ),
)
def test_parse_ok(value, expected):
    assert types.ASN.parse(value) == expected


@pytest.mark.parametrize(
    "value",
    (-1, 4_294_967_296, "foobar"),
)
def test_parse_value_error(value):
    with pytest.raises(ValueError):
        assert types.ASN.parse(value)


@pytest.mark.parametrize(
    ("asn", "expected"),
    (
        (pytest.lazy_fixture("min_asn"), "0"),
        (pytest.lazy_fixture("max_asn"), "65535.65535"),
    ),
)
def test_to_asdot(asn, expected):
    assert asn.to_asdot() == expected


@pytest.mark.parametrize(
    ("asn", "expected"),
    (
        (pytest.lazy_fixture("min_asn"), "0.0"),
        (pytest.lazy_fixture("max_asn"), "65535.65535"),
    ),
)
def test_to_asdotplus(asn, expected):
    assert asn.to_asdotplus() == expected


@pytest.mark.parametrize(
    ("asn", "expected"),
    (
        (pytest.lazy_fixture("min_asn"), "0"),
        (pytest.lazy_fixture("max_asn"), "4294967295"),
    ),
)
def test_to_asplain(asn, expected):
    assert asn.to_asplain() == expected


@pytest.mark.parametrize(
    ("asn", "expected"),
    (
        (pytest.lazy_fixture("min_asn"), 0),
        (pytest.lazy_fixture("max_asn"), 4_294_967_295),
    ),
)
def test_int(asn, expected):
    assert int(asn) == expected


@pytest.mark.parametrize(
    ("asn", "expected"),
    (
        (pytest.lazy_fixture("min_asn"), "0"),
        (pytest.lazy_fixture("max_asn"), "4294967295"),
    ),
)
def test_str(asn, expected):
    assert str(asn) == expected


@pytest.mark.parametrize(
    "asn",
    (
        pytest.lazy_fixture("min_asn"),
        pytest.lazy_fixture("max_asn"),
    ),
)
def test_eq(asn):
    assert asn == types.ASN(int(asn))


@pytest.mark.parametrize(
    "asn",
    (pytest.lazy_fixture("min_asn"),),
)
def test_lt(asn):
    assert asn < types.ASN(int(asn) + 1)


@pytest.mark.parametrize(
    "asn",
    (pytest.lazy_fixture("min_asn"),),
)
def test_le(asn):
    assert asn <= types.ASN(int(asn))
    assert asn <= types.ASN(int(asn) + 1)


@pytest.mark.parametrize(
    "asn",
    (pytest.lazy_fixture("max_asn"),),
)
def test_gt(asn):
    assert asn > types.ASN(int(asn) - 1)


@pytest.mark.parametrize(
    "asn",
    (pytest.lazy_fixture("max_asn"),),
)
def test_ge(asn):
    assert asn >= types.ASN(int(asn))
    assert asn >= types.ASN(int(asn) - 1)


@pytest.mark.parametrize(
    "asn",
    (
        pytest.lazy_fixture("min_asn"),
        pytest.lazy_fixture("max_asn"),
    ),
)
def test_hash(asn):
    assert hash(asn) == hash(asn._number)


@pytest.mark.parametrize(
    ("asn", "expected"),
    (
        (pytest.lazy_fixture("min_asn"), "ASN(0)"),
        (pytest.lazy_fixture("max_asn"), "ASN(4294967295)"),
    ),
)
def test_repr(asn, expected):
    assert repr(asn) == expected
