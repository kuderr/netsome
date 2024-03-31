from netsome.validators import ipv4 as validators
from netsome.converters import ipv4 as converters


class IPv4Address:
    def __init__(self, address: str) -> None:
        validators.validate_address(address)
        self._address = converters.address_to_int(address)

    # TODO: cache?
    def __str__(self) -> str:
        return converters.int_to_address(self._address)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({str(self)})"


# TODO:
class IPv4Network:
    def __init__(self) -> None:
        pass
