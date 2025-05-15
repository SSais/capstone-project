import streamlit as st
import pandas as pd

df1 = pd.read_csv('etl/data/processed/cleaned_company_overview.csv')
df2 = pd.read_csv('etl/data/processed/cleaned_daily_ARGX.csv')
df3 = pd.read_csv('etl/data/processed/cleaned_daily_GMAB.csv')
df4 = pd.read_csv('etl/data/processed/cleaned_daily_PFE.csv')
df5 = pd.read_csv('etl/data/processed/cleaned_daily_GSK.csv')

df_argenx = df2.merge(df1, how='inner', on='company_id')
df_gmab = df3.merge(df1, how='inner', on='company_id')
df_pfe = df4.merge(df1, how='inner', on='company_id')
df_gsk = df5.merge(df1, how='inner', on='company_id')


intermediate_df1 = pd.concat([df_argenx, df_gmab], ignore_index=True)
intermediate_df2 = pd.concat([df_pfe, df_gsk], ignore_index=True)
full_df = pd.concat([intermediate_df1, intermediate_df2], ignore_index=True)


def main():
    st.session_state['full_df'] = full_df    
    
    main_page = st.Page(
        page='pages/main_page.py',
        title="Main Dashboard",
        icon="🏦" 
    )

    comparison = st.Page(
        page='pages/comparison.py',
        title="Comparison",
        icon="📈"
    )

    pg = st.navigation(pages=[main_page, comparison])

    pg.run()



if __name__ == "__main__":
    main()
