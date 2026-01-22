# Terminal Commands Guide

## 🚀 Bot Execution

### Run Bot
```bash
# Basic execution (foreground)
python3 bot.py

# Background execution
python3 bot.py &

# Background execution and get process ID
python3 bot.py &
echo $!
```

### Stop Bot
```bash
# Find process
ps aux | grep "python3 bot.py"

# Stop bot
pkill -f "python3 bot.py"

# Force stop
pkill -9 -f "python3 bot.py"
```

### Test Execution
```bash
# Run test script (30 seconds)
python3 test_bot.py
```

## 📊 Data Analysis

### Basic Analysis
```bash
# Analyze last 24 hours of data
python3 analyze_data.py

# Analyze last 1 hour of data
python3 analyze_data.py 1

# Analyze last 12 hours of data
python3 analyze_data.py 12

# Analyze last 48 hours of data
python3 analyze_data.py 48
```

### CSV Export
```bash
# Analysis + CSV export
python3 analyze_data.py 24 --export
```

## 💾 Database Check

### Direct SQLite DB Query
```bash
# Check database file
ls -lh logs/price_data.db

# Check total record count
python3 -c "import sqlite3; conn = sqlite3.connect('logs/price_data.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM price_data'); print('Total records:', cursor.fetchone()[0]); conn.close()"

# Check last 5 records
python3 -c "import sqlite3; conn = sqlite3.connect('logs/price_data.db'); cursor = conn.cursor(); cursor.execute('SELECT timestamp, market_id, yes_price, no_price, total_cost, arbitrage_opportunity FROM price_data ORDER BY timestamp DESC LIMIT 5'); [print(r) for r in cursor.fetchall()]; conn.close()"

# Check arbitrage opportunity count
python3 -c "import sqlite3; conn = sqlite3.connect('logs/price_data.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM price_data WHERE arbitrage_opportunity = 1'); print('Arbitrage opportunities:', cursor.fetchone()[0]); conn.close()"

# Market statistics
python3 -c "import sqlite3; conn = sqlite3.connect('logs/price_data.db'); cursor = conn.cursor(); cursor.execute('SELECT market_id, COUNT(*) as cnt, AVG(total_cost) as avg_cost FROM price_data GROUP BY market_id ORDER BY cnt DESC LIMIT 10'); [print(f'Market: {r[0]}, Records: {r[1]}, Avg Cost: {r[2]:.4f}') for r in cursor.fetchall()]; conn.close()"
```

### Using SQLite CLI
```bash
# SQLite interactive mode
sqlite3 logs/price_data.db

# Useful SQLite queries:
# .tables                    # List tables
# .schema price_data         # Table structure
# SELECT COUNT(*) FROM price_data;
# SELECT * FROM price_data ORDER BY timestamp DESC LIMIT 10;
# SELECT * FROM price_data WHERE arbitrage_opportunity = 1;
# .quit                      # Exit
```

## 📁 File Check

### CSV File Check
```bash
# Check CSV file size
ls -lh logs/price_data.csv

# Check first 10 lines of CSV file
head -n 10 logs/price_data.csv

# Check last 10 lines of CSV file
tail -n 10 logs/price_data.csv

# Check total line count of CSV file
wc -l logs/price_data.csv

# Filter only arbitrage opportunities from CSV
grep ",1," logs/price_data.csv | head -n 10
```

### Log Directory Check
```bash
# Check log directory contents
ls -lh logs/

# Check log file size
du -sh logs/
```

## 🔍 Process Monitoring

### Bot Process Check
```bash
# Check running bot process
ps aux | grep "python3 bot.py" | grep -v grep

# Process detailed information
ps -p $(pgrep -f "python3 bot.py") -o pid,ppid,cmd,%mem,%cpu,etime

# Real-time process monitoring
watch -n 1 'ps aux | grep "python3 bot.py" | grep -v grep'
```

### System Resource Check
```bash
# CPU and memory usage
top -p $(pgrep -f "python3 bot.py")

# Or use htop (if installed)
htop -p $(pgrep -f "python3 bot.py")
```

## 📈 Real-time Data Monitoring

### Real-time Database Monitoring
```bash
# Check record count in real-time (every 5 seconds)
watch -n 5 'python3 -c "import sqlite3; conn = sqlite3.connect(\"logs/price_data.db\"); cursor = conn.cursor(); cursor.execute(\"SELECT COUNT(*) FROM price_data\"); print(\"Total records:\", cursor.fetchone()[0]); conn.close()"'

# Real-time arbitrage opportunity monitoring
watch -n 5 'python3 -c "import sqlite3; conn = sqlite3.connect(\"logs/price_data.db\"); cursor = conn.cursor(); cursor.execute(\"SELECT COUNT(*) FROM price_data WHERE arbitrage_opportunity = 1\"); print(\"Arbitrage opportunities:\", cursor.fetchone()[0]); conn.close()"'
```

### CSV File Real-time Monitoring
```bash
# Real-time CSV file monitoring (tail -f)
tail -f logs/price_data.csv

# Continuously view last 20 lines
tail -n 20 -f logs/price_data.csv
```

## 🧹 Cleanup Commands

### Log File Cleanup
```bash
# Backup and delete old CSV files (30+ days)
find logs/ -name "*.csv" -mtime +30 -exec mv {} logs/backup/ \;

# Database backup
cp logs/price_data.db logs/backup/price_data_$(date +%Y%m%d_%H%M%S).db

# Delete empty log files
find logs/ -type f -empty -delete
```

## 🔧 Utility Commands

### Python Environment Check
```bash
# Check Python version
python3 --version

# Check installed packages
pip3 list | grep -E "(pandas|requests|web3|sqlite3)"

# Reinstall packages
pip3 install -r requirements.txt
```

### Network Test
```bash
# Test Polymarket API connection
curl -s "https://gamma-api.polymarket.com/markets?limit=1" | head -n 20

# Measure API response time
time curl -s "https://gamma-api.polymarket.com/markets?limit=1" > /dev/null
```

## 📝 Useful Combined Commands

### Bot Status Overview
```bash
# Bot status + database status
echo "=== Bot Process ===" && ps aux | grep "python3 bot.py" | grep -v grep && echo -e "\n=== Database ===" && python3 -c "import sqlite3; conn = sqlite3.connect('logs/price_data.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM price_data'); print('Total records:', cursor.fetchone()[0]); cursor.execute('SELECT COUNT(*) FROM price_data WHERE arbitrage_opportunity = 1'); print('Arbitrage opportunities:', cursor.fetchone()[0]); conn.close()"
```

### Quick Analysis
```bash
# Quick analysis of last 1 hour of data
python3 analyze_data.py 1
```

### Database Size Check
```bash
# Database file size
du -h logs/price_data.db

# Database internal statistics
sqlite3 logs/price_data.db "SELECT COUNT(*) as total, COUNT(DISTINCT market_id) as markets, MIN(timestamp) as first, MAX(timestamp) as last FROM price_data;"
```
