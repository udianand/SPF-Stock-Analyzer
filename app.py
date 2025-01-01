import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from utils import get_stock_data
import logging
import plotly.express as px
from tabs import technicals,research

import finnhub
import os 

# Set up logging
logging.basicConfig(level=logging.INFO)

# Apps title and description
st.title("SPF Stock Market Dashboard")
st.write("This is a stock market dashboard that allows you to view the stock market data for a given ticker symbol.")

# Add user inputs to sidebar
st.sidebar.header("User Inputs")
tickerSymbol = st.sidebar.text_input("Enter a ticker symbol eg AAPL, MSFT, TSLA", )
start_date = st.sidebar.date_input("Start Date",pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Tabs for Technicals and Research
tab1, tab2 = st.tabs(["Technicals", "Research"])
with tab1:
    technicals.render(tickerSymbol, start_date, end_date)
