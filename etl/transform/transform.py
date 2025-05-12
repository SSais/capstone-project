from etl.transform.clean_daily_stock import clean_daily_stock
from etl.transform.clean_company_overview import clean_company_overview
import pandas as pd


def transform_data(data: tuple) -> tuple[pd.DataFrame]:

    transformed_argx_daily = clean_daily_stock(data[0], 'ARGX')
    transformed_gmab_daily = clean_daily_stock(data[1], 'GMAB')

    transformed_company_overview = clean_company_overview(data[2], data[3])

    return (
            transformed_argx_daily,
            transformed_gmab_daily,
            transformed_company_overview
            )
