import re

from netsome import constants as c


class Interface:
    def __init__(self, string: str):
        (
            self._full_name,
            self._short_name,
            self._value,
        ) = self.map_port(string)

    @staticmethod
    def map_port(string):
        for (full_name, short_name), pattern in c.IFACE_PATTERNS.items():
            match = re.match(pattern, string)
            if match:
                return full_name, short_name, match.group("value")

        raise ValueError("Port type doesn't supports")

    def __str__(self):
        return f"{self._full_name}{self._value}"

    def __repr__(self):
        return f'PortInterface("{str(self)}")'

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and (self._full_name == other._full_name)
            and (self._value == other._value)
        )

    @property
    def full_name(self):
        return self._full_name

    @property
    def short_name(self):
        return self._short_name

    @property
    def value(self):
        return self._value
