# TODO:

## types

### ipv4

All:

- [ ] constants for local, global etc. networks

IPv4Interface:

- [ ] implement

IPv4Network:

- [ ] .hosts with /31 network
- [ ] catch .subnets with /32 prefxlen?
- [ ] parse cidr 10/8, 10.2/16, 10.2.3/24, etc.

IPv6Address:

- [ ] implement

IPv6Interface:

- [ ] implement

IPv6Network:

- [ ] implement

### mac

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
