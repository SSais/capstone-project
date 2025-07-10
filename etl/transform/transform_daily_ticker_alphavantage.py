import boto3
import pandas as pd
import json
import os
import io

s3_client = boto3.client('s3')


def transpose_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    transposed_df = dataframe.transpose()
    return transposed_df
    
def reset_dataframe_index(dataframe: pd.DataFrame) -> pd.DataFrame:
    reset_index_df = dataframe.reset_index()
    return reset_index_df
    
def sort_dates_asc(dataframe: pd.DataFrame) -> pd.DataFrame:
    sorted_df = dataframe.sort_values('index', ascending=True, ignore_index=True)
    return sorted_df
    
def rename_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    dataframe.columns = column_names
    return dataframe
    
def reorder_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    return dataframe[column_names].dropna()
    
def daily_return_calculations(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['daily_return'] = dataframe['close'].pct_change()
    dataframe['daily_return_p'] = dataframe['daily_return'] * 100
    return dataframe
    
def wealth_index_calculation(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['wealth_index'] = (dataframe['daily_return'] + 1).cumprod()
    return dataframe

def lambda_handler(event, context):

    S3_BUCKET_NAME= 'sbs-stock-dash-v1.0'
    raw_file_path = event['Records'][0]['s3']['object']['key']

    get_raw_data = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=raw_file_path)
    raw_data_body = get_raw_data['Body'].read().decode('utf-8')

    raw_data = pd.read_json(io.StringIO(raw_data_body))
    
    try:
        
        # Start of transformation
        transformed_df = transpose_dataframe(raw_data)
        transformed_df = reset_dataframe_index(transformed_df)
        transformed_df = sort_dates_asc(transformed_df)
        transformed_df = rename_columns(transformed_df, ['date', 'open', 'high', 'low', 'close', 'volume'])
        
        # Enrichment of the data
        transformed_df = daily_return_calculations(transformed_df)
        transformed_df = wealth_index_calculation(transformed_df)
        transformed_df = reorder_columns(transformed_df, [ 'date', 'open', 'high', 'low', 'close', 'volume','daily_return', 'daily_return_p', 'wealth_index'])


        output_file_name = raw_file_path.replace('raw/', 'enriched/')
        output_file_name = output_file_name.replace('.json', '.csv')
        
        csv_buffer = io.BytesIO()
        transformed_df.to_csv(csv_buffer, index=False) 

        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=output_file_name,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
    except Exception as e:
        raise Exception(f'An unexpected error occurred.\nError: {e}.')