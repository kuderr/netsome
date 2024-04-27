from netsome import constants as c


def validate_vid(vid: int) -> None:
    if not isinstance(vid, int):
        raise TypeError("Invalid type, must be int")

    if not (c.VLAN.VID_MIN <= vid <= c.VLAN.VID_MAX):
        raise ValueError(
            "Invalid vlan number. Must be in range "
            + c.DELIMITERS.DASH.join_as_str(c.VLAN.VID_MIN, c.VLAN.VID_MAX)
        )
