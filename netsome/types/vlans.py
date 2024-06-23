import typing as t

from netsome import constants as c
from netsome.validators import vlans as valids


class VID:
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
