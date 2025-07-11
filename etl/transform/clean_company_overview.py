# import pandas as pd
# import timeit
# from etl.transform.clean_daily_stock import reorder_columns, add_primary_id, rename_columns


# def clean_company_overview(dataframe_argx: pd.DataFrame, dataframe_gmab: pd.DataFrame, dataframe_pfe: pd.DataFrame, dataframe_gsk: pd.DataFrame ) -> pd.DataFrame:
#     start_time = timeit.default_timer()

#     pre_transformed_df1 = concat_dataframes(dataframe_argx, dataframe_gmab)
#     pre_transformed_df2 = concat_dataframes(dataframe_pfe, dataframe_gsk)
#     transformed_df = concat_dataframes(pre_transformed_df1, pre_transformed_df2)
    
#     transformed_df = drop_columns(transformed_df)
#     transformed_df = rename_columns(transformed_df, ['symbol', 'asset_type', 'name', 'description', 'exchange', 'currency', 'sector', 'industry', 'web_site', 'market_cap', 'revenue_per_share', 'profit_margin', 'week_52_high', 'week_52_low', 'moving_average_50'])
#     transformed_df = add_primary_id(transformed_df, 'company_id')
#     transformed_df = reorder_columns(transformed_df, ['company_id', 'symbol', 'asset_type', 'name', 'description', 'exchange', 'currency', 'sector', 'industry', 'web_site', 'market_cap', 'profit_margin', 'week_52_high', 'week_52_low', 'moving_average_50'])

#     clean_overview_time = timeit.default_timer() - start_time
#     print(f'It took {clean_overview_time}s to clean the company overview data.')
#     transformed_df.to_csv('etl/data/processed/cleaned_company_overview.csv', index=False)

#     return transformed_df


# def concat_dataframes(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame) -> pd.DataFrame:
#     concat_df = pd.concat([dataframe1, dataframe2], ignore_index=True)
#     return concat_df


# def drop_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
#     columns_to_drop = ['CIK', 'Country', 'Address', 'FiscalYearEnd', 'LatestQuarter', 'EBITDA', 'PERatio', 'PEGRatio', 'BookValue', 'EPS', 'OperatingMarginTTM', 'ReturnOnAssetsTTM', 'ReturnOnEquityTTM', 'RevenueTTM', 'GrossProfitTTM', 'DilutedEPSTTM', 'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY', 'AnalystTargetPrice', 'AnalystRatingStrongBuy', 'AnalystRatingBuy', 'AnalystRatingHold', 'AnalystRatingSell', 'AnalystRatingStrongSell', 'TrailingPE', 'ForwardPE', 'PriceToSalesRatioTTM', 'PriceToBookRatio', 'EVToRevenue', 'EVToEBITDA', 'Beta', 'SharesOutstanding', '200DayMovingAverage', 'DividendDate', 'ExDividendDate', 'DividendPerShare', 'DividendYield']
#     dropped_df = dataframe.drop(columns=columns_to_drop)
#     return dropped_df
