from datetime import datetime, timedelta, timezone

from pandas import DataFrame
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle

import creds
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


"""
Для видео по get_candles
https://tinkoff.github.io/investAPI
https://tinkoff.github.io/investAPI/marketdata/#getcandlesrequest
https://github.com/Tinkoff/invest-python

https://technical-analysis-library-in-python.readthedocs.io/en/latest/index.html
pip install ta
"""
def run():

    try:
        with Client(creds.token_ro_acc_main) as client:
            r = client.market_data.get_candles(
                # figi='USD000UTSTOM',
                figi='BBG004730N88', # SBER
                from_=datetime.utcnow() - timedelta(hours=10),
                to=datetime.now() ,
                interval=CandleInterval.CANDLE_INTERVAL_15_MIN # см. utils.get_all_candles
            )
            # print(r)

            df = create_df(r.candles)
            # https://technical-analysis-library-in-python.readthedocs.io/en/latest/ta.html#ta.trend.ema_indicator
            df['ema'] = ema_indicator(close=df['close'], window=9)

            print(df[['time', 'close', 'ema']].tail(30))
            # ax=df.plot(x='time', y='close')
            # df.plot(ax=ax, x='time', y='ema')
            # plt.show()

    except RequestError as e:
        print(str(e))


def create_df(candles : [HistoricCandle]):
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])

    return df


def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9 # nano - 9 нулей