import enum
import re


class BYTES(enum.IntEnum):
    ZERO = 0
    ONE = 2**8
    TWO = ONE**2
    FOUR = TWO**2


class DELIMITERS(str, enum.Enum):
    DASH = "-"
    DOT = "."
    COLON = ":"
    SLASH = "/"

    def join_as_str(self, parts):
        return self._value_.join(map(str, parts))


class IPV4(enum.IntEnum):
    PREFIXLEN_MIN = 0
    PREFIXLEN_MAX = 32

    ADDRESS_MIN = 0
    ADDRESS_MAX = BYTES.FOUR - 1

    OCTET_MIN = 0
    OCTET_MAX = BYTES.ONE - 1


class VLAN(enum.IntEnum):
    VID_MIN = 0
    VID_MAX = 2**12 - 1

    VID_DEFAULT = 1


class BGP(enum.IntEnum):
    ASN_MIN = 0
    ASN_MAX = BYTES.FOUR - 1
    ASN_ORDER_MAX = BYTES.TWO - 1


class IFACE_VAL_PATTERN(enum.Enum):
    VAL = re.compile(r"(?P<value>(\d+))")
    VAL_EXTENDED = re.compile(rf"{VAL.pattern[:-1]}(\/\d+)?(\/\d+)?(\/\d+)?)")
    SUB_IFACE = re.compile(r"(?P<sub_iface>\d+)")
    VAL_SUB_IFACE = re.compile(rf"{VAL_EXTENDED.pattern[:-1]}(\.{SUB_IFACE.pattern})?)")


IFACE_PATTERNS = {
    ("Ethernet", "Eth"): re.compile(
        rf"^[Ee]th(ernet)?{IFACE_VAL_PATTERN.VAL_SUB_IFACE.value.pattern}$"
    ),
    ("GigabitEthernet", "GE"): re.compile(
        rf"^(GigabitEthernet|GigEthernet|GigEth|GigE|Gig|GE|Ge|ge|Gi|gi){IFACE_VAL_PATTERN.VAL_SUB_IFACE.value.pattern}$"
    ),
    ("FastEthernet", "FE"): re.compile(
        rf"^(FastEthernet|FastEth|FastE|Fast|Fas|FE|Fa|fa){IFACE_VAL_PATTERN.VAL_SUB_IFACE.value.pattern}$"
    ),
    ("Loopback", "lo"): re.compile(
        rf"^(Loopback|loopback|Lo|lo){IFACE_VAL_PATTERN.VAL.value.pattern}$"
    ),
    ("Management", "Mgmt"): re.compile(
        rf"^(Mgmt|mgmt|Ma(?=nagement$)){IFACE_VAL_PATTERN.VAL.value.pattern}$"
    ),
    ("PortChannel", "Po"): re.compile(
        rf"^(Port-?channel|port-?channel|Po){IFACE_VAL_PATTERN.VAL.value.pattern}$"
    ),
    ("xe", "xe"): re.compile(rf"^xe{IFACE_VAL_PATTERN.VAL.value.pattern}$"),
    ("ce", "ce"): re.compile(rf"^ce{IFACE_VAL_PATTERN.VAL.value.pattern}$"),
}
