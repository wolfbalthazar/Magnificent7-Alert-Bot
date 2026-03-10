import sqlite3
import os

DB_NAME = "alerts.db"

def show_all_alerts():
    """
    Kiolvassa és formázva kiírja az eddigi összes riasztást az adatbázisból.
    """
    if not os.path.exists(DB_NAME):
        print(f"Az adatbázis ({DB_NAME}) még nem létezik. Futtasd előbb a main.py-t!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Lekérjük az összes adatot a táblából
    cursor.execute("SELECT id, ticker, alert_type, price, value, timestamp FROM alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    
    conn.close()
    
    if not rows:
        print("Az adatbázis üres. Még nem rögzítettünk egyetlen riasztást sem.")
        return
        
    print(f"\n{'='*75}")
    print(f"{'ÖSSZES KIKÜLDÖTT RIASZTÁS (Legfrissebbek elöl)':^75}")
    print(f"{'='*75}")
    print(f"{'ID':<4} | {'Dátum és Idő':<20} | {'Ticker':<8} | {'Típus':<10} | {'Ár ($)':<10} | {'Érték/MA':<10}")
    print(f"{'-'*75}")
    
    for row in rows:
        id, ticker, alert_type, price, value, timestamp = row
        # A timestamp formázása olvashatóbbra (pl. 2026-02-25 15:30)
        formatted_time = timestamp[:16].replace("T", " ")
        print(f"{id:<4} | {formatted_time:<20} | {ticker:<8} | {alert_type:<10} | {price:<10.2f} | {value:<10.2f}")
        
    print(f"{'='*75}\n")

if __name__ == "__main__":
    show_all_alerts()
