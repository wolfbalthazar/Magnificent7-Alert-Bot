import sqlite3
import os

DB_NAME = "alerts.db"

def show_all_alerts():
    """
    Reads and formats all past alerts from the database.
    """
    if not os.path.exists(DB_NAME):
        print(f"Database ({DB_NAME}) does not exist yet. Run main.py first!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch all data from the table
    cursor.execute("SELECT id, ticker, alert_type, price, value, timestamp FROM alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    if not rows:
        print("The database is empty. No alerts recorded yet.")
        return
        
    print(f"\n{'='*75}")
    print(f"{'ALL SENT ALERTS (Newest First)':^75}")
    print(f"{'='*75}")
    print(f"{'ID':<4} | {'Date and Time':<20} | {'Ticker':<8} | {'Type':<10} | {'Price ($)':<10} | {'Value/MA':<10}")
    print(f"{'-'*75}")
    
    for row in rows:
        id, ticker, alert_type, price, value, timestamp = row
        # Format timestamp to be more readable (e.g., 2026-02-25 15:30)
        formatted_time = timestamp[:16].replace("T", " ")
        print(f"{id:<4} | {formatted_time:<20} | {ticker:<8} | {alert_type:<10} | {price:<10.2f} | {value:<10.2f}")
        
    print(f"{'='*75}\n")

if __name__ == "__main__":
    show_all_alerts()
