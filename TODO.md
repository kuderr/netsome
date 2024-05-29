# TODO:

## types

### ipv4

All:

- [ ] constants for local, global etc. networks
- [ ] tests

IPv4Interface:

- [x] implement
- [ ] `__lt__`

IPv4Network:

- [x] .hosts with /31, /32 network
- [x] catch .subnets with /32 prefxlen? **/32 networks is valid**
- [ ] parse cidr 10/8, 10.2/16, 10.2.3/24, etc.
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

- [x] better imports `from netsome import types as nst; nst.IPv4Address(...)`
- [ ] better error messages
- [ ] docs
- [ ] base classes in types to reuse code and DRY
- [ ] tests
- [ ] think about public interfaces
- [ ] IpPools? netaddr.IPSet analog
