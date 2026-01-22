"""
Stored price data analysis script
Analyzes arbitrage opportunity statistics from CSV and SQLite DB
"""
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from config import DB_LOG_FILE, CSV_LOG_FILE
import os


def analyze_arbitrage_opportunities(hours: int = 24):
    """Analyze arbitrage opportunities"""
    if not os.path.exists(DB_LOG_FILE):
        print(f"[✗] Database file not found: {DB_LOG_FILE}")
        print("[*] Please run the bot first to collect data.")
        return
    
    conn = sqlite3.connect(DB_LOG_FILE)
    
    # Query data from last N hours
    query = '''
        SELECT 
            COUNT(*) as total_records,
            SUM(CASE WHEN arbitrage_opportunity = 1 THEN 1 ELSE 0 END) as opportunities,
            AVG(CASE WHEN arbitrage_opportunity = 1 THEN potential_profit ELSE NULL END) as avg_profit,
            MAX(CASE WHEN arbitrage_opportunity = 1 THEN potential_profit ELSE NULL END) as max_profit,
            MIN(CASE WHEN arbitrage_opportunity = 1 THEN potential_profit ELSE NULL END) as min_profit,
            COUNT(DISTINCT CASE WHEN arbitrage_opportunity = 1 THEN market_id ELSE NULL END) as unique_markets,
            AVG(total_cost) as avg_total_cost,
            MIN(total_cost) as min_total_cost
        FROM price_data
        WHERE timestamp >= datetime('now', '-' || ? || ' hours')
    '''
    
    cursor = conn.cursor()
    cursor.execute(query, (hours,))
    result = cursor.fetchone()
    
    print("="*60)
    print(f"📊 Arbitrage Opportunity Analysis (Last {hours} hours)")
    print("="*60)
    
    if result and result[0] > 0:
        total_records, opportunities, avg_profit, max_profit, min_profit, unique_markets, avg_cost, min_cost = result
        
        print(f"\n📈 Overall Statistics:")
        print(f"    Total records: {total_records:,}")
        print(f"    Arbitrage opportunities: {opportunities:,} ({opportunities/total_records*100:.2f}%)")
        
        if opportunities > 0:
            print(f"\n💰 Profit Analysis:")
            print(f"    Average profit rate: {avg_profit*100:.4f}%")
            print(f"    Maximum profit rate: {max_profit*100:.4f}%")
            print(f"    Minimum profit rate: {min_profit*100:.4f}%")
            print(f"    Unique markets: {unique_markets}")
        
        print(f"\n💵 Price Analysis:")
        print(f"    Average total cost: ${avg_cost:.4f}")
        print(f"    Minimum total cost: ${min_cost:.4f}")
        
        # Hourly distribution analysis
        print(f"\n⏰ Hourly Distribution:")
        time_query = '''
            SELECT 
                strftime('%H', timestamp) as hour,
                COUNT(*) as count,
                SUM(CASE WHEN arbitrage_opportunity = 1 THEN 1 ELSE 0 END) as opportunities
            FROM price_data
            WHERE timestamp >= datetime('now', '-' || ? || ' hours')
            GROUP BY hour
            ORDER BY hour
        '''
        cursor.execute(time_query, (hours,))
        time_results = cursor.fetchall()
        
        for hour, count, opps in time_results:
            if count > 0:
                print(f"    {hour:>2}:00: {opps:>4} opportunities / {count:>6} records ({opps/count*100:>5.2f}%)")
        
        # Top markets analysis
        print(f"\n🏆 Markets with Most Arbitrage Opportunities (Top 10):")
        market_query = '''
            SELECT 
                market_id,
                market_question,
                COUNT(*) as opportunities,
                AVG(potential_profit) as avg_profit,
                MAX(potential_profit) as max_profit
            FROM price_data
            WHERE arbitrage_opportunity = 1
            AND timestamp >= datetime('now', '-' || ? || ' hours')
            GROUP BY market_id, market_question
            ORDER BY opportunities DESC
            LIMIT 10
        '''
        cursor.execute(market_query, (hours,))
        market_results = cursor.fetchall()
        
        if market_results:
            for i, (market_id, question, opps, avg_p, max_p) in enumerate(market_results, 1):
                question_short = (question[:50] + '...') if question and len(question) > 50 else (question or market_id)
                print(f"    {i:>2}. {question_short}")
                print(f"        Opportunities: {opps} | Avg profit: {avg_p*100:.4f}% | Max profit: {max_p*100:.4f}%")
        else:
            print("    No arbitrage opportunities found.")
    
    else:
        print("\n[!] No data to analyze.")
        print(f"[*] No records found in the last {hours} hours.")
    
    conn.close()
    print("\n" + "="*60)


def export_to_csv(output_file: str = None, hours: int = 24):
    """Export SQLite DB data to CSV"""
    if not os.path.exists(DB_LOG_FILE):
        print(f"[✗] Database file not found: {DB_LOG_FILE}")
        return
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"./logs/export_{timestamp}.csv"
    
    conn = sqlite3.connect(DB_LOG_FILE)
    
    query = '''
        SELECT 
            timestamp,
            market_id,
            market_question,
            yes_price,
            no_price,
            total_cost,
            arbitrage_opportunity,
            potential_profit,
            yes_ask_price,
            no_ask_price,
            yes_bid_price,
            no_bid_price
        FROM price_data
        WHERE timestamp >= datetime('now', '-' || ? || ' hours')
        ORDER BY timestamp DESC
    '''
    
    df = pd.read_sql_query(query, conn, params=(hours,))
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"[✓] Data exported to CSV: {output_file}")
    print(f"    Total {len(df)} records")
    
    conn.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    else:
        hours = 24
    
    analyze_arbitrage_opportunities(hours)
    
    # CSV export option
    if len(sys.argv) > 2 and sys.argv[2] == "--export":
        export_to_csv(hours=hours)
