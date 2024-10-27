
## Working with IPv4 Addresses and Networks

```python
from netsome.types import IPv4Address, IPv4Network, IPv4Interface

# Create address and network objects
addr = IPv4Address("192.168.1.100")
net = IPv4Network("192.168.1.0/24")

# Check if address is in network
if net.contains_address(addr):
    print(f"{addr} is in {net}")

# Iterate over usable host addresses
for host in net.hosts():
    print(f"Host address: {host}")

# Get subnets
for subnet in net.subnets(prefixlen=25):
    print(f"Subnet: {subnet}")

# Create interface (address + network combination)
iface = IPv4Interface("192.168.1.1/24")
print(f"Address: {iface.address}")
print(f"Network: {iface.network}")
```

## Working with MAC Addresses

```python
from netsome.types import MacAddress

# Create from different formats
mac1 = MacAddress("001122334455")
mac2 = MacAddress.from_dashed("00-11-22-33-44-55")
mac3 = MacAddress.from_coloned("00:11:22:33:44:55")

# Check address properties
print(f"OUI: {mac1.oui}")
print(f"NIC: {mac1.nic}")
print(f"Is unicast: {mac1.is_unicast()}")
print(f"Is local: {mac1.is_local()}")

# Format with different delimiters
print(mac1.to_str(delimiter=":", group_len=2))
print(mac1.to_str(delimiter="-", group_len=4))
```

## Working with BGP AS Numbers

```python
from netsome.types import ASN, Community

# Create ASN from different formats
asn1 = ASN(65000)
asn2 = ASN.from_asdot("64512.1")
asn3 = ASN.from_asdotplus("1.10")

# Convert between formats
print(asn1.to_asplain())  # 65000
print(asn1.to_asdot())    # 65000
print(asn1.to_asdotplus())  # 0.65000

# Work with communities
comm = Community.from_str("65000:100")
print(int(comm))  # 4259840100
```

## Working with VLANs

```python
from netsome.types import VID

# Create and validate VLAN IDs
vid1 = VID(100)
vid2 = VID(1)  # Default VLAN

# Check properties
print(vid1.is_reserved())  # False
print(vid2.is_default())   # True

# Compare VLANs
if vid1 > vid2:
    print(f"VLAN {vid1} is higher than VLAN {vid2}")
```

## Working with Interfaces

```python
from netsome.types import Interface

# Parse different interface formats
iface1 = Interface("GigabitEthernet0/1")
iface2 = Interface("Gi0/1.100")
iface3 = Interface("FastEthernet1/0/1")

# Get standardized names
print(iface1.canonical_name)    # GigabitEthernet0/1
print(iface1.abbreviated_name)  # GE0/1

# Access interface properties
print(f"Type: {iface1.type}")
print(f"Number: {iface1.value}")
print(f"Sub-interface: {iface2.sub}")  # 100
```

## Common Patterns

- All types implement proper comparison operators (==, <, >, etc)
- All types provide string representation via __str__() and __repr__()
- Input validation is strict and raises appropriate exceptions
- Most types can be parsed from multiple input formats
- Objects are immutable after creation
