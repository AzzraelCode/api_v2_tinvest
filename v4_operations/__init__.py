from datetime import datetime, timedelta
from typing import Optional

import creds
import pandas as pd
from pandas import DataFrame

from tinkoff.invest import Client, RequestError, PositionsResponse, AccessLevel, OperationsResponse, Operation, \
    OperationState, OperationType
from tinkoff.invest.services import Services

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Для видео по get_operations https://youtu.be/DxqeiwWZI4w
Все видео по API v2 Тинькофф Инвестиции https://www.youtube.com/watch?v=QvPZT5uCU4c&list=PLWVnIRD69wY6j5QvOSU2K_I3NSLnFYiZY

https://tinkoff.github.io/investAPI/operations/#operationsresponse
https://tinkoff.github.io/investAPI
https://github.com/Tinkoff/invest-python
"""


def run():
    try:
        with Client(creds.token_ro_all) as client:
            Hola(client).report()
    except RequestError as e:
        print(str(e))

############################### <=== CLASS ===> ############################

class Hola:
    def __init__(self, client: Services):
        self.usdrur = None
        self.client = client
        self.accounts = []

    def report(self):
        dataframes = []
        for account_id in self.get_accounts():
            df = self.get_operations_df(account_id)
            if df is None: continue
            dataframes.append(df)

        if len(dataframes) > 0:
            df = pd.concat(dataframes, ignore_index=True).sort_values(by='date', ascending=False)
            # df = df[df['otype'] == OperationType.OPERATION_TYPE_BROKER_FEE]

            print(df.head(1000))
            print(len(df), df['payment'].sum())

    def get_accounts(self):
        """
        Получаю все аккаунты и буду использовать только те
        кот текущий токен может хотябы читать,
        остальные акк пропускаю
        :return:
        """
        r = self.client.users.get_accounts()
        for acc in r.accounts:
            if acc.access_level != AccessLevel.ACCOUNT_ACCESS_LEVEL_NO_ACCESS:
                self.accounts.append(acc.id)

        return self.accounts

    def get_usdrur(self):
        """
        Получаю курс только если он нужен
        :return:
        """
        if not self.usdrur:
            # т.к. есть валютные активы (у меня etf), то нужно их отконвертить в рубли
            # я работаю только в долл, вам возможно будут нужны и др валюты
            u = self.client.market_data.get_last_prices(figi=['USD000UTSTOM'])
            self.usdrur = self.cast_money(u.last_prices[0].price)

        return self.usdrur


    def get_operations_df(self, account_id : str) -> Optional[DataFrame]:
        """
        Преобразую PortfolioResponse в pandas.DataFrame

        :param account_id:
        :return:
        """
        r: OperationsResponse = self.client.operations.get_operations(
            account_id=account_id,
            from_=datetime(2015,1,1),
            to=datetime.utcnow()
        )

        if len(r.operations) < 1: return None
        df = pd.DataFrame([self.operation_todict(p, account_id) for p in r.operations])
        return df

    def operation_todict(self, o : Operation, account_id : str):
        """
        Преобразую PortfolioPosition в dict
        :param p:
        :return:
        """
        r = {
            'acc': account_id,
            'date': o.date,
            'type': o.type,
            'otype': o.operation_type,
            'currency': o.currency,
            'instrument_type': o.instrument_type,
            'figi': o.figi,
            'quantity': o.quantity,
            'state': o.state,
            'payment': self.cast_money(o.payment, False),
            'price': self.cast_money(o.price, False),
        }

        return r

    def cast_money(self, v, to_rub=True):
        """
        https://tinkoff.github.io/investAPI/faq_custom_types/
        :param to_rub:
        :param v:
        :return:
        """
        r = v.units + v.nano / 1e9
        if to_rub and hasattr(v, 'currency') and getattr(v, 'currency') == 'usd':
            r *= self.get_usdrur()

        return r