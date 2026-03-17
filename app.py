import streamlit as st
import requests
import time

st.set_page_config(page_title="Smart Hedge V23", layout="wide")

# ----------- SECRETS -----------
CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]

headers = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ----------- FETCH DATA -----------
def get_data():
    url = "https://api.dhan.co/v2/market/quote"

    payload = {
        "IDX_I": ["13", "51", "17"]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()

        result = {"NIFTY": "--", "SENSEX": "--", "VIX": "--"}

        if "data" in data:
            idx = data["data"].get("IDX_I", {})

            result["NIFTY"] = idx.get("13", {}).get("last_price", "--")
            result["SENSEX"] = idx.get("51", {}).get("last_price", "--")
            result["VIX"] = idx.get("17", {}).get("last_price", "--")

        return result

    except Exception as e:
        st.write("ERROR:", e)
        return {"NIFTY": "--", "SENSEX": "--", "VIX": "--"}

# ----------- UI -----------
st.title("📊 Smart Hedge AI Terminal V23")

data = get_data()

col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", data["NIFTY"])
col2.metric("SENSEX", data["SENSEX"])
col3.metric("VIX", data["VIX"])
col4.metric("STATUS", "LIVE")

# ----------- REFRESH -----------
st.write("Refreshing in 5 sec...")
time.sleep(5)
st.stop()
