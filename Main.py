import math
from datetime import datetime
from typing import List, Dict, Tuple

from Account import Account
from Bank import Bank
from Model import Model
from Models.CSVModel import CSVModel
from Parsers.CIBCParser import CIBCParser
from Parsers.ScotiaParser import ScotiaParser
from Simple.SimpleAccount import SimpleAccount
from Simple.SimpleTransaction import SimpleTransaction
from Transaction import Transaction
from dateutil.relativedelta import *
import matplotlib.pyplot as plt

MONTH_END = 14


def categorize_transactions(txns: List[Transaction], m: Model):
    for txn in txns:
        txn.set_category(m.categorize_txn(txn))
    m.save()


def prev_month_end(date=datetime.today()) -> datetime:
    if date.day > MONTH_END:
        raw_date = date.strftime("%Y-%m-") + str(MONTH_END)
    else:
        new_month = date.month - 1
        raw_date = date.strftime("%Y") + f"-{new_month:02}-" + str(MONTH_END)
    return datetime.strptime(raw_date, "%Y-%m-%d")


def get_accounts(txn_list: List[Transaction]) -> List[Account]:
    accs = set()
    for txn in txn_list:
        accs.add(txn.get_account())
    return list(accs)


def generate_balances(txn_list: List[Transaction]) -> Dict[Account, float]:
    accs = {acc: 0 for acc in get_accounts(txn_list)}
    for txn in txn_list:
        accs[txn.get_account()] += float(txn)

    return accs


def get_subset_by_date(txn_list: List[Transaction], start: datetime, end: datetime):
    res = []
    for txn in txn_list:
        if start <= txn.get_date() <= end:
            res.append(txn)
    return res


def get_total_spending(txn_list: List[Transaction], m: Model) -> Tuple[float, List[Transaction]]:
    total = 0.0
    ign = []
    for txn in txn_list:
        if m.is_spending_category(txn.get_category()):
            total += float(txn)
        else:
            ign.append(txn)
    return total, ign


def get_category_breakdown(txn_list: List[Transaction]) -> Dict[str, float]:
    data = {}
    for txn in txn_list:
        if txn.get_category() in data:
            data[txn.get_category()] += float(txn)
        else:
            data[txn.get_category()] = float(txn)

    return data


def get_month_txns_by_datestr(txn_list: List[Transaction], date: str):
    real_date = datetime.strptime(date, "%Y-%m-%d")
    one_month = relativedelta(months=1)
    start_date = prev_month_end(real_date)
    end_date = start_date + one_month
    return get_subset_by_date(txn_list, start_date, end_date)


def generate_all_months(txn_list: List[Transaction], m: Model):
    sorted_lst = sorted(txn_list, key=lambda x: x.get_date())
    first = sorted_lst[0].get_date()
    last = sorted_lst[-1].get_date()

    one_month = relativedelta(months=1)
    start_date = prev_month_end(first)
    end_date = start_date + one_month

    transactions = []
    ignored = []
    spendings = []
    dates = []
    groupings = []
    while start_date < last:
        dates.append(start_date)
        store = get_subset_by_date(txn_list, start_date, end_date)

        transactions.append(store)

        spending, ign = get_total_spending(store, m)
        spendings.append(spending)
        groupings.append(get_category_breakdown(store))
        ignored.append(ign)

        start_date += one_month
        end_date += one_month

    return spendings, transactions, groupings, ignored, dates


def plot_spendings(spendings: List[float], dates: List[datetime], plot=plt):
    plot.title("Balance over time")
    plot.ylabel("Balance ($)")
    plot.xlabel("Date")
    plot.plot(dates, spendings)
    plot.scatter(dates, spendings)
    plt.show()


def plot_groupings(txn_list: List[Transaction], m: Model, plot=plt, select=None, split=False):
    s, _, groupings, _, dates = generate_all_months(txn_list, m)
    data = {group: [] for group in m.get_all_categories()}
    for month_groupings in groupings:
        for group in data:
            if group in month_groupings:
                data[group].append(month_groupings[group])
            else:
                data[group].append(0)

    if split:
        keys = list(data.keys())
        sqrt_len = math.ceil(math.sqrt(len(keys)))
        fig, ax = plot.subplots(nrows=(len(keys) // sqrt_len) + 1, ncols=sqrt_len, sharex=True)
        for y, row in enumerate(ax):
            for x, col in enumerate(row):
                cur_pos = y * sqrt_len + x
                if cur_pos < len(keys):
                    cur_label = keys[cur_pos]
                    col.plot(dates, data[cur_label])
                    col.scatter(dates, data[cur_label])
                    col.set_title(cur_label)

                if cur_pos == len(keys):
                    col.plot(dates, s)
                    col.set_title("Total Balance")
                    col.scatter(dates, s)
                col.tick_params(axis='x', labelrotation=70)
        fig.subplots_adjust(hspace=.5, wspace=0.3)

    else:
        plot.title("Balance per group")
        for group in data:
            if select == group or select is None:
                plot.plot(dates, data[group], label=group)
                plot.scatter(dates, data[group])
        plot.legend()

    plot.show()


if __name__ == "__main__":
    CIBC = Bank("CIBC")
    c_parser = CIBCParser("Inputs/cibc/", CIBC, SimpleTransaction, SimpleAccount)
    CIBC.set_parser(c_parser)

    scotia = Bank("Scotia")
    s_parser = ScotiaParser("Inputs/scotia/", scotia, SimpleTransaction, SimpleAccount)
    scotia.set_parser(s_parser)

    Banks = [CIBC, scotia]

    model = CSVModel("Models/CSVModelData")

    total_list = []
    for bank in Banks:
        total_list += bank.get_parser().parse_all()

    categorize_transactions(total_list, model)

    s, t, g, i, d = generate_all_months(total_list, model)
    # plot_spendings(s, d)
    plot_groupings(total_list, model, split=True)
