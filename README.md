
# Stock Market Dashboard

A web-based dashboard built with Streamlit that allows users to view and analyze stock market data.

## Features

- Real-time stock data retrieval using Yahoo Finance API
- Stock recommendations analysis using Finnhub API
- Interactive date range selection
- Visualization of stock recommendations with Plotly charts
- Company information display including sector and industry

## Requirements

- Python 3.11+
- Required packages are listed in pyproject.toml:
  - finnhub-python
  - matplotlib
  - numpy
  - pandas
  - streamlit
  - yfinance

## Usage

1. Enter a stock ticker symbol (e.g., AAPL, MSFT, TSLA)
2. Select date range for historical data
3. Click "Get Data" to fetch stock information
4. View stock recommendations and company details

## Environment Variables

The application requires a Finnhub API key set as an environment variable:
- `FINNHUB_API_KEY`: Your Finnhub API key

## Running the Application

The application can be run directly on Replit by clicking the Run button.
The dashboard will be accessible through the webview.

## Project Structure

- `app.py`: Main application file with Streamlit interface
- `utils.py`: Utility functions for data fetching
- `main.py`: Entry point file
