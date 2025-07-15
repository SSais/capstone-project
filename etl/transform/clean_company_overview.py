import pandas as pd
import boto3
import io

s3_client = boto3.client('s3')

def rename_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    dataframe.columns = column_names
    return dataframe
    
def reorder_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    return dataframe[column_names].dropna()

def drop_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
        columns_to_drop = ['CIK', 'Country', 'Address', 'FiscalYearEnd', 'LatestQuarter', 'EBITDA', 'PERatio', 'PEGRatio', 'BookValue', 'EPS', 'OperatingMarginTTM', 'ReturnOnAssetsTTM', 'ReturnOnEquityTTM', 'RevenueTTM', 'GrossProfitTTM', 'DilutedEPSTTM', 'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY', 'AnalystTargetPrice', 'AnalystRatingStrongBuy', 'AnalystRatingBuy', 'AnalystRatingHold', 'AnalystRatingSell', 'AnalystRatingStrongSell', 'TrailingPE', 'ForwardPE', 'PriceToSalesRatioTTM', 'PriceToBookRatio', 'EVToRevenue', 'EVToEBITDA', 'Beta', 'SharesOutstanding', '200DayMovingAverage', 'DividendDate', 'ExDividendDate', 'DividendPerShare', 'DividendYield']
        dropped_df = dataframe.drop(columns=columns_to_drop)
        return dropped_df

def lambda_handler(event, context):
    
    S3_BUCKET_NAME = 'sbs-stock-dash-v1.0'
    raw_file_path_argx = 'company_overview/alpha_vantage_overview_ARGX.json'
    
    get_raw_data_argx = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=raw_file_path_argx)
    raw_data_body_argx = get_raw_data_argx['Body'].read().decode('utf-8')
    
    raw_data_df = pd.read_json(io.StringIO(raw_data_body_argx), orient='index').transpose()
    
    transformed_df = drop_columns(raw_data_df)
    
    transformed_df = rename_columns(transformed_df, ['symbol', 'asset_type', 'name', 'description', 'exchange', 'currency', 'sector', 'industry', 'web_site', 'market_cap', 'revenue_per_share', 'profit_margin', 'week_52_high', 'week_52_low', 'moving_average_50'])

    transformed_df = reorder_columns(transformed_df, ['symbol', 'asset_type', 'name', 'description', 'exchange', 'currency', 'sector', 'industry', 'web_site', 'market_cap', 'profit_margin', 'week_52_high', 'week_52_low', 'moving_average_50'])
    
    output_file_name = 'company_overview/enriched_company_overview.csv'
    csv_buffer = io.BytesIO()
    transformed_df.to_csv(csv_buffer, index=False) 
    
    
    s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=output_file_name,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )



#     pre_transformed_df1 = concat_dataframes(dataframe_argx, dataframe_gmab)
#     pre_transformed_df2 = concat_dataframes(dataframe_pfe, dataframe_gsk)
#     transformed_df = concat_dataframes(pre_transformed_df1, pre_transformed_df2)
    


# def concat_dataframes(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame) -> pd.DataFrame:
#     concat_df = pd.concat([dataframe1, dataframe2], ignore_index=True)
#     return concat_df