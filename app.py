import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

# AUTO REFRESH EVERY 5 SECONDS
st_autorefresh(interval=5000, key="datarefresh")

st.title("Smart Hedge AI Terminal")

# FETCH LIVE DATA
nifty = yf.Ticker("^NSEI")
sensex = yf.Ticker("^BSESN")
vix = yf.Ticker("^INDIAVIX")

nifty_price = nifty.history(period="1d")["Close"].iloc[-1]
sensex_price = sensex.history(period="1d")["Close"].iloc[-1]
vix_price = vix.history(period="1d")["Close"].iloc[-1]

# MARKET OVERVIEW
col1, col2, col3 = st.columns(3)

col1.metric("NIFTY 50", round(nifty_price,2))
col2.metric("SENSEX", round(sensex_price,2))
col3.metric("INDIA VIX", round(vix_price,2))

st.divider()

# NIFTY LIVE CHART
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

# TERMINAL PANELS
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("AI Confidence")
    st.metric("Confidence Score", "74%")

with col5:
    st.subheader("Expected Move")
    st.write("180 Points")
    st.write("Range: 24650 – 25030")

with col6:
    st.subheader("Volatility Engine")
    st.success("VOLATILITY EXPANSION")

st.divider()

# OPTIONS + SIGNAL
col7, col8 = st.columns(2)

with col7:
    st.subheader("Options Intelligence")

    st.write("PCR: 1.14")
    st.write("Max Pain: 24800")
    st.write("Call Writing: 25000")
    st.write("Put Writing: 24700")

with col8:
    st.subheader("AI Signal Panel")

    st.success("""
STRONG TRADE SIGNAL

Market: NIFTY 50

Strategy: Volatility Expansion

Trade:
Buy 24900 CE
Buy 24700 PE

Stop Loss: 30

Targets:
60 / 90 / 150

Confidence: 74%
""")
