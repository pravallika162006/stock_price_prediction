import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

def train_and_predict(df):
    """
    Uses previous day's Open, High, Low, Close, and Volume to predict the next day's Close price.
    Returns the predicted price, last closing price, and model evaluation metrics.
    """
    df = df.copy()
    
    # Create features using the previous day's data
    df['Prev_Open'] = df['Open'].shift(1)
    df['Prev_High'] = df['High'].shift(1)
    df['Prev_Low'] = df['Low'].shift(1)
    df['Prev_Close'] = df['Close'].shift(1)
    df['Prev_Volume'] = df['Volume'].shift(1)
    
    # Drop the first row which will have NaN for shifted columns
    df = df.dropna()
    
    # Define features (X) and target (y)
    features = ['Prev_Open', 'Prev_High', 'Prev_Low', 'Prev_Close', 'Prev_Volume']
    X = df[features]
    y = df['Close']
    
    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Predict the next day's stock price
    # The features for tomorrow are today's actual data
    last_row = df.iloc[-1]
    last_close = last_row['Close']
    
    future_X = pd.DataFrame({
        'Prev_Open': [last_row['Open']],
        'Prev_High': [last_row['High']],
        'Prev_Low': [last_row['Low']],
        'Prev_Close': [last_row['Close']],
        'Prev_Volume': [last_row['Volume']]
    })
    
    predicted_next_day = model.predict(future_X)[0]
    
    metrics = {
        'MAE': mae,
        'R2': r2
    }
    
    return predicted_next_day, last_close, metrics
