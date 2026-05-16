import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_fetcher import fetch_stock_data
from model import train_and_predict

st.set_page_config(page_title="Stock Price Prediction Dashboard", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #0E1117;
    }
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .css-18e3th9 {
        background-color: #0E1117;
    }
    h1, h2, h3, h4 {
        color: #00ADB5;
    }
    .stButton>button {
        background-color: #00ADB5;
        color: #0E1117;
    }
    .stProgress>div>div {
        background-color: #00ADB5;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 style='text-align: center; color: #00ADB5;'>
    📈 Stock Price Prediction Dashboard
    </h1>
    <h4 style='text-align: center; color: gray;'>
    Analyze stock trends and predict future prices using Machine Learning
    </h4>
    """,
    unsafe_allow_html=True,
)

stocks = {
    # US TECH
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Tesla": "TSLA",
    "Netflix": "NFLX",
    "Nvidia": "NVDA",
    "Intel": "INTC",
    "AMD": "AMD",
    "Adobe": "ADBE",
    "Oracle": "ORCL",
    "Cisco": "CSCO",
    "IBM": "IBM",
    "Salesforce": "CRM",
    "Uber": "UBER",
    "Airbnb": "ABNB",
    "PayPal": "PYPL",
    "Spotify": "SPOT",
    "Snap": "SNAP",

    # US FINANCE
    "JPMorgan Chase": "JPM",
    "Goldman Sachs": "GS",
    "Bank of America": "BAC",
    "Morgan Stanley": "MS",
    "Visa": "V",
    "Mastercard": "MA",
    "American Express": "AXP",

    # US CONSUMER
    "Coca Cola": "KO",
    "PepsiCo": "PEP",
    "McDonald's": "MCD",
    "Starbucks": "SBUX",
    "Walmart": "WMT",
    "Costco": "COST",
    "Nike": "NKE",
    "Disney": "DIS",

    # US HEALTHCARE
    "Pfizer": "PFE",
    "Johnson & Johnson": "JNJ",
    "Moderna": "MRNA",

    # US AUTOMOBILE
    "Ford": "F",
    "General Motors": "GM",

    # INDIA IT
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "Wipro": "WIPRO.NS",
    "HCL Technologies": "HCLTECH.NS",
    "Tech Mahindra": "TECHM.NS",
    "LTIMindtree": "LTIM.NS",

    # INDIA BANKS
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Axis Bank": "AXISBANK.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "IndusInd Bank": "INDUSINDBK.NS",

    # INDIA ENERGY
    "Reliance Industries": "RELIANCE.NS",
    "ONGC": "ONGC.NS",
    "Indian Oil": "IOC.NS",
    "BPCL": "BPCL.NS",
    "GAIL": "GAIL.NS",

    # INDIA FMCG
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ITC": "ITC.NS",
    "Nestle India": "NESTLEIND.NS",
    "Dabur": "DABUR.NS",
    "Britannia": "BRITANNIA.NS",

    # INDIA AUTOMOBILE
    "Maruti Suzuki": "MARUTI.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",

    # INDIA PHARMA
    "Sun Pharma": "SUNPHARMA.NS",
    "Dr Reddy's": "DRREDDY.NS",
    "Cipla": "CIPLA.NS",
    "Divi's Laboratories": "DIVISLAB.NS",

    # INDIA ADANI GROUP
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Adani Power": "ADANIPOWER.NS",

    # INDIA TATA GROUP
    "Tata Steel": "TATASTEEL.NS",
    "Titan": "TITAN.NS",
    "Tata Consumer": "TATACONSUM.NS",
    "Trent": "TRENT.NS",

    # TELECOM
    "Bharti Airtel": "BHARTIARTL.NS",
    "Vodafone Idea": "IDEA.NS",

    # CRYPTO
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Dogecoin": "DOGE-USD",
    "Solana": "SOL-USD",

    # INDICES
    "Nifty 50": "^NSEI",
    "Sensex": "^BSESN",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI"
}

logo_urls = {
    "Apple": "https://logo.clearbit.com/apple.com",
    "Microsoft": "https://logo.clearbit.com/microsoft.com",
    "Google": "https://logo.clearbit.com/google.com",
    "Amazon": "https://logo.clearbit.com/amazon.com",
    "Meta": "https://logo.clearbit.com/meta.com",
    "Tesla": "https://logo.clearbit.com/tesla.com",
    "Netflix": "https://logo.clearbit.com/netflix.com",
    "Nvidia": "https://logo.clearbit.com/nvidia.com",
    "Intel": "https://logo.clearbit.com/intel.com",
    "Adobe": "https://logo.clearbit.com/adobe.com",
    "TCS": "https://logo.clearbit.com/tcs.com",
    "Infosys": "https://logo.clearbit.com/infosys.com",
    "Reliance Industries": "https://logo.clearbit.com/relianceindustries.com"
}

st.subheader("🔍 Selection & Period")
col_input1, col_input2, col_input3 = st.columns([2, 2, 1])

with col_input1:
    company = st.selectbox("Search Company", list(stocks.keys()), index=0)
    ticker = stocks[company]
    st.write(f"Selected Ticker: **{ticker}**")

    use_custom = st.checkbox("Use custom ticker instead", value=False)
    if use_custom:
        ticker = st.text_input("Enter Custom Ticker (e.g., BTC-USD)", ticker).upper()

with col_input2:
    period_options = {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y",
        "5 Years": "5y"
    }
    selected_period_label = st.selectbox("Select Historical Data Period:", list(period_options.keys()), index=3)
    period_value = period_options[selected_period_label]

with col_input3:
    st.write("")
    st.write("")
    fetch_button = st.button("Fetch and Predict", type="primary", use_container_width=True)

st.markdown("---")

if fetch_button:
    progress = st.progress(0)
    with st.spinner("Fetching stock data..."):
        progress.progress(10)
        df = fetch_stock_data(ticker, period_value)
        progress.progress(40)

    if df is None or df.empty:
        progress.progress(0)
        st.error(f"Invalid ticker '{ticker}' or no data found. Please try another ticker.")
        st.stop()

    st.success("Data fetched successfully!")
    progress.progress(60)

    with st.spinner("Training Machine Learning Model..."):
        predicted_price, last_close, metrics = train_and_predict(df)
        progress.progress(80)

    current_price = float(last_close)
    price_diff = predicted_price - current_price
    accuracy = metrics['R2'] * 100
    mae = metrics['MAE']
    progress.progress(100)

    card1, card2, card3 = st.columns(3)
    card1.metric("Current Price", f"${current_price:.2f}")
    card2.metric("Predicted Price", f"${predicted_price:.2f}", f"{price_diff:+.2f}")
    card3.metric("Model Accuracy", f"{accuracy:.2f}%")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Charts", "📈 Prediction", "📁 Dataset"])

    with tab1:
        st.subheader("Candlestick Chart & Volume")
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.7, 0.3])
        fig.add_trace(
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                x=df['Date'],
                y=df['Volume'],
                marker_color='#00ADB5',
                name='Volume'
            ),
            row=2,
            col=1,
        )
        fig.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            height=700,
            margin=dict(l=0, r=0, t=40, b=0),
            showlegend=False,
        )
        fig.update_xaxes(rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Prediction Summary")
        st.info(
            f"""
Company: {company}

Ticker: {ticker}

Current Price: ${current_price:.2f}

Predicted Price: ${predicted_price:.2f}
"""
        )
        if predicted_price > current_price:
            st.success("📈 Stock price may increase tomorrow")
        else:
            st.error("📉 Stock price may decrease tomorrow")

        st.write(
            f"Based on today's Open, High, Low, Close, and Volume, the model predicts the next closing price will be **${predicted_price:.2f}**."
        )
        st.write("---")
        st.write(
            f"**Mean Absolute Error (MAE):** ${mae:.2f}  \
**R² Score:** {accuracy:.2f}%"
        )
        st.progress(int(min(max(accuracy, 0), 100)))

    with tab3:
        st.subheader("Historical Dataset")
        st.dataframe(df.set_index('Date'), height=500)
else:
    st.info("👈 Select a company, choose a period, then click 'Fetch and Predict' to launch the dashboard.")
