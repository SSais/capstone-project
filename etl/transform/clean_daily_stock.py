import pandas as pd
import timeit

foreign_id_index = {'ARGX': 1,
                    'GMAB': 2,
                    'PFE': 3,
                    'GSK': 4
                    }


def clean_daily_stock(dataframe: pd.DataFrame, symbol: str) -> pd.DataFrame:
    start_time = timeit.default_timer()

    transformed_df = transpose_dataframe(dataframe)
    transformed_df = reset_dataframe_index(transformed_df)
    transformed_df = sort_dates_asc(transformed_df)
    transformed_df = rename_columns(transformed_df, ['date', 'open', 'high', 'low', 'close', 'volume'])
    transformed_df = round_price_2dp(transformed_df)
    transformed_df = add_primary_id(transformed_df, 'stock_id')
    transformed_df = add_foreign_id(transformed_df, 'company_id', symbol)
    transformed_df = reorder_columns(transformed_df, ['stock_id', 'company_id', 'date', 'open', 'high', 'low', 'close', 'volume'])

    # Print time of extraction execution
    clean_daily_time = timeit.default_timer() - start_time
    print(f'It took {clean_daily_time}s to clean the daily data for {symbol}.')

    transformed_df.to_csv(f'etl/data/processed/cleaned_daily_{symbol}.csv', index=False)
    return transformed_df


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


def round_price_2dp(dataframe: pd.DataFrame) -> pd.DataFrame:
    rounded_df = dataframe.round({'open': 2, 'high': 2, 'low': 2, 'close': 2})
    return rounded_df


def add_primary_id(dataframe: pd.DataFrame, id_column_name: str) -> pd.DataFrame:
    dataframe[id_column_name] = dataframe.index + 1
    return dataframe


def add_foreign_id(dataframe: pd.DataFrame, id_column_name: str, symbol: int) -> pd.DataFrame:
    foreign_id = foreign_id_index[symbol]
    dataframe[id_column_name] = foreign_id
    return dataframe


def reorder_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
    return dataframe[column_names]
