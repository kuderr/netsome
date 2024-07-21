import pytest

from netsome import types


@pytest.mark.parametrize(
    "test_input",
    (
        "0.0.0.0/0",
        "1.1.1.1/32",
        "255.255.255.0/24",
    ),
)
def test_init_ok(test_input):
    assert types.IPv4Network(test_input)


@pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
def test_init_type_error(test_input):
    with pytest.raises(TypeError):
        types.IPv4Network(test_input)


@pytest.mark.parametrize(
    "test_input",
    (
        "zzxxccvvbbnn",
        "aabbcc",
        "-1.1.1.1",
        "1.1.1.1",
        "255.255.255.256/24",
        "255.255.255.255/24",
        "255.255.255.255/error",
        "255.255.255.255/-32",
    ),
)
def test_init_value_error(test_input):
    with pytest.raises(ValueError):
        types.IPv4Network(test_input)
