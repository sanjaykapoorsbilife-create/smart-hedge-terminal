import streamlit as st
import requests
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz

# ----------- AUTO REFRESH -----------
st_autorefresh(interval=5000, key="refresh")

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="Smart Hedge V23", layout="wide")

# ----------- DHAN API -----------
CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]

headers = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ----------- MARKET STATUS -----------
def get_market_status():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    hour = now.hour
    minute = now.minute
    day = now.weekday()

    if day >= 5:
        return "CLOSED"

    if (hour > 9 or (hour == 9 and minute >= 15)) and (hour < 15 or (hour == 15 and minute <= 30)):
        return "LIVE"
    else:
        return "CLOSED"


# ----------- LIVE DATA (DHAN) -----------
def get_ltp():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": [13, 51, 21]
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=3)
        data = res.json().get("data", {}).get("IDX_I", {})

        return {
            "NIFTY": data.get("13", {}).get("last_price"),
            "SENSEX": data.get("51", {}).get("last_price"),
            "VIX": data.get("21", {}).get("last_price")
        }
    except:
        return {"NIFTY": None, "SENSEX": None, "VIX": None}


# ----------- PREVIOUS CLOSE -----------
@st.cache_data(ttl=3600)
def get_prev_close():
    try:
        nifty = yf.Ticker("^NSEI").history(period="2d")["Close"]
        sensex = yf.Ticker("^BSESN").history(period="2d")["Close"]
        vix = yf.Ticker("^INDIAVIX").history(period="2d")["Close"]

        return {
            "NIFTY": round(nifty.iloc[-2], 2),
            "SENSEX": round(sensex.iloc[-2], 2),
            "VIX": round(vix.iloc[-2], 2)
        }
    except:
        return {"NIFTY": None, "SENSEX": None, "VIX": None}


# ----------- GIFT NIFTY (FIXED SYMBOL) -----------
def get_gift_nifty():
    try:
        gift = yf.Ticker("NIFTY=F").history(period="1d", interval="1m")
        return round(gift["Close"].iloc[-1], 2)
    except:
        return None


# ----------- CALCULATION -----------
def calc(curr, prev):
    if curr is None or prev is None:
        return None, None
    chg = curr - prev
    pct = (chg / prev) * 100
    return round(chg, 2), round(pct, 2)


# ----------- CLEAN FORMAT (NO ARROWS) -----------
def format_data(chg, pct):
    if chg is None:
        return None
    return f"{chg} ({pct}%)"


def market_phase(vix):
    if vix is None:
        return "Loading..."
    if vix > 18:
        return "🔥 HIGH VOLATILITY"
    elif vix < 13:
        return "😴 LOW VOLATILITY"
    else:
        return "⚖️ NORMAL"


# ----------- UI -----------
st.title("📊 Smart Hedge AI Terminal V23")

ltp = get_ltp()
prev = get_prev_close()
gift = get_gift_nifty()

n_chg, n_pct = calc(ltp["NIFTY"], prev["NIFTY"])
s_chg, s_pct = calc(ltp["SENSEX"], prev["SENSEX"])
v_chg, v_pct = calc(ltp["VIX"], prev["VIX"])

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("NIFTY", ltp["NIFTY"] or "--", format_data(n_chg, n_pct))
col2.metric("SENSEX", ltp["SENSEX"] or "--", format_data(s_chg, s_pct))
col3.metric("VIX", ltp["VIX"] or "--", format_data(v_chg, v_pct))
col4.metric("STATUS", get_market_status())
col5.metric("GIFT NIFTY", gift if gift else "--")

st.subheader(f"Market Phase: {market_phase(ltp['VIX'])}")

# ----------- ERROR HANDLING -----------
if ltp["NIFTY"] is None:
    st.error("❌ Live data error from Dhan API")

st.caption("Live updating every 5 sec ⚡")


# ==========================================
# 🔷 PANEL 1 — MARKET INTELLIGENCE (REAL)
# ==========================================

import numpy as np
import yfinance as yf

# ------------------------------
# 📊 FETCH INTRADAY DATA
# ------------------------------
@st.cache_data(ttl=60)
def get_intraday_data():
    try:
        df = yf.Ticker("^NSEI").history(period="1d", interval="5m")
        return df
    except:
        return None

# ------------------------------
# 🧠 MARKET PHASE (VOLATILITY + BREAKOUT)
# ------------------------------
def calculate_market_phase(df):
    if df is None or len(df) < 20:
        return "Loading..."

    high = df["High"].rolling(10).max()
    low = df["Low"].rolling(10).min()

    if df["Close"].iloc[-1] > high.iloc[-2]:
        return "🔥 EXPANSION (BREAKOUT)"
    elif df["Close"].iloc[-1] < low.iloc[-2]:
        return "🔻 BREAKDOWN"
    else:
        return "🟡 RANGE"

# ------------------------------
# 🚀 APPLY REAL LOGIC
# ------------------------------
df = get_intraday_data()

if df is not None and len(df) > 20:

    current_price = df["Close"].iloc[-1]
    prev_price = df["Close"].iloc[-5]

    # ------------------------------
    # MOMENTUM
    # ------------------------------
    if current_price > prev_price:
        momentum = "🟢 STRONG"
    else:
        momentum = "🔴 WEAK"

    # ------------------------------
    # STRUCTURE
    # ------------------------------
    high = df["High"].rolling(10).max().iloc[-2]
    low = df["Low"].rolling(10).min().iloc[-2]

    if current_price > high:
        structure = "🟢 UPTREND"
    elif current_price < low:
        structure = "🔴 DOWNTREND"
    else:
        structure = "🟡 SIDEWAYS"

    # ------------------------------
    # PRESSURE
    # ------------------------------
    if df["Close"].iloc[-1] > df["Open"].iloc[-1]:
        pressure = "🟢 BUY PRESSURE"
    else:
        pressure = "🔴 SELL PRESSURE"

    # ------------------------------
    # PHASE
    # ------------------------------
    phase = calculate_market_phase(df)

else:
    momentum = "Loading..."
    structure = "Loading..."
    pressure = "Loading..."
    phase = "Loading..."

# ------------------------------
# 🧠 UI DISPLAY
# ------------------------------
st.markdown("## 🧠 Market Intelligence Panel")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Phase", phase)
col2.metric("Momentum", momentum)
col3.metric("Structure", structure)
col4.metric("Pressure", pressure)

# ------------------------------
# 🎯 FINAL DIRECTION
# ------------------------------
direction = final_direction(phase, momentum, structure, pressure)

st.markdown(f"## 🎯 Market Direction: {direction}")

    



# ----------- FINAL DIRECTION LOGIC -----------

def final_direction(phase, momentum, structure, pressure):

    bullish = 0
    bearish = 0

    # 1️⃣ Market Phase
    if "EXPANSION" in phase:
        bullish += 2
    elif "BREAKDOWN" in phase:
        bearish += 2

    # 2️⃣ Momentum
    if "STRONG" in momentum:
        bullish += 2
    elif "WEAK" in momentum:
        bearish += 2

    # 3️⃣ Structure
    if "UPTREND" in structure:
        bullish += 3
    elif "DOWNTREND" in structure:
        bearish += 3

    # 4️⃣ Pressure
    if "BUY" in pressure:
        bullish += 1
    elif "SELL" in pressure:
        bearish += 1

    # 🚫 SIDEWAYS FILTER (VERY IMPORTANT)
    if "SIDEWAYS" in structure:
        return "🟡 SIDEWAYS / NO TRADE"

    # 🎯 FINAL DECISION
    if bullish - bearish >= 3:
        return "🟢 STRONG BULLISH"

    elif bearish - bullish >= 3:
        return "🔴 STRONG BEARISH"

    else:
        return "🟡 SIDEWAYS / NO TRADE"


direction = final_direction(phase, momentum, structure, pressure)

st.markdown(f"## 🎯 Market Direction: {direction}")
