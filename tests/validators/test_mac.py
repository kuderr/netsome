import pytest

from netsome.validators import mac as valids


@pytest.mark.parametrize(
    ("string", "size"),
    (
        ("aabbccddeeff", 12),
        ("ffffffffffff", 12),
        ("aabbcc", 6),
    ),
)
def test_validate_hex_string_ok(string, size):
    valids.validate_hex_string(string, size) is None


@pytest.mark.parametrize(
    "string",
    (1.0, [], object, 1),
)
def test_validate_hex_string_type_error(string):
    with pytest.raises(TypeError):
        valids.validate_hex_string(string, 12)


@pytest.mark.parametrize(
    ("string", "size"),
    (
        ("aabbccddee", 12),
        ("xxxxxxxxxxxx", 12),
    ),
)
def test_validate_hex_string_value_error(string, size):
    with pytest.raises(ValueError):
        valids.validate_hex_string(string, size)


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 281474976710655),
)
def test_validate_int_ok(test_input):
    valids.validate_int(test_input) is None


@pytest.mark.parametrize(
    "test_input",
    (1.0, [], object, "lalal"),
)
def test_validate_int_type_error(test_input):
    with pytest.raises(TypeError):
        valids.validate_int(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        -1,
        281474976710656,
        -281474976710656,
    ),
)
def test_validate_int_value_error(test_input):
    with pytest.raises(ValueError):
        valids.validate_int(test_input)
