
import requests
from dotenv import load_dotenv
# fmt: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.trade_class import Trade
# fmt: on


load_dotenv()  # Loads variables from .env

ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")

print("API Key:", ALPACA_API_KEY)
print("API Key:", ALPACA_API_SECRET_KEY)


holdings = [
    Trade("TSLA", "Tesla Inc"),
    Trade("TSLQ", "ProShares UltraShort Tesla"),
]

headers = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET_KEY
}

for trade in holdings:
    # print(f"Fetching data for {stock} from {url}")
    print(f"Trade object: {trade}")
    response = requests.get(trade.url, headers=headers)
    data = response.json()
    last_price = data["trade"]["p"]
    timestamp = data["trade"]["t"]
    print(data)

    print(f"Last {trade.symbol} trade price: ${last_price} at {timestamp}")
