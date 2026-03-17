import streamlit as st
import requests
import time

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
        "IDX_I": ["NIFTY"]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        return data.get("data", {}).get("NIFTY", {}).get("last_price", "--")
    except:
        return "Error"

# ----------- UI -----------
st.title("📊 Smart Hedge AI Terminal V23")

nifty = get_index_data()

st.metric("NIFTY", nifty)

# ----------- SAFE REFRESH -----------
st.write("Refreshing in 5 sec...")
time.sleep(5)
st.stop()
