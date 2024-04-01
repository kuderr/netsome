from netsome import constants as c
from netsome.validators import vlans as validators


class VID:
    """VLAN ID"""

    _RESERVED = {c.ZERO, c.DEFAULT_VID, c.VID_MAX}

    def __init__(self, vid: int) -> None:
        validators.validate_vid(vid)
        self._vid = vid

    def is_reserved(self) -> bool:
        return self._vid in self._RESERVED

    def is_default(self) -> bool:
        return self._vid == c.DEFAULT_VID
