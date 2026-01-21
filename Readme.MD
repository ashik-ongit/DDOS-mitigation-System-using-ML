🛡️ ShieldX — Machine Learning–Based DDoS Mitigation System
ShieldX is a software‑defined, machine learning–based DDoS mitigation system designed to detect and mitigate application‑layer and volumetric attacks in real time.
It operates as a reverse proxy, dynamically analyzing traffic behavior, blocking malicious sources, and maintaining backend service availability.

🚀 Key Highlights
✅ Machine Learning + Statistical anomaly detection

✅ Real‑time traffic monitoring (RPS, bursts, behavior)

✅ Automatic IP mitigation with escalating ban durations

✅ Dynamic attack signature generation

✅ Persistent IP reputation memory

✅ System health monitoring (Mitigator + Backend)

✅ Live visualization dashboard

✅ Built‑in traffic simulation framework

🧠 System Architecture
[ Client Traffic ]
        |
        v
[ ShieldX Mitigator (Flask Proxy) ]
        |
        |-- Feature Extraction
        |-- ML + Statistical Detection
        |-- Auto Mitigation & Signatures
        |
        v
[ Backend Application Server ]
⚙️ How ShieldX Works
Traffic Interception
All incoming requests pass through the ShieldX proxy before reaching the backend server.

Feature Extraction
Behavioral features are extracted per IP:

Requests per second (RPS)

Burst intensity

Unique endpoint ratio

Inter‑request gap

Error rate

Anomaly Detection
Traffic is analyzed using:

Machine‑learning–based anomaly detection

Statistical threshold checks

Mitigation & Signature Generation

Malicious IPs are automatically blocked

Ban duration escalates for repeat offenders

Behavioral attack signatures are generated and updated dynamically

Monitoring & Visualization
A live dashboard displays traffic metrics, blocked attacks, attack signatures, and system health.

🩺 System Health Monitoring
ShieldX exposes two layers of health monitoring:

Layer 1 — Mitigator Health
Service status

Uptime

Current RPS

Number of blocked IPs

Layer 2 — Backend Health
Continuous reachability check of the protected backend server

This ensures both the protection layer and application server are monitored.

🧪 Simulation Framework
ShieldX includes a lightweight traffic simulation framework for evaluation purposes:

Simulates normal user traffic

Generates flood / burst attack traffic

Supports multi‑IP simulation using headers

Enables observation of mitigation behavior and system stability

This framework is suitable for academic and prototype‑level evaluation.

📊 Dashboard
The Streamlit‑based dashboard provides:

Real‑time RPS visualization

Total attacks blocked

Attack signature inspection

Manual IP block / unblock controls

System connectivity status

🧰 Tech Stack
Frontend
Streamlit

Real‑time charts

JSON visualization

Backend / Mitigation Layer
Python

Flask (Reverse Proxy)

Machine Learning
scikit‑learn

Isolation Forest / anomaly detection logic

Simulation
Python‑based traffic simulator

Curl‑based request flooding

Storage
JSON‑based persistent memory (ip_memory.json)

📁 Project Structure
.
├── mitigator.py        # Core DDoS mitigation proxy
├── dashboard.py        # Streamlit monitoring dashboard
├── simulator.py        # Traffic simulation framework
├── features.py         # Traffic feature extraction
├── ml_detector.py      # ML-based attack detection
├── stat_guard.py       # Statistical detection rules
├── metrics.py          # Real-time metrics collection
├── ip_memory.json      # Persistent IP reputation store
└── README.md
▶️ How to Run
1️⃣ Start Backend Server (example)
python -m http.server 5000
2️⃣ Run ShieldX Mitigator
python mitigator.py
3️⃣ Launch Dashboard
streamlit run dashboard.py
4️⃣ (Optional) Run Traffic Simulator
python simulator.py
📈 Evaluation & Benchmarking
ShieldX is conceptually benchmarked against traditional appliance‑based DDoS mitigation solutions.

Aspect	ShieldX	Traditional Appliances
Deployment	Software‑based	Hardware
Cost	Low	Very High
Detection	ML + Behavioral	Mostly Rule‑based
Adaptability	High	Limited
Visibility	Full Metrics	Limited
Scalability	Horizontal	Fixed
🌟 Novelty & USP
Behavior‑based mitigation instead of static rule enforcement

Dynamic attack signature generation

Persistent learning from historical attacks

Lightweight, low‑cost alternative to hardware appliances

🔮 Future Work
Kernel‑level packet filtering (eBPF)

Signature‑based pre‑blocking

Large‑scale distributed deployment

Advanced latency analysis

📌 Conclusion
ShieldX demonstrates how machine learning and behavioral analysis can be effectively applied to build an adaptive, low‑cost DDoS mitigation system capable of maintaining service availability under attack conditions.
