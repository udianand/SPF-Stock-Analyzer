import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import logging



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


