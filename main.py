import schedule
import time
from datetime import datetime
import pytz

# Import our custom modules
from data_fetcher import get_historical_data
from indicators import calculate_rsi, calculate_moving_averages
from strategy import check_rsi_alert, check_ma_crossover
from notifier import format_rsi_alert, format_ma_alert, send_email
from database_manager import init_db, is_duplicate, log_alert

# Configuration
TICKERS = ["AAPL", "AMZN", "MSFT", "META", "NVDA", "GOOGL", "TSLA"]
INTERVAL = "4h"
PERIOD = "3mo"
TIMEZONE = pytz.timezone("US/Eastern") # US Market timezone

def run_analysis_for_ticker(ticker: str):
    """
    Runs the full analysis pipeline for a single ticker.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Analyzing {ticker}...")
    
    # 1. Fetch Data
    df = get_historical_data(ticker, interval=INTERVAL, period=PERIOD)
    if df is None or df.empty:
        print(f"Skipping {ticker} due to data fetch failure.")
        return
        
    # 2. Calculate Indicators
    df = calculate_rsi(df, period=14)
    df = calculate_moving_averages(df, fast=20, slow=50)
    
    # Extract current values for potential alerts
    current_price = df['Close'].iloc[-1]
    current_rsi = df['RSI_14'].iloc[-1]
    fast_ma = df['MA_20'].iloc[-1]
    slow_ma = df['MA_50'].iloc[-1]
    
    # 3. Check Alerts & Send Notifications
    
    # RSI Check
    if check_rsi_alert(df, threshold=30):
        if not is_duplicate(ticker, "RSI", hours=24):
            print(f" > ALERT: {ticker} RSI is {current_rsi:.2f} (Below 30)")
            subject, body = format_rsi_alert(ticker, current_price, current_rsi, interval=INTERVAL)
            send_email(subject, body)
            log_alert(ticker, "RSI", current_price, current_rsi)
        else:
            print(f" > SKIPPED: {ticker} RSI alert already sent in the last 24h.")
        
    # Moving Average Check
    if check_ma_crossover(df, fast_col='MA_20', slow_col='MA_50'):
        if not is_duplicate(ticker, "MA_CROSS", hours=24):
            print(f" > ALERT: {ticker} MA 20 crossed MA 50 upwards.")
            subject, body = format_ma_alert(ticker, current_price, fast_ma, slow_ma, interval=INTERVAL)
            send_email(subject, body)
            log_alert(ticker, "MA_CROSS", current_price, fast_ma)
        else:
            print(f" > SKIPPED: {ticker} MA Crossover alert already sent in the last 24h.")

def check_market_hours() -> bool:
    """
    Checks if the US stock market is currently open.
    (Simple version: Monday-Friday, 9:30 AM - 4:00 PM Eastern Time)
    Note: Does not account for holidays yet.
    """
    now_et = datetime.now(TIMEZONE)
    
    # Check if weekend (0=Monday, 6=Sunday)
    if now_et.weekday() >= 5:
        return False
        
    # Check if between 9:30 AM and 4:00 PM
    market_open = now_et.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now_et.replace(hour=16, minute=0, second=0, microsecond=0)
    
    return market_open <= now_et <= market_close

def market_scan_job():
    """
    The main job executed by the scheduler.
    """
    # Uncomment the following lines if you only want to scan during market hours
    # if not check_market_hours():
    #     print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Market is closed. Skipping scan.")
    #     return
        
    print(f"\n--- Starting 4h Market Scan for: {', '.join(TICKERS)} ---")
    for ticker in TICKERS:
        run_analysis_for_ticker(ticker)
    print("--- Scan Complete ---\n")

def main():
    print("Tickers Notification System Started!")
    print(f"Configured to scan: {TICKERS}")
    
    # Initialize the database on startup
    init_db()
    
    # Run once immediately on startup
    market_scan_job()
    
    # Schedule to run every 4 hours
    # This is a basic scheduling approach. A more robust way 
    # would be to schedule exactly at specific hours (e.g. 9:30, 13:30).
    
    schedule.every(4).hours.do(market_scan_job)
    
    print("Scheduler running. Waiting for next interval...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
