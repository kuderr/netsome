import re

from netsome import constants as c


class PortInterface:
    def __init__(self, value: str):
        self._type, self._number = self.map_port(value)

    @staticmethod
    def map_port(value):
        for port_type, pattern in c.PORT_PATTERNS.items():
            match = re.match(pattern, value, re.IGNORECASE)
            if match:
                return port_type, match.group("value")

        raise ValueError("Port type doesn't supports")

    def __str__(self):
        return f"{self._type} {self._number}"

    def __repr__(self):
        return f"PortInterface(type={self._type}, number={self._number})"

    def __eq__(self, other):
       return (
            isinstance(other, self.__class__)
            and (self._type == other._type)
            and (self._number == other._number)
        )
