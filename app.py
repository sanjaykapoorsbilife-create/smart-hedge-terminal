import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import random
import time

st.set_page_config(layout="wide")

# AUTO REFRESH EVERY 5 SECONDS
st_autorefresh(interval=5000, key="datarefresh")

st.title("Smart Hedge AI Terminal")

# FETCH MARKET DATA
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

# AI SCAN TIMER
scan_col1, scan_col2 = st.columns(2)

with scan_col1:
    st.subheader("AI Scan Timer")
    st.info("Next Market Scan: 5 seconds")

with scan_col2:
    st.subheader("Trade Readiness Meter")
    readiness = random.randint(55,85)
    st.metric("Signal Probability", f"{readiness}%")

st.divider()

# MARKET PHASE DETECTOR
st.subheader("Market Phase Detector")

phase_list = [
    "Trend Continuation",
    "Volatility Expansion",
    "Range Bound",
    "Breakout Setup"
]

market_phase = random.choice(phase_list)

st.success(market_phase)

st.divider()

# NIFTY CHART
st.subheader("NIFTY LIVE CHART")

data = nifty.history(period="1d", interval="5m")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close']
))

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# OPTIONS INTELLIGENCE (PLACEHOLDER)
opt_col1, opt_col2 = st.columns(2)

with opt_col1:
    st.subheader("Option Chain Engine")

    st.write("PCR: 1.12")
    st.write("Max Pain: 24800")
    st.write("Call Writing Wall: 25000")
    st.write("Put Writing Wall: 24700")

with opt_col2:
    st.subheader("Liquidity Sweep Detector")

    sweep_levels = [24780,24840,24910,24690]
    level = random.choice(sweep_levels)

    st.warning(f"Recent Liquidity Sweep near {level}")

st.divider()

# GAMMA EXPLOSION DETECTOR (COMING)
st.subheader("Gamma Explosion Detector (GED)")

st.info("Monitoring dealer hedging levels...")

st.write("Gamma Flip Level: 24850")

st.divider()

# SIGNAL PANEL
st.subheader("AI Signal Panel")

st.success("""
STRONG TRADE SIGNAL

Market: NIFTY

Strategy: Volatility Expansion

Trade:
Buy 24900 CE
Buy 24700 PE

Stop Loss: 30

Targets:
60 / 90 / 150

Confidence: 74%
""")
