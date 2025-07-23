import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Get data from session state
complete_ticker_df = st.session_state['daily_data']
company_df = st.session_state['company_data']

st.dataframe(company_df)S

# Set up tabs
tab1, tab2 = st.tabs(['General', 'Stock'])

# Set up sidebar
with st.sidebar:
    # Select box to select company ticker
    selected_company_name = st.selectbox(
        "Select Company:",
        options=sorted(complete_ticker_df['symbol'].unique())
    )

    # Select filtered data
    selected_company_df = complete_ticker_df[complete_ticker_df['symbol'] == selected_company_name]
    selected_overview_df = company_df[company_df['Symbol'] == selected_company_name]

    # Option to select a date range
    min_date = selected_company_df['date'].min()
    max_date = selected_company_df['date'].max()
    start_date = st.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)

    # Option to show data 
    show_data = st.checkbox('Display Dataset', value=False)


with tab1:
    # Display general stock info
    st.title(selected_overview_df['Name'].item())
    st.subheader(selected_overview_df['Symbol'].item())
    st.write(selected_overview_df['Exchange'].item() + ':' + selected_overview_df['Currency'].item())
    st.write(selected_overview_df['Sector'].item())
    st.write(selected_overview_df['Description'].item())
    st.write(selected_overview_df['OfficialSite'].item())


with tab2:

    st.title('Stock Data for: ' + selected_overview_df['Name'].item())

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**52 Week High:** {selected_overview_df['52WeekHigh'].item()} {selected_overview_df['Currency'].item()}")
        st.write(f"**Market Capitalisation:** {selected_overview_df['MarketCapitalization'].item()}")
    with col2:
        st.write(f"**52 Week Low:** {selected_overview_df['52WeekLow'].item()} {selected_overview_df['Currency'].item()}")
        st.write(f"**Profit Margin:** {selected_overview_df['ProfitMargin'].item()} %")

    filtered_data = selected_company_df[(selected_company_df['date'] >= str(start_date)) & (selected_company_df['date'] <= str(end_date))]

    # Define candle stick figure
    fig_candle = go.Figure(go.Candlestick(
                                          x=filtered_data['date'],
                                          open=filtered_data['open'],
                                          high=filtered_data['high'],
                                          low =filtered_data['low'],
                                          close=filtered_data['close']))
    fig_candle.update_xaxes(title_text='Date')
    fig_candle.update_yaxes(title_text='Prices')
    
    # Dislay candle stick figure
    st.plotly_chart(fig_candle)

    # Define volume figure
    fig_volume = px.bar(filtered_data, x='date', y='volume')
    fig_volume.update_layout(xaxis_title='Date (YYYY/MM/DD)', yaxis_title='Volume')

    # Display volume figure
    st.plotly_chart(fig_volume)

    # Define scatter plot of returns 
    fig_scatter = px.line(filtered_data, x='date', y='daily_return_p', title='Daily returns over Time')

    # Display scatter plot
    st.plotly_chart(fig_scatter)

    # Define histogram of returns
    fig_histogram = px.histogram(filtered_data, x='daily_return_p', nbins=1000) # Need to adjust bins based on the number of datapoints that has been filtered.

    # Display histogram
    st.plotly_chart(fig_histogram)
    
    # Display source data if check box is selected in sidebar
    if show_data:
        st.write('See complete data below:')
        st.dataframe(selected_company_df)
