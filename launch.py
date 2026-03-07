# launch.py — NetAudit Pro
# HOW IT WORKS:
#   1. Python runs the scan
#   2. Results are embedded INTO the HTML file
#   3. Browser just displays — no fetch() needed at all
#   4. PDF is opened directly via webbrowser module

import http.server, socketserver, webbrowser, threading
import os, sys, json, time, datetime, urllib.parse, socket

PORT = 8765

# ── Will be set after scan ──
_last_results = {}

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_OPTIONS(self):
        self._cors(); self.end_headers()

    def _cors(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_GET(self):
        path = urllib.parse.unquote(self.path.split("?")[0])

        # ── Serve PDF ──────────────────────────────────────────────────
        if path.startswith("/pdf/"):
            fname = path[5:]
            fpath = os.path.join(os.getcwd(), fname)
            if os.path.exists(fpath) and fname.endswith(".pdf"):
                data = open(fpath, "rb").read()
                self._cors()
                self.send_header("Content-Type",        "application/pdf")
                self.send_header("Content-Disposition", f"inline; filename={fname}")
                self.send_header("Content-Length",      str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            self.send_response(404); self.end_headers()
            self.wfile.write(b"PDF not found"); return

        # ── Serve topology ─────────────────────────────────────────────
        if path in ("/topology", "/topology.html"):
            fpath = os.path.join(os.getcwd(), "topology.html")
            if os.path.exists(fpath):
                data = open(fpath, "rb").read()
                self._cors()
                self.send_header("Content-Type",   "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            self.send_response(404); self.end_headers(); return

        # ── Serve GUI ──────────────────────────────────────────────────
        if path in ("/", "/gui.html", "/index.html"):
            fpath = os.path.join(os.getcwd(), "gui.html")
            if os.path.exists(fpath):
                data = open(fpath, "rb").read()
                self._cors()
                self.send_header("Content-Type",   "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return

        # ── Serve last results (cached) ────────────────────────────────
        if path == "/last_results":
            out = json.dumps(_last_results, default=str).encode()
            self._cors()
            self.send_header("Content-Type",   "application/json")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out); return

        self.send_response(404); self.end_headers()

    def do_POST(self):
        global _last_results
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}
        result = {"success": False, "error": "Unknown"}

        try:
            if self.path == "/scan":
                result = run_scan(body)
                _last_results = result
            elif self.path == "/ping":
                result = {"success": True, "message": "pong", "port": PORT}
        except Exception as e:
            import traceback; traceback.print_exc()
            result = {"success": False, "error": str(e)}

        out = json.dumps(result, default=str).encode()
        self._cors()
        self.send_header("Content-Type",   "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)


def run_scan(body):
    from scanner      import (scan_network, scan_ports, check_vulnerabilities,
                               detect_os, calculate_risk_score, get_risk_label)
    from report       import generate_report
    from attack_detector import AttackDetector
    import logging_system

    auditor     = body.get("auditor", "Anonymous Auditor")
    report_name = body.get("report_name", "")
    ts          = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not report_name:
        report_name = f"network_audit_{ts}.pdf"
    if not report_name.endswith(".pdf"):
        report_name += ".pdf"

    print(f"\n  [SCAN] Auditor : {auditor}")
    print(f"  [SCAN] Report  : {report_name}")

    log_file = logging_system.start_log(auditor, report_name)

    print("  [MODULE 1] Device Discovery...")
    devices, my_ip = scan_network()
    logging_system.log(log_file, f"Devices: {[d['ip'] for d in devices]} | My IP: {my_ip}")
    print(f"  [MODULE 1] Found {len(devices)} devices")

    all_results = []
    for d in devices:
        ip, mac = d["ip"], d["mac"]
        print(f"  [SCAN] Scanning {ip}...")

        os_info    = detect_os(ip)
        open_ports = scan_ports(ip)
        vulns      = check_vulnerabilities(open_ports)
        risk_score = calculate_risk_score(open_ports, vulns)
        risk_label = get_risk_label(risk_score)

        logging_system.log(log_file,
            f"{ip} | OS:{os_info['os']} | Ports:{len(open_ports)} | Vulns:{len(vulns)} | Risk:{risk_label}")
        print(f"  [SCAN] {ip} — {risk_label} ({risk_score}/10) — {len(open_ports)} ports — {len(vulns)} vulns")

        all_results.append({
            "ip": ip, "mac": mac, "is_me": (ip == my_ip),
            "os_info":        os_info,
            "open_ports":     open_ports,
            "vulnerabilities": vulns,
            "risk_score":     risk_score,
            "risk_label":     risk_label,
        })

    # Attack detection
    detector = AttackDetector()
    alerts   = detector.analyze_existing_ports(all_results)

    # PDF
    print("  [MODULE 4] Generating PDF...")
    generate_report(devices, all_results, auditor_name=auditor, output_file=report_name)
    print(f"  [MODULE 4] PDF saved: {report_name}")

    # Topology
    try:
        from topology import generate_topology
        generate_topology(all_results, my_ip, "topology.html")
    except Exception as e:
        print(f"  [TOPO] {e}")

    tV = sum(len(r["vulnerabilities"]) for r in all_results)
    tC = sum(1 for r in all_results for v in r["vulnerabilities"]
             if "CRITICAL" in v.get("severity",""))
    mR = max((r["risk_score"] for r in all_results), default=0)
    rl = get_risk_label(mR)

    logging_system.finish_log(log_file, len(devices), tV, tC, rl)
    print(f"  [DONE] {len(devices)} devices | {tV} vulns | {tC} critical | Risk:{rl}\n")

    return {
        "success":      True,
        "devices":      all_results,
        "alerts":       alerts,
        "report_file":  report_name,
        "report_url":   f"http://localhost:{PORT}/pdf/{report_name}",
        "topology_url": f"http://localhost:{PORT}/topology",
        "my_ip":        my_ip,
        "summary": {
            "total_devices": len(devices),
            "total_vulns":   tV,
            "critical":      tC,
            "max_risk":      mR,
            "risk_label":    rl,
            "alerts":        len(alerts),
        }
    }


def is_termux():
    """Detect if running inside Termux on Android."""
    return ("com.termux" in os.environ.get("PREFIX", "") or
            "com.termux" in os.environ.get("HOME", "") or
            os.path.exists("/data/data/com.termux"))


def check_admin():
    """Check admin/root — Termux skips root check and runs in limited mode."""
    if is_termux():
        return True   # Android Termux — skip root, run with available features
    if os.name == "nt":  # Windows
        try:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False
    else:  # Linux / macOS
        try:
            return os.getuid() == 0
        except Exception:
            return False


def relaunch_as_admin():
    """
    Elevate privileges — platform-aware:
      Windows → UAC popup (ShellExecuteW runas)
      Linux   → print sudo instructions and exit
      macOS   → print sudo instructions and exit
    """
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable,
                f'"{os.path.abspath(__file__)}"',
                os.path.dirname(os.path.abspath(__file__)), 1
            )
        except Exception as e:
            print(f"\n  ❌ Could not auto-elevate: {e}")
            print("  Please right-click RUN_ME.bat → Run as Administrator")
            input("\n  Press Enter to exit...")
        sys.exit(0)
    else:
        # Linux / macOS — can't auto-elevate, guide the user
        print("\n  ❌ Admin/root required for ARP network scanning.")
        print(f"\n  Run with sudo:")
        print(f"  sudo python3 \"{os.path.abspath(__file__)}\"")
        print("\n  Or on macOS/Linux you can also run:")
        print("  sudo python3 launch.py")
        input("\n  Press Enter to exit...")
        sys.exit(1)


def is_port_free(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(("127.0.0.1", port))
        s.close()
        return result != 0
    except:
        return True


def main():
    # ── CD to script directory so all files (gui.html etc) are found ──────
    # This fixes the issue when launched via double-click from any location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 60)
    print("  🛡️  NETAUDIT PRO  —  By SaiDinesh Andekar")
    print("=" * 60)

    # ── Check files ────────────────────────────────────────────────────
    if not os.path.exists("gui.html"):
        print(f"\n  ❌ gui.html not found!")
        print(f"  Make sure all project files are in the same folder.")
        input("\n  Press Enter to exit..."); sys.exit(1)

    # ── Auto-elevate to admin/root ─────────────────────────────────────
    if not check_admin():
        if os.name == "nt":
            print("\n  🔐 Requesting admin rights for network scanning...")
            print("  A UAC popup will appear — click YES to continue.")
        else:
            print("\n  🔐 Root required for ARP network scanning.")
        time.sleep(1.0)
        relaunch_as_admin()
        return

    if is_termux():
        print(f"\n  Mode       : 📱 Android Termux (limited — no ARP scan)")
        print(f"  Available  : Port scan, Vuln analysis, PDF, Risk scoring")
    else:
        print(f"\n  Admin mode : ✅ YES")

    # ── Check if already running ────────────────────────────────────────
    if not is_port_free(PORT):
        print(f"\n  ⚠️  Port {PORT} already in use.")
        print(f"  Another launch.py may already be running.")
        print(f"  Opening browser to existing server...")
        webbrowser.open(f"http://localhost:{PORT}/gui.html")
        input("\n  Press Enter to exit..."); return

    print(f"  Project dir: {os.getcwd()}")
    print(f"  Server URL : http://localhost:{PORT}")

    # ── Start server ────────────────────────────────────────────────────
    try:
        socketserver.TCPServer.allow_reuse_address = True
        server = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
    except OSError as e:
        print(f"\n  ❌ Cannot start server: {e}")
        print(f"  Try a different port or close other programs.")
        input("\n  Press Enter to exit..."); sys.exit(1)

    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.4)

    # ── Verify server is up ─────────────────────────────────────────────
    ok = not is_port_free(PORT)
    print(f"  Server up  : {'✅ YES' if ok else '❌ FAILED'}")

    if not ok:
        print("\n  ❌ Server failed to start!")
        print("  Possible fix: Try running as Administrator")
        input("\n  Press Enter to exit..."); sys.exit(1)

    # ── Open browser ────────────────────────────────────────────────────
    url = f"http://localhost:{PORT}/gui.html"
    webbrowser.open(url)
    print(f"\n  ✅ GUI opened: {url}")
    print(f"\n  📌 KEEP THIS WINDOW OPEN while using NetAudit Pro!")
    print(f"  📌 Press Ctrl+C to stop.\n")
    print("=" * 60)

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n  👋 Stopping server...")
        server.shutdown()
        print("  Goodbye!\n")


if __name__ == "__main__":
    main()