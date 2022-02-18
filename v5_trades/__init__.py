"""
Самые дешевые акции для минимизации расходов на комиссии
при отладке скриптов на реальном счете

132  BBG000QQPXZ5     LNTA       TQBR     0.20        1      rub    True    174.30     174.30
133  BBG00F9XX7H4     RNFT       TQBR     0.50        1      rub    True    160.00     160.00
134  BBG004S68598     MTLR       TQBR    10.00        1      rub    True    159.29     159.29
135  BBG000K3STR7     APTK       TQBR     0.64       10      rub    True     13.78     137.78
136  BBG0014PFYM2     RUGR       TQBR     1.00       10      rub    True     11.94     119.44
137  BBG001M2SC01     ETLN       TQBR     1.00        1      rub    True     92.78      92.78

# Фонды ТИ вообще без комиссии, но на них лимиты
69  BBG333333333   TMOS       TQTF        0    1      rub    True     6.44       6.44
70  BBG000000001   TRUR       TQTF        0    1      rub    True     6.07       6.07
71  TCS00A1039N1   TBRU       TQTF        0    1      rub    True     4.86       4.86
"""

FIGI = "TCS00A1039N1"

from datetime import datetime
from tinkoff.invest import Client, RequestError, OrderDirection, OrderType, Quotation
import creds


def cast_money(v):
    return v.units + v.nano / 1e9

def run():
    print("** Trade Examples")
    try:
        # Токен с правами на чтение на соотв субсчете
        with Client(creds.token_wr_test) as client:

            # Открытые ордера или частично исполненные
            # orders = client.orders.get_orders(account_id=creds.account_id_test).orders
            # print(orders)

            # не исполненные заявки можно отменить
            # order_id = orders[0].order_id
            # print("Lets cancel order w id %s" % order_id)
            # r = client.orders.cancel_order(account_id=creds.account_id_test, order_id=order_id)
            # print(r)

            book = client.market_data.get_order_book(figi=FIGI, depth=50)
            print(book)

            # fast_price_sell, fast_price_buy = book.asks[0], book.bids[0] # центр стакана, мин спред
            # best_price_sell, best_price_buy = book.asks[-1], book.bids[-1]  # края стакана, макс спред
            # print(fast_price_sell, fast_price_buy)
            # print(best_price_sell, best_price_buy)
            #
            # # только для удобной отладки, в проде - лишнее
            # bids = [cast_money(p.price) for p in book.bids] # покупатели
            # asks = [cast_money(p.price) for p in book.asks] # продавцы
            # print(bids, asks, sep="\n")

            # ! также нужно учитывать объемы
            # е. price >= max(asks), а quantity > max(asks).quantity, то заберем из сл глубины,
            # по цене ВЫШЕ чем нам надо !!!
            # см. https://tinkoff.github.io/investAPI/faq_orders/

            # r = client.orders.post_order(
            #     order_id=str(datetime.utcnow().timestamp()),
            #     figi=FIGI,
            #     quantity=1,
            #     account_id=creds.account_id_test,
            #     direction=OrderDirection.ORDER_DIRECTION_BUY,
            #     order_type=OrderType.ORDER_TYPE_MARKET
            # )

            # Рыночная, без указания цены (по лучшей доступной для объема)
            # r = client.orders.post_order(
            #     order_id=str(datetime.utcnow().timestamp()),
            #     figi=FIGI,
            #     quantity=1,
            #     account_id=creds.account_id_test,
            #     direction=OrderDirection.ORDER_DIRECTION_BUY,
            #     order_type=OrderType.ORDER_TYPE_MARKET
            # )

            # Лимитка (ограничения цен - нижние края стакана)
            # r = client.orders.post_order(
            #     order_id=str(datetime.utcnow().timestamp()),
            #     figi=FIGI,
            #     quantity=1,
            #     price=Quotation(units=99, nano=0),
            #     account_id=creds.account_id_test,
            #     direction=OrderDirection.ORDER_DIRECTION_SELL,
            #     order_type=OrderType.ORDER_TYPE_LIMIT
            # )
            #
            # print(r)


    except RequestError as e:
        print(str(e))



