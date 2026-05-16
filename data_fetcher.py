import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker, period="1y"):
    """
    Fetches stock data from Yahoo Finance for a given ticker and period.
    Returns a dataframe with Date, Open, High, Low, Close, and Volume.
    Handles invalid ticker errors.
    """
    try:
        stock_data = yf.download(ticker, period=period)
        
        if stock_data.empty:
            return None
            
        # Flatten MultiIndex columns if they exist (yfinance >= 0.2.40)
        if isinstance(stock_data.columns, pd.MultiIndex):
            stock_data.columns = [col[0] if isinstance(col, tuple) else col for col in stock_data.columns]
            
        # Reset index to make Date a column
        stock_data.reset_index(inplace=True)
        
        # Keep relevant columns
        columns_to_keep = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = stock_data[columns_to_keep].copy()
        df['Date'] = pd.to_datetime(df['Date']).dt.date # Keep just the date part for clean UI
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
