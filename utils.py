import yfinance as yf
import logging
import finnhub
from datetime import datetime,timedelta
import streamlit as st

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_stock_data(symbol, start_date, end_date):
    """
    Fetch stock data from Yahoo Finance
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)
        return hist, stock.info
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return None, None

@st.cache_data
def get_company_news(tickerSymbol, start_date=None, end_date=None):
    """
    Fetch company news from FinnHub
    """
    try:
        if tickerSymbol:

            finhub_api_key = st.secrets["FINNHUB_API_KEY"]
            finnhub_client = finnhub.Client(api_key=finhub_api_key)
            
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y-%m-%d')

            return finnhub_client.company_news(tickerSymbol, _from=start_date, to=end_date)
    except Exception as e:
        logger.error(f"Error fetching company news: {str(e)}")
        return None, None