import pytest

from netsome.converters import bgp as converters


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("0.0", 0),
        ("0.1", 1),
        ("1.0", 65536),
        ("0.65535", 65535),
        ("65535.65535", 4294967295),
    ),
)
def test_asdotplus_to_asplain(test_input, expected):
    assert converters.asdotplus_to_asplain(test_input) == expected


@pytest.mark.parametrize(
    "test_input",
    ("0", "1", "65535"),
)
def test_asdotplus_to_asplain_value_error(test_input):
    with pytest.raises(ValueError):
        assert converters.asdotplus_to_asplain(test_input)


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 65535),
)
def test_asdotplus_to_asplain_attribute_error(test_input):
    with pytest.raises(AttributeError):
        assert converters.asdotplus_to_asplain(test_input)
