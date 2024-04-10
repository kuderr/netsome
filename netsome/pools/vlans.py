from netsome.pools import number
from netsome.types import vlans


class VlanPool(number.IntRangePool):
    _ITEM_CLS = vlans.VID
