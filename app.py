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

    # ✅ IMPORTANT: NUMBERS (not strings)
    payload = {
        "IDX_I": [13, 51, 21]   # NIFTY, SENSEX, VIX
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()

        # Debug (remove later if needed)
        st.write("API RESPONSE:", data)

        return {
            "NIFTY": data.get("data", {}).get("13", {}).get("last_price", "--"),
            "SENSEX": data.get("data", {}).get("51", {}).get("last_price", "--"),
            "VIX": data.get("data", {}).get("21", {}).get("last_price", "--")
        }

    except Exception as e:
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
st.stop()
