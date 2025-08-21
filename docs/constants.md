
## Constants

The library provides several constant collections that define valid ranges and formats:

### IPV4 Constants

```python
from netsome.constants import IPV4

IPV4.PREFIXLEN_MIN  # 0
IPV4.PREFIXLEN_MAX  # 32
IPV4.ADDRESS_MIN    # 0
IPV4.ADDRESS_MAX    # 2^32 - 1
IPV4.OCTETS_COUNT   # 4
IPV4.OCTET_MIN     # 0
IPV4.OCTET_MAX     # 255
```

### IPV6 Constants

```python
from netsome.constants import IPV6

IPV6.PREFIXLEN_MIN   # 0
IPV6.PREFIXLEN_MAX   # 128
IPV6.ADDRESS_MIN     # 0
IPV6.ADDRESS_MAX     # 2^128 - 1
IPV6.GROUPS_COUNT    # 8 (number of 16-bit groups)
IPV6.BITS_PER_GROUP  # 16
IPV6.GROUP_MIN       # 0
IPV6.GROUP_MAX       # 0xFFFF (65535)
```

### VLAN Constants

```python
from netsome.constants import VLAN

VLAN.VID_MIN      # 0
VLAN.VID_MAX      # 4095
VLAN.VID_DEFAULT  # 1
```

### BGP Constants

```python
from netsome.constants import BGP

BGP.ASN_MIN        # 0
BGP.ASN_MAX        # 2^32 - 1
BGP.ASN_ORDER_MAX  # 2^16 - 1
```

### MAC Constants

```python
from netsome.constants import MAC

MAC.ADDRESS_MIN     # 0
MAC.ADDRESS_MAX     # 2^48 - 1
MAC.OUI_MAX        # 2^24 - 1
MAC.NIC_MAX        # 2^24 - 1
MAC.NIC64_MAX      # 2^40 - 1
MAC.ADDRESS64_MAX  # 2^64 - 1
```

### Delimiters

```python
from netsome.constants import DELIMITERS

DELIMITERS.DASH   # "-"
DELIMITERS.DOT    # "."
DELIMITERS.COLON  # ":"
DELIMITERS.SLASH  # "/"
```

## Validators

The library provides validation functions for all data types:

### IPv4 Validators

```python
from netsome.validators import ipv4

ipv4.validate_address_str("192.168.1.1")
ipv4.validate_address_int(3232235777)
ipv4.validate_prefixlen_int(24)
ipv4.validate_octet_str("192")
ipv4.validate_network_int(3232235776, 24)
ipv4.validate_cidr("192.168.1.0/24")
```

### IPv6 Validators

```python
from netsome.validators import ipv6

ipv6.validate_address_str("2001:db8::1")
ipv6.validate_address_int(42540766411282592856903984951653826561)
ipv6.validate_prefixlen_int(64)
ipv6.validate_group_str("db8")
ipv6.validate_group_int(3512)
ipv6.validate_network_int(42540766411282592856903984951653826560, 32)
ipv6.validate_cidr("2001:db8::/32")
```

### MAC Validators

```python
from netsome.validators import mac

mac.validate_hex_string("001122334455", 12)
mac.validate_int(1144201745)
```

### BGP Validators

```python
from netsome.validators import bgp

bgp.validate_asplain(65000)
bgp.validate_asdot("64512.1")
bgp.validate_asdotplus("1.10")
bgp.validate_community("65000:100")
```

### VLAN Validators

```python
from netsome.validators import vlans

vlans.validate_vid(100)
```

All validators raise appropriate exceptions (TypeError, ValueError) when validation fails.
