from netsome import constants as c


def validate_vid(vid: int) -> None:
    if not isinstance(vid, int):
        raise TypeError("Invalid type, must be int")

    if vid < c.ZERO or vid > c.VID_MAX:
        raise ValueError(f"Invalid vlan number. Must be in range {c.ZERO}-{c.VID_MAX}")
