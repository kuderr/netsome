from netsome.pools import number
from netsome.types import bgp


class AsnPool(number.IntRangePool):
    _ITEM_CLS = bgp.ASN
