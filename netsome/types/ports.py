import functools
import re

from netsome import constants as c


class Interface:
    def __init__(self, string: str):
        self._type, self._value = self.map_port(string)
        self._full_name, self._short_name = c.IFACE_TYPES[self._type.name].value
        self._split_value()

    @staticmethod
    def map_port(string):
        for type, pattern in c.IFACE_PATTERNS.items():
            match = re.match(pattern, string)
            if match:
                return type, match.group("value")

        raise ValueError("Port type doesn't supports")

    def _split_value(self):
        vals, *sub_iface = self._value.split(c.DELIMITERS.DOT)
        self._sub_iface = int(sub_iface[0]) if sub_iface else None

        vals = vals.split(c.DELIMITERS.SLASH)
        self._chassis, self._slot, self._port = (vals + [None] * 2)[:3]

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def sub_iface(self):
        return self._sub_iface

    @property
    def chassis(self):
        return self._chassis

    @property
    def slot(self):
        return self._slot

    @property
    def port(self):
        return self._port

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
