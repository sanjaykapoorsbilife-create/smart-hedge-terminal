import streamlit as st
import requests
import time

st.set_page_config(page_title="Smart Hedge V23", layout="wide")

# ---------------- SECRETS ----------------
CLIENT_ID = st.secrets["DHAN_CLIENT_ID"]
ACCESS_TOKEN = st.secrets["DHAN_ACCESS_TOKEN"]

headers = {
    "access-token": ACCESS_TOKEN,
    "client-id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ---------------- FETCH DATA ----------------
def get_data():
    url = "https://api.dhan.co/v2/marketfeed/ltp"

    payload = [
        {"exchangeSegment": "IDX_I", "securityId": "13"},  # NIFTY
        {"exchangeSegment": "IDX_I", "securityId": "51"},  # SENSEX
        {"exchangeSegment": "IDX_I", "securityId": "17"}   # VIX
    ]

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()

        result = {"NIFTY": "--", "SENSEX": "--", "VIX": "--"}

        if isinstance(data.get("data"), list):
            for item in data["data"]:
                sid = item.get("securityId")
                if sid == "13":
                    result["NIFTY"] = item.get("last_price", "--")
                elif sid == "51":
                    result["SENSEX"] = item.get("last_price", "--")
                elif sid == "17":
                    result["VIX"] = item.get("last_price", "--")

        return result

    except Exception as e:
        st.write("ERROR:", e)
        return {"NIFTY": "--", "SENSEX": "--", "VIX": "--"}

# ---------------- UI ----------------
st.title("📊 Smart Hedge AI Terminal V23")

data = get_data()

col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", data["NIFTY"])
col2.metric("SENSEX", data["SENSEX"])
col3.metric("VIX", data["VIX"])
col4.metric("STATUS", "LIVE")

# ---------------- REFRESH ----------------
st.write("Refreshing in 5 sec...")
time.sleep(5)
st.stop()
