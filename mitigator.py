from flask import Flask, request, Response
import requests
import time
import json
import os

# ---- our modules ----
from features import add_request, extract_features
from ml_detector import is_attack
from stat_guard import stat_check
from metrics import add_metric, get_metrics   # ✅ correct imports

app = Flask(__name__)

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
TARGET = "http://localhost:5000"      # real backend server

banned = {}          # ip -> unblock time
signatures = []      # generated attack signatures

# ---------------------------------------------------
# PERSISTENT IP MEMORY
# ---------------------------------------------------
MEM_FILE = "ip_memory.json"

def load_memory():
    if os.path.exists(MEM_FILE):
        try:
            return json.load(open(MEM_FILE))
        except:
            return {}
    return {}

def save_memory(data):
    json.dump(data, open(MEM_FILE, "w"), indent=2)

ip_memory = load_memory()

def get_ban_duration(count):
    if count == 1:
        return 120          # 2 min
    elif count == 2:
        return 600          # 10 min
    else:
        return 1800         # 30 min

# ---------------------------------------------------

def add_signature(ip, feature):
    signatures.append({
        "ip": ip,
        "rps": feature[0],
        "burst": feature[1],
        "uniq_ratio": feature[2],
        "avg_gap": feature[3],
        "error_rate": feature[4],
        "time": time.strftime("%H:%M:%S")
    })

def is_banned(ip):
    return ip in banned and banned[ip] > time.time()

# ---------------------------------------------------
# MAIN PROXY
# ---------------------------------------------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):

    ip = request.remote_addr
    now = time.time()

    # ---- Instant block for known repeat offenders ----
    if ip in ip_memory and ip_memory[ip].get("count", 0) >= 2:
        banned[ip] = now + get_ban_duration(ip_memory[ip]["count"])
        add_metric(0, True)     # ✅ still record blocked traffic
        return "Previously identified attacker – instant block", 403

    # ---- Active ban check ----
    if is_banned(ip):
        add_metric(0, True)     # ✅ still record traffic
        return "BLOCKED by ShieldX", 403

    # ---- Log request for feature extraction ----
    add_request(ip, path, 200)

    # ---- Extract behavior features ----
    features = extract_features(ip)

    # ---- Hybrid Detection ----
    ml_decision = is_attack(features)
    stat_decision = stat_check(features)
    decision = ml_decision or stat_decision

    # ---- Update metrics (RPS always updates) ----
    add_metric(features[0], decision)

    # ================= MITIGATION =================
    if decision:
        info = ip_memory.get(ip, {"count": 0})
        info["count"] += 1
        info["last_seen"] = now
        ip_memory[ip] = info
        save_memory(ip_memory)

        banned[ip] = now + get_ban_duration(info["count"])
        add_signature(ip, features)

        return f"Blocked (offense #{info['count']})", 403

    # ================= FORWARD ====================
    try:
        resp = requests.get(f"{TARGET}/{path}", timeout=2)
        return Response(resp.content, status=resp.status_code)
    except Exception as e:
        return f"Backend error: {e}", 500

# ---------------------------------------------------
# MONITORING ENDPOINTS
# ---------------------------------------------------

@app.route("/metrics")
def metrics_api():
    return get_metrics()    # ✅ returns rps + attacks

@app.route("/signatures")
def show_signatures():
    return {"rules": signatures}

@app.route("/banned")
def show_banned():
    return banned

@app.route("/reputation")
def show_reputation():
    return ip_memory

# ---------------------------------------------------

if __name__ == "__main__":
    print("ShieldX Mitigator Running on port 4000")
    app.run(port=4000)
