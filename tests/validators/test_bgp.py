import pytest

from netsome.validators import bgp as valids


@pytest.mark.parametrize(
    "test_input",
    (65535, 0, 1, 4294967295),
)
def test_validate_asplain_ok(test_input):
    valids.validate_asplain(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0.1", "foobar", 0.1, [], [1, 2, 3]),
)
def test_validate_asplain_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_asplain(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-65535, -1, 4294967296),
)
def test_validate_asplain_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_asplain(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("65535.0", "0.0", "0.1", "1.0"),
)
def test_validate_asdotplus_ok(test_input):
    valids.validate_asdotplus(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (65535, -65535, 0.1, [], [1, 2, 3]),
)
def test_validate_asdotplus_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_asdotplus(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0.1", "-100", "100"),
)
def test_validate_asdotplus_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_asdotplus(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("65535.0", "0.0", "0.1", "1.0", "1", "0", "65535"),
)
def test_validate_asdot_ok(test_input):
    valids.validate_asdot(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (65535, -65535, 0.1, [], [1, 2, 3]),
)
def test_validate_asdot_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_asdot(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0.1", "-100", "65536", "4294967296"),
)
def test_validate_asdot_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_asdot(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("65535:0", "0:0", "0:1", "1:0"),
)
def test_validate_community_ok(test_input):
    valids.validate_community(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (65535, -65535, 0.1, [], [1, 2, 3]),
)
def test_validate_community_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_community(test_input)


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0.1", "-100", "65536", "4294967296", "65535:0:0", "65700:0", "0:65700"),
)
def test_validate_community_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_community(test_input)
