from datetime import datetime

from tinkoff.invest import Client, OrderDirection, OrderType
from tinkoff.invest.services import SandboxService
import creds
import pandas as pd

"""
Для видео по Песочнице https://tinkoff.github.io/investAPI/head-sandbox/
Все видео по API v2 Тинькофф Инвестиции https://www.youtube.com/watch?v=QvPZT5uCU4c&list=PLWVnIRD69wY6j5QvOSU2K_I3NSLnFYiZY

https://tinkoff.github.io/investAPI
https://github.com/Tinkoff/invest-python
"""

# figi = 'BBG004730N88' # SBER
# figi = 'BBG005DXJS36' # TCS
figi = 'BBG000B9XRY4' # AAPL
account_id = 'xxx'


def run():
    print("Песочница API v2 Тинькофф Инвестиции")

    with Client(creds.token_sandbox) as cl:
        sb: SandboxService = cl.sandbox

        # r = sb.get_sandbox_accounts().accounts
        # [print(acc.id, acc.opened_date) for acc in r]

        # https://tinkoff.github.io/investAPI/sandbox/#postsandboxorder
        r = sb.post_sandbox_order(
            figi=figi,
            quantity=1,
            # price=Quotation(units=1, nano=0),
            account_id=account_id,
            order_id=datetime.now().strftime("%Y-%m-%dT %H:%M:%S"),
            direction=OrderDirection.ORDER_DIRECTION_SELL,
            order_type=OrderType.ORDER_TYPE_MARKET
        )
        print(r)

        # r = sb.cancel_sandbox_order(account_id=account_id, order_id='xxx')
        # print(r)
        #
        # r = sb.get_sandbox_orders(account_id=account_id).orders
        # print(r)
        #
        # # sleep(3)
        # r = sb.get_sandbox_portfolio(account_id=account_id).positions
        # print(r)


run()