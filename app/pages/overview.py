import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Get data from session state
complete_ticker_df = st.session_state['daily_data']
company_df = st.session_state['company_data']

# list tickers

# for each ticker filter for symbol and then select the last returns p (which will be columns 8)

# add those last numbers to the 

data_argenx_today = data_argenx.iloc[-1, 8]
data_gmab_today = data_gmab.iloc[-1, 8]

data_overview.loc[data_overview['Symbol'] == 'ARGX', 'returns_p'] = data_argenx_today
data_overview.loc[data_overview['Symbol'] == 'GMAB', 'returns_p'] = data_gmab_today


fig = px.treemap(
    data_overview,
    path=['Sector', 'Symbol'],
    values='MarketCapitalization',
    color='returns_p',
    color_continuous_midpoint=0,
    color_continuous_scale='RdYlGn',
    custom_data=['returns_p']
)

fig.update_layout(coloraxis_showscale=False)
fig.update_traces(hovertemplate='<b>%{label}</b><br>Market Cap: %{value}<br>Return: %{customdata[0]:.2f}%<extra></extra>')


st.plotly_chart(fig)
