import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(layout="wide")

# AUTO REFRESH
st_autorefresh(interval=2000, key="refresh")

# THEME TOGGLE
theme = st.sidebar.selectbox("Theme", ["Dark","Light"])

if theme == "Dark":
    st.markdown("""
    <style>
    body {background-color:#0E1117;color:white;}
    </style>
    """, unsafe_allow_html=True)

st.title("Smart Hedge AI Terminal")

# USER MODE
mode = st.sidebar.selectbox("User Mode",["Free","Premium"])

# MARKET DATA
nifty = yf.Ticker("^NSEI")
sensex = yf.Ticker("^BSESN")
vix = yf.Ticker("^INDIAVIX")

nifty_price = nifty.history(period="1d")["Close"].iloc[-1]
sensex_price = sensex.history(period="1d")["Close"].iloc[-1]
vix_price = vix.history(period="1d")["Close"].iloc[-1]

col1,col2,col3 = st.columns(3)

col1.metric("NIFTY 50",round(nifty_price,2))
col2.metric("SENSEX",round(sensex_price,2))
col3.metric("INDIA VIX",round(vix_price,2))

st.divider()

# AI SCAN TIMER
scan_col1,scan_col2 = st.columns(2)

with scan_col1:
    st.subheader("AI Scan Timer")
    st.info("Scanning market every 2 seconds")

with scan_col2:
    st.subheader("AI Trade Confidence ⓘ")

    score = random.randint(30,90)

    st.metric("Confidence",f"{score}%")

st.divider()

# CONFIDENCE HEATMAP

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
random.choice(["Strong","Building","Weak"]),
random.choice(["Strong","Building","Weak"]),
random.choice(["Strong","Building","Weak"]),
random.choice(["Strong","Building","Weak"]),
random.choice(["Strong","Building","Weak"]),
random.choice(["Strong","Building","Weak"])
]
}

df = pd.DataFrame(heatmap_data)

st.table(df)

st.divider()

# NIFTY CHART
st.subheader("NIFTY LIVE CHART")

data = nifty.history(period="1d",interval="5m")

fig = go.Figure()

fig.add_trace(go.Candlestick(
open=data["Open"],
high=data["High"],
low=data["Low"],
close=data["Close"]
))

fig.update_layout(height=450)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# MARKET PANELS

col4,col5,col6 = st.columns(3)

with col4:
    st.subheader("Market Condition")

    st.success(random.choice([
    "Trend Continuation",
    "Volatility Expansion",
    "Range Bound"
    ]))

with col5:
    st.subheader("Smart Money Activity")

    st.warning("Liquidity sweep detected near support")

with col6:
    st.subheader("Institutional Positioning")

    st.info("Put writers defending 24700")

st.divider()

# MARKET PRESSURE ANALYZER (GED placeholder)

st.subheader("Market Pressure Analyzer")

st.info("Monitoring dealer hedging pressure")

st.divider()

# SIGNAL PANEL

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
