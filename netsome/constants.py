import enum


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
