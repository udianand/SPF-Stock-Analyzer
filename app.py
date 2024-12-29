import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from utils import get_stock_data
import logging

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

# FINNHUB RECO TEST
fiinhub_api_key  = os.environ['FINNHUB_API_KEY']
finnhub_client = finnhub.Client(api_key = fiinhub_api_key)
latest_recommendation = finnhub_client.recommendation_trends('AAPL')[0]
latest_buy = latest_recommendation['buy']
latest_hold = latest_recommendation['hold']
latest_sell = latest_recommendation['sell']
latest_strong_buy = latest_recommendation['strongBuy']
latest_strong_sell = latest_recommendation['strongSell']
latest_period = latest_recommendation['period']

# Create recommendation bar chart
fig, ax = plt.subplots(figsize=(10, 6))
recommendations = ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']
values = [latest_strong_buy, latest_buy, latest_hold, latest_sell, latest_strong_sell]

ax.bar(recommendations, values)
ax.set_title(f'Analyst Recommendations ({latest_period})')
ax.set_ylabel('Number of Analysts')
plt.xticks(rotation=45)

# Display the chart in Streamlit
st.subheader("Analyst Recommendations")
st.pyplot(fig)
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



  