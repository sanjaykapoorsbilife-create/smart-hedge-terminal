import streamlit as st
import requests
import time

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
def get_index_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": ["NIFTY", "SENSEX", "INDIA VIX"]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json().get("data", {})
    except:
        return {}

# ----------- UI -----------
st.markdown("## 📊 Smart Hedge AI Terminal V23")

data = get_index_data()

col1, col2, col3, col4 = st.columns(4)

nifty = data.get("NIFTY", {}).get("last_price", "--")
sensex = data.get("SENSEX", {}).get("last_price", "--")
vix = data.get("INDIA VIX", {}).get("last_price", "--")

col1.metric("NIFTY", nifty)
col2.metric("SENSEX", sensex)
col3.metric("VIX", vix)
col4.metric("STATUS", "LIVE")

# ----------- AUTO REFRESH SAFE -----------
time.sleep(5)
st.experimental_rerun()
