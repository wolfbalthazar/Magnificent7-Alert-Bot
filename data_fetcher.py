import yfinance as yf
import pandas as pd
from typing import Optional, Dict

def get_historical_data(ticker: str, interval: str = "30m", period: str = "1mo") -> Optional[pd.DataFrame]:
    """
    Downloads historical data for a given ticker and timeframe using yfinance.

    Args:
        ticker (str): The stock symbol (e.g., 'AAPL').
        interval (str): The timeframe for candles (e.g., '30m', '1h', '1d').
        period (str): The lookback period (e.g., '1mo', '60d').

    Returns:
        pd.DataFrame or None: A pandas dataframe containing the OHLCV data, or None if download fails.
    """
    try:
        # yfinance creates an internally cached ticker object
        stock = yf.Ticker(ticker)
        
        # Download historical data
        df = stock.history(period=period, interval=interval)
        
        # Clean dataframe (remove extra multi-level index columns if any and ensure timezone consistency if needed)
        # Check if the dataframe is empty
        if df.empty:
            print(f"Warning: No data found for ticker {ticker} with interval {interval} and period {period}.")
            return None
            
        return df
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

if __name__ == "__main__":
    # Test script locally
    df = get_historical_data("AAPL", interval="1m", period="7d")
    if df is not None:
        print("Successfully fetched data for AAPL.")
        print(df.tail())
