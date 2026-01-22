"""
Polymarket Price Data Logger
Saves price data to CSV and SQLite DB for arbitrage opportunity analysis
"""
import csv
import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json


class DataLogger:
    """Class for saving price data to CSV and SQLite DB"""
    
    def __init__(self, csv_file: str, db_file: str):
        self.csv_file = csv_file
        self.db_file = db_file
        
        # Create log directory
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        
        # Initialize CSV file
        self._init_csv()
        
        # Initialize DB
        self._init_db()
    
    def _init_csv(self):
        """Initialize CSV file header"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp',
                    'market_id',
                    'market_question',
                    'yes_price',
                    'no_price',
                    'total_cost',
                    'arbitrage_opportunity',
                    'potential_profit',
                    'yes_ask_price',
                    'no_ask_price',
                    'yes_bid_price',
                    'no_bid_price'
                ])
    
    def _init_db(self):
        """Initialize SQLite DB table"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                market_id TEXT NOT NULL,
                market_question TEXT,
                yes_price REAL,
                no_price REAL,
                total_cost REAL,
                arbitrage_opportunity INTEGER,
                potential_profit REAL,
                yes_ask_price REAL,
                no_ask_price REAL,
                yes_bid_price REAL,
                no_bid_price REAL,
                raw_data TEXT
            )
        ''')
        
        # Create indexes (improve search performance)
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_market_timestamp 
            ON price_data(market_id, timestamp)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_arbitrage 
            ON price_data(arbitrage_opportunity, timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    def log_price_data(
        self,
        market_id: str,
        market_question: str,
        yes_price: float,
        no_price: float,
        yes_ask: Optional[float] = None,
        no_ask: Optional[float] = None,
        yes_bid: Optional[float] = None,
        no_bid: Optional[float] = None,
        min_profit_margin: float = 0.01
    ):
        """Save price data to CSV and DB"""
        timestamp = datetime.now().isoformat()
        total_cost = yes_price + no_price
        arbitrage_opportunity = 1 if total_cost < (1.0 - min_profit_margin) else 0
        potential_profit = max(0, 1.0 - total_cost) if arbitrage_opportunity else 0
        
        # Save to CSV
        self._write_csv([
            timestamp,
            market_id,
            market_question,
            yes_price,
            no_price,
            total_cost,
            arbitrage_opportunity,
            potential_profit,
            yes_ask or yes_price,
            no_ask or no_price,
            yes_bid or yes_price,
            no_bid or no_price
        ])
        
        # Save to DB
        self._write_db({
            'timestamp': timestamp,
            'market_id': market_id,
            'market_question': market_question,
            'yes_price': yes_price,
            'no_price': no_price,
            'total_cost': total_cost,
            'arbitrage_opportunity': arbitrage_opportunity,
            'potential_profit': potential_profit,
            'yes_ask_price': yes_ask or yes_price,
            'no_ask_price': no_ask or no_price,
            'yes_bid_price': yes_bid or yes_price,
            'no_bid_price': no_bid or no_price
        })
        
        return arbitrage_opportunity == 1
    
    def _write_csv(self, row: list):
        """Write data to CSV file"""
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
    
    def _write_db(self, data: Dict[str, Any]):
        """Write data to SQLite DB"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO price_data 
            (timestamp, market_id, market_question, yes_price, no_price, 
             total_cost, arbitrage_opportunity, potential_profit,
             yes_ask_price, no_ask_price, yes_bid_price, no_bid_price, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['timestamp'],
            data['market_id'],
            data['market_question'],
            data['yes_price'],
            data['no_price'],
            data['total_cost'],
            data['arbitrage_opportunity'],
            data['potential_profit'],
            data['yes_ask_price'],
            data['no_ask_price'],
            data['yes_bid_price'],
            data['no_bid_price'],
            json.dumps(data)
        ))
        
        conn.commit()
        conn.close()
    
    def get_arbitrage_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Query arbitrage opportunity statistics for specified time period"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Query data from last N hours
        cursor.execute('''
            SELECT 
                COUNT(*) as total_opportunities,
                AVG(potential_profit) as avg_profit,
                MAX(potential_profit) as max_profit,
                MIN(potential_profit) as min_profit,
                COUNT(DISTINCT market_id) as unique_markets
            FROM price_data
            WHERE arbitrage_opportunity = 1
            AND timestamp >= datetime('now', '-' || ? || ' hours')
        ''', (hours,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] > 0:
            return {
                'total_opportunities': result[0],
                'avg_profit': result[1],
                'max_profit': result[2],
                'min_profit': result[3],
                'unique_markets': result[4],
                'hours': hours
            }
        else:
            return {
                'total_opportunities': 0,
                'avg_profit': 0,
                'max_profit': 0,
                'min_profit': 0,
                'unique_markets': 0,
                'hours': hours
            }
