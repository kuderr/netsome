from netsome import constants as c


def validate_vid(vid: int) -> None:
    if not isinstance(vid, int):
        raise TypeError(
            f'Provided invalid value "{vid}" of type "{type(vid)}", int expected'
        )

    if not (c.VLAN.VID_MIN <= vid <= c.VLAN.VID_MAX):
        raise ValueError(
            f'Value "{vid}" must be in range {c.VLAN.VID_MIN}-{c.VLAN.VID_MAX}'
        )
