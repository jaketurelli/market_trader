# fmt: off
from alpaca.trading.client import TradingClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.alpaca_keys import ALPACA_API_KEY, ALPACA_API_SECRET_KEY
# fmt: on


trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET_KEY)

print(trading_client.get_all_positions())
