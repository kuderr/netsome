import sortedcontainers
import contextlib
from netsome.types import ipv4
from netsome.validators import ipv4 as valids


# TODO: ip pools
class IpPool:
    def __init__(self, subnet: ipv4.IPv4Network) -> None:
        self._subnet = subnet
        self._reserved_addrs = sortedcontainers.SortedSet()

    def allocate_address(
        self, address: ipv4.IPv4Address | None = None
    ) -> ipv4.IPv4Address:
        # WIP
        if address and address in self._reserved_addrs:
            raise ValueError("blabla")

        if address:
            self._reserved_addrs.add(address)
            return address

        if not self._reserved_addrs:
            ...

        for index, addr in enumerate(self._reserved_addrs):
            if addr != self._reserved_addrs[index - 1] + 1:
                addr_int = self._reserved_addrs[index - 1] + 1
                addr = ipv4.IPv4Address.from_int(addr_int)
                self._reserved_addrs.add(addr)
                return addr

    def allocate_prefixlen(self, prefixlen: int) -> ipv4.IPv4Network:
        # WIP
        print(self._reserved_addrs)
        if not self._reserved_addrs:
            net = ipv4.IPv4Network.from_int(int(self._subnet.netaddress), prefixlen)
            self._reserved_addrs.update(net.hosts())
            return net

        for index, addr in enumerate(self._reserved_addrs):
            # found gap
            if addr != (addr_int := int(self._reserved_addrs[index - 1]) + 1):
                print(addr, addr_int)
                with contextlib.suppress(Exception):
                    net = ipv4.IPv4Network.from_int(addr_int, prefixlen)
                    # check all addrs not in reserved
                    self._reserved_addrs.update(net.hosts())
                    return net

    def allocate_subnet(self, subnet: ipv4.IPv4Network) -> ipv4.IPv4Network:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._subnet})"
