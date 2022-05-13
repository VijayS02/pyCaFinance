import datetime

from Account import Account
from Transaction import Transaction


class SimpleTransaction(Transaction):
    _date: datetime.datetime
    _desc: str
    _account: Account
    _value: float
    _category: str

    def __init__(self, value: float, desc: str, date: datetime.datetime, account: Account):
        super().__init__(value, desc, date, account)
        self._category = "test"

    def get_date(self) -> datetime.datetime:
        return self._date

    def get_desc(self) -> str:
        return self._desc

    def get_account(self) -> Account:
        return self._account

    def get_accounting_value(self) -> float:
        return self._value

    def get_category(self) -> str:
        if self._category == "":
            raise AttributeError("Category not defined, please call set_category before get_category")
        return self._category

    def set_category(self, cat: str):
        self._category = cat
