from netsome import constants as c
import re
import contextlib

# TODO(kuderr):
# 1. Parse canonical formats:
# 1.1 AC-DE-48-01-02-03 (Windows)
# 1.2 AC:DE:48:01:02:03 (Unix)
# 1.3 ACDE.4801.0203 (Cisco)
# 2. Parse bitreverse (noncanonical) format?
# 2.1 35:7B:12:80:40:C0
# 3. Is methods for b0/b1 bits in first octet
# 3.1 unicast/multicast
# 3.2 oui/local


def validate_hex(string: str) -> None:
    if not re.match(r"^[0-9a-fA-F]{12}$", string):
        raise ValueError


# TODO: rename
def validate_ietf(string: str) -> None:
    if not re.match(r"^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$", string):
        raise ValueError


class MacAddress:
    # MAC-48/EUI-48

    MIN = c.MAC.ADDRESS_MIN
    MAX = c.MAC.ADDRESS_MAX

    OUI_MAX = c.MAC.OUI_MAX
    NIC_MAX = c.MAC.NIC_MAX

    def __init__(self, addr: int) -> None:
        if not (self.MIN <= addr <= self.MAX):
            raise ValueError

        self._addr = addr

    @classmethod
    def from_hex(cls, string: str) -> "MacAddress":
        # ACDE48127B80
        validate_hex(string)
        return cls(int(string, base=16))

    @classmethod
    def from_ieee(cls, string: str) -> "MacAddress":
        # AC-DE-48-12-7B-80
        return cls.from_hex(string.replace(c.DELIMITERS.DASH, ""))

    @classmethod
    def from_ieee_bit_reversed(cls, string: str) -> "MacAddress":
        # AC-DE-48-12-7B-80 bit reversed = 35:7B:12:48:DE:01
        # reverse bits order in every part
        raise NotImplementedError

    @classmethod
    def from_ietf(cls, string: str) -> "MacAddress":
        # AC:DE:48:12:7B:80
        return cls.from_hex(string.replace(c.DELIMITERS.COLON, ""))

    @classmethod
    def from_cisco(cls, string: str) -> "MacAddress":
        # ACDE.4812.7B80
        return cls.from_hex(string.replace(c.DELIMITERS.DOT, ""))

    @classmethod
    def parse(cls, string: str) -> "MacAddress":
        # TODO: can collect all this from cls attrs?
        from_fmts = tuple(
            cls.from_hex,
            cls.from_ieee,
            # cls.from_ieee_bit_reversed,
            cls.from_ietf,
            cls.from_cisco,
        )

        for fmt in from_fmts:
            with contextlib.suppress(ValueError, TypeError):
                return fmt(string)

        raise ValueError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({hex(self._addr)})"


class Mac64Address:
    # EUI-64

    MIN = c.MAC.ADDRESS_MIN
    MAX = c.MAC.ADDRESS64_MAX

    OUI_MAX = c.MAC.OUI_MAX
    NIC_MAX = c.MAC.NIC64_MAX

    def __init__(self) -> None:
        self._oui = ...
        self._nic = ...
