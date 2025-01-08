import pytest

from netsome._converters import ipv6 as convs


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        # All zero
        ("::", 0),
        # Last 16 bits set
        ("::1", 1),
        ("::ff", 255),
        # Example global unicast address
        ("2001:db8::", int("20010db8000000000000000000000000", 16)),
        # Another sample with a single block
        ("2001:db8::1", int("20010db8000000000000000000000001", 16)),
    ],
)
def test_address_to_int(test_input: str, expected: int):
    assert convs.address_to_int(test_input) == expected


@pytest.mark.parametrize(
    ("test_input", "expected"),
    [
        # All zero
        (0, "0:0:0:0:0:0:0:0"),
        # Last 16 bits set
        (1, "0:0:0:0:0:0:0:1"),
        (255, "0:0:0:0:0:0:0:ff"),
        # Example global unicast address
        (int("20010db8000000000000000000000000", 16), "2001:db8:0:0:0:0:0:0"),
        # Another sample with a single block
        (int("20010db8000000000000000000000001", 16), "2001:db8:0:0:0:0:0:1"),
    ],
)
def test_int_to_address(test_input: int, expected: str):
    assert convs.int_to_address(test_input) == expected
