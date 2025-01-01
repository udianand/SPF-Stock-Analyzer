import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils import get_stock_data

def render(tickerSymbol, start_date, end_date):
    st.header("Technical Analysis")

    if tickerSymbol:
        with st.spinner("Fetching historical data..."):
            try:
                # Fetch historical stock data
                hist_data, stock_info = get_stock_data(tickerSymbol, start_date, end_date)

                if hist_data is not None:
                    # Display price chart
                    st.subheader(f"Price Chart for {tickerSymbol}")
                    fig, ax = plt.subplots()
                    hist_data['Close'].plot(ax=ax, title=f"{tickerSymbol} Price Chart", legend=True)
                    ax.set_ylabel("Price (in USD)")
                    st.pyplot(fig)

                    # Display moving averages
                    st.subheader("Moving Averages")
                    hist_data["SMA_50"] = hist_data["Close"].rolling(window=50).mean()
                    hist_data["SMA_200"] = hist_data["Close"].rolling(window=200).mean()
                    st.line_chart(hist_data[["Close", "SMA_50", "SMA_200"]])
                else:
                    st.warning("No data available for the selected ticker.")
            except Exception as e:
                st.error("Error fetching data. Please check the ticker and try again.")
