# 🛡️ ShieldX — Machine Learning–Based DDoS Mitigation System

ShieldX is a **software‑defined, machine learning–based DDoS mitigation system**
that detects and mitigates application‑layer and volumetric attacks in real time.
It operates as a **reverse proxy** in front of a protected backend server.

---

## 🚀 Key Highlights

- Machine Learning + Statistical anomaly detection  
- Real‑time traffic monitoring (RPS, bursts, behavior)  
- Automatic IP mitigation with escalating ban durations  
- Dynamic attack signature generation  
- Persistent IP reputation memory  
- System health monitoring (Mitigator + Backend)  
- Live visualization dashboard  
- Built‑in traffic simulation framework  

---

## 🧠 System Architecture

Client
|
v
ShieldX Mitigator (Flask Proxy)
|-- Feature Extraction
|-- ML + Statistical Detection
|-- Auto Mitigation & Signatures
|
v
Backend Server


---

## ⚙️ How ShieldX Works

### 1️⃣ Traffic Interception
All incoming requests first pass through the ShieldX proxy before reaching the backend server.

### 2️⃣ Feature Extraction
The system extracts behavioral features per IP:
- Requests per second (RPS)
- Burst intensity
- Unique endpoint ratio
- Inter‑request gap
- Error rate

### 3️⃣ Anomaly Detection
Traffic is analyzed using:
- Machine‑learning‑based anomaly detection  
- Statistical threshold checks  

### 4️⃣ Mitigation & Signature Generation
- Malicious IPs are automatically blocked  
- Ban duration increases for repeat offenders  
- Behavioral attack signatures are generated dynamically  

### 5️⃣ Monitoring & Visualization
A live dashboard visualizes traffic rate, blocked attacks, signatures, and system health.

---

## 🩺 System Health Monitoring

### Layer 1 — Mitigator Health
- Service status  
- Uptime  
- Current RPS  
- Number of blocked IPs  

### Layer 2 — Backend Health
- Continuous reachability check to the backend server  

---

## 🧪 Simulation Framework

ShieldX includes a lightweight **traffic simulation framework** that:
- Simulates normal user traffic  
- Generates flood / burst attacks  
- Supports multi‑IP simulation  
- Enables evaluation of mitigation behavior  

---

## 📊 Dashboard

The Streamlit dashboard provides:
- Real‑time RPS charts  
- Total attacks blocked  
- Attack signature visualization  
- Manual IP block / unblock  
- System connectivity status  

---

## 🧰 Tech Stack

### Frontend
- Streamlit (real‑time charts & JSON visualization)

### Backend / Mitigation Layer
- Python  
- Flask (Reverse Proxy)

### Machine Learning
- scikit‑learn (Isolation Forest / anomaly detection)

### Simulation
- Python‑based traffic simulator  
- Curl‑based flood generation  

### Storage
- JSON‑based persistent memory (`ip_memory.json`)

---

## 📁 Project Structure

.
├── mitigator.py
├── dashboard.py
├── simulator.py
├── features.py
├── ml_detector.py
├── stat_guard.py
├── metrics.py
├── ip_memory.json
└── README.md


---

## ▶️ How to Run

### Start Backend Server
```bash
python -m http.server 5000
Run ShieldX Mitigator
python mitigator.py
Launch Dashboard
streamlit run dashboard.py
Run Simulator (Optional)
python simulator.py
📈 Evaluation & Benchmarking
ShieldX is compared conceptually against traditional appliance‑based DDoS mitigation systems.

Feature	ShieldX	Traditional Appliances
Deployment	Software‑based	Hardware
Cost	Low	Very High
Detection	ML + Behavioral	Rule‑based
Adaptability	High	Limited
Visibility	Full metrics	Limited
🌟 Novelty & USP
Behavior‑based DDoS mitigation

Dynamic attack signature generation

Persistent learning from past attacks

Lightweight alternative to hardware appliances

🔮 Future Work
Kernel‑level filtering (eBPF)

Signature‑based pre‑blocking

Large‑scale distributed deployment

✅ Conclusion
ShieldX demonstrates how machine learning and behavioral analysis
can be used to build an adaptive, low‑cost DDoS mitigation system
while maintaining service availability during attacks.


