import typing as t

from netsome import constants as c
from netsome.validators import vlans as valids


class VID:
    """
    Represents a VLAN ID.

    The VID class handles VLAN IDs with proper range validation and provides
    methods to check special VLAN properties.

    Args:
        vid (int): VLAN ID (0-4095)

    Attributes:
        MIN (int): Minimum valid VLAN ID (0)
        MAX (int): Maximum valid VLAN ID (4095)
        DEFAULT (int): Default VLAN ID (1)
        RESERVED (set): Set of reserved VLAN IDs (0, 1, 4095)

    Raises:
        TypeError: If input is not an integer
        ValueError: If VLAN ID is outside valid range

    Examples:
        >>> vid = VID(100)
        >>> vid.is_reserved()
        False
        >>> vid.is_default()
        False
        >>> int(vid)
        100
    """

    MIN = c.VLAN.VID_MIN
    MAX = c.VLAN.VID_MAX
    DEFAULT = c.VLAN.VID_DEFAULT

    RESERVED = {MIN, DEFAULT, MAX}

    def __init__(self, vid: int) -> None:
        valids.validate_vid(vid)
        self._vid = vid

    @property
    def vid(self) -> int:
        return self._vid

    def __eq__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._vid == other._vid)

    def __lt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._vid < other._vid)

    def __le__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._vid <= other._vid)

    def __gt__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._vid > other._vid)

    def __ge__(self, other: t.Any) -> bool:
        return isinstance(other, self.__class__) and (self._vid >= other._vid)

    def __hash__(self) -> int:
        return hash(self._vid)

    def __int__(self) -> int:
        return self._vid

    def __str__(self) -> str:
        return str(self._vid)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._vid})"

    def is_reserved(self) -> bool:
        return self._vid in self.RESERVED

    def is_default(self) -> bool:
        return self._vid == self.DEFAULT
