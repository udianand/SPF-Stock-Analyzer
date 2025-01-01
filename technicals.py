
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from utils import get_stock_data

def calculate_rsi(data, periods=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def render(tickerSymbol, start_date, end_date):
    st.header("Technical Analysis")

    if tickerSymbol:
        with st.spinner("Fetching historical data..."):
            try:
                hist_data, stock_info = get_stock_data(tickerSymbol, start_date, end_date)
                
                if hist_data is not None:
                    # Calculate technical indicators
                    hist_data["SMA_20"] = hist_data["Close"].rolling(window=20).mean()
                    hist_data["SMA_50"] = hist_data["Close"].rolling(window=50).mean()
                    hist_data["SMA_200"] = hist_data["Close"].rolling(window=200).mean()
                    hist_data["RSI"] = calculate_rsi(hist_data["Close"])
                    hist_data["Volume_MA"] = hist_data["Volume"].rolling(window=20).mean()

                    # Create main price chart with volume
                    fig = make_subplots(rows=3, cols=1, 
                                      shared_xaxes=True,
                                      vertical_spacing=0.05,
                                      row_heights=[0.5, 0.25, 0.25])

                    # Candlestick chart
                    fig.add_trace(go.Candlestick(
                        x=hist_data.index,
                        open=hist_data['Open'],
                        high=hist_data['High'],
                        low=hist_data['Low'],
                        close=hist_data['Close'],
                        name='OHLC'
                    ), row=1, col=1)

                    # Add Moving Averages
                    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['SMA_20'],
                                           name='SMA 20', line=dict(color='blue')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['SMA_50'],
                                           name='SMA 50', line=dict(color='orange')), row=1, col=1)
                    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['SMA_200'],
                                           name='SMA 200', line=dict(color='red')), row=1, col=1)

                    # Volume chart
                    fig.add_trace(go.Bar(x=hist_data.index, y=hist_data['Volume'],
                                       name='Volume'), row=2, col=1)
                    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['Volume_MA'],
                                           name='Volume MA', line=dict(color='orange')), row=2, col=1)

                    # RSI
                    fig.add_trace(go.Scatter(x=hist_data.index, y=hist_data['RSI'],
                                           name='RSI', line=dict(color='purple')), row=3, col=1)
                    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
                    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

                    # Update layout
                    fig.update_layout(
                        title=f'{tickerSymbol} Technical Analysis',
                        yaxis_title='Price (USD)',
                        yaxis2_title='Volume',
                        yaxis3_title='RSI',
                        height=800,
                        showlegend=True,
                        xaxis_rangeslider_visible=False
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    
                else:
                    st.warning("No data available for the selected ticker.")
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
