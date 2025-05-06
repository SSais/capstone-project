from dotenv import load_dotenv
import os

from etl.extract.extract import get_request_coingecko_api


print("Fetching API Key...")
# Load env variables
load_dotenv()
API_KEY = os.environ.get('API_KEY')
print("API key retrieved.")

print("Starting data extraction...")
get_request_coingecko_api(API_KEY)
print("Data extraction complete.")

print("Starting data transformation...")
# Transform data
print("Data transformation complete.")

print("Loading data into Pagilla database...")
# Load data into database
print("Data loading complete.")


print("Streamlit can be run with updated data")