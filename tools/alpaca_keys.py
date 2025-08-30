from dotenv import load_dotenv
# fmt: off
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# fmt: on

load_dotenv()  # Loads variables from .env

ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")
