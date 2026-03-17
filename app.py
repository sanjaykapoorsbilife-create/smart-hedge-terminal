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
def get_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": [13, 51, 21]
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=3)
        data = res.json()

        idx_data = data.get("data", {}).get("IDX_I", {})

        return {
            "NIFTY": idx_data.get(13, {}).get("last_price"),
            "SENSEX": idx_data.get(51, {}).get("last_price"),
            "VIX": idx_data.get(21, {}).get("last_price")
        }

    except:
        return None

# ----------- UI -----------
st.title("📊 Smart Hedge AI Terminal V23")

placeholder = st.empty()

while True:
    data = get_data()

    with placeholder.container():
        col1, col2, col3, col4 = st.columns(4)

        if data:
            col1.metric("NIFTY", data["NIFTY"])
            col2.metric("SENSEX", data["SENSEX"])
            col3.metric("VIX", data["VIX"])
        else:
            col1.metric("NIFTY", "Loading...")
            col2.metric("SENSEX", "Loading...")
            col3.metric("VIX", "Loading...")

        col4.metric("STATUS", "LIVE")

        st.caption("Auto refreshing every 5 seconds...")

    time.sleep(5)
