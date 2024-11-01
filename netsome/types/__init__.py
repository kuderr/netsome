"""
Network types package providing classes for handling common networking objects.

The package includes classes for:
- IPv4 addresses and networks
- MAC addresses (48-bit and 64-bit)
- BGP AS numbers and communities
- VLAN IDs
- Network interface names

All types provide proper validation, comparison operations, and string representations.
Consistent interfaces enable seamless integration into network automation workflows.
"""

from netsome.types.bgp import ASN
from netsome.types.bgp import Community
from netsome.types.interfaces import Interface
from netsome.types.ipv4 import IPv4Address
from netsome.types.ipv4 import IPv4Interface
from netsome.types.ipv4 import IPv4Network
from netsome.types.mac import MacAddress
from netsome.types.vlans import VID


__all__ = [
    "ASN",
    "Community",
    "Interface",
    "IPv4Address",
    "IPv4Interface",
    "IPv4Network",
    "MacAddress",
    "VID",
]
