from typing import List

from Transaction import Transaction


class Parser:
    def parse_all(self) -> List[Transaction]:
        return self.parse_chequing("chq.csv") + self.parse_credit("credit.csv") + self.parse_savings("savings.csv")

    def parse_chequing(self, csv_file: str) -> List[Transaction]:
        raise NotImplementedError

    def parse_savings(self, csv_file: str) -> List[Transaction]:
        raise NotImplementedError

    def parse_credit(self, csv_file: str) -> List[Transaction]:
        raise NotImplementedError
