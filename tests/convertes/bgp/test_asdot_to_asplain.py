from netsome.converters import bgp as converters
import pytest


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("0.0", 0),
        ("0", 0),
        ("0.1", 1),
        ("1", 1),
        ("1.0", 65536),
        ("0.65535", 65535),
        ("65535", 65535),
        ("65535.65535", 4294967295),
        ("4294967295", 4294967295),
    ),
)
def test_asdot_to_asplain(test_input, expected):
    assert converters.asdot_to_asplain(test_input) == expected


@pytest.mark.parametrize(
    "test_input",
    (0, 1, 65535),
)
def test_asdot_to_asplain_attribute_error(test_input):
    with pytest.raises(TypeError):
        assert converters.asdot_to_asplain(test_input)
