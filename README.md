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
from netsome.types import IPv4Address, IPv4Network, MacAddress, ASN, VID

# Create and manipulate IPv4 addresses
addr = IPv4Address("192.168.1.1")
net = IPv4Network("192.168.1.0/24")

# Work with MAC addresses
mac = MacAddress("00:11:22:33:44:55")
print(mac.is_unicast())  # True
print(mac.oui)  # "001122"

# Handle BGP AS numbers
asn = ASN.from_asdot("64512.1")
print(asn.to_asplain())  # "4244897793"

# Manage VLAN IDs
vid = VID(100)
print(vid.is_reserved())  # False
```

# Authors

- Dmitriy Kudryavtsev - author - [kuderr](https://github.com/kuderr)
