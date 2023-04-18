from pandas import DataFrame
from tinkoff.invest import MoneyValue, Quotation

figi_sber = "BBG004730N88"  # SBER
figi_tatn = "BBG004RVFFC0"  # TATN
figi_bond = 'BBG00T22WKV5'


def cast_money(v):
    return v.units + v.nano / 1e9 if isinstance(v, (Quotation, MoneyValue)) else v


def to_dict(o):
    return {k: cast_money(v) for k, v in o.__dict__.items()}


def to_df(data: list, ) -> DataFrame:
    return DataFrame([to_dict(r) for r in data])
