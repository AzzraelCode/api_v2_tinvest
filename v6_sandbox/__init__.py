from datetime import datetime, timedelta
from typing import Optional
from tinkoff.invest import Client, MoneyValue
from tinkoff.invest.services import SandboxService, Services, InstrumentsService, MarketDataService

import creds
import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""
Для видео по Песочнице https://tinkoff.github.io/investAPI/head-sandbox/
Все видео по API v2 Тинькофф Инвестиции https://www.youtube.com/watch?v=QvPZT5uCU4c&list=PLWVnIRD69wY6j5QvOSU2K_I3NSLnFYiZY

https://tinkoff.github.io/investAPI
https://github.com/Tinkoff/invest-python
"""

def run():
    print("Песочница API v2 Тинькофф Инвестиции")

    with Client(token=creds.token_sandbox2) as cl:
        print(creds.token_sandbox2)
        sb : SandboxService = cl.sandbox
        # print(cl)
        # account_id = 'xxx'
        #
        # sb.sandbox_pay_in(
        #     account_id=account_id,
        #     amount=MoneyValue(units=0, nano=10000000, currency='usd')
        # )
        #
        # r = sb.get_sandbox_portfolio(account_id=account_id)
        # print(r)

        # sb.close_sandbox_account(account_id=account_id)

        # r = sb.open_sandbox_account().account_id
        # print(r)

        r = sb.get_sandbox_accounts().accounts
        [print(acc.id, acc.opened_date) for acc in r]

if __name__ == '__main__':
    print("** Hola Hey, Azzrael Code YT subs!!!\n")
    run()