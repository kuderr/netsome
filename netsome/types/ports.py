import re

import constants as c


class PortInterface:
    def __init__(self, value: str):
        self._type, self._number = self.map_port(value)

    @staticmethod
    def map_port(value):
        for pattern in c.PORT_PATTERNS:
            match = re.match(pattern, value, re.IGNORECASE)
