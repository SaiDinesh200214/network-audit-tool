# logging_system.py — Scan Logging System
import os, datetime, json

LOG_DIR = "scan_logs"

def start_log(auditor, report_name):
    os.makedirs(LOG_DIR, exist_ok=True)
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(LOG_DIR, f"scan_{ts}.log")
    with open(path,"w") as f:
        f.write(f"=== NETAUDIT PRO SCAN LOG ===\n")
        f.write(f"Started : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Auditor : {auditor}\n")
        f.write(f"Report  : {report_name}\n")
        f.write("="*40 + "\n\n")
    return path

def log(log_file, message):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    with open(log_file,"a") as f:
        f.write(f"[{ts}] {message}\n")

def finish_log(log_file, devices, vulns, critical, risk):
    with open(log_file,"a") as f:
        f.write("\n" + "="*40 + "\n")
        f.write(f"=== SCAN COMPLETE ===\n")
        f.write(f"Devices  : {devices}\n")
        f.write(f"Vulns    : {vulns}\n")
        f.write(f"Critical : {critical}\n")
        f.write(f"Risk     : {risk}\n")
        f.write(f"Ended    : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
