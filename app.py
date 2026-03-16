import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")

st.title("Smart Hedge AI Terminal")

# TIMER
placeholder = st.empty()

for seconds in range(60,0,-1):
    placeholder.info(f"Next AI Signal Update: 00:{seconds:02d}")
    time.sleep(1)

# LIVE DATA
nifty = yf.Ticker("^NSEI")
sensex = yf.Ticker("^BSESN")
vix = yf.Ticker("^INDIAVIX")

nifty_price = nifty.history(period="1d")["Close"].iloc[-1]
sensex_price = sensex.history(period="1d")["Close"].iloc[-1]
vix_price = vix.history(period="1d")["Close"].iloc[-1]

col1,col2,col3 = st.columns(3)

col1.metric("NIFTY 50", round(nifty_price,2))
col2.metric("SENSEX", round(sensex_price,2))
col3.metric("INDIA VIX", round(vix_price,2))

st.divider()

st.subheader("NIFTY LIVE CHART")

data = nifty.history(period="1d", interval="5m")

fig = go.Figure()

fig.add_trace(go.Candlestick(
open=data['Open'],
high=data['High'],
low=data['Low'],
close=data['Close']
))

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("AI Signal Panel")

st.success("""
STRONG TRADE SIGNAL

Market: NIFTY 50

Strategy: Volatility Expansion

Trade:
Buy 24900 CE
Buy 24700 PE

Stop Loss: 30

Targets: 60 / 90 / 150

Confidence: 74%
""")
