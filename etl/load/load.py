from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')

# Create engine
db_url = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'
engine = create_engine(db_url)

schema_name = 'c12de'


def load_data(data: tuple):
    try:
        load_company_overview(data[4])

        load_daily_stock(data[0], 'daily_stocks_argx')
        load_daily_stock(data[1], 'daily_stocks_gmab')
        load_daily_stock(data[2], 'daily_stocks_pfe')
        load_daily_stock(data[3], 'daily_stocks_gsk')

    finally:
        engine.dispose()


def load_daily_stock(daily_df: pd.DataFrame, table: str):
    with engine.connect() as connection:
        id_column = 'company_id'
        table_name = table
        schema = 'c12de'

        count_query = text(f"SELECT COUNT({id_column}) FROM {schema}.{table_name}")
        result = connection.execute(count_query)
        id_count_from_db = result.scalar_one()

        id_count_from_df = daily_df[id_column].count()

        if id_count_from_db < id_count_from_df:
            select_rows_from_df = daily_df[id_count_from_db:]

            select_rows_from_df.to_sql(
                table_name,
                engine,
                if_exists='append',
                index=False,
                schema=schema
            )
            print(f"Successfully added {id_count_from_df - id_count_from_db} new records to {schema}.{table_name}.")
        else:
            print(f"No new records added to {schema}.{table_name}.")


def load_company_overview(overview_df: pd.DataFrame):
    schema = 'c12de'
    table_name = 'company_overviews'
    # temp_table = 'temp_company_overviews'

    with engine.begin() as connection:
        overview_df.to_sql(
                           table_name,
                           engine,
                           schema=schema,
                           if_exists='append',
                           index=False
                          )

    # with engine.begin() as connection:
    #     # Had assisstance from chat GPT to create this
    #     overview_df.to_sql(
    #         temp_table,
    #         engine,
    #         schema=schema,
    #         if_exists='replace',
    #         index=False
    #     )

    #     # Had assisstance from chat GPT to create this
    #     columns = ', '.join(overview_df.columns)
    #     updates = ', '.join([f'{col}=EXCLUDED.{col}' for col in overview_df.columns if col != 'company_id'])

    #     upsert_query = text(f"""
    #         INSERT INTO {schema}.{table_name} ({columns})
    #         SELECT {columns} FROM {schema}.{temp_table}
    #         ON CONFLICT (company_id)
    #         DO UPDATE SET {updates};
    #     """)
    #     connection.execute(upsert_query)

    #     connection.execute(text(f'DROP TABLE {schema}.{temp_table}'))

    #     print(f'Successfully upserted {len(overview_df)} records into {schema}.{table_name}.')
