import streamlit as st
import pandas as pd
import plotly.express as px

# Get data from session state
complete_ticker_df = st.session_state['daily_data']
company_df = st.session_state['company_data']

with st.sidebar:
    # Select companies to compare
    selected_company_names = st.multiselect(
        "Select Companies:",
        options=sorted(complete_ticker_df['symbol'].unique())
    )
    
    # Filter selected data
    selected_companies_df = complete_ticker_df[complete_ticker_df['symbol'].isin(selected_company_names)]

    # Option to select date range of data
    min_date = selected_companies_df['date'].min()
    max_date = selected_companies_df['date'].max()
    start_date = st.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)

st.title('Stock Explorer')


# Display data if data has been selected
if len(selected_company_names) == 0:
    st.write('Please select options on the left.')
else:
    filtered_data = selected_companies_df[(selected_companies_df['date'] >= str(start_date)) & (selected_companies_df['date'] <= str(end_date))]

    # Define graph for comparison
    fig_stock1 = px.line(filtered_data, x='date', y='wealth_index', color='name', markers=True)
    fig_stock1.update_layout(xaxis_title='Date (YYYY/MM/DD)', yaxis_title='Price (USD)')

    # Display graph
    st.plotly_chart(fig_stock1)
