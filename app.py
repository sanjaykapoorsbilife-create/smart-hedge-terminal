import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")

st.title("Smart Hedge AI Terminal")

# LIVE TIMER
placeholder = st.empty()

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = f"Next AI Signal Update: {mins:02d}:{secs:02d}"
        placeholder.info(timer)
        time.sleep(1)
        t -= 1

countdown(60)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Market Overview")
    st.metric("NIFTY 50", "24,820", "+0.62%")
    st.metric("SENSEX", "81,450", "+0.54%")

with col2:
    st.subheader("AI Confidence")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 74,
        gauge = {'axis': {'range': [0,100]},
        'bar': {'color': "green"}}))
    st.plotly_chart(fig)

with col3:
    st.subheader("Volatility Meter")
    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 65,
        gauge = {'axis': {'range': [0,100]},
        'bar': {'color': "orange"}}))
    st.plotly_chart(fig2)

st.subheader("AI Signal Panel")

st.success("""
🟢 STRONG TRADE SIGNAL

Market: NIFTY 50

Strategy: Volatility Expansion

Trade:
Buy 24900 CE
Buy 24700 PE

Stop Loss: 30

Targets:
60 / 90 / 150
""")

st.subheader("Options Intelligence")

data = {
"Indicator":["PCR","Max Pain","Call Writing","Put Writing"],
"Value":["1.14","24800","25000","24700"]
}

df = pd.DataFrame(data)

st.table(df)

st.subheader("Market Heatmap")

heatmap_data = pd.DataFrame({
    "Sector":["Banking","IT","Pharma","Auto","FMCG"],
    "Strength":[80,30,70,55,60]
})

st.bar_chart(heatmap_data.set_index("Sector"))

st.sidebar.title("Smart Hedge AI")

st.sidebar.info("""
AI ENGINE ANALYZING MARKET...
● ● ●
""")
