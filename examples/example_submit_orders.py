from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.client import TradingClient
import sys
import os
# fmt: off
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.alpaca_keys import ALPACA_API_KEY, ALPACA_API_SECRET_KEY
# fmt: on


trading_client = TradingClient(ALPACA_API_KEY,
                               ALPACA_API_SECRET_KEY,
                               paper=True)

# preparing orders
market_order_data = MarketOrderRequest(
    symbol="SPY",
    qty=0.023,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY
)

# Market order
market_order = trading_client.submit_order(
    order_data=market_order_data
)

print(market_order)


limit_order_data = LimitOrderRequest(
    symbol="TSLQ",
    limit_price=30,
    notional=4000,
    side=OrderSide.SELL,
    time_in_force=TimeInForce.FOK
)

# Limit order
limit_order = trading_client.submit_order(
    order_data=limit_order_data
)

print(limit_order)
