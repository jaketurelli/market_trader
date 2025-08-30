# fmt: off
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.security_class import Security
from tools.alpaca_keys import ALPACA_API_KEY, ALPACA_API_SECRET_KEY
# fmt: on

SIMULATE = True


def update_securities_prices(security_obj_list: Security, timestamp):
    """This will request all securities prices from the alpaca server and update all Securities objects with latest data point"""
    print('todo: possibly: get all security prices')
    if SIMULATE:
        return
    client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET_KEY)
    multisymbol_request_params = StockLatestQuoteRequest(
        symbol_or_symbols=[x.symbol for x in security_obj_list])
    latest_multisymbol_quotes = client.get_stock_latest_quote(
        multisymbol_request_params)

    for security in security_obj_list:
        # todo: need to figure out if we should use bid vs ask vs current price here
        security.add_price_point(
            timestamp, latest_multisymbol_quotes[security.symbol].ask_price)


def sell_security(security_to_sell):
    print("todo: figure out how to sell a security with alpaca")


def sell_securities(security_obj_list: Security):
    for security in security_obj_list:
        security_sells = security.get_sellable_holdings()
        if security_sells is None:
            return

        for sec_sell in security_sells:
            sell_security(sec_sell)


def get_buy_rankings(security_obj_list: Security):
    security_buy_ranks = []
    for security in security_obj_list:
        security_buy_ranks.append(security.get_buy_rank())

    return security_buy_ranks


def buy_security(security: Security):
    # todo
    return True


def buy_based_on_rankings(buy_ranks):
    buy_security(max(buy_ranks))


def update_open_orders(purchases: Security):
    for purch in purchases:
        purch.add_open_order(purch)


if __name__ == "__main__":
    security_obj_list = [
        Security('TSLA', 'Tesla Inc.'),
        Security('TSLQ', 'Inverse Tesla 2x')
    ]

    while True:

        update_securities_prices(security_obj_list)

        sell_securities(security_obj_list)

        buy_ranks = get_buy_rankings(security_obj_list)

        purchases = buy_based_on_rankings(buy_ranks)

        update_open_orders(purchases)

        break
