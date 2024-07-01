import pytest

from netsome import constants as c
from netsome import types


class TestASN:
    @pytest.mark.parametrize("test_input", (0, 2_147_483_648, 4_294_967_295))
    def test_init_ok(self, test_input):
        assert types.ASN(test_input)

    @pytest.mark.parametrize("test_input", ("asn", 1.1, [], object()))
    def test_init_type_error(self, test_input):
        with pytest.raises(TypeError):
            types.ASN(test_input)

    @pytest.mark.parametrize("test_input", (-1, 4_294_967_296))
    def test_init_value_error(self, test_input):
        with pytest.raises(ValueError):
            types.ASN(test_input)

    @pytest.mark.parametrize(("asn", "number"), ((pytest.lazy_fixture("min_asn"), 0),))
    def test_property_bumber(self, asn, number):
        assert asn.number == number

    @pytest.mark.parametrize(
        ("string", "expected"),
        (
            ("0", pytest.lazy_fixture("min_asn")),
            ("65535.65535", pytest.lazy_fixture("max_asn")),
        ),
    )
    def test_from_asdot(self, string, expected):
        assert types.ASN.from_asdot(string) == expected

    @pytest.mark.parametrize(
        ("string", "expected"),
        (
            ("0.0", pytest.lazy_fixture("min_asn")),
            ("65535.65535", pytest.lazy_fixture("max_asn")),
        ),
    )
    def test_from_asdotplus(self, string, expected):
        assert types.ASN.from_asdotplus(string) == expected

    @pytest.mark.parametrize(
        ("string", "expected"),
        (
            (0, pytest.lazy_fixture("min_asn")),
            (4_294_967_295, pytest.lazy_fixture("max_asn")),
        ),
    )
    def test_from_asplain(self, string, expected):
        assert types.ASN.from_asplain(string) == expected

    @pytest.mark.parametrize(
        ("asn", "expected"),
        (
            (pytest.lazy_fixture("min_asn"), "0"),
            (pytest.lazy_fixture("max_asn"), "65535.65535"),
        ),
    )
    def test_to_asdot(self, asn, expected):
        assert asn.to_asdot() == expected

    @pytest.mark.parametrize(
        ("asn", "expected"),
        (
            (pytest.lazy_fixture("min_asn"), "0.0"),
            (pytest.lazy_fixture("max_asn"), "65535.65535"),
        ),
    )
    def test_to_asdotplus(self, asn, expected):
        assert asn.to_asdotplus() == expected

    @pytest.mark.parametrize(
        ("asn", "expected"),
        (
            (pytest.lazy_fixture("min_asn"), "0"),
            (pytest.lazy_fixture("max_asn"), "4294967295"),
        ),
    )
    def test_to_asplain(self, asn, expected):
        assert asn.to_asplain() == expected

    def test_int(self, asn, expected): ...
    def test_str(self, asn, expected): ...

    def test_lt(self, asn, expected): ...

    def test_le(self, asn, expected): ...

    def test_gt(self, asn, expected): ...

    def test_ge(self, asn, expected): ...

    def test_hash(self, asn, expected): ...

    def test_repr(self, asn, expected): ...


class TestCommunity: ...
