import sortedcontainers

from netsome.types import bgp, vlans


class IntRangePool:
    _ITEM_CLS = int

    def __init__(self, start: int, end: int) -> None:
        # TODO: validations
        self._start = start
        self._end = end

        self._reserved = sortedcontainers.SortedSet()
        self._free = sortedcontainers.SortedSet(
            self._ITEM_CLS(num) for num in range(start, end)
        )

    @classmethod
    def with_reserved(
        cls,
        start: int,
        end: int,
        reserved: list[_ITEM_CLS],
    ) -> "IntRangePool":
        pool = cls(start, end)

        # TODO: validate reserved start, end

        reserved = sortedcontainers.SortedSet(reserved)
        pool._reserved = reserved
        pool._free -= reserved

        return pool

    def allocate(self, item: _ITEM_CLS | None = None) -> _ITEM_CLS:
        if item and item not in self._free:
            raise ValueError("blabla")

        if item:
            self._free.discard(item)

        item = item or self._free.pop(0)
        self._reserved.add(item)
        return item

    def release(self, item: _ITEM_CLS) -> None:
        if item not in self._reserved:
            raise ValueError("blabla")

        self._reserved.remove(item)
        self._free.add(item)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._start}, {self._end})"


class VlanPool(IntRangePool):
    _ITEM_CLS = vlans.VID


class AsnPool(IntRangePool):
    _ITEM_CLS = bgp.ASN


# TODO: ip pools
