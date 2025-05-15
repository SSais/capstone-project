import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Stock Explorer')

full_df = st.session_state["full_df"]


with st.sidebar:
    selected_company_names = st.multiselect(
        "Select Companies:",
        options=sorted(full_df['symbol'].unique())
    )

    selected_companies_df = full_df[full_df['symbol'].isin(selected_company_names)]

    min_date = selected_companies_df['date'].min()
    max_date = selected_companies_df['date'].max()

    start_date = st.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)


if len(selected_company_names) == 0:
    st.write('Please select options on the left.')
else:
    filtered_data = selected_companies_df[(selected_companies_df['date'] >= str(start_date)) & (selected_companies_df['date'] <= str(end_date))]

    fig_stock1 = px.line(filtered_data, x='date', y='high', color='name', markers=True)
    fig_stock1.update_layout(xaxis_title='Date (YYYY/MM/DD)', yaxis_title='Price (USD)')
    st.plotly_chart(fig_stock1)
