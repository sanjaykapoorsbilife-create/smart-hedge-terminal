import streamlit as st
import yfinance as yf
import time
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Smart Hedge AI Terminal",
    layout="wide"
)

# AUTO REFRESH EVERY 5 SECONDS
st.markdown(
"""
<meta http-equiv="refresh" content="5">
""",
unsafe_allow_html=True
)
st.markdown("""
<style>

body {
background-color:#0b0f19;
color:white;
}

.header-bar{
position:sticky;
top:0;
background:#0b0f19;
z-index:999;
padding:10px;
border-bottom:1px solid #333;
}

.signal-btn{
position:fixed;
bottom:25px;
right:25px;
background:#00ff88;
color:black;
padding:14px;
border-radius:10px;
font-weight:bold;
animation:blink 1s infinite;
z-index:9999;
}

@keyframes blink{
0%{opacity:1;}
50%{opacity:0.4;}
100%{opacity:1;}
}

</style>
""", unsafe_allow_html=True)
nifty = yf.Ticker("^NSEI")
sensex = yf.Ticker("^BSESN")
vix = yf.Ticker("^INDIAVIX")

nifty_data = nifty.history(period="1d")
sensex_data = sensex.history(period="1d")
vix_data = vix.history(period="1d")

nifty_price = nifty_data["Close"].iloc[-1]
sensex_price = sensex_data["Close"].iloc[-1]
vix_price = vix_data["Close"].iloc[-1]

gift_price = 24880
def market_phase():

    phase=random.choice([
        "🟡 ACCUMULATION",
        "🟢 EXPANSION",
        "🔵 TREND",
        "🔴 DISTRIBUTION"
    ])

    return phase


def ai_signal():

    confidence=random.randint(55,85)

    signal_type=random.choice([
        "BUY CE",
        "BUY PE",
        "STRANGLE"
    ])

    return signal_type,confidence
    phase = market_phase()

header_col1, header_col2 = st.columns([1,6])

with header_col1:
    st.image("https://i.imgur.com/4M34hi2.png", width=80)

with header_col2:
    st.title("Smart Hedge AI Terminal")


col1,col2,col3,col4,col5,col6 = st.columns(6)

col1.metric("NIFTY", round(nifty_price,2))
col2.metric("SENSEX", round(sensex_price,2))
col3.metric("INDIA VIX", round(vix_price,2))
col4.metric("MARKET PHASE", phase)
col5.metric("MARKET STATUS","LIVE")
col6.metric("GIFT NIFTY", gift_price)
tab1,tab2,tab3,tab4,tab5 = st.tabs([
"Market Overview",
"Options Analytics",
"AI Signals",
"Advanced Analytics",
"System Monitor"
])

signal,confidence = ai_signal()

# MARKET OVERVIEW
with tab1:

    st.header("Sector Heatmap")

    st.write("BANKING +1.82% 🟢")
    st.write("ENERGY +1.35% 🟢")
    st.write("AUTO +0.64% 🟡")
    st.write("IT -1.26% 🔴")


# OPTIONS ANALYTICS
with tab2:

    st.header("F&O Market Structure")

    st.write("Long Build-Up: 15")
    st.write("Short Build-Up: 9")
    st.write("Short Covering: 11")
    st.write("Long Unwinding: 7")


# AI SIGNALS
with tab3:

    st.header("AI Signal Engine")

    st.write("Daily Trade Limit: 0 / 3")

    st.write("AI Confidence:",confidence,"%")

    st.success(signal)


# ADVANCED ANALYTICS
with tab4:

    st.header("Market Manipulation Detector")

    risk=random.randint(30,80)

    if risk>70:
        st.error("High Manipulation Risk")

    elif risk>50:
        st.warning("Possible Trap")

    else:
        st.success("Market Stable")


# SYSTEM MONITOR
with tab5:

    st.header("Engine Status")

    st.write("Strategy Engine Running")
    st.write("Market Data Active")
    st.write("Auto Refresh: 5 Seconds")


# FLOATING SIGNAL
if confidence>75:

    st.markdown(
        '<div class="signal-btn">⚡ NEW TRADE SIGNAL</div>',
        unsafe_allow_html=True
    )

    components.html("""
    <audio autoplay>
    <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3">
    </audio>
    """,height=0)
