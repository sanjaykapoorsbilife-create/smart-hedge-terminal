import streamlit as st
import time
from live_data import live_prices, start_background_ws

st.set_page_config(page_title="Smart Hedge V23", layout="wide")

# START WEBSOCKET (only once)
if "ws_started" not in st.session_state:
    start_background_ws()
    st.session_state.ws_started = True

st.title("📊 Smart Hedge AI Terminal V23")

col1, col2, col3, col4 = st.columns(4)

col1.metric("NIFTY", live_prices["NIFTY"])
col2.metric("SENSEX", live_prices["SENSEX"])
col3.metric("VIX", live_prices["VIX"])
col4.metric("STATUS", "LIVE")

st.write("Live updating...")
time.sleep(2)
st.stop()
