
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

## Working with IPv6 Addresses and Networks

```python
from netsome.types import IPv6Address, IPv6Network, IPv6Interface

# Create IPv6 address objects
addr = IPv6Address("2001:db8::1")
link_local = IPv6Address("fe80::1")
multicast = IPv6Address("ff02::1")

# Check address properties
print(f"Address: {addr}")                    # 2001:db8::1
print(f"Expanded: {addr.expanded}")          # 2001:0db8:0000:0000:0000:0000:0000:0001
print(f"Is global: {addr.is_global}")       # True
print(f"Is link-local: {link_local.is_link_local}")  # True
print(f"Is multicast: {multicast.is_multicast}")     # True

# Create IPv6 networks
net = IPv6Network("2001:db8::/32")
subnet = IPv6Network("2001:db8:1::/64")

# Check network containment
if net.contains_address(addr):
    print(f"{addr} is in {net}")

if net.contains_subnet(subnet):
    print(f"{subnet} is contained in {net}")

# Generate subnets (be careful with large networks!)
print("First 4 /64 subnets:")
for i, sub in enumerate(net.subnets(prefixlen=64)):
    if i >= 4:  # Limit output for demonstration
        break
    print(f"Subnet: {sub}")

# Create supernet
parent = subnet.supernet(prefixlen=48)
print(f"Parent network: {parent}")

# IPv6 Interface
iface = IPv6Interface("2001:db8::1/64")
print(f"Interface address: {iface.address}")
print(f"Interface network: {iface.network}")

# IPv4-mapped IPv6 addresses
ipv4_mapped = IPv6Address("::ffff:192.0.2.1")
print(f"IPv4-mapped: {ipv4_mapped}")
print(f"Expanded: {ipv4_mapped.expanded}")
```

## IPv6 Special Address Types

```python
from netsome.types import IPv6Address

# Special IPv6 addresses
addresses = [
    ("::", "Unspecified"),
    ("::1", "Loopback"),
    ("fe80::1", "Link-local"),
    ("fc00::1", "Unique local (private)"),
    ("ff02::1", "Multicast"),
    ("2001:db8::1", "Global unicast"),
    ("::ffff:192.0.2.1", "IPv4-mapped"),
]

for addr_str, description in addresses:
    addr = IPv6Address(addr_str)
    print(f"{description:25} {str(addr):40} "
          f"multicast={addr.is_multicast} "
          f"link_local={addr.is_link_local} "
          f"private={addr.is_private} "
          f"global={addr.is_global}")
```

## IPv6 Network Operations

```python
from netsome.types import IPv6Network

# Large network operations
net = IPv6Network("2001:db8::/48")

print(f"Network: {net}")
print(f"Prefix length: {net.prefixlen}")
print(f"Network address: {net.netaddress}")

# Subnetting examples
print("\nSubnetting /48 into /52 networks:")
for i, subnet in enumerate(net.subnets(prefixlen=52)):
    if i >= 16:  # Show first 16 subnets
        break
    print(f"  {subnet}")

# Host iteration (careful with large networks!)
small_net = IPv6Network("2001:db8::/126")  # Only 4 addresses
print(f"\nAll addresses in {small_net}:")
for host in small_net.hosts():
    print(f"  {host}")
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
