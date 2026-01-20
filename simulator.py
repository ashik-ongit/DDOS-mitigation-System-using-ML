import requests
import time
import random
import sys

URL = "http://localhost:4000"

print("""
Choose Mode
1 - Normal Users
2 - DDoS Simulation
3 - Mixed Traffic
q - Quit anytime
""")

mode = input("mode: ")

def safe_get():
    try:
        requests.get(URL, timeout=1)
    except:
        pass        # ignore connection errors (demo friendly)

def normal():
    time.sleep(random.uniform(0.3, 1.0))
    safe_get()

def attack():
    for _ in range(200):
        safe_get()
        time.sleep(0.005)
def mixed():
    if random.random() < 0.85:   # 85% normal users
        normal()
    else:
        # small attack burst, not full DDoS
        for _ in range(5):
            safe_get()
            time.sleep(0.05)


print("Press CTRL+C or type 'q' to stop...\n")

try:
    while True:

        # allow quick cancel
        if mode.lower() == "q":
            print("Simulator stopped safely.")
            sys.exit(0)

        if mode == "1":
            normal()

        elif mode == "2":
            attack()
            

        else:
            # mixed realistic
            mixed()

except KeyboardInterrupt:
    print("\nSimulation cancelled safely 👍")
