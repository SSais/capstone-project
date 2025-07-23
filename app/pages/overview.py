import streamlit as st
import pandas as pd
import plotly.express as px

# Get data from session state
complete_ticker_df = st.session_state['daily_data']
company_df = st.session_state['company_data']

# List tickers
TICKERS = [
    'ARGX',  # Argenx
    'GMAB',  # Genmab
    'AAPL',  # Apple
    'IBM',   # IBM
    ]

# For each ticker filter for symbol and then select the last returns p
for ticker in TICKERS:
    # Filter for the current ticker
    ticker_data = complete_ticker_df[complete_ticker_df['symbol'] == ticker]

    # Get the latest returns_p
    last_return_p = ticker_data['daily_return_p'].iloc[-1]
        
    # Update the 'returns_p' in data_overview for the corresponding symbol
    company_df.loc[company_df['Symbol'] == ticker, 'daily_return_p'] = last_return_p


fig = px.treemap(
    company_df,
    path=['Sector', 'Symbol'],
    values='MarketCapitalization',
    color='daily_return_p',
    color_continuous_midpoint=0,
    color_continuous_scale='RdYlGn',
    custom_data=['daily_return_p']
)

fig.update_layout(coloraxis_showscale=False)
fig.update_traces(hovertemplate='<b>%{label}</b><br>Market Cap: %{value}<br>Return: %{customdata[0]:.2f}%<extra></extra>')


st.plotly_chart(fig)