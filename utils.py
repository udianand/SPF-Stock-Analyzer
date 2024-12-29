
import finnhub
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_stock_data(symbol, start_date, end_date):
    """
    Fetch stock data from Finnhub
    """
    try:
        # Initialize Finnhub client
        finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
        
        # Convert dates to UNIX timestamps
        start_timestamp = int(pd.Timestamp(start_date).timestamp())
        end_timestamp = int(pd.Timestamp(end_date).timestamp())
        
        # Get stock candles
        data = finnhub_client.stock_candles(symbol, 'D', start_timestamp, end_timestamp)
        
        if data['s'] == 'no_data':
            logger.error("No data found for the symbol")
            return None, None
            
        # Convert to pandas DataFrame
        df = pd.DataFrame({
            'Open': data['o'],
            'High': data['h'],
            'Low': data['l'],
            'Close': data['c'],
            'Volume': data['v']
        }, index=pd.to_datetime(data['t'], unit='s'))
        
        # Get company profile
        company_info = finnhub_client.company_profile2(symbol=symbol)
        
        return df, company_info
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return None, None
