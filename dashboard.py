import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("ShieldX – Live Mitigation Monitor")

# ---- Containers ----
health_container = st.container()   # ✅ NEW
chart_container = st.container()
stats_container = st.container()
sig_container = st.container()
manual_container = st.container()

# ---- Session history ----
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["RPS"])

# ---------------- API CALLS ----------------
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

# ✅ HEALTH API
def get_health():
    try:
        return requests.get("http://localhost:4000/health", timeout=1).json()
    except:
        return None

# ================= DATA =================
metrics = get_metrics()
health = get_health()

rps = metrics["rps"]
attacks = metrics["attacks"]

st.session_state.history = pd.concat(
    [st.session_state.history, pd.DataFrame({"RPS": [rps]})],
    ignore_index=True
)

if len(st.session_state.history) > 20:
    st.session_state.history = st.session_state.history.iloc[-20:]

# ================= HEALTH UI =================
with health_container:
    st.subheader("🩺 System Health")

    if health:
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("ShieldX", health.get("status", "unknown"))
        col2.metric("Uptime (s)", health.get("uptime_seconds", 0))
        col3.metric("RPS", health.get("current_rps", 0))
        col4.metric("Blocked IPs", health.get("blocked_ips", 0))

        if health.get("backend") == "up":
            col5.success("Backend UP")
        else:
            col5.error("Backend DOWN")
    else:
        st.error("Health endpoint not reachable")

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

# ================= MANUAL OVERRIDE =================
with manual_container:
    st.subheader("Manual IP Override")

    ip = st.text_input("IP Address", placeholder="e.g. 10.0.0.5")

    col1, col2 = st.columns(2)

    if col1.button("🚫 Block IP"):
        if ip:
            r = requests.post("http://localhost:4000/block_ip", json={"ip": ip})
            if r.status_code == 200:
                st.success(f"{ip} blocked")
        else:
            st.warning("Enter IP")

    if col2.button("✅ Unblock IP"):
        if ip:
            r = requests.post("http://localhost:4000/unblock_ip", json={"ip": ip})
            if r.status_code == 200:
                st.success(f"{ip} unblocked")
        else:
            st.warning("Enter IP")

st.success("Dashboard connected to ShieldX")

time.sleep(2)
st.rerun()
