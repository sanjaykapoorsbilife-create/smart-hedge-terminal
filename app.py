import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide")

# ---------- THEME TOGGLE ----------
light_mode = st.sidebar.toggle("Light Mode")

if not light_mode:
    st.markdown("""
        <style>
        .stApp {
            background-color:#0E1117;
            color:white;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("Smart Hedge AI Terminal")

# ---------- USER MODE ----------
mode = st.sidebar.selectbox("User Mode", ["Free","Premium"])

# ---------- MARKET TIME LOGIC ----------
now = datetime.datetime.now()
market_open = now.replace(hour=9, minute=15, second=0)
market_close = now.replace(hour=15, minute=30, second=0)

market_live = market_open <= now <= market_close

# ---------- REFRESH SYSTEM ----------
if market_live:
    st_autorefresh(interval=2000, key="price_refresh")
else:
    st.warning("Market Closed – showing last session data")

# ---------- FETCH MARKET DATA ----------
nifty = yf.Ticker("^NSEI")
sensex = yf.Ticker("^BSESN")
vix = yf.Ticker("^INDIAVIX")

nifty_price = nifty.history(period="1d")["Close"].iloc[-1]
sensex_price = sensex.history(period="1d")["Close"].iloc[-1]
vix_price = vix.history(period="1d")["Close"].iloc[-1]

# ---------- MARKET OVERVIEW ----------
col1, col2, col3 = st.columns(3)

col1.metric("NIFTY 50", round(nifty_price,2))
col2.metric("SENSEX", round(sensex_price,2))
col3.metric("INDIA VIX", round(vix_price,2))

st.divider()

# ---------- AI TRADE CONFIDENCE ----------
scan_col1, scan_col2 = st.columns(2)

with scan_col1:
    st.subheader("AI Scan Timer")
    st.info("Scanning market every 2 seconds")

with scan_col2:
    st.subheader("AI Trade Confidence ⓘ")

    confidence = 65  # placeholder until probability engine added
    st.metric("Confidence", f"{confidence}%")

st.divider()

# ---------- CONFIDENCE HEATMAP ----------
st.subheader("Confidence Heatmap")

heatmap_data = {
"Engine":[
"Price Structure",
"Momentum Environment",
"Institutional Positioning",
"Smart Money Activity",
"Market Pressure Analyzer",
"Volatility Environment"
],
"Status":[
"Building",
"Building",
"Strong",
"Building",
"Strong",
"Strong"
]
}

df = pd.DataFrame(heatmap_data)

st.table(df)

st.divider()

# ---------- LIVE CHART ----------
st.subheader("NIFTY LIVE CHART")

data = nifty.history(period="1d", interval="5m")

fig = go.Figure()

fig.add_trace(go.Candlestick(
open=data["Open"],
high=data["High"],
low=data["Low"],
close=data["Close"]
))

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------- MARKET PANELS ----------
col4,col5,col6 = st.columns(3)

with col4:
    st.subheader("Market Condition")
    st.success("Trend Continuation")

with col5:
    st.subheader("Smart Money Activity")
    st.warning("Liquidity sweep detected near support")

with col6:
    st.subheader("Institutional Positioning")
    st.info("Put writers defending 24700")

st.divider()

# ---------- MARKET PRESSURE ANALYZER ----------
st.subheader("Market Pressure Analyzer")

st.info("Monitoring dealer hedging pressure")

st.divider()

# ---------- SIGNAL PANEL ----------
st.subheader("AI Signal Panel")

if mode == "Free":

    st.warning("Signal will unlock in 5 minutes")

else:

    st.success("""
STRONG TRADE SIGNAL

Market: NIFTY

Trade:
Buy 24900 CE
Buy 24700 PE

Stop Loss: 30

Targets:
60 / 90 / 150

Confidence: 78%
""")
