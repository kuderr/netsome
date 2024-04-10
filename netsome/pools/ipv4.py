import sortedcontainers

from netsome.types import ipv4


# TODO: ip pools
class IpPool:
    def __init__(self, subnet: ipv4.IPv4Network) -> None:
        self._subnet = subnet

        self._reserved_addrs = sortedcontainers.SortedSet()
        self._free_addrs = sortedcontainers.SortedSet(subnet.hosts())

        self._reserved_subnets = sortedcontainers.SortedSet()

    def allocate_address(
        self, address: ipv4.IPv4Address | None = None
    ) -> ipv4.IPv4Address:
        if address and address not in self._free_addrs:
            raise ValueError("blabla")

        if address:
            self._free_addrs.discard(address)

        address = address or self._free_addrs.pop(0)
        self._reserved_addrs.add(address)
        return address

    def allocate_prefixlen(self, prefixlen: int) -> ipv4.IPv4Network:
        pass

    def allocate_subnet(self, subnet: ipv4.IPv4Network) -> ipv4.IPv4Network:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._subnet})"
