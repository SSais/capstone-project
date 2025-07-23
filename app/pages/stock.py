import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Get data from session state
complete_ticker_df = st.session_state['daily_data']
company_df = st.session_state['company_data']

# Set up tabs
tab1, tab2 = st.tabs(['General', 'Stock'])

# Set up sidebar
with st.sidebar:
    # Select box to select company ticker
    selected_company_name = st.selectbox(
        "Select Company:",
        options=sorted(complete_ticker_df['symbol'].unique())
    )

    # Filter data using the selected ticker
    def filter_by_symbol(selected_company_name):
        if selected_company_name == 'ARGX':
            return data_argenx
        if selected_company_name == 'GMAB':
            return data_gmab
    selected_company_df = filter_by_symbol(selected_company_name)
    selected_overview_df = data_overview[data_overview['Symbol'] == selected_company_name]

    min_date = selected_company_df['date'].min()
    max_date = selected_company_df['date'].max()
    start_date = st.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)

    show_data = st.checkbox('Display Dataset', value=False)


with tab1:
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

    fig_candle = go.Figure(go.Candlestick(
                                          x=filtered_data['date'],
                                          open=filtered_data['open'],
                                          high=filtered_data['high'],
                                          low =filtered_data['low'],
                                          close=filtered_data['close']))
    fig_candle.update_xaxes(title_text='Date')
    fig_candle.update_yaxes(title_text='Prices')
    st.plotly_chart(fig_candle)

    fig_volume = px.bar(filtered_data, x='date', y='volume')
    fig_volume.update_layout(xaxis_title='Date (YYYY/MM/DD)', yaxis_title='Volume')

    st.plotly_chart(fig_volume)


    if show_data:
        st.write('See complete data below:')
        st.dataframe(selected_company_df)

    fig_scatter = px.line(filtered_data, x='date', y='daily_return_p', title='Daily returns over Time')
    st.plotly_chart(fig_scatter)

    fig_histogram = px.histogram(filtered_data, x='daily_return_p', nbins=1000)
    st.plotly_chart(fig_histogram)

    #     title='Frequency Distribution of Returns',
    #     labels={'Returns (%)': 'Returns (%)', 'count': 'Frequency'},
