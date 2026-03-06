<div align="center">

# 🛡️ NetAudit Pro
### Home Network Security Audit Tool

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-✅-0078D6?style=flat-square&logo=windows)](https://github.com/SaiDinesh200214)
[![Linux](https://img.shields.io/badge/Linux-✅-FCC624?style=flat-square&logo=linux&logoColor=black)](https://github.com/SaiDinesh200214)
[![macOS](https://img.shields.io/badge/macOS-✅-000000?style=flat-square&logo=apple)](https://github.com/SaiDinesh200214)
[![Version](https://img.shields.io/badge/Version-2.1-brightgreen?style=flat-square)](https://github.com/SaiDinesh200214)
[![Author](https://img.shields.io/badge/Author-SaiDinesh%20Andekar-purple?style=flat-square)](https://github.com/SaiDinesh200214)

**Scan your network. Find vulnerabilities. Generate professional PDF reports.**  
*Built entirely in Python. Runs on Windows, Linux, and macOS.*

</div>

---

## ✨ Features

| Module | What it does |
|--------|-------------|
| 📡 **Device Discovery** | Finds all devices via ARP broadcast + Ping sweep + ARP table |
| 💻 **OS Detection** | Identifies Windows / Linux / Android via TTL analysis |
| 🚪 **Port Scanner** | Scans 20 critical ports with CVSS scores |
| ⚠️ **Vuln Analysis** | Maps open ports to real CVE-based vulnerabilities |
| 📊 **Risk Scoring** | Gives every device a 0–10 risk score |
| 🗺️ **Network Map** | Interactive topology map — drag, zoom, hover |
| 🔎 **Attack Detection** | Flags dangerous combos (RDP+SMB = ransomware vector) |
| 📄 **PDF Report** | Auto-generates a dark-themed professional audit report |

---

## 🖥️ Platform Support

| OS | Support | How to run |
|----|---------|-----------|
| **Windows 10/11** | ✅ Full | Double-click `RUN_ME.bat` |
| **Linux** (Ubuntu, Kali, Debian...) | ✅ Full | `bash RUN_ME.sh` |
| **macOS** | ✅ Full | `bash RUN_ME.sh` |

> **ARP scanning requires admin/root on all platforms.** The launchers handle this automatically.

---

## 🚀 Installation

### Step 1 — Install Python
- **Windows:** [python.org](https://python.org) → ✅ check **"Add Python to PATH"**
- **Linux:** `sudo apt install python3 python3-pip`
- **macOS:** `brew install python3`

### Step 2 — Install dependencies
```bash
pip install scapy reportlab
```
> Linux/macOS: `pip3 install scapy reportlab`

### Step 3 — Download project
```bash
git clone https://github.com/SaiDinesh200214/network-audit-tool
cd network-audit-tool
```

### Step 4 — Run

**Windows** — Just double-click:
```
RUN_ME.bat
```

**Linux / macOS** — In terminal:
```bash
bash RUN_ME.sh
```

Browser opens at `http://localhost:8765` automatically. Enter your name → click **Start Scan**.

---

## 📱 Access from Phone / Tablet

Your phone can view the results live while scan runs on your PC/Mac:

1. Phone and computer must be on **same WiFi**
2. Find your computer's IP:
   - **Windows:** run `ipconfig` → find IPv4 Address
   - **Linux/macOS:** run `ip addr` or `ifconfig`
3. Open phone browser: `http://YOUR_IP:8765`

Allow firewall if phone can't connect:

**Windows:**
```bash
netsh advfirewall firewall add rule name="NetAudit Pro" dir=in action=allow protocol=TCP localport=8765
```
**Linux:**
```bash
sudo ufw allow 8765/tcp
```

---

## 📁 Project Structure

```
network-audit-tool/
│
├── 🪟 RUN_ME.bat          ← Windows launcher (double-click)
├── 🐧 RUN_ME.sh           ← Linux/macOS launcher
├── RUN_ME.vbs             ← Windows silent launcher
│
├── launch.py              ← Web server + orchestrator
├── scanner.py             ← Device discovery + port scanning
├── report.py              ← PDF generator (ReportLab)
├── topology.py            ← Network map (HTML5 Canvas)
├── attack_detector.py     ← Threat pattern detection
├── logging_system.py      ← Scan logging
├── main.py                ← CLI mode (no browser)
│
├── gui.html               ← Dark-themed frontend
├── topology.html          ← Auto-generated after scan
│
└── scan_logs/             ← Auto-created on first scan
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ |
| Device Discovery | Scapy ARP + `ping` + `arp`/`ip neigh` |
| Port Scanning | Python `socket` (50 concurrent threads) |
| PDF Reports | ReportLab |
| Network Map | HTML5 Canvas (offline, no CDN) |
| Frontend | Vanilla HTML/CSS/JS |
| Web Server | Python `http.server` |

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| No devices found | Make sure you're running with admin/root (use the launcher scripts) |
| `scapy` not found | `pip install scapy` |
| `reportlab` not found | `pip install reportlab` |
| Linux: permission denied | Run `bash RUN_ME.sh` (it uses sudo automatically) |
| macOS: permission denied | Run `bash RUN_ME.sh` (it uses sudo automatically) |
| Phone can't connect | Open port 8765 in firewall (see above) |
| Browser doesn't open | Go to `http://localhost:8765` manually |

---

## 📋 Changelog

### v2.1 (Latest)
- ✅ Full cross-platform support: Windows, Linux, macOS
- ✅ Added `RUN_ME.sh` for Linux/macOS (auto sudo)
- ✅ `scanner.py` now uses `ip neigh`, `ifconfig`, `ip addr` on Linux/Mac
- ✅ Fixed MAC address format differences (Windows dashes vs Linux colons)

### v2.0
- ✅ Fixed MAC address splitting in PDF
- ✅ Fixed PDF crash (hexToDecimal error)
- ✅ Fixed text truncation in vulnerability table
- ✅ Fixed security bug (new Function → safe handler)
- ✅ Added `RUN_ME.bat` — no more manual CMD on Windows
- ✅ Auto UAC elevation on Windows

### v1.0
- Initial release

---

## ⚠️ Disclaimer

For **educational purposes** and **authorized auditing only**.

- ✅ Only scan networks you **own** or have **explicit permission** to test
- ❌ Unauthorized network scanning is **illegal**

---

## 👨‍💻 Developer

**SaiDinesh Andekar**  
📧 [saidineshandekar1402@gmail.com](mailto:saidineshandekar1402@gmail.com)  
🐙 [github.com/SaiDinesh200214](https://github.com/SaiDinesh200214)

---

<div align="center">
<sub>Built with 🐍 Python · Windows · Linux · macOS · For learning cybersecurity</sub>
</div>
