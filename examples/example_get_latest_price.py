
import asyncio
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient
import requests
from dotenv import load_dotenv
# fmt: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.security_class import Security
# fmt: on


load_dotenv()  # Loads variables from .env

ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")

print("API Key:", ALPACA_API_KEY)
print("API Key:", ALPACA_API_SECRET_KEY)


holdings = [
    Security("TSLA", "Tesla Inc"),
    Security("TSLQ", "ProShares UltraShort Tesla"),
]

headers = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_API_SECRET_KEY
}

for security in holdings:
    # print(f"Fetching data for {stock} from {url}")
    print(f"Security object: {security}")
    response = requests.get(security.url, headers=headers)
    data = response.json()
    last_price = data["security"]["p"]
    timestamp = data["security"]["t"]
    print(data)

    print(f"Last {security.symbol} security price: ${last_price} at {timestamp}")


# keys required for stock historical data client
client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_API_SECRET_KEY)
# multi symbol request - single symbol is similar
multisymbol_request_params = StockLatestQuoteRequest(
    symbol_or_symbols=[x.symbol for x in holdings])

latest_multisymbol_quotes = client.get_stock_latest_quote(
    multisymbol_request_params)

for security in holdings:
    # print(latest_multisymbol_quotes[security.symbol])
    print(
        f'latest bid vs ask {security.symbol}: {latest_multisymbol_quotes[security.symbol].bid_price} vs. {latest_multisymbol_quotes[security.symbol].ask_price}')

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
