import pandas as pd
import requests
import os
from datetime import datetime

# Define constants for data sources
STOCK_EXCHANGE_API = "https://api.example.com/stock_exchange"
GOLD_PRICE_API = "https://api.example.com/gold_price"
INFLATION_DATA_API = "https://api.example.com/inflation_data"

# API keys (use environment variables for security)
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")
INFLATION_API_KEY = os.getenv("INFLATION_API_KEY")

# Data Directory
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_data(api_url, params=None):
    """Fetch data from a given API."""
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None

def fetch_stock_data():
    """Fetch stock market data."""
    params = {"api_key": STOCK_API_KEY}
    data = fetch_data(STOCK_EXCHANGE_API, params)
    if data:
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(DATA_DIR, "stock_data.csv"), index=False)
        print("Stock data saved.")
    else:
        print("Failed to fetch stock data.")

def fetch_gold_price_data():
    """Fetch gold price data."""
    params = {"api_key": GOLD_API_KEY}
    data = fetch_data(GOLD_PRICE_API, params)
    if data:
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(DATA_DIR, "gold_price_data.csv"), index=False)
        print("Gold price data saved.")
    else:
        print("Failed to fetch gold price data.")

def fetch_inflation_data():
    """Fetch inflation rate data."""
    params = {"api_key": INFLATION_API_KEY}
    data = fetch_data(INFLATION_DATA_API, params)
    if data:
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(DATA_DIR, "inflation_data.csv"), index=False)
        print("Inflation data saved.")
    else:
        print("Failed to fetch inflation data.")

def preprocess_data():
    """Merge and preprocess all data."""
    try:
        # Load datasets
        stock_data = pd.read_csv(os.path.join(DATA_DIR, "stock_data.csv"))
        gold_price_data = pd.read_csv(os.path.join(DATA_DIR, "gold_price_data.csv"))
        inflation_data = pd.read_csv(os.path.join(DATA_DIR, "inflation_data.csv"))
        
        # Merge data on date
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        gold_price_data['date'] = pd.to_datetime(gold_price_data['date'])
        inflation_data['date'] = pd.to_datetime(inflation_data['date'])
        
        merged_data = pd.merge(stock_data, gold_price_data, on='date', how='inner')
        merged_data = pd.merge(merged_data, inflation_data, on='date', how='inner')
        
        # Save preprocessed data
        merged_data.to_csv(os.path.join(DATA_DIR, "merged_data.csv"), index=False)
        print("Merged and preprocessed data saved.")
    except Exception as e:
        print(f"Error during data preprocessing: {e}")

def main():
    print(f"Pipeline started at {datetime.now()}")
    fetch_stock_data()
    fetch_gold_price_data()
    fetch_inflation_data()
    preprocess_data()
    print(f"Pipeline completed at {datetime.now()}")

if __name__ == "__main__":
    main()