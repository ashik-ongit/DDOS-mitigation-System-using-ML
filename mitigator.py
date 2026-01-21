from flask import Flask, request, Response
import requests
import time
import json
import os

# ---- our modules ----
from features import add_request, extract_features
from ml_detector import is_attack
from stat_guard import stat_check
from metrics import add_metric, get_metrics

app = Flask(__name__)

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
TARGET = "http://localhost:5000"  # real backend server

banned = {}          # ip -> unblock time OR -1 for manual block
signatures = {}      # ip -> attack signature

# ---------------------------------------------------
# START TIME (FOR HEALTH / UPTIME)
# ---------------------------------------------------
START_TIME = time.time()

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
        return 120
    elif count == 2:
        return 600
    else:
        return 1800

# ---------------------------------------------------
# IP RESOLUTION
# ---------------------------------------------------
def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr

# ---------------------------------------------------
# SIGNATURE HANDLING
# ---------------------------------------------------
def add_signature(ip, feature):
    sig = signatures.get(ip, {
        "ip": ip,
        "first_seen": time.strftime("%H:%M:%S"),
        "hits": 0
    })

    sig.update({
        "rps": round(feature[0], 2),
        "burst": feature[1],
        "uniq_ratio": round(feature[2], 3),
        "avg_gap": round(feature[3], 3),
        "error_rate": round(feature[4], 3),
        "last_seen": time.strftime("%H:%M:%S")
    })

    sig["hits"] += 1
    signatures[ip] = sig

def is_banned(ip):
    if ip in banned and banned[ip] == -1:
        return True
    return ip in banned and banned[ip] > time.time()

# ---------------------------------------------------
# BACKEND HEALTH CHECK (LAYER 2)
# ---------------------------------------------------
def check_backend_health():
    try:
        r = requests.get(TARGET, timeout=1)
        return "up" if r.status_code < 500 else "down"
    except:
        return "down"

# ---------------------------------------------------
# MAIN PROXY
# ---------------------------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def proxy(path):

    ip = get_client_ip()
    now = time.time()

    # ---- BANNED IP (ALLOW SIGNATURE EVOLUTION) ----
    if is_banned(ip):
        features = extract_features(ip)        # ✅ NEW (minimal)
        add_signature(ip, features)             # ✅ signature shifts
        add_metric(0, True)
        return "BLOCKED by ShieldX", 403

    # ---- LOG REQUEST ----
    add_request(ip, path, 200)

    # ---- FEATURE EXTRACTION ----
    features = extract_features(ip)

    # ---- DETECTION ----
    ml_decision = is_attack(features)
    stat_decision = stat_check(features)
    decision = ml_decision or stat_decision

    # ---- SIGNATURE UPDATE ON STAT SUSPICION ----
    if stat_decision:
        add_signature(ip, features)             # ✅ signature evolves early

    # ---- METRICS ----
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
# MANUAL OVERRIDE (DASHBOARD)
# ---------------------------------------------------
@app.route("/block_ip", methods=["POST"])
def block_ip():
    data = request.get_json()
    ip = data.get("ip")

    if not ip:
        return {"error": "IP required"}, 400

    banned[ip] = -1
    return {"status": "blocked", "ip": ip}

@app.route("/unblock_ip", methods=["POST"])
def unblock_ip():
    data = request.get_json()
    ip = data.get("ip")

    if not ip:
        return {"error": "IP required"}, 400

    banned.pop(ip, None)
    ip_memory.pop(ip, None)
    save_memory(ip_memory)

    return {"status": "unblocked", "ip": ip}

# ---------------------------------------------------
# HEALTH ENDPOINT (LAYER 1 + LAYER 2)
# ---------------------------------------------------
@app.route("/health")
def health():
    uptime = int(time.time() - START_TIME)

    try:
        metrics = get_metrics()
        rps = metrics.get("rps", 0)
    except:
        rps = 0

    return {
        "status": "ok",
        "uptime_seconds": uptime,
        "current_rps": rps,
        "blocked_ips": len(banned),
        "backend": check_backend_health()
    }

# ---------------------------------------------------
# MONITORING
# ---------------------------------------------------
@app.route("/metrics")
def metrics_api():
    return get_metrics()

@app.route("/signatures")
def show_signatures():
    return {"rules": list(signatures.values())}

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
