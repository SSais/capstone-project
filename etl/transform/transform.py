# from etl.transform.clean_daily_stock import clean_daily_stock
# from etl.transform.clean_company_overview import clean_company_overview
# import pandas as pd


# def transform_data(data: tuple) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

#     transformed_argx_daily = clean_daily_stock(data[0], 'ARGX')
#     transformed_gmab_daily = clean_daily_stock(data[1], 'GMAB')
#     transformed_pfe_daily = clean_daily_stock(data[2], 'PFE')
#     transformed_gsk_daily = clean_daily_stock(data[3], 'GSK')

#     transformed_company_overview = clean_company_overview(data[4], data[5], data[6], data[7])

#     return (
#             transformed_argx_daily,
#             transformed_gmab_daily,
#             transformed_pfe_daily,
#             transformed_gsk_daily,
#             transformed_company_overview
#             )
