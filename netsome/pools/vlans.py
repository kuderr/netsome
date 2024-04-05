import sortedcontainers

from netsome.types import vlans


class VlanPool:
    def __init__(
        self,
        start: int,
        end: int,
        reserved: list[vlans.VID] | None,
        free: list[vlans.VID] | None,
    ) -> None:
        # TODO: validations
        self._start = start
        self._end = end

        self._reserved = sortedcontainers.SortedSet(reserved or [])
        self._free = sortedcontainers.SortedSet(
            free or vlans.VID(vid) for vid in range(start, end)
        )

    def allocate(self, vid: vlans.VID | None = None) -> vlans.VID:
        if vid and vid not in self._free:
            raise ValueError("blabla")

        vid = vid or self._free.pop(0)
        self._reserved.add(vid)
        return vid

    def release(self, vid: vlans.VID) -> None:
        if vid not in self._reserved:
            raise ValueError("blabla")

        self._reserved.remove(vid)
        self._free.add(vid)
