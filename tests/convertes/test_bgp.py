import pytest

from netsome._converters import bgp as convs


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
    assert convs.asdot_to_asplain(test_input) == expected


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
    assert convs.asdotplus_to_asplain(test_input) == expected


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
    assert convs.asplain_to_asdot(test_input) == expected


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
    assert convs.asplain_to_asdotplus(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        (0, "0:0"),
        (1, "0:1"),
        (65536, "1:0"),
        (65535, "0:65535"),
        (4294967295, "65535:65535"),
    ),
)
def test_asplain_to_community(test_input, expected):
    assert convs.asplain_to_community(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("0:0", 0),
        ("0:1", 1),
        ("1:0", 65536),
        ("0:65535", 65535),
        ("65535:65535", 4294967295),
    ),
)
def test_community_to_asplain(test_input, expected):
    assert convs.community_to_asplain(test_input) == expected
