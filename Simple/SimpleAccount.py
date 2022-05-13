from Account import Account, TYPES
from Bank import Bank


class SimpleAccount(Account):
    _name: str
    _bank: Bank
    _type: str

    def get_name(self) -> str:
        return self._name

    def get_bank(self) -> Bank:
        return self._bank

    def get_type(self) -> str in TYPES:
        return self._type