
import streamlit as st
import plotly.graph_objects as go
from utils import get_stock_data, get_company_news
from datetime import datetime

def render(tickerSymbol, start_date, end_date):
    if tickerSymbol:
        hist_data, stock_info = get_stock_data(tickerSymbol, start_date, end_date)
        
        if hist_data is not None and stock_info is not None:
            # Main header with company info
            st.title(f"{stock_info.get('longName', tickerSymbol)} ({tickerSymbol})")
            
            # Company metadata in a container
            with st.container():
                st.subheader("Company Information")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Industry", stock_info.get('industry', 'N/A'))
                    st.metric("Market Cap", f"${stock_info.get('marketCap', 0)/1e9:.2f}B")
                with col2:
                    st.metric("Sector", stock_info.get('sector', 'N/A'))
                    current_price = hist_data['Close'][-1]
                    price_change = ((current_price - hist_data['Close'][0]) / hist_data['Close'][0]) * 100
                    st.metric("Price", f"${current_price:.2f}", f"{price_change:.2f}%")
            
            # Price chart in its own container
            with st.container():
                st.subheader("Price History")
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=hist_data.index,
                    y=hist_data['Close'],
                    name='Close Price',
                    line=dict(color='#26A69A', width=2)
                ))
                
                fig.update_layout(
                    yaxis_title='Price (USD)',
                    xaxis_title='Date',
                    height=500,
                    showlegend=True,
                    plot_bgcolor='white',
                    margin=dict(t=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # News section with expander
            with st.expander("Latest Company News", expanded=True):
                news = get_company_news(tickerSymbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                
                if news:
                    for idx, article in enumerate(news[:5]):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{article['headline']}**")
                            st.write(article['summary'])
                        with col2:
                            st.write(f"Source: {article['source']}")
                            st.write(datetime.fromtimestamp(article['datetime']).strftime('%Y-%m-%d'))
                            if article['url']:
                                st.markdown(f"[Read more]({article['url']})")
                        if idx < 4:  # Don't add separator after last item
                            st.divider()
                else:
                    st.info("No recent news available for this company")
        else:
            st.warning("No data available for the selected ticker.")
    else:
        st.header("Welcome to Stock Analysis")
        st.write("Please select a stock symbol to begin analysis.")
