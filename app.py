import streamlit as st
import requests
import time

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="Smart Hedge V23", layout="wide")

# ----------- DHAN API (FROM SECRETS) -----------
CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]

headers = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ----------- FETCH LIVE DATA -----------
def get_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": [13, 51, 21]   # NIFTY, SENSEX, VIX
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()

        idx_data = data.get("data", {}).get("IDX_I", {})

        return {
            "NIFTY": idx_data.get(13, {}).get("last_price", "--"),
            "SENSEX": idx_data.get(51, {}).get("last_price", "--"),
            "VIX": idx_data.get(21, {}).get("last_price", "--")
        }

    except Exception:
        return {
            "NIFTY": "Error",
            "SENSEX": "Error",
            "VIX": "Error"
        }

# ----------- UI -----------
st.title("📊 Smart Hedge AI Terminal V23")

data = get_data()

col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", data["NIFTY"])
col2.metric("SENSEX", data["SENSEX"])
col3.metric("VIX", data["VIX"])
col4.metric("STATUS", "LIVE")

# ----------- AUTO REFRESH -----------
st.write("Refreshing in 5 sec...")
time.sleep(5)
st.rerun()
