import sys
import os
from collections import deque
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.models import Order
from alpaca.common.types import Union, RawData
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.requests import MarketOrderRequest
# fmt: off
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.open_position_class import OpenPosition
from tools.alpaca_keys import ALPACA_API_KEY, ALPACA_API_SECRET_KEY
# fmt: on


class Security:
    def __init__(self, symbol, name, max_positions=5, max_analyis_samples=5*60, paper_trade=True):
        self.symbol = symbol
        self.name = name
        self.url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"
        self.trading_client = TradingClient(ALPACA_API_KEY,
                                            ALPACA_API_SECRET_KEY)
        self.max_positions = max_positions
        self.paper_trade = paper_trade
        self.open_positions = []

        self.price_queue = deque(maxlen=max_analyis_samples)
        self.time_queue = deque(maxlen=max_analyis_samples)
        self.max_analyis_samples = max_analyis_samples

        self.price_linear_approx = None
        self.linear_coeffs = None
        self.linear_slope = 0
        self.linear_slope_threshold = 0
        self.price_2nd_position_approx = None
        self.quad_coeffs = None

    def __repr__(self):
        return f"Security:\n \
                symbol='{self.symbol}'\n \
                name={self.name}\n \
                paper_trade:{self.paper_trade}\n \
                max_positions:{self.max_positions}"

    def get_buy_rank(self):
        # todo
        return -1

    def retrieve_open_positions(self):
        for alpaca_position in self.trading_client.get_all_positions():
            self.open_positions.append(OpenPosition(alpaca_position))

    def market_order(self, qty: float, limit_price, side: OrderSide = OrderSide.BUY, time_in_force: TimeInForce = TimeInForce.DAY) -> Union[Order, RawData]:
        # Market order
        return self.trading_client.submit_order(order_data=MarketOrderRequest(symbol=self.symbol,
                                                                              qty=qty,
                                                                              side=side,
                                                                              time_in_force=time_in_force))

    def limit_order(self, limit_price: float, qty: float, side: OrderSide = OrderSide.BUY, time_in_force: TimeInForce = TimeInForce.DAY) -> Union[Order, RawData]:
        # Limit order
        return self.trading_client.submit_order(order_data=LimitOrderRequest(symbol=self.symbol,
                                                                             limit_price=limit_price,
                                                                             qty=qty,
                                                                             side=side,
                                                                             time_in_force=time_in_force))

    def add_price_point(self, time_point, price_point):
        self.time_queue.append(time_point)
        self.price_queue.append(price_point)

    def is_open_position_sellable(self, position):
        # todo
        return False

    def get_sellable_holdings(self):

        if len(self.price_queue) != self.max_analyis_samples:
            return None

        sellable_holdings = []
        for position in self.open_positions:
            if self.is_open_position_sellable(position):
                sellable_holdings.append(position)

        return sellable_holdings
