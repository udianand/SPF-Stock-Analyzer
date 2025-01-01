import streamlit as st
import pandas as pd
import logging
import plotly.express as px
from technicals import render as technicals_render
from research import render as research_render
from home import render as home_render

# Set up logging
logging.basicConfig(level=logging.INFO)

# Apps title and description
st.title("SPF Stock Market Dashboard")
st.write(
    "This is a stock market dashboard that allows you to view the stock market data for a given ticker symbol."
)

# Add user inputs to sidebar
st.sidebar.header("User Inputs")
tickerSymbol = st.sidebar.text_input(
    "Enter a ticker symbol eg AAPL, MSFT, TSLA", ).upper()
if tickerSymbol and not tickerSymbol.isalpha():
    st.sidebar.error("Please enter a valid ticker symbol (letters only)")
    tickerSymbol = None
start_date = st.sidebar.date_input("Start Date", pd.to_datetime('2020-01-01'))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# Tabs for Technicals and Research
tab1, tab2, tab3 = st.tabs(["Home","Technicals", "Research"])
with tab1:
    home_render(tickerSymbol, start_date, end_date)
with tab2:
    technicals_render(tickerSymbol, start_date, end_date)
with tab3:
    research_render(tickerSymbol)
