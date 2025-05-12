import os
import pandas as pd
import requests
import timeit

# Load env variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.environ.get('API_KEY')


def get_request_daily_alphavantage(symbol: str) -> pd.DataFrame:
    start_time = timeit.default_timer()

    try:

        # Get the response
        daily_data = get_request('TIME_SERIES_DAILY', symbol)

        # Convert json data to dataframe
        df = json_to_dataframe(daily_data, 0)

        # Print time of extraction execution
        extract_daily_time = timeit.default_timer() - start_time
        print(f'It took {extract_daily_time}s to extract the daily data for {symbol}.')

        return df
    except Exception as e:
        raise Exception(f'An unexpected error occurred.\nError: {e}.')


def get_request_overview_alphavantage(symbol: str) -> pd.DataFrame:
    start_time = timeit.default_timer()

    try:

        # Get the response
        overview_data = get_request('OVERVIEW', symbol)

        # Convert json data to dataframe
        df = json_to_dataframe(overview_data, 1)

        # Print time of extraction execution
        extract_overview_time = timeit.default_timer() - start_time
        print(f'It took {extract_overview_time}s to extract the overview for {symbol}.')

        return df
    except Exception as e:
        raise Exception(f'An unexpected error occurred.\nError: {e}.')


def get_request(function: str, symbol: str):
    try:
        
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}'
        response = requests.get(url)
        data = response.json()

        if function == 'TIME_SERIES_DAILY':
            return data['Time Series (Daily)']
        elif function == 'OVERVIEW':
            return data
    except Exception as e:
        raise Exception(f'An unexpected error occurred.\nError: {e}.')


def json_to_dataframe(data, index: int) -> pd.DataFrame:
    if index == 1:
        return pd.DataFrame(data, index=[0])
    elif index == 0:
        return pd.DataFrame(data)
