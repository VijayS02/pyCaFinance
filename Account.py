TYPES = ["chequing", "savings", "credit"]


class Account:
    def __init__(self, name: str, bank, acc_type: str):
        if acc_type not in TYPES:
            raise ValueError
        self._name = name
        self._bank = bank
        self._type = acc_type

    def get_name(self) -> str:
        raise NotImplementedError

    def get_bank(self):
        raise NotImplementedError

    def get_type(self) -> str in TYPES:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self._name}"

    def __repr__(self) -> str:
        return f"<Account({self.__class__}) name={self.get_name()} bank={self.get_bank().get_name()} " \
               f"type={self.get_type()}>"
