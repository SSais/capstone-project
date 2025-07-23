import streamlit as st
import pandas as pd
import boto3
from dotenv import load_dotenv
import datetime

# Load AWS environment variables
load_dotenv()

# Initialise the S3 client
s3_client = boto3.client('s3')

# Define S3 bucket and path for storing ticker data
S3_BUCKET_NAME = 'sbs-stock-dash-v1.0'
S3_PARTIAL_PATH = 'enriched/ticker-data'

# Get the current date to get up to date data from S3
current_date = datetime.datetime.now()
year = current_date.strftime('%Y')
month = current_date.strftime('%m')
day = current_date.strftime('%d')
s3_date_path = f"{S3_PARTIAL_PATH}/{year}/{month}/{day}"

# Define function to get daily ticker data from S3 and cache it for 24 hours
@st.cache_data(ttl=86400)
def load_daily_data_from_s3(ticker: str) -> pd.DataFrame:
    """
    Load data from the S3 bucket.
    """
    try:
        complete_file_path = f'{s3_date_path}/alpha_vantage_daily_{ticker}.csv'
        response = s3_client.get_object(Bucket= S3_BUCKET_NAME, Key=complete_file_path)
        data = pd.read_csv(response['Body'])
        return data
    except Exception as e:
        st.error(f"Error loading data from S3: {e}")

# Get daily ticker data from S3
data_argx = load_daily_data_from_s3('ARGX')
data_gmab = load_daily_data_from_s3('GMAB')
data_ibm = load_daily_data_from_s3('IBM')
data_aapl = load_daily_data_from_s3('AAPL')

# Place loaded ticker dataframes into a list
all_loaded_dataframes = [df for df in [data_argx, data_gmab, data_ibm, data_aapl]]

# Conacatonate loaded ticker data
complete_ticker_df = pd.concat(all_loaded_dataframes, ignore_index=True)

# Define function to get company overview data from S3 and cache it for 24 hours
@st.cache_data(ttl=86400)
def load_company_overview_from_s3() -> pd.DataFrame:
    """
    Load company overview data from the S3 bucket.
    """
    complete_file_path = 'company_overview/enriched_company_overview.csv'
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=complete_file_path)
        data = pd.read_csv(response['Body'])
        return data
    except Exception as e:
        st.error(f"Error loading company overview data from S3: {e}")

# Get company overview data from S3
company_df = load_company_overview_from_s3()



def main():
    # Save all data in session state, so that S3 is not called again on other pages
    st.session_state['daily_data'] = complete_ticker_df
    st.session_state['company_data'] = company_df

    # Set up overview page
    overview = st.Page(
        page='pages/overview.py',
        title="Overview",
        # icon="🏦" 
    )

    # Set up stock page
    stock = st.Page(
        page='pages/stock.py',
        title="Stock",
        # icon="🏦" 
    )

    # Set up comparison page
    comparison = st.Page(
        page='pages/comparison.py',
        title="Comparison",
        # icon="📈"
    )

    pg = st.navigation(pages=[overview, stock, comparison])

    pg.run()


if __name__ == "__main__":
    main()
