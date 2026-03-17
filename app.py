import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

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


# ----------- SESSION STATE -----------
if "base_data" not in st.session_state:
    st.session_state.base_data = None


# ----------- CALCULATION FUNCTIONS -----------

def calculate_change(curr, base):
    if curr is None or base is None:
        return None, None
    
    change = curr - base
    percent = (change / base) * 100
    
    return round(change, 2), round(percent, 2)


def format_display(chg, pct):
    if chg is None:
        return None
    if chg > 0:
        return f"▲ {chg} ({pct}%)"
    elif chg < 0:
        return f"▼ {abs(chg)} ({abs(pct)}%)"
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


# ----------- UI START -----------
st.title("📊 Smart Hedge AI Terminal V23")

data = get_data()

# ----------- SET BASE (FIRST VALUE) -----------
if st.session_state.base_data is None and data["NIFTY"] is not None:
    st.session_state.base_data = data


# ----------- CALCULATIONS -----------
base = st.session_state.base_data

nifty_chg, nifty_pct = calculate_change(data["NIFTY"], base["NIFTY"] if base else None)
sensex_chg, sensex_pct = calculate_change(data["SENSEX"], base["SENSEX"] if base else None)
vix_chg, vix_pct = calculate_change(data["VIX"], base["VIX"] if base else None)


# ----------- DISPLAY -----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", data["NIFTY"] if data["NIFTY"] else "--", format_display(nifty_chg, nifty_pct))
col2.metric("SENSEX", data["SENSEX"] if data["SENSEX"] else "--", format_display(sensex_chg, sensex_pct))
col3.metric("VIX", data["VIX"] if data["VIX"] else "--", format_display(vix_chg, vix_pct))
col4.metric("STATUS", "LIVE")


# ----------- MARKET PHASE -----------
st.subheader(f"Market Phase: {market_phase(data['VIX'])}")


# ----------- ERROR HANDLING -----------
if data["NIFTY"] is None:
    st.warning("⚠️ Data fetch issue — check API / internet")


# ----------- FOOTER -----------
st.caption("Live auto-refresh every 5 seconds 🚀")
