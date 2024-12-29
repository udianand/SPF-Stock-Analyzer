import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from utils import get_stock_data
import logging
import plotly.express as px

import finnhub
import os 

# Set up logging
logging.basicConfig(level=logging.INFO)

# Apps title and description
st.title("SPF Stock Market Dashboard")
st.write("This is a stock market dashboard that allows you to view the stock market data for a given ticker symbol.")

# Add user inputs
tickerSymbol = st.text_input("Enter a ticker symbol eg AAPL, MSFT, TSLA", )
start_date = st.date_input("Start Date",pd.to_datetime('2020-01-01'))
end_date = st.date_input("End Date", pd.to_datetime("today"))

# TODO: Move to button with get data
# FINNHUB RECO TEST
fiinhub_api_key  = os.environ['FINNHUB_API_KEY']
finnhub_client = finnhub.Client(api_key = fiinhub_api_key)
latest_recommendation = finnhub_client.recommendation_trends('NVDA')[0]
latest_period = latest_recommendation['period']
# Prepare data for the bar chart
data = {
    "Category": ["Buy", "Hold", "Sell", "Stong Buy", "Strong Sell"],
    "Values": [
        latest_recommendation["buy"],
        latest_recommendation["hold"],
        latest_recommendation["sell"],
        latest_recommendation["strongBuy"],
        latest_recommendation["strongSell"]
    ]
}

# Convert to DataFrame for visualization
df = pd.DataFrame(data)

# Streamlit bar chart
# Plotly bar chart with automatic color assignment
fig = px.bar(
    df,
    x="Category",
    y="Values",
    title="Stock Recommendation Analysis for " + latest_recommendation["period"],
    color="Category",  # Automatically assigns a distinct color to each category
    labels={"Values": "Number of Recommendations", "Category": "Recommendation Type"}
)

# Display the chart in Streamlit
st.plotly_chart(fig)


# Fetch and display data
if st.button("Get Data"):
  with st.spinner("Fetching data..."):
      try:
          hist_data, stock_info = get_stock_data(tickerSymbol, start_date, end_date)

          if hist_data is not None and stock_info is not None:
              # Stock info header
              st.subheader(f"{stock_info.get('longName', tickerSymbol)} ({tickerSymbol})")
              st.markdown(f"**Sector:** {stock_info.get('sector', 'N/A')} | **Industry:** {stock_info.get('industry', 'N/A')}")
              
              #st.write(stock_info.calendar)
              #st.write(stock_info.analyst_price_targets)
              # st.write(hist_data)
      except Exception as e:
        st.error("Error fetching data. Please check the ticker and try again.")



  