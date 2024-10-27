
## Core Types

### IPv4Address

Represents an IPv4 address.

```python
addr = IPv4Address("192.168.1.1")
```

#### Properties

- `address` - Returns string representation of the address
- `cidr` - Returns CIDR notation (x.x.x.x/32)

#### Methods

- `from_int(number: int) -> IPv4Address` - Create from 32-bit integer
- `from_cidr(string: str) -> IPv4Address` - Create from CIDR notation

### IPv4Network

Represents an IPv4 network.

```python
net = IPv4Network("192.168.1.0/24")
```

#### Properties

- `address` - Network address string
- `prefixlen` - Network prefix length
- `netmask` - Network mask as IPv4Address
- `broadcast` - Broadcast address as IPv4Address
- `hostmask` - Host mask as IPv4Address

#### Methods

- `hosts()` - Generator yielding valid host addresses
- `subnets()` - Generator yielding subnet networks
- `supernet()` - Returns parent network
- `contains_address(addr: IPv4Address)` - Checks if network contains address
- `contains_subnet(net: IPv4Network)` - Checks if network contains subnet

### MacAddress

Represents a MAC-48/EUI-48 address.

```python
mac = MacAddress("00:11:22:33:44:55")
```

#### Properties

- `address` - Returns hex string without delimiters
- `oui` - Returns OUI portion
- `nic` - Returns NIC portion

#### Methods

- `is_multicast()` - Check if multicast address
- `is_unicast()` - Check if unicast address
- `is_local()` - Check if locally administered
- `is_global()` - Check if globally unique
- `to_str(delimiter: str, group_len: int)` - Format with custom delimiter

### ASN

Represents a BGP Autonomous System Number.

```python
asn = ASN(65000)
```

#### Properties

- `number` - Returns ASN as integer

#### Methods

- `from_asdot(string: str)` - Create from asdot notation
- `from_asdotplus(string: str)` - Create from asdotplus notation
- `from_asplain(string: str)` - Create from asplain notation
- `to_asdot()` - Convert to asdot string
- `to_asdotplus()` - Convert to asdotplus string
- `to_asplain()` - Convert to asplain string

### VID

Represents a VLAN ID.

```python
vid = VID(100)
```

#### Properties

- `vid` - Returns VLAN ID as integer
- `MIN` - Minimum valid VLAN ID (0)
- `MAX` - Maximum valid VLAN ID (4095)
- `DEFAULT` - Default VLAN ID (1)
- `RESERVED` - Set of reserved VLAN IDs

#### Methods

- `is_reserved()` - Check if reserved VLAN ID
- `is_default()` - Check if default VLAN ID

### Interface

Represents a network interface name.

```python
iface = Interface("GigabitEthernet0/1")
```

#### Properties

- `type` - Interface type constant
- `value` - Interface number/ID
- `sub` - Sub-interface number if present
- `canonical_name` - Full standardized name
- `abbreviated_name` - Short standardized name
