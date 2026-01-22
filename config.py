"""
Polymarket Arbitrage Bot Configuration File
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API endpoints
GAMMA_API_URL = "https://gamma-api.polymarket.com"
CLOB_API_URL = "https://clob.polymarket.com"
DATA_API_URL = "https://data-api.polymarket.com"

# WebSocket endpoints (for real-time data)
WS_CLOB_URL = "wss://clob-ws.polymarket.com"

# Bot settings
MIN_PROFIT_MARGIN = float(os.getenv("MIN_PROFIT_MARGIN", "0.01"))  # Minimum 1% profit margin
SCAN_INTERVAL = float(os.getenv("SCAN_INTERVAL", "1.0"))  # Scan interval (seconds)
MAX_MARKETS_TO_MONITOR = int(os.getenv("MAX_MARKETS_TO_MONITOR", "100"))  # Number of markets to monitor simultaneously

# Web3 settings (for actual trading)
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")  # Wallet private key (loaded from environment variable)
POLYGON_RPC_URL = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")

# Data logger settings
ENABLE_DATA_LOGGING = os.getenv("ENABLE_DATA_LOGGING", "true").lower() == "true"
LOG_DIR = os.getenv("LOG_DIR", "./logs")
CSV_LOG_FILE = os.path.join(LOG_DIR, "price_data.csv")
DB_LOG_FILE = os.path.join(LOG_DIR, "price_data.db")

# Trading settings
MIN_TRADE_SIZE = float(os.getenv("MIN_TRADE_SIZE", "0.01"))  # Minimum trade amount
MAX_SLIPPAGE = float(os.getenv("MAX_SLIPPAGE", "0.01"))  # Maximum slippage (1%)
