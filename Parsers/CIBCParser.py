import csv
from datetime import datetime
from typing import List, Type

from Account import Account
from Bank import Bank
from Parser import Parser
from Transaction import Transaction


class CIBCParser(Parser):
    _parent_dir: str
    _bank: Bank
    _txn_type: Type[Transaction]
    _acc_type: Type[Account]

    def __init__(self, folder_dir: str, bank: Bank, txn_type, acc_type):
        if folder_dir[-1] == "/":
            self._parent_dir = folder_dir[:-1]
        else:
            self._parent_dir = folder_dir
        self._bank = bank
        self._txn_type = txn_type
        self._acc_type = acc_type

    def uniform_parse(self, csv_file: str, account: Account) -> List[Transaction]:
        txns = []
        with open(csv_file) as csv_file_obj:
            for row in csv.reader(csv_file_obj):
                date = datetime.strptime(row[0], '%Y-%m-%d')
                if row[3] == "":
                    value = -float(row[2])
                else:
                    value = float(row[3])
                txns.append(self._txn_type(value, row[1], date, account))
        return txns

    def parse_chequing(self, csv_file: str) -> List[Transaction]:
        chequing_acc = self._acc_type("Main Chq", self._bank, "chequing")
        return self.uniform_parse(self._parent_dir + "/" + csv_file, chequing_acc)

    def parse_savings(self, csv_file: str) -> List[Transaction]:
        savings_acc = self._acc_type("Main Sav", self._bank, "savings")
        return self.uniform_parse(self._parent_dir + "/" + csv_file, savings_acc)

    def parse_credit(self, csv_file: str) -> List[Transaction]:
        credit_acc = self._acc_type("***5035", self._bank, "savings")
        return self.uniform_parse(self._parent_dir + "/" + csv_file, credit_acc)
