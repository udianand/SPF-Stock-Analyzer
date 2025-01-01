import streamlit as st
import pandas as pd
import plotly.express as px
import finnhub
import os
import yfinance as yf

def render(tickerSymbol):
    st.header("Research")

    if tickerSymbol:
        with st.spinner("Fetching research data..."):
            try:
                # FINNHUB Recommendation Trends
                finhub_api_key = os.environ['FINNHUB_API_KEY']
                finnhub_client = finnhub.Client(api_key=finhub_api_key)
                latest_recommendation = finnhub_client.recommendation_trends(tickerSymbol)[0]
                latest_period = latest_recommendation['period']

                # Prepare data for the bar chart
                data = {
                    "Category": ["Buy", "Hold", "Sell", "Strong Buy", "Strong Sell"],
                    "Values": [
                        latest_recommendation["buy"],
                        latest_recommendation["hold"],
                        latest_recommendation["sell"],
                        latest_recommendation["strongBuy"],
                        latest_recommendation["strongSell"]
                    ]
                }
                df = pd.DataFrame(data)

                # Display recommendations
                st.subheader(f"Stock Recommendation Analysis for {tickerSymbol}")
                fig = px.bar(
                    df,
                    x="Category",
                    y="Values",
                    title=f"Recommendation Trends for {latest_period}",
                    color="Category",
                    labels={"Values": "Number of Recommendations", "Category": "Recommendation Type"}
                )
                st.plotly_chart(fig)
                
                # Display Key Statistics
                st.subheader("Key Statistics")
                stock = yf.Ticker(tickerSymbol)
                info = stock.info
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Market Cap", f"${info.get('marketCap', 'N/A'):,}")
                with col2:
                    st.metric("P/E Ratio", round(info.get('trailingPE', 0), 2))
                with col3:
                    st.metric("52 Week High", f"${info.get('fiftyTwoWeekHigh', 0):,.2f}")

            except Exception as e:
                st.error(f"Error fetching research data: {str(e)}")
