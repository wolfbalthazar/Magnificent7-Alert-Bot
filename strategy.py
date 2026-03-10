import pandas as pd

def check_rsi_alert(df: pd.DataFrame, threshold: int = 30) -> bool:
    """
    Checks if the most recently closed candle's RSI is below the threshold.
    
    Args:
        df (pd.DataFrame): DataFrame containing 'RSI_14' column.
        threshold (int): The RSI threshold (default 30).
        
    Returns:
        bool: True if RSI is below threshold, False otherwise.
    """
    if 'RSI_14' not in df.columns or len(df) < 2:
        return False
        
    # We look at the last completed row (index -1)
    last_rsi = df['RSI_14'].iloc[-1]
    
    return last_rsi < threshold

def check_ma_crossover(df: pd.DataFrame, fast_col: str = 'MA_20', slow_col: str = 'MA_50') -> bool:
    """
    Checks if the fast moving average has crossed the slow moving average upwards on the last closed candle.
    (Golden Cross)
    
    Args:
        df (pd.DataFrame): DataFrame containing the fast and slow MA columns.
        fast_col (str): The column name of the fast MA.
        slow_col (str): The column name of the slow MA.
        
    Returns:
        bool: True if crossed upwards, False otherwise.
    """
    if fast_col not in df.columns or slow_col not in df.columns or len(df) < 2:
        return False
        
    # We need the last two rows to check for a crossover
    prev_fast = df[fast_col].iloc[-2]
    prev_slow = df[slow_col].iloc[-2]
    
    curr_fast = df[fast_col].iloc[-1]
    curr_slow = df[slow_col].iloc[-1]
    
    # Previous: Fast was below or equal to Slow
    # Current: Fast is strictly above Slow
    has_crossed_upwards = (prev_fast <= prev_slow) and (curr_fast > curr_slow)
    
    return has_crossed_upwards

if __name__ == "__main__":
    # Test script locally
    # Create simple mock data for RSI
    df_rsi_test = pd.DataFrame({'RSI_14': [40, 35, 29]})
    print(f"RSI < 30 alert should be True: {check_rsi_alert(df_rsi_test, 30)}")
    
    # Create mock data for MA Crossover
    df_ma_test = pd.DataFrame({
        'MA_20': [100, 105], # Fast crossover
        'MA_50': [102, 103]  # Slow moving
    })
    print(f"MA Crossover alert should be True: {check_ma_crossover(df_ma_test)}")
