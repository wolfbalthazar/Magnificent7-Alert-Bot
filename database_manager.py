import sqlite3
from datetime import datetime, timedelta
import os

DB_NAME = "alerts.db"

def init_db():
    """
    Initializes the database table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create table for alerts
    # We store:
    # - ticker: The stock symbol (e.g. AAPL)
    # - alert_type: 'RSI' or 'MA_CROSS'
    # - price: The price at the time of alert
    # - value: The indicator value (e.g. RSI=28.5)
    # - timestamp: When it happened
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            price REAL,
            value REAL,
            timestamp TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database {DB_NAME} initialized/checked.")

def log_alert(ticker: str, alert_type: str, price: float, value: float):
    """
    Saves a new alert to the database.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    cursor.execute('''
        INSERT INTO alerts (ticker, alert_type, price, value, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (ticker, alert_type, price, value, timestamp))
    
    conn.commit()
    conn.close()
    print(f"Logged alert to DB: {ticker} - {alert_type}")

def is_duplicate(ticker: str, alert_type: str, hours: int = 24) -> bool:
    """
    Checks if an alert of the same type for the same ticker exists within the last X hours.
    Returns: True if duplicate found (should NOT send email), False otherwise.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Calculate the cutoff time
    cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
    
    cursor.execute('''
        SELECT id FROM alerts 
        WHERE ticker = ? AND alert_type = ? AND timestamp > ?
    ''', (ticker, alert_type, cutoff_time))
    
    result = cursor.fetchone()
    conn.close()
    
    return result is not None
