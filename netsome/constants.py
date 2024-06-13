import enum
import re


class NUMERALSYSTEMS(enum.IntEnum):
    BIN = 2
    DEC = 10
    HEX = 16


class BYTES(enum.IntEnum):
    ZERO = 0
    ONE = 2**8
    TWO = 2 ** (8 * 2)
    THREE = 2 ** (8 * 3)
    FOUR = 2 ** (8 * 4)
    FIVE = 2 ** (8 * 5)
    SIX = 2 ** (8 * 6)
    EIGHT = 2 ** (8 * 8)


class DELIMITERS(str, enum.Enum):
    DASH = "-"
    DOT = "."
    COLON = ":"
    SLASH = "/"

    def join_as_str(self, *parts):
        return self._value_.join(map(str, parts))


class IPV4(enum.IntEnum):
    PREFIXLEN_MIN = 0
    PREFIXLEN_MAX = 32

    ADDRESS_MIN = 0
    ADDRESS_MAX = BYTES.FOUR - 1

    OCTETS_COUNT = 4

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


class MAC(enum.IntEnum):
    ADDRESS_MIN = 0
    ADDRESS_MAX = BYTES.SIX - 1

    OUI_MAX = BYTES.THREE - 1
    NIC_MAX = BYTES.THREE - 1

    NIC64_MAX = BYTES.FIVE - 1
    ADDRESS64_MAX = BYTES.EIGHT - 1


class IFACE_VAL_PATTERN(enum.Enum):
    VAL = re.compile(r"(?P<value>\d+)")
    VAL_EXTENDED = re.compile(rf"{VAL.pattern[:-1]}" + r"((\/\d+)?){1,2})")
    SUB_IFACE = re.compile(r"(?P<sub>\d+)")
    VAL_SUB_IFACE = re.compile(rf"{VAL_EXTENDED.pattern[:-1]}(\.{SUB_IFACE.pattern})?)")


# TODO(kuderr): add juniper interfaces
class IFACE_TYPES(enum.Enum):
    ETHERNET = enum.auto()
    GIGABIT_ETHERNET = enum.auto()
    FAST_ETHERNET = enum.auto()
    LOOPBACK = enum.auto()
    MANAGEMENT = enum.auto()
    PORT_CHANNEL = enum.auto()
    XE = enum.auto()
    CE = enum.auto()


IFACE_NAMES = {
    # type: (long name, short name)
    IFACE_TYPES.ETHERNET: ("Ethernet", "Eth"),
    IFACE_TYPES.GIGABIT_ETHERNET: ("GigabitEthernet", "GE"),
    IFACE_TYPES.FAST_ETHERNET: ("FastEthernet", "FE"),
    IFACE_TYPES.LOOPBACK: ("Loopback", "lo"),
    IFACE_TYPES.MANAGEMENT: ("Management", "Mgmt"),
    IFACE_TYPES.PORT_CHANNEL: ("PortChannel", "Po"),
    IFACE_TYPES.XE: ("xe", "xe"),
    IFACE_TYPES.CE: ("ce", "ce"),
}

IFACE_PATTERNS = {
    IFACE_TYPES.ETHERNET: re.compile(
        rf"^[Ee]th(ernet)?{IFACE_VAL_PATTERN.VAL_SUB_IFACE.value.pattern}$"
    ),
    IFACE_TYPES.GIGABIT_ETHERNET: re.compile(
        r"^(GigabitEthernet|GigEthernet|GigEth|GigE|Gig|GE|Ge|ge|Gi|gi)"
        rf"{IFACE_VAL_PATTERN.VAL_SUB_IFACE.value.pattern}$"
    ),
    IFACE_TYPES.FAST_ETHERNET: re.compile(
        r"^(FastEthernet|FastEth|FastE|Fast|Fas|FE|Fa|fa)"
        rf"{IFACE_VAL_PATTERN.VAL_SUB_IFACE.value.pattern}$"
    ),
    IFACE_TYPES.LOOPBACK: re.compile(
        rf"^([Ll]o(opback)?){IFACE_VAL_PATTERN.VAL.value.pattern}$"
    ),
    IFACE_TYPES.MANAGEMENT: re.compile(
        rf"^([Mm]gmt|Management){IFACE_VAL_PATTERN.VAL.value.pattern}$"
    ),
    IFACE_TYPES.PORT_CHANNEL: re.compile(
        rf"^([Pp]o(rt-?channel)?){IFACE_VAL_PATTERN.VAL.value.pattern}$"
    ),
    IFACE_TYPES.XE: re.compile(rf"^xe{IFACE_VAL_PATTERN.VAL.value.pattern}$"),
    IFACE_TYPES.CE: re.compile(rf"^ce{IFACE_VAL_PATTERN.VAL.value.pattern}$"),
}
