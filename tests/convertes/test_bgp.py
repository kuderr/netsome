import pytest

from netsome._converters import bgp as converters


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
    ("test_input", "expected"),
    (
        (0, "0"),
        (1, "1"),
        (65536, "1.0"),
        (65535, "65535"),
        (4294967295, "65535.65535"),
    ),
)
def test_asplain_to_asdot(test_input, expected):
    assert converters.asplain_to_asdot(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        (0, "0.0"),
        (1, "0.1"),
        (65536, "1.0"),
        (65535, "0.65535"),
        (4294967295, "65535.65535"),
    ),
)
def test_asplain_to_asdotplus(test_input, expected):
    assert converters.asplain_to_asdotplus(test_input) == expected
