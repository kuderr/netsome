import pytest

from netsome.validators import bgp as validators


@pytest.mark.parametrize(
    "test_input",
    (65535, 0, 1, 4294967295),
)
def test_validate_asplain_ok(test_input):
    validators.validate_asplain(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("0.0.0.1", "foobar", 0.1, [], [1, 2, 3]),
)
def test_validate_asplain_type_error(test_input):
    with pytest.raises(TypeError):
        validators.validate_asplain(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-65535, -1, 4294967296),
)
def test_validate_asplain_value_error(test_input):
    with pytest.raises(ValueError):
        validators.validate_asplain(test_input)
