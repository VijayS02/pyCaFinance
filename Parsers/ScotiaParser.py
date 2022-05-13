import csv
from datetime import datetime
from typing import List, Type

from Account import Account
from Bank import Bank
from Parser import Parser
from Transaction import Transaction


class ScotiaParser(Parser):
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

    def parse_chequing(self, csv_file: str) -> List[Transaction]:
        chequing_acc = self._acc_type("2nd Chq", self._bank, "chequing")
        txn_lst = []
        with open(self._parent_dir + "/" + csv_file) as csv_file_obj:
            for i in csv.reader(csv_file_obj):
                row = i
                date = datetime.strptime(row[0], '%m/%d/%Y')
                txn_lst.append(self._txn_type(float(row[1]), row[3] + " " + row[4], date, chequing_acc))
        return txn_lst

    def parse_savings(self, csv_file: str) -> List[Transaction]:
        return []

    def parse_credit(self, csv_file: str) -> List[Transaction]:
        credit_acc = self._acc_type("***4016", self._bank, "savings")
        txn_lst = []
        with open(self._parent_dir + "/" + csv_file) as csv_file_obj:
            for i in csv.reader(csv_file_obj):
                row = i
                date = datetime.strptime(row[0], '%m/%d/%Y')
                txn_lst.append(self._txn_type(float(row[2]), row[1], date, credit_acc))
        return txn_lst
