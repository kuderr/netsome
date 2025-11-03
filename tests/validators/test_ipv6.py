import pytest

from netsome import constants as c
from netsome.validators import ipv6 as valids


class TestValidateCidr:
    @pytest.mark.parametrize(
        "test_input",
        (
            "2001:db8::1/128",
            "::/0",
            "fe80::/10",
            "::ffff:192.0.2.1/128",
        ),
    )
    def test_ok(self, test_input):
        valids.validate_cidr(test_input)

    @pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_cidr(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            "invalid",
            "2001:db8::1",  # Missing prefix
            "2001:db8::1/129",  # Invalid prefix
            "invalid::1/64",  # Invalid address
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_cidr(test_input)


class TestValidateAddressStr:
    @pytest.mark.parametrize(
        "test_input",
        (
            "::",
            "::1",
            "2001:db8::1",
            "2001:0db8:0000:0000:0000:0000:0000:0001",
            "fe80::1",
            "ff02::1",
            "::ffff:192.0.2.1",
        ),
    )
    def test_ok(self, test_input):
        valids.validate_address_str(test_input)

    @pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_address_str(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            "",
            "invalid",
            "2001:db8::1::2",  # Multiple ::
            "2001:db8:gggg::1",  # Invalid hex
            "2001:db8::12345",  # Group too long
            "2001:db8:1:2:3:4:5:6:7:8:9",  # Too many groups
            "::ffff:256.1.1.1",  # Invalid IPv4 in mapped
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_address_str(test_input)


class TestValidateAddressInt:
    @pytest.mark.parametrize(
        "test_input",
        (
            0,
            1,
            c.IPV6.ADDRESS_MAX,
            0x20010DB8000000000000000000000001,
        ),
    )
    def test_ok(self, test_input):
        valids.validate_address_int(test_input)

    @pytest.mark.parametrize("test_input", (1.1, "string", [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_address_int(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            -1,
            c.IPV6.ADDRESS_MAX + 1,
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_address_int(test_input)


class TestValidateGroupStr:
    @pytest.mark.parametrize(
        "test_input",
        (
            "0",
            "1",
            "a",
            "ff",
            "ffff",
            "FFFF",  # Uppercase should work
        ),
    )
    def test_ok(self, test_input):
        valids.validate_group_str(test_input)

    @pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_group_str(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            "",
            "gggg",  # Invalid hex
            "12345",  # Too long
            "xyz",  # Invalid hex
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_group_str(test_input)


class TestValidateGroupInt:
    @pytest.mark.parametrize(
        "test_input",
        (
            0,
            1,
            0xFFFF,
            0x1234,
        ),
    )
    def test_ok(self, test_input):
        valids.validate_group_int(test_input)

    @pytest.mark.parametrize("test_input", (1.1, "string", [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_group_int(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            -1,
            0x10000,  # Too large
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_group_int(test_input)


class TestValidatePrefixlenStr:
    @pytest.mark.parametrize(
        "test_input",
        (
            "0",
            "64",
            "128",
        ),
    )
    def test_ok(self, test_input):
        valids.validate_prefixlen_str(test_input)

    @pytest.mark.parametrize("test_input", (0, 1.1, [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_prefixlen_str(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            "abc",
            "129",  # Too large
            "-1",
            "",
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_prefixlen_str(test_input)


class TestValidatePrefixlenInt:
    @pytest.mark.parametrize(
        "test_input",
        (
            0,
            64,
            128,
        ),
    )
    def test_ok(self, test_input):
        valids.validate_prefixlen_int(test_input)

    def test_with_custom_bounds(self):
        valids.validate_prefixlen_int(64, min_len=32, max_len=96)

    @pytest.mark.parametrize("test_input", (1.1, "string", [], object()))
    def test_type_error(self, test_input):
        with pytest.raises(TypeError):
            valids.validate_prefixlen_int(test_input)

    def test_type_error_bounds(self):
        with pytest.raises(TypeError):
            valids.validate_prefixlen_int(64, min_len="32", max_len=96)

    @pytest.mark.parametrize(
        "test_input",
        (
            -1,
            129,
        ),
    )
    def test_value_error(self, test_input):
        with pytest.raises(ValueError):
            valids.validate_prefixlen_int(test_input)

    def test_value_error_custom_bounds(self):
        with pytest.raises(ValueError):
            valids.validate_prefixlen_int(64, min_len=96, max_len=128)


class TestValidateNetworkInt:
    @pytest.mark.parametrize(
        ("address", "prefixlen"),
        (
            (0, 0),  # ::/0
            (0x20010DB8000000000000000000000000, 32),  # 2001:db8::/32
            (0x20010DB8000000000000000000000000, 64),  # 2001:db8::/64
        ),
    )
    def test_ok(self, address, prefixlen):
        valids.validate_network_int(address, prefixlen)

    @pytest.mark.parametrize(
        ("address", "prefixlen"),
        (
            (
                0x20010DB8000000000000000000000001,
                32,
            ),  # Host bits set (last bit set for /32)
            (
                0x20010DB8000000000000000000000001,
                64,
            ),  # Host bits set (host portion has bit set)
        ),
    )
    def test_host_bits_set_error(self, address, prefixlen):
        with pytest.raises(ValueError, match="Host bits set"):
            valids.validate_network_int(address, prefixlen)


class TestValidateIpv4InIpv6:
    @pytest.mark.parametrize(
        "test_input",
        (
            "192.0.2.1",
            "127.0.0.1",
            "255.255.255.255",
            "0.0.0.0",
        ),
    )
    def test_ok(self, test_input):
        from netsome.validators.ipv6 import _validate_ipv4_in_ipv6

        _validate_ipv4_in_ipv6(test_input)

    @pytest.mark.parametrize(
        "test_input",
        (
            "256.1.1.1",  # Octet too large
            "1.1.1",  # Too few octets
            "1.1.1.1.1",  # Too many octets
            "1.1.1.a",  # Non-digit
            "01.1.1.1",  # Leading zero
        ),
    )
    def test_value_error(self, test_input):
        from netsome.validators.ipv6 import _validate_ipv4_in_ipv6

        with pytest.raises(ValueError):
            _validate_ipv4_in_ipv6(test_input)
