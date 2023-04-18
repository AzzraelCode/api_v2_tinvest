from tinkoff.invest import Client
import creds

def run():
    with Client(creds.token_ro_all) as client:
        print("Stream started")
        for m in client.orders_stream.trades_stream():
            print(m)
