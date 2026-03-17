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
