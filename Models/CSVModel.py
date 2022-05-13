import os
from typing import List, Dict

from Model import Model
from Transaction import Transaction

PRIORITY = ["rent", "ignored", "income"]
NON_CAL = ["rent", "ignored", "income", "branch_txn", "school"]


class CSVModel(Model):
    _data_dir: str
    _model: Dict
    _priority: Dict
    _categories: List[str]

    def __init__(self, data_dir):
        if data_dir[-1] == "/":
            self._data_dir = data_dir[:-1]
        else:
            self._data_dir = data_dir

        super().__init__()
        raw_types = os.listdir(data_dir)
        self._categories = [typ.replace(".txt", "") for typ in raw_types]

        self._model = {}
        self._priority = {}

        for file in raw_types:
            key = file.replace(".txt", "")
            with open(data_dir + "/" + file) as type_model:
                for item in type_model:
                    if key in PRIORITY:
                        self._priority[item] = key
                    item = item.replace("\n", "")
                    self._model[item] = key

    def categorize_txn(self, txn: Transaction) -> str:
        needle = txn.get_desc()
        for search_term in self._priority.keys():
            if search_term.lower() in needle.lower():
                return self._priority[search_term]

        for search_term in reversed(sorted(self._model.keys(), key=lambda x: len(x))):
            if search_term.lower() in needle.lower():
                return self._model[search_term]
        return self.create_match(txn)

    def create_match(self, issue: Transaction) -> str:
        print(f"'{issue}' of value {issue.get_accounting_value()} on {issue.get_date().strftime('%d-%m-%Y')} "
              f"does not fall under any model's matches.")
        print("Types:\n")
        index = 0
        for type in self._categories:
            print(f"{index:5} : {type:50}")
            index += 1
        print(f"{index:5} : {'Create a new type.'}")

        ind = get_int_input("Which type does this transaction fall under?\n")
        if ind == index:
            res = input("What would you like to call this new type?\n")
            self._categories.append(res)
        else:
            res = self._categories[ind]

        keyword = input("What is the keyword match for this transaction?\n")
        self._model[keyword] = res
        return res

    def get_all_categories(self) -> List[str]:
        return self._categories

    def is_spending_category(self, category: str) -> bool:
        return category not in NON_CAL

    def save(self):
        reversed_dict = {}
        for k, v in self._model.items():
            if v in reversed_dict:
                reversed_dict[v].append(k)
            else:
                reversed_dict[v] = [k]

        for category_name in reversed_dict:
            filename = category_name + ".txt"
            with open(self._data_dir + "/" + filename, "w") as typeFile:
                typeFile.write("\n".join(reversed_dict[category_name]))


def get_int_input(prompt):
    res = input(prompt)
    try:
        return int(res)
    except:
        print("Unable to get an integer value, please try again.")
        return get_int_input(prompt)
