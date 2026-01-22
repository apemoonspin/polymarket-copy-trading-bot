# Polymarket Arbitrage Bot

A bot that automatically detects and executes arbitrage opportunities when the sum of Yes/No ticket prices on Polymarket is less than 1.0.

## 🎯 Key Features

- **Real-time Price Monitoring**: Tracks Yes/No ticket prices across multiple markets in real-time
- **Arbitrage Detection**: Automatically detects when `yes_price + no_price < 0.99` condition is met
- **Data Logging**: Saves price data to CSV and SQLite DB (for arbitrage opportunity analysis)
- **Automatic Trade Execution**: Automatic order execution via Web3 (optional)

## 📋 Prerequisites

- Python 3.8 or higher
- Polymarket account and wallet (for actual trading)
- Polygon network RPC access

## 🚀 Installation

1. **Clone or download the repository**

```bash
cd polymarket_arbitrage_bot
```

2. **Create and activate virtual environment** (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
cp .env.example .env
# Open .env file and modify with actual values
```

## ⚙️ Configuration

You can adjust the following settings in the `.env` file:

- `MIN_PROFIT_MARGIN`: Minimum profit margin (default: 0.01 = 1%)
- `SCAN_INTERVAL`: Market scan interval (seconds)
- `MAX_MARKETS_TO_MONITOR`: Number of markets to monitor simultaneously
- `PRIVATE_KEY`: Wallet private key (required for actual trading)
- `ENABLE_DATA_LOGGING`: Enable/disable data logging

## 📖 Usage

### 1. Data Logging Mode (record prices only, no trading)

```bash
# Leave PRIVATE_KEY empty in .env to only perform data logging
python bot.py
```

In this mode:
- Periodically queries prices of active markets
- Saves price data to CSV and SQLite DB
- Outputs to console when arbitrage opportunities are found (does not execute trades)

### 2. Actual Trading Mode

```bash
# Set PRIVATE_KEY in .env and run
python bot.py
```

**⚠️ Warning**: Actual trading mode uses real funds. Use only after sufficient testing.

### 3. Monitor Specific Markets Only

You can modify the `bot.py` file to monitor only specific market IDs:

```python
bot = PolyArbitrageBot(market_ids=["market-id-1", "market-id-2"])
bot.run()
```

## 📊 Data Analysis

### Using Analysis Script

```bash
# Analyze last 24 hours of data
python3 analyze_data.py

# Analyze last 1 hour of data
python3 analyze_data.py 1

# Analysis + CSV export
python3 analyze_data.py 24 --export
```

For detailed terminal commands, see [COMMANDS.md](COMMANDS.md).

### CSV File Analysis

Log data is saved to `./logs/price_data.csv`. It includes the following information:

- `timestamp`: Record time
- `market_id`: Market ID
- `yes_price`, `no_price`: Yes/No ticket prices
- `total_cost`: Price sum
- `arbitrage_opportunity`: Whether arbitrage opportunity exists (1/0)
- `potential_profit`: Expected profit rate

### SQLite DB Query Example

```python
import sqlite3

conn = sqlite3.connect('./logs/price_data.db')
cursor = conn.cursor()

# Query arbitrage opportunities from last 24 hours
cursor.execute('''
    SELECT market_id, timestamp, potential_profit 
    FROM price_data 
    WHERE arbitrage_opportunity = 1 
    AND timestamp >= datetime('now', '-24 hours')
    ORDER BY potential_profit DESC
''')

for row in cursor.fetchall():
    print(row)
```

### Statistics Query

Statistics are periodically output during bot execution. You can also directly call the `get_arbitrage_statistics()` method from `data_logger.py`.

## 🔧 Code Structure

```
polymarket_arbitrage_bot/
├── bot.py              # Main bot code
├── analyze_data.py     # Data analysis script
├── data_logger.py      # Data logging module
├── config.py           # Configuration file
├── test_bot.py         # Test script
├── requirements.txt    # Required packages list
├── .env.example        # Environment variables example
├── .gitignore          # Git ignore file list
├── README.md           # This file
├── COMMANDS.md         # Terminal commands guide
└── logs/               # Log file storage directory (Git excluded)
    ├── price_data.csv
    └── price_data.db
```

## 🚨 Warnings

1. **API Rate Limits**: Polymarket API has request limits. Set `SCAN_INTERVAL` appropriately.
2. **Gas Fees**: Polygon network has low gas fees, but gas fees can eat into profits when targeting small profits.
3. **Slippage**: Slippage may occur due to price movements during actual trading.
4. **Concurrency**: Arbitrage requires "concurrency". If you buy a Yes ticket and the No ticket price rises in the meantime, losses may occur.

## 🔮 Future Improvements

- [ ] Real-time price updates via WebSocket
- [ ] Parallel market monitoring using `asyncio`
- [ ] Atomic Arbitrage implementation (atomic trading via smart contracts)
- [ ] `py-clob-client` SDK integration
- [ ] Backtesting functionality
- [ ] Notification features (Telegram, email, etc.)

## 📚 References

- [Polymarket API Documentation](https://docs.polymarket.com)
- [CLOB API Documentation](https://docs.polymarket.com/developers/CLOB)
- [py-clob-client GitHub](https://github.com/Polymarket/py-clob-client)

## ⚖️ Disclaimer

This bot is provided for educational and research purposes. The developer is not responsible for any losses that may occur when using it for actual trading. Please use only after sufficient testing and verification.

## 📝 License

This project is freely available for educational purposes.
