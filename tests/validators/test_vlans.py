import pytest

from netsome.validators import vlans as valids


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 4095),
)
def test_validate_vid_ok(test_input):
    valids.validate_vid(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    ("lala", 1.0, [], object),
)
def test_validate_vid_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_vid(test_input)


@pytest.mark.parametrize(
    "test_input",
    (-1, 4096, 65535, 4294967295),
)
def test_validate_vid_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_vid(test_input)
