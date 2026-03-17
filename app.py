import streamlit as st
import requests
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Hedge V23", layout="wide")

# ---------------- DHAN SECRETS ----------------
CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]

headers = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ---------------- FETCH LIVE DATA ----------------
def get_index_price(security_id):
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": [
            {
                "exchangeSegment": "IDX_I",
                "securityId": security_id
            }
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        return data["data"][0]["last_price"]
    except:
        return "--"

# ---------------- GET DATA ----------------
nifty = get_index_price("13")      # NIFTY
sensex = get_index_price("51")    # SENSEX
vix = get_index_price("17")       # INDIA VIX

# ---------------- UI ----------------
st.markdown("## 📊 Smart Hedge AI Terminal V23")

col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", nifty)
col2.metric("SENSEX", sensex)
col3.metric("VIX", vix)
col4.metric("STATUS", "LIVE")

# ---------------- AUTO REFRESH SAFE ----------------
st.write("Refreshing in 5 sec...")
time.sleep(5)
st.stop()
