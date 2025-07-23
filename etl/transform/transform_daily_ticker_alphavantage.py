import boto3
import pandas as pd
import json
import io

# Initialise the S3 client
s3_client = boto3.client('s3')

# Functions have been moved out of the lambda handler, for a warm start.

# Define function to transpose a dataframe
def transpose_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """    
    Function to transpose a dataframe.
    Args:
        dataframe (pd.Dataframe): The dataframe to be transposed.
    Returns:
        dataframe (pd.Dataframe): Transposed dataframe.
    """
    transposed_df = dataframe.transpose()
    return transposed_df

# Define function to reset the dataframe index
def reset_dataframe_index(dataframe: pd.DataFrame) -> pd.DataFrame:
    """    
    Function to reset the index of a dataframe.
    Args:
        dataframe (pd.Dataframe): The dataframe to be transformed.
    Returns:
        dataframe (pd.Dataframe): Transformed dataframe.
    """
    reset_index_df = dataframe.reset_index()
    return reset_index_df

# Define function to sort the index of a dataframe by ascending order
def sort_dates_asc(dataframe: pd.DataFrame) -> pd.DataFrame:
    """    
    Function to sort the index of a dataframe by ascending order.
    Args:
        dataframe (pd.Dataframe): The dataframe to be transformed.
    Returns:
        dataframe (pd.Dataframe): Transformed dataframe.
    """
    sorted_df = dataframe.sort_values('index', ascending=True, ignore_index=True)
    return sorted_df

# Define function to rename columns
def rename_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    """    
    Function to rename columns.
    Args:
        dataframe (pd.Dataframe): The dataframe to be transformed.
        column names (list): A list of the new column names. 
    Returns:
        dataframe (pd.Dataframe): Transformed dataframe.
    """
    dataframe.columns = column_names
    return dataframe

# Define function to reorder columns and to remove n/a value created by enrichment
def reorder_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    """    
    Function to reorder columns and to remove n/a value created by enrichment.
    Args:
        dataframe (pd.Dataframe): The dataframe to be transformed.
        column names (list): A list of the new column order.
    Returns:
        dataframe (pd.Dataframe): Transformed dataframe.
    """
    return dataframe[column_names].dropna()

# Define function to calculate daily return and daily return as a percentage
def daily_return_calculations(dataframe: pd.DataFrame) -> pd.DataFrame:
    """    
    Function to calculate daily return and daily return as a percentage.
    Args:
        dataframe (pd.Dataframe): The dataframe to be enriched.
    Returns:
        dataframe (pd.Dataframe): Enriched dataframe.
    """
    dataframe['daily_return'] = dataframe['close'].pct_change()
    dataframe['daily_return_p'] = dataframe['daily_return'] * 100
    return dataframe

# Define function to calculate the wealth index
def wealth_index_calculation(dataframe: pd.DataFrame) -> pd.DataFrame:
    """    
    Function to calculate the wealth index.
    Args:
        dataframe (pd.Dataframe): The dataframe to be enriched.
    Returns:
        dataframe (pd.Dataframe): Enriched dataframe.
    """
    dataframe['wealth_index'] = (dataframe['daily_return'] + 1).cumprod()
    return dataframe

def lambda_handler(event, context):
    """
    AWS Lambda handler function to transform daily ticker data that has been saved in the S3 raw parition.
    
    """
    
    # Define S3 bucket
    S3_BUCKET_NAME= 'sbs-stock-dash-v1.0'

    # Get the file name from the event
    raw_file_path = event['Records'][0]['s3']['object']['key']
    
    # Get the ticker from the file name
    file_name_parts = raw_file_path.split('_')
    ticker = file_name_parts[-1].replace('.json', '')
    print(ticker)

    # Prepare the output file name
    output_file_name = raw_file_path.replace('raw/', 'enriched/')
    output_file_name = output_file_name.replace('.json', '.csv')

    # Get the S3 data that has triggered the event
    get_raw_data = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=raw_file_path)
    raw_data_body = get_raw_data['Body'].read().decode('utf-8')

    # Load the raw data into a dataframe
    raw_data = pd.read_json(io.StringIO(raw_data_body))
    
    try:
        # Start of transformation
        transformed_df = transpose_dataframe(raw_data)
        transformed_df = reset_dataframe_index(transformed_df)
        transformed_df = sort_dates_asc(transformed_df)
        transformed_df = rename_columns(transformed_df, ['date', 'open', 'high', 'low', 'close', 'volume'])

        
        # Enrichment of the data
        transformed_df['symbol'] = ticker # Add a column for identification
        transformed_df = daily_return_calculations(transformed_df)
        transformed_df = wealth_index_calculation(transformed_df)

        # Reordering for organisation
        transformed_df = reorder_columns(transformed_df, [ 'symbol', 'date', 'open', 'high', 'low', 'close', 'volume','daily_return', 'daily_return_p', 'wealth_index'])
        
        # Convert data to csv
        csv_buffer = io.BytesIO()
        transformed_df.to_csv(csv_buffer, index=False) 

        # Save transformed data in S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=output_file_name,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
    except Exception as e:
        raise Exception(f'An unexpected error occurred.\nError: {e}.')
