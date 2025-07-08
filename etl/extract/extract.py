# Commented out as the extract function will be rewritten for lambda and S3 storage.

# import pandas as pd
# from etl.extract.extract_alphavantage_api import get_request_daily_alphavantage, get_request_overview_alphavantage


# def extract_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

#     argenx_daily_data = get_request_daily_alphavantage('ARGX')
#     print('Argenx daily extraction has been completed')
#     genmab_daily_data = get_request_daily_alphavantage('GMAB')
#     print('Genmab daily extraction has been completed')
#     pfizer_daily_data = get_request_daily_alphavantage('PFE')
#     print('Pfizer daily extraction has been completed')
#     gsk_daily_data = get_request_daily_alphavantage('GMAB')
#     print('GSK daily extraction has been completed')

#     argenx_overview_data = get_request_overview_alphavantage('ARGX')
#     print('Argenx overview extraction has been completed')
#     genmab_overview_data = get_request_overview_alphavantage('GMAB')
#     print('Genmab overview extraction has been completed')
#     pfizer_overview_data = get_request_overview_alphavantage('PFE')
#     print('Pfizer overview extraction has been completed')
#     gsk_overview_data = get_request_overview_alphavantage('GSK')
#     print('GSK overview extraction has been completed')

#     return (
#             argenx_daily_data,
#             genmab_daily_data,
#             pfizer_daily_data,
#             gsk_daily_data,
#             argenx_overview_data,
#             genmab_overview_data,
#             pfizer_overview_data,
#             gsk_overview_data
#             )




# Commenting out old data extraction functions as they will be replaced with a new approach using AWS Lambda and S3 storage.

# def get_request_daily_alphavantage(symbol: str) -> pd.DataFrame:
#     start_time = timeit.default_timer()

#     try:
#         # Get the response
#         daily_data = get_request('TIME_SERIES_DAILY', symbol)

#         # Convert json data to dataframe
#         df = json_to_dataframe(daily_data, 0)

#         # Print time of extraction execution
#         extract_daily_time = timeit.default_timer() - start_time
#         print(f'It took {extract_daily_time}s to extract the daily data for {symbol}.')

#         return df
#     except Exception as e:
#         raise Exception(f'An unexpected error occurred.\nError: {e}.')


# def get_request_overview_alphavantage(symbol: str) -> pd.DataFrame:
#     start_time = timeit.default_timer()

#     try:
#         # Get the response
#         overview_data = get_request('OVERVIEW', symbol)

#         # Convert json data to dataframe
#         df = json_to_dataframe(overview_data, 1)

#         # Print time of extraction execution
#         extract_overview_time = timeit.default_timer() - start_time
#         print(f'It took {extract_overview_time}s to extract the overview for {symbol}.')

#         return df
#     except Exception as e:
#         raise Exception(f'An unexpected error occurred.\nError: {e}.')


# def get_request(function: str, symbol: str):
#     try:
#         url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}'
#         response = requests.get(url)
#         data = response.json()

#         if function == 'TIME_SERIES_DAILY':
#             return data['Time Series (Daily)']
#         elif function == 'OVERVIEW':
#             return data
#     except Exception as e:
#         raise Exception(f'An unexpected error occurred.\nError: {e}.')


# def json_to_dataframe(data, index: int) -> pd.DataFrame:
#     if index == 1:
#         return pd.DataFrame(data, index=[0])
#     elif index == 0:
#         return pd.DataFrame(data)
