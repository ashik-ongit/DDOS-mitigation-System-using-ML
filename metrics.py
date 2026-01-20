import time

state = {
    "count": 0,
    "rps": 0,
    "attacks": 0,
    "window_start": time.time(),
    "last_update": time.time()
}

WINDOW = 1.0  # 1 second window

def add_metric(_, is_attack):
    now = time.time()

    # count every request
    state["count"] += 1
    state["last_update"] = now

    if is_attack:
        state["attacks"] += 1

    # calculate RPS every second
    if now - state["window_start"] >= WINDOW:
        state["rps"] = round(state["count"] / (now - state["window_start"]), 2)
        state["count"] = 0
        state["window_start"] = now

def get_metrics():
    # drop to zero if no traffic
    if time.time() - state["last_update"] > 3:
        return {
            "rps": 0,
            "attacks": state["attacks"]
        }

    return {
        "rps": state["rps"],
        "attacks": state["attacks"]
    }
