# TODO:

## types

### ipv4

All:

- [ ] constants for local, global etc. networks
- [ ] link constants to classes

IPv4Interface:

- [ ] `__lt__`

IPv4Network:

- [ ] `__lt__`
- [ ] contains for IPv4Address, IPv4Network

IPv6Address:

- [ ] implement

IPv6Interface:

- [ ] implement

IPv6Network:

- [ ] implement

IPAddress/IPNetwork/IPInterface? (ipv4 + ipv6)

### mac

Mac64Address:

- [ ] implement

### dns

DnsRecord:

- [ ] implement?

## validators

- [ ] build common set of validators:
  - [ ] int size
  - [ ] str is digit ?
  - ...

## utils

- [ ] ranges/pools ?

## other

- [ ] docs
- [ ] base classes in types to reuse code and DRY
- [ ] think about public interfaces
- [ ] IpPools? netaddr.IPSet analog
- [ ] rewrite `__eq__` to return NotImplemented if not same class
- [ ] rename VID to VlanID
- [ ] run easy (minimal checks) & hard (run all possible data through code ??? all asn/ipv4 for example) tests suits
- [ ] make hash/str/repr/eq tests as in ipv4 network?
