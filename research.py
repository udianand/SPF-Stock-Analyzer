import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import finnhub

def render(tickerSymbol):
    st.header("Research")

    if tickerSymbol:
        with st.spinner("Fetching research data..."):
            try:
                # FINNHUB Recommendation Trends
                fiinhub_api_key = st.secrets["FINNHUB_API_KEY"]
                finnhub_client = finnhub.Client(api_key=fiinhub_api_key)
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
                
                # Get historical recommendations (last 3 months)
                recommendations = finnhub_client.recommendation_trends(tickerSymbol)[:3]
                
                # Prepare data for time series chart
                periods = [rec['period'] for rec in recommendations]
                strong_buy = [rec['strongBuy'] for rec in recommendations]
                buy = [rec['buy'] for rec in recommendations]
                hold = [rec['hold'] for rec in recommendations]
                sell = [rec['sell'] for rec in recommendations]
                strong_sell = [rec['strongSell'] for rec in recommendations]

                # Create stacked bar chart
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Strong Buy', x=periods, y=strong_buy, marker_color='#1A7F37'))
                fig.add_trace(go.Bar(name='Buy', x=periods, y=buy, marker_color='#2DA44E'))
                fig.add_trace(go.Bar(name='Hold', x=periods, y=hold, marker_color='#6E7781'))
                fig.add_trace(go.Bar(name='Sell', x=periods, y=sell, marker_color='#CF222E'))
                fig.add_trace(go.Bar(name='Strong Sell', x=periods, y=strong_sell, marker_color='#A40E26'))

                fig.update_layout(
                    barmode='stack',
                    title=f'Recommendation Trends for {tickerSymbol}',
                    xaxis_title='Period',
                    yaxis_title='Number of Recommendations',
                    height=500,
                    showlegend=True,
                    legend={'traceorder': 'reversed'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display latest recommendations as metrics
                st.subheader("Latest Recommendations")
                latest = recommendations[0]
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Strong Buy", latest['strongBuy'])
                with col2:
                    st.metric("Buy", latest['buy'])
                with col3:
                    st.metric("Hold", latest['hold'])
                with col4:
                    st.metric("Sell", latest['sell'])
                with col5:
                    st.metric("Strong Sell", latest['strongSell'])

            except Exception as e:
                st.error("Error fetching research data.: " + str(e))
