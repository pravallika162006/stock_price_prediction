# Stock Price Prediction Dashboard

A Streamlit-based stock price prediction dashboard that uses historical stock data and a simple machine learning model to estimate the next closing price. This project is designed as a student-level stock prediction system with a polished UI and interactive dashboard.

## Features

- Company name dropdown with internal ticker mapping
- Historical data fetch via Yahoo Finance
- Machine learning prediction using multiple linear regression
- Interactive Plotly candlestick chart with volume
- Metric cards for current price, predicted price, and model accuracy
- Tabs for charts, prediction summary, and dataset
- Dark theme styling and professional dashboard layout

## Files

- `app.py` - Streamlit app entrypoint
- `data_fetcher.py` - Fetches stock data from Yahoo Finance
- `model.py` - Trains the regression model and predicts next-day price
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Requirements

- Python 3.8+
- Streamlit
- yfinance
- pandas
- scikit-learn
- plotly

## Setup

1. Create a Python virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python -m streamlit run app.py
```

4. Open the URL shown by Streamlit in your browser (usually `http://localhost:8501`).

## Usage

1. Select a company from the dropdown.
2. Optionally enter a custom ticker.
3. Select the historical data period.
4. Click **Fetch and Predict**.
5. View the prediction summary, candlestick chart, and dataset.

## Notes

- This is a demonstration project and should not be used for live trading or investment decisions.
- The model is a basic linear regression model intended for learning and experimentation.

## License

This project is provided as-is for educational purposes.
