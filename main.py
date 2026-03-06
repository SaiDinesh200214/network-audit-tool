# main.py — NetAudit Pro Master Controller
# Runs all modules + logging system

import datetime
import os
import sys
import json

def setup_logging():
    """Create scan_logs folder and log file"""
    log_dir = "scan_logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"scan_{timestamp}.log")
    return log_file, timestamp

def write_log(log_file, message):
    """Write message to log file"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n" + "=" * 65)
    print("   🛡️   NETAUDIT PRO — HOME NETWORK SECURITY AUDIT TOOL")
    print("   Version 1.0  |  By SaiDinesh Andekar")
    print("   📧 saidineshandekar1402@gmail.com")
    print("   🐙 github.com/SaiDinesh200214")
    print("=" * 65)
    print("""
  This tool will:
  📡 Scan your network for connected devices
  💻 Detect device operating systems (TTL analysis)
  🚪 Check open ports on each device
  ⚠️  Analyze vulnerabilities with CVSS scoring
  📊 Calculate device risk scores (0-10)
  📄 Generate a professional PDF report
  📝 Save detailed logs to scan_logs/
""")
    print("=" * 65)

    # Setup logging
    log_file, timestamp = setup_logging()

    # Get user input
    auditor_name = input("\n  👤 Enter your name (for the report): ").strip()
    if not auditor_name:
        auditor_name = "Anonymous Auditor"

    report_name = input("  📄 Enter report filename (press Enter for default): ").strip()
    if not report_name:
        report_name = f"network_audit_{timestamp}.pdf"
    elif not report_name.endswith('.pdf'):
        report_name += '.pdf'

    print(f"\n  ✅ Starting scan as: {auditor_name}")
    print(f"  ✅ Report: {report_name}")
    print(f"  ✅ Log: scan_logs/scan_{timestamp}.log")
    input("\n  Press Enter to begin scan...")

    write_log(log_file, f"=== NETAUDIT PRO SCAN STARTED ===")
    write_log(log_file, f"Auditor: {auditor_name}")
    write_log(log_file, f"Report file: {report_name}")

    from scanner import (scan_network, scan_ports, check_vulnerabilities,
                          detect_os, calculate_risk_score, get_risk_label)
    from report import generate_report

    # ── MODULE 1: DEVICE DISCOVERY ──────────────────────────
    print("\n" + "=" * 65)
    print("   📡  MODULE 1 — DEVICE DISCOVERY")
    print("=" * 65)
    write_log(log_file, "MODULE 1: Starting device discovery...")

    devices, my_ip = scan_network()
    write_log(log_file, f"Found {len(devices)} device(s). My IP: {my_ip}")

    if not devices:
        print("  ❌ No devices found! Run as Administrator.")
        write_log(log_file, "ERROR: No devices found")
        sys.exit(1)

    print(f"\n  ✅ Found {len(devices)} device(s):\n")
    for i, device in enumerate(devices, 1):
        note = "⬅️ YOU" if device['ip'] == my_ip else "📱 Device"
        print(f"  {i}. {device['ip']:<18} {device['mac']}  {note}")
        write_log(log_file, f"  Device {i}: {device['ip']} | MAC: {device['mac']} | {note}")

    all_results = []

    for device in devices:
        ip  = device['ip']
        mac = device['mac']
        label = "YOUR MACHINE" if ip == my_ip else "Network Device"

        print(f"\n{'=' * 65}")
        print(f"   📍 {ip} — {label}")
        print("=" * 65)
        write_log(log_file, f"\n--- Scanning {ip} ({label}) ---")

        # ── OS DETECTION ────────────────────────────────────
        print(f"\n  💻 OS Detection...")
        os_info = detect_os(ip)
        print(f"  ✅ OS: {os_info['os']} (TTL: {os_info['ttl']}, Confidence: {os_info['confidence']})")
        write_log(log_file, f"OS Detection: {os_info['os']} | TTL: {os_info['ttl']}")

        # ── MODULE 2: PORT SCAN ─────────────────────────────
        print(f"\n  🚪 MODULE 2 — PORT SCAN")
        write_log(log_file, "MODULE 2: Starting port scan...")
        open_ports = scan_ports(ip)

        if open_ports:
            print(f"\n  {'PORT':<8}{'SERVICE':<12}{'RISK':<10}{'CVSS':<6}DESCRIPTION")
            print(f"  {'─'*60}")
            for p in open_ports:
                risk_icons = {"CRITICAL":"🔴","HIGH":"🟠","MEDIUM":"🟡","LOW":"🟢"}
                icon = risk_icons.get(p['risk'], "⚪")
                print(f"  {str(p['port']):<8}{p['service']:<12}{icon} {p['risk']:<8}{p['cvss']:<6}{p['desc']}")
                write_log(log_file, f"  Port {p['port']}: {p['service']} | {p['risk']} | CVSS {p['cvss']}")
        else:
            print("  ✅ No open risky ports found!")
            write_log(log_file, "No open ports found")

        # ── MODULE 3: VULNERABILITY ANALYSIS ────────────────
        print(f"\n  ⚠️  MODULE 3 — VULNERABILITY ANALYSIS")
        write_log(log_file, "MODULE 3: Analyzing vulnerabilities...")
        vulns = check_vulnerabilities(open_ports)

        if vulns:
            for v in vulns:
                print(f"\n  ┌─ Port {v['port']} — {v['name']}")
                print(f"  │  Severity : {v['severity']}  (CVSS: {v['cvss_score']}/10)")
                print(f"  │  Hacker can:")
                for h in v['hacker_can']:
                    print(f"  │    💀 {h}")
                print(f"  │  How to fix:")
                for f in v['fix']:
                    print(f"  │    🛡️  {f}")
                print(f"  └{'─' * 45}")
                write_log(log_file, f"  VULN Port {v['port']}: {v['severity']} CVSS {v['cvss_score']}")
        else:
            print("  ✅ No vulnerabilities found!")
            write_log(log_file, "No vulnerabilities found")

        # ── RISK SCORING ─────────────────────────────────────
        risk_score = calculate_risk_score(open_ports, vulns)
        risk_label = get_risk_label(risk_score)
        risk_icons = {"CRITICAL":"🔴","HIGH":"🟠","MEDIUM":"🟡","LOW":"🟢","MINIMAL":"⚪"}
        print(f"\n  📊 Device Risk Score: {risk_icons.get(risk_label,'')} {risk_score}/10 — {risk_label}")
        write_log(log_file, f"Risk Score: {risk_score}/10 — {risk_label}")

        all_results.append({
            'ip': ip, 'mac': mac,
            'os_info': os_info,
            'open_ports': open_ports,
            'vulnerabilities': vulns,
            'risk_score': risk_score,
            'risk_label': risk_label,
        })

    # ── FINAL SUMMARY ────────────────────────────────────────
    total_vulns   = sum(len(r['vulnerabilities']) for r in all_results)
    total_critical= sum(1 for r in all_results for v in r['vulnerabilities'] if 'CRITICAL' in v['severity'])
    max_risk      = max(r['risk_score'] for r in all_results)
    net_risk_lbl  = get_risk_label(max_risk)

    print(f"\n{'=' * 65}")
    print("   📊  FINAL NETWORK SUMMARY")
    print("=" * 65)
    print(f"  🖥️  Devices Scanned      : {len(devices)}")
    print(f"  ⚠️  Total Vulnerabilities : {total_vulns}")
    print(f"  🔴 Critical Issues       : {total_critical}")
    print(f"  📊 Highest Risk Score    : {max_risk}/10 — {net_risk_lbl}")

    write_log(log_file, f"\n=== SUMMARY: {len(devices)} devices | {total_vulns} vulns | {total_critical} critical | Risk {net_risk_lbl} ===")

    # ── MODULE 4: PDF REPORT ─────────────────────────────────
    print(f"\n{'=' * 65}")
    print("   📄  MODULE 4 — GENERATING PDF REPORT")
    print("=" * 65)
    write_log(log_file, "MODULE 4: Generating PDF report...")

    try:
        generate_report(devices, all_results, auditor_name=auditor_name, output_file=report_name)
        print(f"\n  ✅ Report saved: {report_name}")
        write_log(log_file, f"PDF saved: {report_name}")
    except Exception as e:
        print(f"  ❌ PDF Error: {e}")
        write_log(log_file, f"PDF Error: {e}")

    # ── SAVE JSON LOG ─────────────────────────────────────────
    json_log = os.path.join("scan_logs", f"scan_{timestamp}.json")
    try:
        with open(json_log, "w") as f:
            json.dump({
                "timestamp": timestamp,
                "auditor": auditor_name,
                "devices": all_results,
                "summary": {
                    "total_devices": len(devices),
                    "total_vulns": total_vulns,
                    "critical": total_critical,
                    "risk_label": net_risk_lbl,
                }
            }, f, indent=2, default=str)
        write_log(log_file, f"JSON log saved: {json_log}")
    except:
        pass

    write_log(log_file, "=== SCAN COMPLETE ===")
    print(f"\n  📝 Log saved: scan_logs/scan_{timestamp}.log")
    print(f"\n{'=' * 65}")
    print("   🏆  ALL MODULES COMPLETE!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
