import pytest

from netsome._converters import ipv4 as convs


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        ("0.0.0.0", 0),
        ("0.0.0.1", 1),
        ("0.0.1.0", 256),
    ),
)
def test_address_to_int(test_input, expected):
    assert convs.address_to_int(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    (
        (0, "0.0.0.0"),
        (1, "0.0.0.1"),
        (256, "0.0.1.0"),
    ),
)
def test_int_to_address(test_input, expected):
    assert convs.int_to_address(test_input) == expected
