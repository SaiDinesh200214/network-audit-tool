# 🛡️ Home Network Security Audit Tool

A professional network security auditing tool built in Python that scans your home network, detects connected devices, identifies open ports, analyzes vulnerabilities, and generates a detailed PDF report.

---

## 🎯 What It Does

| Module | Description |
|--------|-------------|
| 📡 Device Scanner | Discovers all devices connected to your WiFi |
| 🚪 Port Scanner | Detects open ports on each device |
| ⚠️ Vulnerability Analyzer | Analyzes security risks with CVSS scoring |
| 📄 PDF Report Generator | Creates a professional audit report |

---

## 🖥️ Sample Output
```
═══════════════════════════════════════════════════════════════
   🛡️   HOME NETWORK SECURITY AUDIT TOOL
═══════════════════════════════════════════════════════════════
✅ Found 2 device(s) on your network

📍 192.168.1.5 — YOUR MACHINE
  Port 445   SMB      🔴 HIGH    Windows sharing — WannaCry target
  Port 3389  RDP      🔴 HIGH    Remote Desktop — brute force target

📊 FINAL SUMMARY
  🖥️  Devices Scanned      : 2
  ⚠️  Total Vulnerabilities : 4
  🔴 Critical Issues       : 3
  Overall Risk Score       : 100/100 — HIGH RISK
```

---

## ⚙️ Requirements

- Python 3.x
- Windows / Linux / MacOS
- Administrator / sudo privileges
- Npcap (Windows only) — [Download here](https://npcap.com)
- Nmap — [Download here](https://nmap.org)

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/network-audit-tool.git
cd network-audit-tool
```

**2. Install dependencies**
```bash
pip install scapy python-nmap reportlab
```

**3. Windows users — Install Npcap**

Download and install from [npcap.com](https://npcap.com)
During install check:
- ✅ Install Npcap in WinPcap API-compatible Mode
- ✅ Support raw 802.11 traffic

---

## 🚀 Usage

**Windows — Run as Administrator:**
```bash
python main.py
```

**Linux/Mac — Run with sudo:**
```bash
sudo python3 main.py
```

You will be prompted to enter:
- Your name (for the report)
- Report filename (or press Enter for auto-generated name)

---

## 📄 PDF Report Includes

- Executive Summary with Risk Score
- All discovered devices with MAC addresses
- Detailed vulnerability analysis per device
- CVSS scores for each vulnerability
- Attack scenarios for each open port
- Step-by-step remediation guide
- Top 7 prioritized recommendations

---

## 🔍 Vulnerabilities Detected

The tool checks for these high-risk ports:

| Port | Service | Risk Level |
|------|---------|------------|
| 21 | FTP | 🔴 Critical |
| 22 | SSH | 🟡 Medium |
| 23 | Telnet | 🔴 Critical |
| 80 | HTTP | 🟡 Medium |
| 135 | RPC | 🔴 Critical |
| 139 | NetBIOS | 🔴 Critical |
| 443 | HTTPS | 🟢 Low |
| 445 | SMB | 🔴 Critical |
| 3306 | MySQL | 🔴 Critical |
| 3389 | RDP | 🔴 Critical |
| 5900 | VNC | 🔴 Critical |
| 27017 | MongoDB | 🔴 Critical |

---

## 📁 Project Structure
```
network-audit-tool/
│
├── main.py          # Main controller — runs all modules
├── scanner.py       # Device scanner, port scanner, vulnerability checker
├── report.py        # PDF report generator
└── README.md        # You are here!
```

---

## ⚠️ Legal Disclaimer

This tool is for **educational purposes** and **authorized network auditing only**.
Only run this tool on networks you **own or have permission** to scan.
Unauthorized network scanning may be **illegal** in your country.

---

## 🛠️ Built With

- [Python](https://python.org) — Core language
- [Scapy](https://scapy.net) — Network packet manipulation
- [python-nmap](https://pypi.org/project/python-nmap/) — Port scanning
- [ReportLab](https://reportlab.com) — PDF generation
- [Socket](https://docs.python.org/3/library/socket.html) — Cross-platform port scanning

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐ on GitHub!