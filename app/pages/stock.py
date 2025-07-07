import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


full_df = st.session_state['full_df']

tab1, tab2, tab3 = st.tabs(['General', 'Stock', 'News'])

with st.sidebar:
    selected_company_name = st.selectbox(
        "Select Company:",
        options=sorted(full_df['name'].unique())
    )

    selected_company_df = full_df[full_df['name'] == selected_company_name]
    company_data = selected_company_df.iloc[0]

    min_date = selected_company_df['date'].min()
    max_date = selected_company_df['date'].max()
    start_date = st.date_input('Start Date', min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input('End Date', min_value=min_date, max_value=max_date, value=max_date)

    show_open = st.checkbox('Show Open Price', value=True)
    show_high = st.checkbox('Show High Price', value=True)
    show_low = st.checkbox('Show Low Price', value=True)
    show_close = st.checkbox('Show Close Price', value=True)

    show_candlestick = st.checkbox('Show Candlestick Plot', value=False)
    show_data = st.checkbox('Display Dataset', value=False)


with tab1:
    # Added as a test
    st.dataframe(full_df)
    
    
    st.title(company_data['name'])
    st.subheader(f'**{company_data['symbol']}**')
    st.write(f'**{company_data['exchange']}: {company_data['currency']}**')

    st.write(f'{company_data['sector']}')
    st.write(f'**Description:** {company_data['description']}')

    st.write(f'**Website:** {company_data['web_site']}')


with tab2:
    st.title(f'Stock Data for {selected_company_name}')

    col1, col2 = st.columns(2)
    with col1:
        st.write(f'**52 Week High:** {company_data['week_52_high']} {company_data['currency']}')
        st.write(f'**Market Capitalisation:** {company_data['market_cap']}')
    with col2:
        st.write(f'**52 Week Low:** {company_data['week_52_low']} {company_data['currency']}')
        st.write(f'**Profit Margin:** {company_data['profit_margin']} %')

    filtered_data = selected_company_df[(selected_company_df['date'] >= str(start_date)) & (selected_company_df['date'] <= str(end_date))]

    fig_stock = px.line(filtered_data, x='date', y='high', markers=True)
    if show_open:
        fig_stock.add_scatter(x=filtered_data['date'], y=filtered_data['open'], mode='lines', name='Open')
    if show_high:
        fig_stock.add_scatter(x=filtered_data['date'], y=filtered_data['high'], mode='lines', name='High')
    if show_low:
        fig_stock.add_scatter(x=filtered_data['date'], y=filtered_data['low'], mode='lines', name='Low')
    if show_close:
        fig_stock.add_scatter(x=filtered_data['date'], y=filtered_data['close'], mode='lines', name='Close')

    fig_stock.update_layout(xaxis_title='Date (YYYY/MM/DD)', yaxis_title='Price (USD)')
    st.plotly_chart(fig_stock)

    
    fig_volume = px.bar(filtered_data, x='date', y='volume')
    fig_volume.update_layout(xaxis_title='Date (YYYY/MM/DD)', yaxis_title='Volume')

    st.plotly_chart(fig_volume)


    if show_data:
        st.write('See complete data below:')
        st.dataframe(selected_company_df)

    if show_candlestick:
        fig_candle = go.Figure(go.Candlestick(
                                              x=filtered_data['date'],
                                              open=filtered_data['open'],
                                              high=filtered_data['high'],
                                              low =filtered_data['low'],
                                              close=filtered_data['close']))
        fig_candle.update_xaxes(title_text='Date')
        fig_candle.update_yaxes(title_text='Prices')
        st.plotly_chart(fig_candle)

with tab3:
    st.title('Placeholder')
