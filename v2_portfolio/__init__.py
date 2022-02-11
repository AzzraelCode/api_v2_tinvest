from typing import Optional

import creds
import pandas as pd
from pandas import DataFrame

from tinkoff.invest import Client, RequestError, PortfolioResponse, PositionsResponse, PortfolioPosition, AccessLevel
from tinkoff.invest.services import Services

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Для видео по get_portfolio https://youtu.be/sHu6CxzAmWA
Все видео по API v2 Тинькофф Инвестиции https://www.youtube.com/watch?v=QvPZT5uCU4c&list=PLWVnIRD69wY6j5QvOSU2K_I3NSLnFYiZY

https://tinkoff.github.io/investAPI/operations/#portfoliorequest
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
            df = self.get_portfolio_df(account_id)
            if df is None: continue
            dataframes.append(df)

        df = pd.concat(dataframes, ignore_index=True)

        # надо что-то сделать с дублями бумаг по счетам
        # todo: Есть крутые спецы по панде? Надо оптимизировать ;)
        # <быдлокод_start
        dup_cond =df.figi.duplicated() # индекс дублей
        if dup_cond.sum() > 0:
            duples = df[dup_cond] # дф дублей (без оригиналов)
            df = df[~dup_cond] # чистим от дублей

            # перебираю дубли, их может быть несколько на разных счетах, поэтому обн ориг дф
            for _, dup in duples.iterrows():
                t = df[df.figi == dup.figi].iloc[0]
                # усредняю цену покупки
                t.average_buy_price = ( t.average_buy_price*t.quantity + dup.average_buy_price*dup.quantity )/( t.quantity + dup.quantity )
                t.quantity += dup.quantity
                t.expected_yield += dup.expected_yield
                df[df.figi == dup.figi] = t
        # быдлокод_end>

        # суммы продаж, налоги и комиссии
        df['sell_sum'] = (df['current_price'] + df['current_nkd']) * df['quantity']
        df['comission'] = df['sell_sum'] * 0.003
        df['tax'] = df.apply(lambda row: row['expected_yield'] * 0.013 if row['expected_yield'] > 0 else 0, axis=1)

        print(df.head(1000))


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


    def get_portfolio_df(self, account_id : str) -> Optional[DataFrame]:
        """
        Преобразую PortfolioResponse в pandas.DataFrame

        :param account_id:
        :return:
        """
        r: PortfolioResponse = self.client.operations.get_portfolio(account_id=account_id)
        if len(r.positions) < 1: return None
        df = pd.DataFrame([self.portfolio_pose_todict(p) for p in r.positions])
        return df

    def portfolio_pose_todict(self, p : PortfolioPosition):
        """
        Преобразую PortfolioPosition в dict

        :param p:
        :return:
        """
        r = {
            'figi': p.figi,
            'quantity': self.cast_money(p.quantity),
            'expected_yield': self.cast_money(p.expected_yield),
            'instrument_type': p.instrument_type,
            'average_buy_price': self.cast_money(p.average_position_price),
            'current_price': self.cast_money(p.current_price),
            'currency': p.average_position_price.currency,
            'current_nkd': self.cast_money(p.current_nkd),
        }

        if r['currency'] == 'usd':
            # expected_yield в Quotation а там нет currency
            r['expected_yield'] *= self.get_usdrur()

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