from dotenv import load_dotenv
import os

from etl.extract.extract import pytest_confirm

# from etl.extract import pytest_confirm

# Load env variables
load_dotenv()
API_KEY = os.environ.get('API_KEY')
print(API_KEY)

# ETL pipeline will be run here - in one function 

print("Setting up environment...")
pytest_confirm(1)
# Load env variables
print("Environment setup complete.")

print("Starting data extraction...")
# Extract data
print("Data extraction complete.")

print("Starting data transformation...")
# Transform data
print("Data transformation complete.")

print("Loading data into Pagilla database...")
# Load data into database
print("Data loading complete.")


print("Streamlit can be run with updated data")