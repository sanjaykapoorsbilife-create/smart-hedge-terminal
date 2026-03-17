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

# ----------- GET LIVE DATA -----------
def get_nifty_price():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = {
        "IDX_I": ["NIFTY"]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        return data["data"]["NIFTY"]["last_price"]
    except:
        return "Error"

# ----------- UI HEADER -----------
st.title("Smart Hedge AI Terminal V23")

# ----------- LIVE DATA DISPLAY -----------
col1, col2, col3 = st.columns(3)

nifty = get_nifty_price()

col1.metric("NIFTY", nifty)
col2.metric("SENSEX", "Loading...")
col3.metric("VIX", "Loading...")

# ----------- AUTO REFRESH -----------
time.sleep(5)
st.rerun()
