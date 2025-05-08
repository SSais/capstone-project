import pandas as pd
from etl.extract.extract_alphavantage_api import get_request_daily_alphavantage, get_request_overview_alphavantage


def extract_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    argenx_daily_data = get_request_daily_alphavantage('ARGX')
    print('Argenx daily extraction has been completed')
    genmab_daily_data = get_request_daily_alphavantage('GMAB')
    print('Genmab daily extraction has been completed')

    argenx_overview_data = get_request_overview_alphavantage('ARGX')
    print('Argenx overview extraction has been completed')
    genmab_overview_data = get_request_overview_alphavantage('GMAB')
    print('Genmab overview extraction has been completed')

    return (
            argenx_daily_data,
            genmab_daily_data,
            argenx_overview_data,
            genmab_overview_data
            )
