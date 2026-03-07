<div align="center">

# 🛡️ NetAudit Pro
### Home Network Security Audit Tool

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Windows](https://img.shields.io/badge/Windows-✅-0078D6?style=flat-square&logo=windows)](https://github.com/SaiDinesh200214)
[![Linux](https://img.shields.io/badge/Linux-✅-FCC624?style=flat-square&logo=linux&logoColor=black)](https://github.com/SaiDinesh200214)
[![macOS](https://img.shields.io/badge/macOS-✅-000000?style=flat-square&logo=apple)](https://github.com/SaiDinesh200214)
[![Android](https://img.shields.io/badge/Android-✅-3DDC84?style=flat-square&logo=android&logoColor=white)](https://github.com/SaiDinesh200214)
[![Version](https://img.shields.io/badge/Version-2.4-brightgreen?style=flat-square)](https://github.com/SaiDinesh200214)
[![Author](https://img.shields.io/badge/Author-SaiDinesh%20Andekar-purple?style=flat-square)](https://github.com/SaiDinesh200214)

**Scan your network. Find vulnerabilities. Generate professional PDF reports.**  
*Built entirely in Python. Runs on Windows, Linux, macOS and Android (Termux).*

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
| **Android** (Termux) | ✅ Limited | `python launch.py` |

> **ARP scanning requires admin/root** on Windows/Linux/macOS — launchers handle this automatically.  
> **Android (Termux)** runs in limited mode — port scan + vuln analysis + PDF work, ARP needs root.

---

## 🚀 Installation

### 🪟 Windows
**Step 1 — Install Python**  
Download from [python.org](https://python.org) → ✅ check **"Add Python to PATH"**

**Step 2 — Install dependencies**
```bash
pip install scapy reportlab
```

**Step 3 — Download project**
```bash
git clone https://github.com/SaiDinesh200214/network-audit-tool
cd network-audit-tool
```

**Step 4 — Run (just double-click!)**
```
RUN_ME.bat
```
UAC popup appears → click **Yes** → browser opens automatically ✅

---

### 🐧 Linux (Ubuntu / Kali / Debian)
```bash
sudo apt update && sudo apt install python3 python3-pip git -y
```

> ⚠️ **Kali Linux / Ubuntu 23+** blocks normal pip install. Use this instead:
```bash
sudo pip3 install scapy reportlab --break-system-packages
```

> ✅ **Ubuntu 22 and older** use normal pip:
```bash
pip3 install scapy reportlab
```

```bash
git clone https://github.com/SaiDinesh200214/network-audit-tool
cd network-audit-tool
sudo bash RUN_ME.sh
```

> ⚠️ Must use `sudo` on Linux — ARP scanning requires root privileges.

---

### 🍎 macOS
```bash
brew install python3
pip3 install scapy reportlab
git clone https://github.com/SaiDinesh200214/network-audit-tool
cd network-audit-tool
bash RUN_ME.sh
```

---

### 📱 Android (Termux)

**Step 1 — Install Termux**  
Download from [F-Droid](https://f-droid.org/packages/com.termux/) ← NOT Play Store

**Step 2 — Setup**
```bash
pkg update && pkg upgrade -y
pkg install python git clang libjpeg-turbo libpng libtiff -y
pip install pillow reportlab
```

**Step 3 — Clone and run**
```bash
git clone https://github.com/SaiDinesh200214/network-audit-tool
cd network-audit-tool
python launch.py
```

**Step 4 — Open in browser**  
Termux will show:
```
📱 OPEN THIS URL IN YOUR PHONE BROWSER:
     http://localhost:8765/gui.html
```
Just open that URL in Chrome/Firefox on your phone ✅

> ⚠️ Android limitations: ARP device discovery needs root. Port scanning, vulnerability analysis, risk scoring and PDF reports all work without root.

---

## 📱 View Results from Any Phone/Tablet

No install needed on phone — just view from PC scan:

1. PC and phone on **same WiFi**
2. **Windows:** run `ipconfig` → find IPv4 Address  
   **Linux/macOS:** run `ip addr`
3. Open phone browser: `http://YOUR_PC_IP:8765`

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
├── 🐧 RUN_ME.sh           ← Linux/macOS launcher (auto sudo)
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
    ├── scan_YYYYMMDD.log
    ├── scan_YYYYMMDD.json
    └── alerts_YYYYMMDD.json
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.8+ |
| Device Discovery | Scapy ARP + `ping` + `arp` / `ip neigh` |
| Port Scanning | Python `socket` (50 concurrent threads) |
| PDF Reports | ReportLab + Pillow |
| Network Map | HTML5 Canvas (offline, no CDN) |
| Frontend | Vanilla HTML/CSS/JS (dark theme) |
| Web Server | Python `http.server` |

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| No devices found | Use launcher scripts — admin/root required for ARP |
| `scapy` not found (Windows) | `pip install scapy` |
| `reportlab` not found (Windows) | `pip install reportlab` |
| `externally-managed-environment` on Kali/Linux | `sudo pip3 install scapy reportlab --break-system-packages` |
| `No module named reportlab` on Linux | `sudo pip3 install reportlab --break-system-packages` |
| Permission denied on Linux | Always use `sudo python3 main.py` or `sudo bash RUN_ME.sh` |
| Android: pillow fails | `pkg install libjpeg-turbo libpng libtiff -y` then `pip install pillow` |
| Android: sudo not found | Normal — app runs without root in limited mode |
| Phone can't connect to PC | Open port 8765 in firewall (see above) |
| Browser doesn't open | Go to `http://localhost:8765/gui.html` manually |
| Topology map blank | Delete `topology.html` and run a new scan |

---

## 📋 Changelog

### v2.4 (Latest)
- ✅ Fixed Linux/Kali pip install — added `--break-system-packages` instructions
- ✅ Updated troubleshooting for Kali Linux externally-managed-environment error
- ✅ Tested and verified on Kali Linux VM

### v2.3
- ✅ **Stunning CLI redesign** — cyan ASCII art banner, colored output, animated spinners
- ✅ Auto-fit boxes using terminal width detection — no more broken borders
- ✅ Color-coded risk scores with visual progress bar per device
- ✅ Animated progress bar for PDF generation
- ✅ Android Termux support — runs without root
- ✅ Auto-detects Termux environment, skips sudo requirement
- ✅ Shows URL clearly in Termux instead of trying to open browser
- ✅ Scanner skips ARP on Android, scans local device

### v2.2
- ✅ Termux root check bypass
- ✅ is_termux() detection added to launch.py and scanner.py

### v2.1
- ✅ Full cross-platform: Windows, Linux, macOS
- ✅ Added `RUN_ME.sh` for Linux/macOS
- ✅ Fixed MAC address format (Windows dashes vs Linux colons)
- ✅ Added `ip neigh`, `ifconfig`, `ip addr` support

### v2.0
- ✅ Fixed PDF crash (hexToDecimal)
- ✅ Fixed MAC address splitting in PDF
- ✅ Fixed text truncation in vulnerability table
- ✅ Fixed XSS security bug (new Function → safe handler)
- ✅ Added `RUN_ME.bat` — no more manual CMD
- ✅ Auto UAC elevation on Windows

### v1.0
- 🚀 Initial release

---

## 📜 License & Copyright

Copyright © 2026 **SaiDinesh Andekar**. All rights reserved.

This project is licensed under the **MIT License with Attribution**.

- ✅ You are free to use, modify, and distribute this software
- ✅ You must give **clear credit** to SaiDinesh Andekar as the original author
- ✅ You must include a link to the original repository
- ❌ You may **NOT** claim this as your own original work
- ❌ You may **NOT** remove copyright notices from any files

See the [LICENSE](./LICENSE) file for full terms.

---

## ⚠️ Disclaimer

For **educational purposes** and **authorized auditing only**.

- ✅ Only scan networks you **own** or have **explicit written permission** to test
- ❌ Unauthorized network scanning is **illegal** in most countries
- ❌ Do not use on public networks, school/college networks without permission

---

## 👨‍💻 Developer

**SaiDinesh Andekar**  
📧 [saidineshandekar1402@gmail.com](mailto:saidineshandekar1402@gmail.com)  
🐙 [github.com/SaiDinesh200214](https://github.com/SaiDinesh200214)

---

<div align="center">
<sub>Built with 🐍 Python · Windows · Linux · macOS · Android · For learning cybersecurity</sub>
</div>