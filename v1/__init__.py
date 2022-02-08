from datetime import datetime, timedelta

from tinkoff.invest import Client, InstrumentStatus, CandleInterval

import creds

def run():
    print("** Hola Hey, Azzrael Code YT subs!!!\n")

    # клиент НУЖНО оборачивать в try - именно клиент выкидывает искл. в сл. ошибок API
    with Client(creds.token_ro_acc_main) as client:
        # r = client.users.get_accounts()
        r = client.operations.get_portfolio(account_id=creds.account_id_main)

        # r = client.operations.get_operations(
        #     account_id=creds.account_id_main,
        #     from_= datetime.datetime(2021,1,1),
        #     to=datetime.datetime.now()
        # )

        # r = client.instruments.bonds()
        # r = client.instruments.bonds(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED)
        # figi = 'BBG00T22WKV5'
        # r = client.instruments.bond_by(id=figi, id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI)
        # ticker = 'SU29013RMFS8'
        # class_code = 'TQOB'
        # r = client.instruments.bond_by(id=ticker, id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code=class_code)

        # r = client.instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE)

        # figi = 'BBG00T22WKV5'
        # r = client.market_data.get_order_book(figi=figi, depth=50) # 50 макс (стаканов (с глубиной 10, 20, 30, 40 или 50);)
        # r = len(r.bids)

        print(r)