import datetime
import requests
import boto3
import json
import os

# Initialise the S3 client
S3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda handler function to extract daily ticker data from Alpha Vantage API
    and store it in an S3 bucket with YYYY/MM/DD partitioning.
    """
    
    # Import API Key
    API_KEY = os.environ.get('MY_API_KEY')
    
    # Define ticker names for which data will be extracted
    TICKERS = [
        'ARGX',  # Argenx
        'GMAB',  # Genmab
        'AAPL',  # Apple
        'IBM',   # IBM
        ]
    
    # Define S3 bucket and path for storing ticker data
    S3_BUCKET_NAME= 'sbs-stock-dash-v1.0'
    S3_PARTIAL_PATH = 'raw/ticker-data'
    
    # Get the current date to create a partition path in S3
    current_date = datetime.datetime.now()
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    day = current_date.strftime('%d')
    s3_date_path = f"{S3_PARTIAL_PATH}/{year}/{month}/{day}"
    
    # Define function to get full historical daily ticker data from Alpha Vantage API
    def get_daily_ticker_data(symbol: str, API_KEY: str) -> dict:
        """    
        Fetch daily ticker data from Alpha Vantage API.
        Args:
            symbol (str): The stock symbol to fetch data for.
        Returns:
            dict: The daily stock data for the specified symbol.
        Raises:
            Exception: If an error occurs during the API request or data processing.
        """
        try:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=full&apikey={API_KEY}'
            response = requests.get(url, timeout=30)
            data = response.json()
            return data['Time Series (Daily)']
        except Exception as e:
            raise Exception(f'An unexpected error occurred.\nError: {e}.')

    try:
        # Loop through each ticker name and fetch data
        for ticker in TICKERS:
            print(f'Fetching daily data for:{ticker}...')
            daily_data = get_daily_ticker_data(ticker, API_KEY)
            
            #  Prepare the data for S3 upload
            raw_data = json.dumps(daily_data)
            raw_data = raw_data.encode('utf-8')
            print(f"Successfully fetched daily data for {ticker}!")
            
            print(f"Preparing to upload {ticker} daily data to S3...")
            # Define the S3 file path
            s3_final_path = f"{s3_date_path}/alpha_vantage_daily_{ticker}.json"
            
            # Upload the data to S3
            S3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_final_path,
                Body=raw_data,
                ContentType='application/json'
            )
            print(f"Successfully uploaded {ticker} daily data to S3 at {s3_final_path}!")
    except Exception as e:
        print(f"An error occurred: {e}")
