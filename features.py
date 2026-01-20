import time
from collections import defaultdict, Counter

WINDOW = 5

logs = defaultdict(list)      # ip → timestamps
paths = defaultdict(list)     # ip → endpoints
errors = defaultdict(int)     # ip → error count

def add_request(ip, path, status):
    now = time.time()

    logs[ip].append(now)
    paths[ip].append(path)

    if status >= 400:
        errors[ip] += 1


def extract_features(ip):
    now = time.time()

    # keep windowed data
    logs[ip]  = [t for t in logs[ip] if now - t < WINDOW]
    paths[ip] = paths[ip][-50:]

    rps = len(logs[ip]) / WINDOW

    # burst = max requests in any 1 sec slice
    burst = max(
        Counter(int(t) for t in logs[ip]).values()
    ) if logs[ip] else 0

    # unique path ratio
    unique = len(set(paths[ip])) / (len(paths[ip]) + 1)

    # avg gap between requests
    gaps = [j-i for i,j in zip(logs[ip], logs[ip][1:])]
    avg_gap = sum(gaps)/len(gaps) if gaps else 1

    error_rate = errors[ip] / (len(paths[ip]) + 1)

    return [rps, burst, unique, avg_gap, error_rate]
