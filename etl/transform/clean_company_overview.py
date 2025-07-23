import pandas as pd
import boto3
import io

# Initialise the S3 client
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    """
    AWS Lambda handler function to transform daily ticker data that has been saved in the S3 raw parition.
    This API call will not be automated and will be called manually when needed, using a HTTPS endpoint.
    """

    # Define S3 bucket
    S3_BUCKET_NAME = 'sbs-stock-dash-v1.0'

    # Define ticker names for which data will be extracted
    TICKERS = [
        'ARGX',  # Argenx
        'GMAB',  # Genmab
        'AAPL',  # Apple
        'IBM',   # IBM
    ]
    
    # Define output file path and name
    output_file_name = 'company_overview/enriched_company_overview.csv'

    # Define empty array
    all_dataframes = []
 
    for ticker in TICKERS:
        # Define raw data file paths
        raw_file_path = f'company_overview/alpha_vantage_overview_{ticker}.json'
        try:
            # Get the raw data from S3 and read raw data into a dataframe
            get_raw_data = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=raw_file_path)
            raw_data_body = get_raw_data['Body'].read().decode('utf-8')
            raw_data_df = pd.read_json(io.StringIO(raw_data_body), orient='index').transpose()
            all_dataframes.append(raw_data_df)
        except Exception as e:
            raise Exception(f'An unexpected error occurred.\nError: {e}.')

    # Concatonate the data
    complete_concat_df = pd.concat(all_dataframes, ignore_index=True)

    # Prepare to save data into S3
    csv_buffer = io.StringIO()
    complete_concat_df.to_csv(csv_buffer, index=False) 

    # Save transformed data to S3
    s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=output_file_name,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
