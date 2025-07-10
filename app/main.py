import streamlit as st
import pandas as pd
import boto3
from dotenv import load_dotenv
import os
import datetime

# Load AWS environment variables
load_dotenv()

# Define S3 bucket and path for storing ticker data
S3_BUCKET_NAME= 'sbs-stock-dash-v1.0'
S3_PARTIAL_PATH = 'enriched/ticker-data'

# Get the current date to create a partition path in S3
current_date = datetime.datetime.now()
year = current_date.strftime('%Y')
month = current_date.strftime('%m')
day = current_date.strftime('%d')
s3_date_path = f"{S3_PARTIAL_PATH}/{year}/{month}/{day}"

# Initialise the S3 client
s3_client = boto3.client('s3')

# Define a function to load data from S3 and cache it for 24 hours
@st.cache_data(ttl=86400)
def load_daily_from_s3(bucket_name: str, partial_file_path: str, ticker: str) -> pd.DataFrame:
    """
    Load test data from the S3 bucket.
    """
    try:
        complete_file_path = f'{partial_file_path}/alpha_vantage_daily_{ticker}.csv'
        response = s3_client.get_object(Bucket=bucket_name, Key=complete_file_path)
        data = pd.read_csv(response['Body'])
        return data
    except Exception as e:
        st.error(f"Error loading data from S3: {e}")
        return None

# Load data from S3
@st.cache_data(ttl=86400)
data_argenx = load_daily_from_s3(S3_BUCKET_NAME, s3_date_path, 'ARGX')

@st.cache_data(ttl=86400)
data_gmab = load_daily_from_s3(S3_BUCKET_NAME, s3_date_path, 'GMAB')

# @st.cache_data(ttl=86400)
# data_pfe = load_daily_from_s3(S3_BUCKET_NAME, s3_date_path, 'PFE')

# @st.cache_data(ttl=86400)
# data_gsk = load_daily_from_s3(S3_BUCKET_NAME, s3_date_path, 'GSK')  

def main():
    st.session_state['full_df'] = data

    st.dataframe(data)
    
    overview = st.Page(
        page='pages/overview.py',
        title="Overview",
        icon="🏦" 
    )
    
    stock = st.Page(
        page='pages/stock.py',
        title="Stock",
        icon="🏦" 
    )

    comparison = st.Page(
        page='pages/comparison.py',
        title="Comparison",
        icon="📈"
    )
    
    financial = st.Page(
        page='pages/financial.py',
        title="Financial",
        icon="🏦" 
    )

    pg = st.navigation(pages=[overview,stock, comparison, financial])

    pg.run()



if __name__ == "__main__":
    main()
 
# df1 = pd.read_csv('etl/data/processed/cleaned_company_overview.csv')
# df2 = pd.read_csv('etl/data/processed/cleaned_daily_ARGX.csv')
# df3 = pd.read_csv('etl/data/processed/cleaned_daily_GMAB.csv')
# df4 = pd.read_csv('etl/data/processed/cleaned_daily_PFE.csv')
# df5 = pd.read_csv('etl/data/processed/cleaned_daily_GSK.csv')

# df_argenx = df2.merge(df1, how='inner', on='company_id')
# df_gmab = df3.merge(df1, how='inner', on='company_id')
# df_pfe = df4.merge(df1, how='inner', on='company_id')
# df_gsk = df5.merge(df1, how='inner', on='company_id')

# intermediate_df1 = pd.concat([df_argenx, df_gmab], ignore_index=True)
# intermediate_df2 = pd.concat([df_pfe, df_gsk], ignore_index=True)
# full_df = pd.concat([intermediate_df1, intermediate_df2], ignore_index=True)