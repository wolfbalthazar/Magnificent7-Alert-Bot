import pandas as pd
import ta

def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculates the Relative Strength Index (RSI) for the given DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing at least a 'Close' column.
        period (int): The lookback period for RSI calculation.
        
    Returns:
        pd.DataFrame: Original DataFrame with an additional 'RSI_{period}' column.
    """
    # Create the RSI indicator object using TA library
    rsi_indicator = ta.momentum.RSIIndicator(close=df['Close'], window=period)
    
    # Add the RSI values as a new column
    df[f'RSI_{period}'] = rsi_indicator.rsi()
    
    return df

def calculate_moving_averages(df: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.DataFrame:
    """
    Calculates the Fast and Slow Simple Moving Averages.
    
    Args:
        df (pd.DataFrame): DataFrame containing at least a 'Close' column.
        fast (int): The lookback period for the fast MA.
        slow (int): The lookback period for the slow MA.
        
    Returns:
        pd.DataFrame: Original DataFrame with additional 'MA_{fast}' and 'MA_{slow}' columns.
    """
    # Calculate simple moving averages
    sma_fast = ta.trend.SMAIndicator(close=df['Close'], window=fast)
    sma_slow = ta.trend.SMAIndicator(close=df['Close'], window=slow)
    
    # Add columns
    df[f'MA_{fast}'] = sma_fast.sma_indicator()
    df[f'MA_{slow}'] = sma_slow.sma_indicator()
    
    return df

if __name__ == "__main__":
    # Test script locally with mocked data
    import numpy as np
    
    # Generate mock price data
    np.random.seed(42)
    prices = np.random.normal(100, 5, 100).cumsum()
    df_test = pd.DataFrame({'Close': prices})
    
    # Apply indicators
    df_test = calculate_rsi(df_test, period=14)
    df_test = calculate_moving_averages(df_test, fast=5, slow=10) # Using smaller periods for quick test
    
    print("Test Indicator calculations:")
    print(df_test.tail(10))
