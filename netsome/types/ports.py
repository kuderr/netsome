import functools
import re

from netsome import constants as c


class Interface:
    def __init__(self, string: str):
        self._type, self._value = self.map_port(string)
        self._full_name, self._short_name = c.IFACE_TYPES[self._type.name].value

        vals, sub_iface = self.parse_iface_val(self._value)
        self._sub_iface = int(sub_iface[0]) if sub_iface else None

        # FIXME
        vals = map(int, vals)
        *lhs, self.port = vals
        if lhs:
            *lhs, self.slot = lhs
            if lhs:
                self.chassis = lhs[0]

    @staticmethod
    def map_port(string):
        for type, pattern in c.IFACE_PATTERNS.items():
            match = re.match(pattern, string)
            if match:
                return type, match.group("value")

        raise ValueError("Port type doesn't supports")

    @staticmethod
    def parse_iface_val(string):
        vals, *sub_iface = string.split(c.DELIMITERS.DOT)
        return vals.split(c.DELIMITERS.SLASH), sub_iface

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @functools.cached_property
    def canonical_name(self):
        return f"{self._full_name}{self._value}"

    @functools.cached_property
    def abbreviated_name(self):
        return f"{self._short_name}{self._value}"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.canonical_name}")'

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and (self._full_name == other._full_name)
            and (self._value == other._value)
        )
