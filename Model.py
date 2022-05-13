from typing import List

from Transaction import Transaction


class Model:
    def categorize_txn(self, txn: Transaction) -> str:
        raise NotImplementedError

    def get_all_categories(self) -> List[str]:
        raise NotImplementedError

    def is_spending_category(self, category: str) -> bool:
        raise NotImplementedError

    def save(self):
        raise NotImplementedError
