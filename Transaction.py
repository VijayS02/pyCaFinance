import datetime

from Account import Account


class Transaction:
    def __init__(self, value: float, desc: str, date: datetime.datetime, account: Account):
        self._value = value
        self._desc = desc
        self._date = date
        self._account = account

    def get_date(self) -> datetime.datetime:
        raise NotImplementedError

    def get_desc(self) -> str:
        raise NotImplementedError

    def get_account(self) -> Account:
        raise NotImplementedError

    def get_accounting_value(self) -> float:
        raise NotImplementedError

    def is_credit(self) -> bool:
        return self.get_accounting_value() < 0

    def get_category(self) -> str:
        raise NotImplementedError

    def set_category(self, cat: str):
        raise NotImplementedError

    def __float__(self) -> float:
        return self.get_accounting_value()

    def __str__(self) -> str:
        return f"{self._date.strftime('%m/%d/%Y'):10} | {str(self._account):10} | ${self._value :10.2f} | {self._desc}"

    def __repr__(self) -> str:
        return f"<{self.__class__} value=${float(self)} category={self.get_category()} " \
               f"account={self.get_account().get_name()}>"
