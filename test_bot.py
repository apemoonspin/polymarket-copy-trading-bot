"""
Bot Test Script
Run for a short time to verify operation
"""
import signal
import sys
from bot import PolyArbitrageBot
import time

# Exit signal handler
def signal_handler(sig, frame):
    print("\n\n[*] Shutting down test...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("="*60)
    print("🧪 Bot Test Mode Starting")
    print("="*60)
    print("[*] Test will run for approximately 30 seconds.")
    print("[*] Press Ctrl+C to interrupt.")
    print("-"*60)
    
    # Initialize bot
    bot = PolyArbitrageBot()
    
    # Get market list
    print("\n[*] Searching for active markets...")
    markets = bot.get_active_markets(limit=5)  # Only 5 for testing
    
    if not markets:
        print("[✗] No markets found.")
        sys.exit(1)
    
    print(f"[✓] Found {len(markets)} markets")
    for i, market in enumerate(markets[:3], 1):
        print(f"  {i}. {market['question'][:60]}")
    
    # Run test
    print(f"\n[*] Starting to monitor {len(markets)} markets...")
    print("[*] Querying prices for each market and saving data.\n")
    
    start_time = time.time()
    test_duration = 30  # 30 second test
    scan_count = 0
    
    try:
        while time.time() - start_time < test_duration:
            opportunities_found = 0
            
            for market in markets:
                try:
                    if bot.monitor_market(market['id'], market['question']):
                        opportunities_found += 1
                except Exception as e:
                    print(f"[✗] Market monitoring error ({market['id']}): {e}")
                    continue
                
                # Short delay
                time.sleep(0.5)
            
            scan_count += 1
            elapsed = time.time() - start_time
            remaining = test_duration - elapsed
            
            if scan_count % 3 == 0:  # Output status every 3 scans
                print(f"\n[📊] Scan {scan_count} complete (Elapsed: {elapsed:.1f}s, Remaining: {remaining:.1f}s)")
            
            time.sleep(bot.scan_interval)
    
    except KeyboardInterrupt:
        pass
    
    # Final statistics
    elapsed_time = time.time() - start_time
    print("\n" + "="*60)
    print("📊 Test Results")
    print("="*60)
    print(f"Execution time: {elapsed_time:.1f} seconds")
    print(f"Scan count: {scan_count}")
    print(f"Markets monitored: {len(markets)}")
    
    # Database statistics
    if bot.logger:
        import sqlite3
        import os
        from config import DB_LOG_FILE
        
        if os.path.exists(DB_LOG_FILE):
            conn = sqlite3.connect(DB_LOG_FILE)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM price_data')
            total_records = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM price_data WHERE arbitrage_opportunity = 1')
            opportunities = cursor.fetchone()[0]
            conn.close()
            
            print(f"\nDatabase Statistics:")
            print(f"  Total records: {total_records}")
            print(f"  Arbitrage opportunities: {opportunities}")
    
    print("\n[✓] Test complete!")
    print("="*60)
