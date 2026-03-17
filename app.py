import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# ----------- AUTO REFRESH (STABLE) -----------
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

# ----------- FETCH DATA -----------
def get_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": [13, 51, 21]  # NIFTY, SENSEX, VIX
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=3)
        data = res.json()

        idx_data = data.get("data", {}).get("IDX_I", {})

        return {
            "NIFTY": idx_data.get("13", {}).get("last_price", None),
            "SENSEX": idx_data.get("51", {}).get("last_price", None),
            "VIX": idx_data.get("21", {}).get("last_price", None)
        }

    except:
        return {"NIFTY": None, "SENSEX": None, "VIX": None}

# ----------- SESSION STATE (STORE PREVIOUS DATA) -----------
if "prev_data" not in st.session_state:
    st.session_state.prev_data = {"NIFTY": None, "SENSEX": None, "VIX": None}

# ----------- HELPER FUNCTIONS -----------

def get_delta(curr, prev):
    if curr is None or prev is None:
        return None
    return round(curr - prev, 2)

def format_delta(delta):
    if delta is None:
        return None
    if delta > 0:
        return f"▲ {delta}"
    elif delta < 0:
        return f"▼ {abs(delta)}"
    else:
        return "• 0"

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

data = get_data()

# ----------- DELTA CALCULATION -----------
nifty_delta = get_delta(data["NIFTY"], st.session_state.prev_data["NIFTY"])
sensex_delta = get_delta(data["SENSEX"], st.session_state.prev_data["SENSEX"])
vix_delta = get_delta(data["VIX"], st.session_state.prev_data["VIX"])

# ----------- FORMAT DELTA -----------
nifty_text = format_delta(nifty_delta)
sensex_text = format_delta(sensex_delta)
vix_text = format_delta(vix_delta)

# ----------- METRICS -----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", data["NIFTY"] if data["NIFTY"] else "--", nifty_text)
col2.metric("SENSEX", data["SENSEX"] if data["SENSEX"] else "--", sensex_text)
col3.metric("VIX", data["VIX"] if data["VIX"] else "--", vix_text)
col4.metric("STATUS", "LIVE")

# ----------- MARKET PHASE -----------
st.subheader(f"Market Phase: {market_phase(data['VIX'])}")

# ----------- ERROR HANDLING -----------
if data["NIFTY"] is None:
    st.warning("⚠️ Data fetch issue — check API / internet")

# ----------- SAVE CURRENT DATA -----------
st.session_state.prev_data = data

# ----------- FOOTER -----------
st.caption("Live auto-refresh every 5 seconds 🚀")
