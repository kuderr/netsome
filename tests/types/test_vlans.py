import pytest

from netsome import types


@pytest.mark.parametrize("test_input", (0, 1, 4095))
def test_init_ok(test_input):
    assert types.VID(test_input)


@pytest.mark.parametrize("test_input", ("0", 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.VID(test_input)


@pytest.mark.parametrize("test_input", (-1, -4095, 4096))
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.VID(test_input)


vids = pytest.mark.parametrize(
    "vid",
    (
        pytest.lazy_fixture("default_vid"),
        pytest.lazy_fixture("mid_vid"),
    ),
)


@vids
def test_property_vid(vid):
    assert vid.vid == vid._vid


@vids
def test_eq(vid):
    assert vid == types.VID(vid.vid)


@vids
def test_lt(vid):
    assert vid < types.VID(vid.vid + 1)


@vids
def test_hash(vid):
    assert hash(vid) == hash(vid.vid)


@vids
def test_repr(vid):
    assert repr(vid) == f"VID({vid.vid})"


@pytest.mark.parametrize(
    ("vid", "is_reserved"),
    (
        (pytest.lazy_fixture("default_vid"), True),
        (pytest.lazy_fixture("mid_vid"), False),
    ),
)
def test_is_reserved(vid, is_reserved):
    assert vid.is_reserved() is is_reserved


@pytest.mark.parametrize(
    ("vid", "is_default"),
    (
        (pytest.lazy_fixture("default_vid"), True),
        (pytest.lazy_fixture("mid_vid"), False),
    ),
)
def test_is_default(vid, is_default):
    assert vid.is_default() is is_default
