# Netsome

[![pypi](https://img.shields.io/pypi/v/netsome.svg)](https://pypi.org/project/netsome/)
[![downloads](https://static.pepy.tech/badge/netsome)](https://www.pepy.tech/projects/netsome)
[![downloads](https://static.pepy.tech/badge/netsome/month)](https://www.pepy.tech/projects/netsome)
[![versions](https://img.shields.io/pypi/pyversions/netsome.svg)](https://github.com/kuderr/netsome)
[![license](https://img.shields.io/github/license/kuderr/netsome.svg)](https://github.com/kuderr/netsome/blob/master/LICENSE)

A Python library for working with common networking types and conversions, including IPv4 addresses/networks, MAC addresses, BGP ASNs, VLANs and network interfaces.

## Installation

```bash
pip install netsome
```

## Features

- IPv4 address and network manipulation (addresses, networks, interfaces)
- MAC address handling (MAC-48/EUI-48)
- BGP AS number conversions (asplain, asdot, asdotplus formats)
- VLAN ID validation and management
- Network interface name parsing and standardization
- Robust validation for all data types
- Type-safe implementation with proper error handling

## Basic Usage

```python
from netsome.types import (
    IPv4Address,
    IPv4Network,
    IPv4Interface,
    MacAddress,
    ASN,
    VID,
    Community,
    Interface,
)

# Create and manipulate IPv4 addresses
ipv4_addr = IPv4Address("192.168.1.1")
print(ipv4_addr.address)  # "192.168.1.1"
print(ipv4_addr.cidr)  # "192.168.1.1/32"

ipv4_net = IPv4Network("192.168.1.0/24")
print(ipv4_net.prefixlen)  # 24
print(ipv4_net.netaddress)  # "192.168.1.0"

ipv4_interface = IPv4Interface("192.168.1.1/24")
print(ipv4_interface.address)  # "192.168.1.1"
print(ipv4_interface.network)  # "192.168.1.0/24"

# Work with MAC addresses
mac = MacAddress("001122334455")
print(mac.is_unicast())  # True
print(mac.oui)  # "001122"

# Handle BGP AS numbers
asn = ASN.from_asdot("64512.1")
print(asn.to_asplain())  # "4244897793"

# Work with BGP Communities
community = Community.from_str("65000:100")
print(str(community))  # "65000:100"
print(int(community))  # 4259840100

# Manage VLAN IDs
vid = VID(100)
print(vid.is_reserved())  # False

# Parse and work with network interface names
iface = Interface("eth0")
print(iface.type)  # IFACE_TYPES.ETHERNET
print(iface.value)  # "0"
print(iface.canonical_name)  # "Ethernet0"
print(iface.abbreviated_name)  # "Eth0"
```

# Authors

- Dmitriy Kudryavtsev - author - [kuderr](https://github.com/kuderr)
