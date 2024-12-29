import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from utils import get_stock_data
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Apps title and description
st.title("SPF Stock Market Dashboard")
st.write("This is a stock market dashboard that allows you to view the stock market data for a given ticker symbol.")

# Add user inputs
tickerSymbol = st.text_input("Enter a ticker symbol eg AAPL, MSFT, TSLA", )
start_date = st.date_input("Start Date",pd.to_datetime('2020-01-01'))
end_date = st.date_input("End Date", pd.to_datetime("today"))

print(start_date)
print(end_date)
# Fetch and display data
if st.button("Get Data"):
  with st.spinner("Fetching data..."):
      try:
          hist_data, stock_info = get_stock_data(tickerSymbol, start_date, end_date)

          if hist_data is not None and stock_info is not None:
              # Stock info header
              st.subheader(f"{stock_info.get('longName', tickerSymbol)} ({tickerSymbol})")
              st.markdown(f"**Sector:** {stock_info.get('sector', 'N/A')} | **Industry:** {stock_info.get('industry', 'N/A')}")
              st.markdown(f"**RecommendationKey:** {stock_info.get('recommendationKey', 'N/A')} | **Currency:** {stock_info.get('currency', 'N/A')}")
              #st.write(stock_info.calendar)
              #st.write(stock_info.analyst_price_targets)
              st.write(hist_data)
      except Exception as e:
        st.error("Error fetching data. Please check the ticker and try again.")



  