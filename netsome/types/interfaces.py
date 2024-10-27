import functools
import re

from netsome import constants as c


class Interface:
    """
    Represents a network interface name.

    The Interface class parses and standardizes network interface names across
    different formats and vendors. It supports common interface types like
    Ethernet, FastEthernet, GigabitEthernet, etc.

    Args:
        string (str): Interface name (e.g. "GigabitEthernet0/1" or "Gi0/1")

    Raises:
        TypeError: If input is not a string
        ValueError: If interface name format is invalid

    Examples:
        >>> iface = Interface("GigabitEthernet0/1")
        >>> iface.canonical_name
        'GigabitEthernet0/1'
        >>> iface.abbreviated_name
        'GE0/1'
        >>> iface.type
        <IFACE_TYPES.GIGABIT_ETHERNET>
    """

    IFACE_NAMES = c.IFACE_NAMES
    IFACE_PATTERNS = c.IFACE_PATTERNS

    def __init__(self, string: str):
        self._type, self._value, self._sub = self.parse_string(string)

    def parse_string(self, string):
        for tp, pattern in self.IFACE_PATTERNS.items():
            if match := re.match(pattern, string):
                groups = match.groupdict()
                return tp, groups["value"], groups.get("sub")

        raise ValueError(f'Unable to parse "{string}" of type "{type(string)}"')

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def sub(self):
        return self._sub

    @functools.cached_property
    def canonical_name(self):
        full_name, _ = self.IFACE_NAMES[self._type]
        return f"{full_name}{self._value}"

    @functools.cached_property
    def abbreviated_name(self):
        _, short_name = self.IFACE_NAMES[self._type]
        return f"{short_name}{self._value}"

    def __hash__(self) -> int:
        return hash((self._type, self._value, self._sub))

    def __str__(self) -> str:
        return self.canonical_name

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.canonical_name}")'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return (
            (self._type == other._type)
            and (self._value == other._value)
            and (self._sub == other._sub)
        )
