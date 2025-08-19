from alpaca.trading.client import TradingClient
import json

from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
from dotenv import load_dotenv
# fmt: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# fmt: on


load_dotenv()  # Loads variables from .env

ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")
trading_client = TradingClient(ALPACA_API_KEY, ALPACA_API_SECRET_KEY)

account = trading_client.get_account()
# print(account)
# # print(json.dumps(account, indent=2))

# account = trading_client.get_account()
# print(json.dumps(account.__dict__, indent=2))
for item in account.__dict__:
    print(f"{item}: {getattr(account, item)}")
