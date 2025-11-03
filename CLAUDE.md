# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Netsome is a Python library for working with common networking types and conversions. It provides type-safe implementations for:
- IPv4/IPv6 addresses, networks, and interfaces
- MAC addresses (MAC-48/EUI-48)
- BGP AS numbers (asplain, asdot, asdotplus formats) and communities
- VLAN IDs
- Network interface name parsing and standardization

## Development Commands

### Setup
```bash
poetry install
```

### Linting
```bash
poetry poe lint
```
This runs:
- `basedpyright` for type checking
- `ruff check` for code quality (no auto-fix)
- `toml-sort` to verify pyproject.toml is sorted

### Formatting
```bash
poetry poe pretty
```
This runs:
- `ruff check --fix` to auto-fix issues
- `ruff format` to format code
- `toml-sort --in-place` to sort pyproject.toml

### Testing
```bash
# Run all tests with coverage
poetry poe tests

# Run specific test file
poetry run pytest tests/types/test_ipv4.py -vvv

# Run specific test function
poetry run pytest tests/types/test_ipv4.py::test_ipv4_address_creation -vvv
```

## Code Architecture

### Package Structure
```
netsome/
├── types/          # Main public API - network type classes
├── validators/     # Input validation functions
├── _converters/    # Internal conversion utilities (private API)
└── constants.py    # Shared constants and enums
```

### Design Patterns

**Type Classes**: All network types follow a consistent pattern:
- Store internal state as integers for efficient operations
- Provide multiple factory methods (`from_int`, `from_cidr`, etc.)
- Use `functools.cached_property` for expensive computed properties
- Implement full comparison operators (`__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`)
- Support hashing for use in sets/dicts

**Validation**: All input validation is handled by dedicated validator modules before conversion. Validators raise `TypeError` for type mismatches and `ValueError` for invalid values.

**Converters**: Internal conversion functions in `_converters/` handle transformations between representations (string ↔ int, compression, formatting). These are private implementation details.

**Constants**: Shared constants are defined in `constants.py` using enums:
- `IPV4`, `IPV6`: Address ranges, prefix lengths, octet/group counts
- `VLAN`, `BGP`, `MAC`: Type-specific constants
- `IFACE_TYPES`, `IFACE_PATTERNS`: Interface name matching
- `DELIMITERS`: String separators with a `join_as_str()` helper

### Key Type Relationships

**IPv4/IPv6 Hierarchy**:
- `Address`: Single IP address (stored as int)
- `Network`: Network prefix with length (netaddress + prefixlen)
- `Interface`: Combines an Address with its Network

**Address Containment**:
- Networks can contain addresses via `contains_address()`
- Networks can contain other networks via `contains_subnet()`
- Use subnet/supernet generators for network manipulation

## Code Style

- Python 3.10+ required
- Type hints enforced via `basedpyright` with strict mode
- Line length: 88 characters
- Import style: one import per line (forced by ruff isort config)
- Docstrings: Class-level docstrings with Args/Raises/Examples sections

## Testing

Tests are in `tests/` with parallel structure to `netsome/`:
```
tests/
├── types/          # Tests for public type classes
├── validators/     # Tests for validation functions
└── converters/     # Tests for conversion functions
```

Test fixtures are defined in `conftest.py` files using `pytest-lazy-fixture`.

## Current Work (from TODO.md)

The IPv6 implementation is complete. Remaining major items:
- Adding comparison operators to IPv4Interface
- Implementing MAC-64 (EUI-64) address support
- Creating IP address/network pools (similar to netaddr.IPSet)
- Renaming VID to VlanID for clarity
