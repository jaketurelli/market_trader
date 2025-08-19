
import asyncio
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
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


# keys required for stock historical data client
client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET_KEY)
# multi symbol request - single symbol is similar
multisymbol_request_params = StockLatestQuoteRequest(
    symbol_or_symbols=[x.symbol for x in holdings])

latest_multisymbol_quotes = client.get_stock_latest_quote(
    multisymbol_request_params)

for trade in holdings:
    # print(latest_multisymbol_quotes[trade.symbol])
    print(
        f'latest bid vs ask {trade.symbol}: {latest_multisymbol_quotes[trade.symbol].bid_price} vs. {latest_multisymbol_quotes[trade.symbol].ask_price}')

# fmt: off
from alpaca.data.live import StockDataStream
wss_client = StockDataStream(ALPACA_API_KEY, ALPACA_API_SECRET_KEY)
# fmt: on


async def quote_data_handler(data):
    # async handler
    # quote data will arrive here
    print(data)
print("Subscribing to quotes for:", holdings[0].symbol)
wss_client.subscribe_quotes(quote_data_handler, holdings[0].symbol)
wss_client.run()

# async def run_with_timeout(client, seconds):
#     task = asyncio.create_task(client.run())
#     try:
#         await asyncio.wait_for(task, timeout=seconds)
#     except asyncio.TimeoutError:
#         print("Timeout reached, stopping WebSocket client.")
#         task.cancel()
# timeout = 100
# run_with_timeout(wss_client, timeout)
