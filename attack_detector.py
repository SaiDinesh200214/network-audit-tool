# attack_detector.py — Attack Simulation Detection (Safe Mode)
# Detects scanning behavior and brute force attempts on local machine

import socket
import time
import threading
import datetime
import os
import json
from collections import defaultdict

class AttackDetector:
    def __init__(self, log_dir="scan_logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.connection_counts = defaultdict(list)  # ip -> [timestamps]
        self.port_scan_threshold = 10   # ports/10s = port scan
        self.brute_threshold = 5        # connections/5s = brute force
        self.alerts = []
        self.running = False
        
    def analyze_existing_ports(self, scan_results):
        """
        Analyze scan results to detect suspicious patterns (safe mode).
        Does NOT open any ports — only analyzes existing data.
        """
        alerts = []
        
        for result in scan_results:
            ip = result.get("ip","")
            ports = result.get("open_ports",[])
            
            # Check for mass open ports (possible compromised machine)
            if len(ports) >= 5:
                alerts.append({
                    "type": "PORT_SWEEP_DETECTED",
                    "severity": "HIGH",
                    "ip": ip,
                    "detail": f"{len(ports)} open ports detected — possible compromised or misconfigured device",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "recommendation": "Review all services running on this device"
                })
            
            # Check for remote access combo (classic attack vector)
            port_nums = [p["port"] for p in ports]
            if 3389 in port_nums and 445 in port_nums:
                alerts.append({
                    "type": "REMOTE_ACCESS_COMBO",
                    "severity": "CRITICAL",
                    "ip": ip,
                    "detail": "RDP + SMB both open — classic ransomware attack vector",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "recommendation": "Disable RDP and block SMB externally immediately"
                })
            
            # Check for database exposure
            db_ports = {1433,3306,5432,27017,6379}
            exposed_dbs = [p["port"] for p in ports if p["port"] in db_ports]
            if exposed_dbs:
                alerts.append({
                    "type": "DATABASE_EXPOSED",
                    "severity": "CRITICAL",
                    "ip": ip,
                    "detail": f"Database ports exposed: {exposed_dbs} — data breach risk",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "recommendation": "Bind databases to localhost only. Never expose to network."
                })
            
            # Check for Telnet (ancient and dangerous)
            if 23 in port_nums:
                alerts.append({
                    "type": "INSECURE_PROTOCOL",
                    "severity": "CRITICAL",
                    "ip": ip,
                    "detail": "Telnet (port 23) is running — all traffic is unencrypted plaintext",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "recommendation": "Disable Telnet immediately. Use SSH instead."
                })
            
            # FTP check
            if 21 in port_nums:
                alerts.append({
                    "type": "INSECURE_PROTOCOL",
                    "severity": "HIGH",
                    "ip": ip,
                    "detail": "FTP (port 21) detected — credentials sent in plaintext",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "recommendation": "Replace FTP with SFTP or FTPS"
                })
            
            # Check risk score threshold
            if result.get("risk_score", 0) >= 8:
                alerts.append({
                    "type": "HIGH_RISK_DEVICE",
                    "severity": "CRITICAL",
                    "ip": ip,
                    "detail": f"Device risk score {result['risk_score']}/10 — immediate action required",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "recommendation": "Review and close unnecessary ports immediately"
                })
        
        self.alerts = alerts
        self._save_alerts()
        return alerts
    
    def _save_alerts(self):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.log_dir, f"alerts_{ts}.json")
        with open(path, "w") as f:
            json.dump(self.alerts, f, indent=2)
        return path
