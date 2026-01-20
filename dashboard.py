import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("ShieldX – Live Mitigation Monitor")

# ---- Persistent containers ----
chart_container = st.container()
stats_container = st.container()
sig_container = st.container()

# ---- Session history ----
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["RPS"])

def get_metrics():
    try:
        return requests.get("http://localhost:4000/metrics", timeout=1).json()
    except:
        return {"rps": 0, "attacks": 0}

def get_signatures():
    try:
        return requests.get("http://localhost:4000/signatures", timeout=1).json()
    except:
        return {"rules": []}

# ================= DATA =================

metrics = get_metrics()
rps = metrics["rps"]
attacks = metrics["attacks"]

# ---- Update RPS history ----
st.session_state.history = pd.concat(
    [st.session_state.history, pd.DataFrame({"RPS": [rps]})],
    ignore_index=True
)

if len(st.session_state.history) > 20:
    st.session_state.history = st.session_state.history.iloc[-20:]

# ================= UI =================

with chart_container:
    st.subheader("Traffic Rate (RPS – Last 20 samples)")
    st.line_chart(st.session_state.history, use_container_width=True)

with stats_container:
    col1, col2 = st.columns(2)
    col1.metric("Current RPS", rps)
    col2.metric("Total Attacks Blocked", attacks)

with sig_container:
    with st.expander("Attack Signatures (latest)"):
        st.json(get_signatures())

st.success("Dashboard connected to ShieldX")

time.sleep(2)
st.rerun()
