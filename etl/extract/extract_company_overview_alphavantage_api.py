import os
import requests
import boto3
import json

# Initialise the S3 client
S3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda handler function to extract company overview data from Alpha Vantage API. 
    This API call will not be automated and will be called manually when needed.
    """
    # Import API Key
    API_KEY = os.environ.get('MY_API_KEY')

    # Define ticker names for which data will be extracted
    TICKER_NAMES = [
        'ARGX',  # Argenx
        'GMAB',  # Genmab
        'AAPL',  # Apple
        'IBM',   # IBM
        ]

    # Define S3 bucket and path for storing company overview data
    S3_BUCKET_NAME = 'sbs-stock-dash-v1.0'
    S3_PATH= 'company_overview'


    # Define function to get daily ticker data from Alpha Vantage API
    def get_overview_ticker_data(symbol: str, API_KEY:str) -> dict:
        """
        Fetch company overview data from Alpha Vantage API.
        Args:
            symbol (str): The stock symbol to fetch data for.
            API_KEY (str): The API key for Alpha Vantage.
        Returns:
            dict: The daily stock data for the specified symbol.
        Raises:
            Exception: If an error occurs during the API request or data processing.
        """
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
            response = requests.get(url, timeout=30)
            data = response.json()
            return data
        except Exception as e:
            raise Exception(f'An unexpected error occurred.\nError: {e}.')

    try:
        # Loop through each ticker name and fetch data
        for ticker in TICKER_NAMES:
            print(f'Fetching overview data for:{ticker}...')
            daily_data = get_overview_ticker_data(ticker, API_KEY)

            #  Prepare the data for S3 upload
            raw_data = json.dumps(daily_data)
            raw_data = raw_data.encode('utf-8')
            print(f"Successfully fetched overview data for {ticker}!")

            print(f"Preparing to upload {ticker} overview to S3...")
            # Define the S3 file path
            s3_final_path = f"{S3_PATH}/alpha_vantage_overview_{ticker}.json"

            # Upload the data to S3
            S3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=s3_final_path,
                Body=raw_data,
                ContentType='application/json'
            )
            print(f"Successfully uploaded {ticker} overview data to S3 at {s3_final_path}!")
    except Exception as e:
        print(f"An error occurred: {e}")
