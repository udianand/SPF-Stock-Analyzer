
import streamlit as st
import plotly.graph_objects as go
from utils import get_stock_data

def render(tickerSymbol, start_date, end_date):
    if tickerSymbol:
        hist_data, stock_info = get_stock_data(tickerSymbol, start_date, end_date)
        
        if hist_data is not None and stock_info is not None:
            # Display stock info
            st.header(f"{stock_info.get('longName', tickerSymbol)} ({tickerSymbol})")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Industry", stock_info.get('industry', 'N/A'))
            with col2:
                st.metric("Sector", stock_info.get('sector', 'N/A'))
            
            # Display price metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                current_price = hist_data['Close'][-1]
                st.metric("Current Price", f"${current_price:.2f}")
            with col2:
                market_cap = stock_info.get('marketCap', 0)
                market_cap_b = market_cap / 1e9 if market_cap else 0
                st.metric("Market Cap", f"${market_cap_b:.2f}B")
            with col3:
                price_change = ((current_price - hist_data['Close'][0]) / hist_data['Close'][0]) * 100
                st.metric("Price Change", f"{price_change:.2f}%")

            # Create price chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist_data.index,
                y=hist_data['Close'],
                name='Close Price',
                line=dict(color='blue')
            ))
            
            fig.update_layout(
                title=f"{tickerSymbol} Historical Price",
                yaxis_title='Price (USD)',
                xaxis_title='Date',
                height=500,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected ticker.")
    else:
        st.header("Welcome to Stock Analysis")
        st.write("Please select a stock symbol to begin analysis.")
