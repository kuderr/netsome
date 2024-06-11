# TODO:

## types

### ipv4

All:

- [ ] constants for local, global etc. networks

IPv4Interface:

- [ ] `__lt__`

IPv4Network:

- [ ] `__lt__`

IPv6Address:

- [ ] implement

IPv6Interface:

- [ ] implement

IPv6Network:

- [ ] implement

### mac

MacAddress:

- [ ] to_int/`__int__` ?

Mac64Address:

- [ ] implement

### dns

DnsRecord:

- [ ] implement?

### ports

InterfaceName:

- [ ] implement

## validators

- [ ] build common set of validators:
  - [ ] int size
  - [ ] str is digit ?
  - ...

## utils

- [ ] dns resolve ?
- [ ] ranges/pools ?
- [ ] mappings:
  - [ ] oui mapping ?

## other

- [ ] better error messages
- [ ] docs
- [ ] base classes in types to reuse code and DRY
- [ ] tests
- [ ] think about public interfaces
- [ ] IpPools? netaddr.IPSet analog
- [ ] rewrite `__eq__` to return NotImplemented if not same class
