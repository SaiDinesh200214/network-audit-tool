# main.py
# HOME NETWORK SECURITY AUDIT TOOL

from scanner import scan_network, scan_ports, check_vulnerabilities
import datetime
import os

# ─── WELCOME SCREEN ─────────────────────────────
os.system('cls' if os.name == 'nt' else 'clear')

print("\n" + "=" * 65)
print("   🛡️   HOME NETWORK SECURITY AUDIT TOOL")
print("   Version 1.0 | By SaiDinesh Andekar")
print("   📧 saidineshandekar1402@gmail.com")
print("   🐙 github.com/SaiDinesh200214")
print("=" * 65)
print("""
  This tool will:
  📡 Scan your network for connected devices
  🚪 Check open ports on each device
  ⚠️  Analyze vulnerabilities
  📄 Generate a professional PDF report
""")
print("=" * 65)

# Ask for auditor name
auditor_name = input("\n  👤 Enter your name (for the report): ").strip()
if not auditor_name:
    auditor_name = "Anonymous Auditor"

report_name = input("  📄 Enter report filename (press Enter for default): ").strip()
if not report_name:
    report_name = f"network_audit_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
elif not report_name.endswith('.pdf'):
    report_name += '.pdf'

print(f"\n  ✅ Starting scan as: {auditor_name}")
print(f"  ✅ Report will be saved as: {report_name}")
input("\n  Press Enter to begin scan...")

# ─── HEADER ─────────────────────────────────────
print("\n" + "=" * 65)
print("   🛡️   HOME NETWORK SECURITY AUDIT TOOL")
print("   Created by SaiDinesh Andekar | github.com/SaiDinesh200214")
print("=" * 65)
print(f"   📅 Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 65)

# ─── MODULE 1 — DEVICE SCAN ─────────────────────
print("\n📡 MODULE 1 — SCANNING FOR DEVICES...\n")
devices, my_ip = scan_network()

if not devices:
    print("❌ No devices found. Run as Administrator.")
    exit()

print(f"✅ Found {len(devices)} device(s):\n")
print(f"  {'No.':<5} {'IP Address':<18} {'MAC Address':<20} {'Note'}")
print("  " + "-" * 58)
for i, device in enumerate(devices, 1):
    note = "⬅️  YOU" if device['ip'] == my_ip else "📱 Device"
    print(f"  {i:<5} {device['ip']:<18} {device['mac']:<20} {note}")

# ─── MODULE 2 & 3 — PORT SCAN + VULN CHECK ──────
all_results = []

for device in devices:
    ip = device['ip']
    label = "⬅️  YOUR MACHINE" if ip == my_ip else "📱 Unknown Device"

    print(f"\n\n{'=' * 65}")
    print(f"  📍 {ip}  {label}")
    print(f"{'=' * 65}")

    # Module 2 — Port Scan
    print(f"\n🚪 MODULE 2 — PORT SCAN\n")
    open_ports = scan_ports(ip)

    if open_ports:
        print(f"  {'Port':<8} {'Service':<14} {'Risk':<12} {'Description'}")
        print("  " + "-" * 62)
        for p in open_ports:
            print(f"  {p['port']:<8} {p['service']:<14} {p['risk']:<12} {p['description']}")
    else:
        print(f"  ✅ No common open ports found — this device looks safe!")

    # Module 3 — Vulnerability Check
    print(f"\n⚠️  MODULE 3 — VULNERABILITY ANALYSIS\n")
    vulns = check_vulnerabilities(open_ports)

    if vulns:
        for v in vulns:
            print(f"  ┌─ Port {v['port']} — {v['name']}")
            print(f"  │  Severity  : {v['severity']}  (CVSS: {v['cvss_score']}/10)")
            print(f"  │  What is it: {v['what_is_it']}")
            print(f"  │  Hacker can:")
            for h in v['hacker_can']:
                print(f"  │    💀 {h}")
            print(f"  │  How to fix:")
            for f in v['fix']:
                print(f"  │    🛡️  {f}")
            print(f"  └{'─' * 55}")
    else:
        print(f"  ✅ No known vulnerabilities found!")

    all_results.append({
        'ip': ip,
        'mac': device['mac'],
        'open_ports': open_ports,
        'vulnerabilities': vulns
    })

# ─── SUMMARY ────────────────────────────────────
print(f"\n\n{'=' * 65}")
print("📊 FINAL SUMMARY")
print(f"{'=' * 65}")
total_vulns = sum(len(r['vulnerabilities']) for r in all_results)
critical = sum(1 for r in all_results for v in r['vulnerabilities'] if '🔴' in v['severity'])
print(f"  🖥️  Devices Scanned       : {len(devices)}")
print(f"  ⚠️  Total Vulnerabilities : {total_vulns}")
print(f"  🔴 Critical Issues       : {critical}")
print(f"\n{'=' * 65}")
print("✅ Modules 1, 2 & 3 DONE! One more module left — PDF Report!")
print(f"{'=' * 65}\n")

# ─── MODULE 4 — GENERATE PDF REPORT ─────────────
print("\n📄 MODULE 4 — GENERATING PDF REPORT...\n")
from report import generate_report
report_file = generate_report(devices, all_results, auditor_name=auditor_name, output_file=report_name)
print(f"\n{'=' * 65}")
print(f"🏆 ALL 4 MODULES COMPLETE!")
print(f"📄 Your report is saved as: {report_file}")
print(f"{'=' * 65}\n")