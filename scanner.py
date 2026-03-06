# scanner.py — NetAudit Pro Network Scanner
# Cross-platform: Windows 10/11, Linux, macOS
# Methods auto-select based on platform.system()

import socket, subprocess, platform, concurrent.futures, re

SYSTEM = platform.system().lower()   # "windows" | "linux" | "darwin"

VULN_DB = {
    21:   {"service":"FTP",       "risk":"HIGH",     "cvss":7.5,  "desc":"File Transfer Protocol",
           "hacker_can":["Brute force credentials","Anonymous login exploit","Sniff credentials in transit"],
           "fix":["Disable FTP, use SFTP instead","Block port 21 on firewall","Enforce strong passwords"]},
    22:   {"service":"SSH",       "risk":"MEDIUM",   "cvss":5.0,  "desc":"Secure Shell - remote access",
           "hacker_can":["Brute force SSH password","Exploit weak SSH keys","Dictionary attacks"],
           "fix":["Use SSH key authentication","Disable root login","Change default port"]},
    23:   {"service":"Telnet",    "risk":"CRITICAL", "cvss":9.8,  "desc":"Telnet - completely unencrypted",
           "hacker_can":["Capture all traffic in plaintext","Steal credentials instantly","Session hijacking"],
           "fix":["Disable Telnet immediately","Use SSH instead","Block port 23 on firewall"]},
    25:   {"service":"SMTP",      "risk":"MEDIUM",   "cvss":5.3,  "desc":"Email server",
           "hacker_can":["Open relay spam abuse","Email enumeration"],
           "fix":["Require SMTP authentication","Configure SPF/DKIM/DMARC"]},
    53:   {"service":"DNS",       "risk":"LOW",      "cvss":2.5,  "desc":"Domain Name System",
           "hacker_can":["DNS cache poisoning if misconfigured"],
           "fix":["Keep DNS software updated","Enable DNSSEC"]},
    80:   {"service":"HTTP",      "risk":"MEDIUM",   "cvss":5.0,  "desc":"Unencrypted web server",
           "hacker_can":["Intercept web traffic","Inject malicious content","Credential theft"],
           "fix":["Redirect to HTTPS","Install SSL certificate","Use HSTS headers"]},
    110:  {"service":"POP3",      "risk":"MEDIUM",   "cvss":4.8,  "desc":"Email retrieval unencrypted",
           "hacker_can":["Intercept email credentials","Read email in transit"],
           "fix":["Use POP3S (port 995)","Enforce TLS encryption"]},
    135:  {"service":"RPC",       "risk":"CRITICAL", "cvss":9.8,  "desc":"Remote Procedure Call",
           "hacker_can":["Exploit RPC (Blaster worm)","Execute remote code","Crash system remotely"],
           "fix":["Block port 135 on firewall","Keep Windows updated","Disable unused RPC services"]},
    139:  {"service":"NetBIOS",   "risk":"HIGH",     "cvss":8.1,  "desc":"Legacy Windows file sharing",
           "hacker_can":["Enumerate users and shares","Exploit null sessions","Lateral movement attacks"],
           "fix":["Disable NetBIOS over TCP/IP","Block ports 137-139","Use modern file sharing"]},
    143:  {"service":"IMAP",      "risk":"MEDIUM",   "cvss":4.8,  "desc":"Internet Message Access Protocol",
           "hacker_can":["Intercept email content","Credential theft in transit"],
           "fix":["Use IMAPS (port 993)","Enforce TLS"]},
    443:  {"service":"HTTPS",     "risk":"LOW",      "cvss":1.0,  "desc":"Encrypted web server",
           "hacker_can":["Possible SSL misconfiguration"],
           "fix":["Keep SSL certificates updated","Use TLS 1.3"]},
    445:  {"service":"SMB",       "risk":"CRITICAL", "cvss":10.0, "desc":"Server Message Block",
           "hacker_can":["Deploy WannaCry/NotPetya ransomware","Access shared files without auth","Execute remote code (EternalBlue)"],
           "fix":["Block port 445 on firewall immediately","Disable SMBv1","Keep Windows fully updated"]},
    1433: {"service":"MSSQL",     "risk":"HIGH",     "cvss":8.5,  "desc":"Microsoft SQL Server",
           "hacker_can":["SQL injection attacks","Brute force SA account","Data exfiltration"],
           "fix":["Restrict to trusted IPs only","Use strong SA password","Enable SQL Server Audit"]},
    3306: {"service":"MySQL",     "risk":"HIGH",     "cvss":8.0,  "desc":"MySQL Database Server",
           "hacker_can":["Brute force root account","SQL injection","Database dumping"],
           "fix":["Bind to localhost only","Use strong passwords","Disable remote root login"]},
    3389: {"service":"RDP",       "risk":"CRITICAL", "cvss":9.8,  "desc":"Remote Desktop Protocol",
           "hacker_can":["Brute force Windows password","Exploit BlueKeep","Take complete desktop control","Install ransomware"],
           "fix":["Disable RDP if not needed","Use VPN before RDP","Enable Network Level Authentication"]},
    5432: {"service":"PostgreSQL","risk":"HIGH",     "cvss":7.8,  "desc":"PostgreSQL Database",
           "hacker_can":["Brute force postgres account","Execute OS commands via COPY TO/FROM"],
           "fix":["Restrict pg_hba.conf access","Use strong passwords","Bind to localhost"]},
    6379: {"service":"Redis",     "risk":"CRITICAL", "cvss":9.8,  "desc":"Redis Cache - often no auth",
           "hacker_can":["Access all cached data without password","Write files to server","Execute remote code"],
           "fix":["Set requirepass in redis.conf","Bind to localhost","Never expose to internet"]},
    8080: {"service":"HTTP-Alt",  "risk":"MEDIUM",   "cvss":4.5,  "desc":"Alternate HTTP port",
           "hacker_can":["Intercept unencrypted traffic","Access web admin panels"],
           "fix":["Use HTTPS instead","Restrict access with firewall"]},
    8443: {"service":"HTTPS-Alt", "risk":"LOW",      "cvss":1.0,  "desc":"Alternate HTTPS port",
           "hacker_can":["Possible SSL misconfiguration"],
           "fix":["Keep certificates updated"]},
    27017:{"service":"MongoDB",   "risk":"CRITICAL", "cvss":9.8,  "desc":"MongoDB - often no auth",
           "hacker_can":["Access all databases without credentials","Delete or modify all data","Export entire database"],
           "fix":["Enable MongoDB authentication","Bind to localhost","Never expose to internet"]},
}
PORTS_TO_SCAN = list(VULN_DB.keys())


# ── OS DETECTION ──────────────────────────────────────────────────────────────
def detect_os(ip):
    try:
        if SYSTEM == "windows":
            cmd = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
        ttl = None
        for word in result.stdout.split():
            if "ttl=" in word.lower():
                try:
                    ttl = int(word.lower().split("ttl=")[1].rstrip("."))
                    break
                except ValueError:
                    pass
        if ttl is None:
            return {"os": "Unknown", "ttl": None, "confidence": "Low"}
        if ttl <= 64:
            return {"os": "Linux / Unix / Android", "ttl": ttl, "confidence": "Medium"}
        elif ttl <= 128:
            return {"os": "Windows", "ttl": ttl, "confidence": "Medium"}
        else:
            return {"os": "Network Device (Router/Switch)", "ttl": ttl, "confidence": "Medium"}
    except Exception:
        return {"os": "Unknown", "ttl": None, "confidence": "Low"}


# ── GET REAL LOCAL IP ─────────────────────────────────────────────────────────
def get_real_local_ip():
    candidates = []

    # Method 1: UDP route trick (works on all platforms)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if not ip.startswith(("127.", "169.254")):
            candidates.append(ip)
    except Exception:
        pass

    # Method 2: Hostname resolution (all platforms)
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None):
            ip = info[4][0]
            if not ip.startswith(("127.", "169.254", "::")) and ":" not in ip:
                candidates.append(ip)
    except Exception:
        pass

    # Method 3: Platform-specific IP tools
    if SYSTEM == "windows":
        try:
            result = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=5)
            for line in result.stdout.split("\n"):
                line = line.strip()
                if "IPv4" in line and ":" in line:
                    ip = line.split(":")[-1].strip()
                    if not ip.startswith(("169.254", "127.")):
                        candidates.append(ip)
        except Exception:
            pass
    elif SYSTEM == "linux":
        try:
            result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True, timeout=5)
            for match in re.findall(r"inet (\d+\.\d+\.\d+\.\d+)", result.stdout):
                if not match.startswith(("127.", "169.254")):
                    candidates.append(match)
        except Exception:
            pass
    elif SYSTEM == "darwin":
        try:
            result = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=5)
            for match in re.findall(r"inet (\d+\.\d+\.\d+\.\d+)", result.stdout):
                if not match.startswith(("127.", "169.254")):
                    candidates.append(match)
        except Exception:
            pass

    for ip in candidates:
        if ip.startswith(("192.168.", "10.", "172.")):
            return ip
    for ip in candidates:
        if not ip.startswith("169.254"):
            return ip
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "127.0.0.1"


# ── PING HELPER ───────────────────────────────────────────────────────────────
def _ping(ip):
    try:
        if SYSTEM == "windows":
            r = subprocess.run(["ping", "-n", "1", "-w", "500", ip], capture_output=True, timeout=2)
        else:
            r = subprocess.run(["ping", "-c", "1", "-W", "1", ip], capture_output=True, timeout=2)
        return ip if r.returncode == 0 else None
    except Exception:
        return None


# ── MAC FROM ARP TABLE ────────────────────────────────────────────────────────
def _get_mac_arp_table(ip):
    """Windows uses dashes (aa-bb-cc), Linux/Mac use colons (aa:bb:cc)."""
    try:
        if SYSTEM == "windows":
            r = subprocess.run(["arp", "-a", ip], capture_output=True, text=True, timeout=3)
            for line in r.stdout.split("\n"):
                if ip in line:
                    for part in line.split():
                        if re.match(r"^([0-9a-f]{2}-){5}[0-9a-f]{2}$", part.lower()):
                            return part.replace("-", ":").lower()
        else:
            r = subprocess.run(["arp", "-n", ip], capture_output=True, text=True, timeout=3)
            for line in r.stdout.split("\n"):
                if ip in line:
                    for part in line.split():
                        if re.match(r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$", part.lower()):
                            return part.lower()
    except Exception:
        pass
    return "00:00:00:00:00:00"


# ── PARSE FULL ARP TABLE ──────────────────────────────────────────────────────
def _parse_arp_table():
    devices   = []
    skip_pfx  = ("224.", "239.", "255.", "169.254", "127.", "0.")
    skip_macs = {"ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00"}
    seen_ips  = set()

    def _add(ip, mac):
        seg = ip.split(".")
        if len(seg) != 4:
            return
        try:
            nums = [int(s) for s in seg]
            if not all(0 <= n <= 255 for n in nums) or nums[3] in (0, 255):
                return
        except ValueError:
            return
        if any(ip.startswith(s) for s in skip_pfx):
            return
        if mac in skip_macs or ip in seen_ips:
            return
        seen_ips.add(ip)
        devices.append({"ip": ip, "mac": mac})

    if SYSTEM == "windows":
        try:
            r = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                parts = line.split()
                if len(parts) < 2:
                    continue
                ip = parts[0].strip("()")
                mac_raw = parts[1] if len(parts) > 1 else ""
                if re.match(r"^([0-9a-f]{2}-){5}[0-9a-f]{2}$", mac_raw.lower()):
                    _add(ip, mac_raw.replace("-", ":").lower())
        except Exception:
            pass

    elif SYSTEM == "linux":
        # arp -n
        try:
            r = subprocess.run(["arp", "-n"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                parts = line.split()
                if not parts:
                    continue
                ip = parts[0]
                for part in parts:
                    if re.match(r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$", part.lower()):
                        _add(ip, part.lower())
                        break
        except Exception:
            pass
        # ip neigh (modern Linux — more complete)
        try:
            r = subprocess.run(["ip", "neigh"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                parts = line.split()
                if not parts:
                    continue
                ip = parts[0]
                for part in parts:
                    if re.match(r"^([0-9a-f]{2}:){5}[0-9a-f]{2}$", part.lower()):
                        _add(ip, part.lower())
                        break
        except Exception:
            pass

    elif SYSTEM == "darwin":
        try:
            r = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5)
            # macOS: hostname (ip) at mac on interface
            for line in r.stdout.split("\n"):
                m_ip  = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)", line)
                m_mac = re.search(r"(([0-9a-f]{1,2}:){5}[0-9a-f]{1,2})", line.lower())
                if m_ip and m_mac:
                    mac = ":".join(p.zfill(2) for p in m_mac.group(1).split(":"))
                    _add(m_ip.group(1), mac)
        except Exception:
            pass

    return devices


# ── NETWORK SCANNER ───────────────────────────────────────────────────────────
def scan_network():
    local_ip = get_real_local_ip()
    print(f"  [SCANNER] Platform  : {platform.system()} {platform.release()}")
    print(f"  [SCANNER] Local IP  : {local_ip}")

    if local_ip.startswith("169.254"):
        print("  [SCANNER] *** WARNING: APIPA — not properly connected to network! ***")

    parts = local_ip.split(".")
    if len(parts) != 4:
        return [], local_ip
    base    = ".".join(parts[:3])
    network = base + ".0/24"
    print(f"  [SCANNER] Network   : {network}")

    devices = []

    # Method 1: Scapy ARP broadcast
    print("  [SCANNER] Method 1: Scapy ARP broadcast...")
    try:
        from scapy.all import ARP, Ether, srp
        ether  = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp    = ARP(pdst=network)
        result = srp(ether/arp, timeout=3, verbose=0)[0]
        for _, rcv in result:
            ip  = rcv.psrc
            mac = rcv.hwsrc.lower()
            if not any(d["ip"] == ip for d in devices):
                devices.append({"ip": ip, "mac": mac})
        print(f"  [SCANNER] Scapy found: {len(devices)}")
    except ImportError:
        print("  [SCANNER] Scapy not installed — skipping (install: pip install scapy)")
    except Exception as e:
        print(f"  [SCANNER] Scapy failed: {e}")

    # Method 2: Ping sweep
    print("  [SCANNER] Method 2: Ping sweep...")
    all_ips = [f"{base}.{i}" for i in range(1, 255)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=80) as ex:
        alive = list(filter(None, ex.map(_ping, all_ips)))
    for ip in alive:
        if not any(d["ip"] == ip for d in devices):
            devices.append({"ip": ip, "mac": _get_mac_arp_table(ip)})
    print(f"  [SCANNER] Ping found: {len(alive)} alive")

    # Method 3: ARP table
    print("  [SCANNER] Method 3: ARP table...")
    added = 0
    for d in _parse_arp_table():
        if d["ip"].startswith(base + "."):
            if not any(e["ip"] == d["ip"] for e in devices):
                devices.append(d)
                added += 1
    print(f"  [SCANNER] ARP table added: {added}")

    # Always include self
    if not any(d["ip"] == local_ip for d in devices):
        devices.insert(0, {"ip": local_ip, "mac": _get_mac_arp_table(local_ip) or "00:00:00:00:00:00"})

    # Always check router (.1)
    router_ip = base + ".1"
    if not any(d["ip"] == router_ip for d in devices):
        if _ping(router_ip):
            devices.append({"ip": router_ip, "mac": _get_mac_arp_table(router_ip)})
            print(f"  [SCANNER] Router found: {router_ip}")

    # Final cleanup — remove duplicates, broadcast, multicast
    seen    = set()
    cleaned = []
    for d in devices:
        ip  = d["ip"]
        mac = d.get("mac", "00:00:00:00:00:00").lower()
        if ip in seen:
            continue
        try:
            last = int(ip.split(".")[-1])
            if last in (0, 255):
                continue
        except ValueError:
            continue
        if mac == "ff:ff:ff:ff:ff:ff":
            continue
        seen.add(ip)
        cleaned.append(d)

    cleaned.sort(key=lambda d: int(d["ip"].split(".")[-1]))
    print(f"  [SCANNER] Final: {[d['ip'] for d in cleaned]}")
    return cleaned, local_ip


# ── PORT SCANNER ──────────────────────────────────────────────────────────────
def scan_single_port(ip, port, timeout=1.0):
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        return port if result == 0 else None
    except Exception:
        return None
    finally:
        if s:
            try: s.close()
            except Exception: pass


def scan_ports(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        futures = {ex.submit(scan_single_port, ip, p): p for p in PORTS_TO_SCAN}
        for f in concurrent.futures.as_completed(futures):
            p = f.result()
            if p:
                info = VULN_DB.get(p, {})
                open_ports.append({
                    "port":    p,
                    "service": info.get("service", "Unknown"),
                    "risk":    info.get("risk",    "UNKNOWN"),
                    "cvss":    info.get("cvss",    0),
                    "desc":    info.get("desc",    ""),
                })
    return sorted(open_ports, key=lambda x: x["cvss"], reverse=True)


# ── VULNERABILITY ANALYSIS ────────────────────────────────────────────────────
def check_vulnerabilities(open_ports):
    vulns = []
    for p in open_ports:
        port = p["port"]
        if port in VULN_DB and VULN_DB[port]["cvss"] >= 4.0:
            db = VULN_DB[port]
            vulns.append({
                "port":       port,
                "name":       db["service"] + " - " + db["desc"],
                "severity":   ("CRITICAL" if db["cvss"] >= 9 else
                               "HIGH"     if db["cvss"] >= 7 else "MEDIUM"),
                "cvss_score": db["cvss"],
                "hacker_can": db["hacker_can"],
                "fix":        db["fix"],
            })
    return vulns


# ── RISK SCORING ──────────────────────────────────────────────────────────────
def calculate_risk_score(open_ports, vulnerabilities):
    if not open_ports:
        return 0.0
    score = min(2.0, len(open_ports) * 0.4)
    if vulnerabilities:
        avg   = sum(v["cvss_score"] for v in vulnerabilities) / len(vulnerabilities)
        mx    = max(v["cvss_score"] for v in vulnerabilities)
        score += (avg / 10) * 3.5 + (mx / 10) * 3.5
    if any(p["port"] in {23, 445, 3389, 6379, 27017} for p in open_ports):
        score += 0.5
    return min(10.0, round(score, 1))


def get_risk_label(score):
    if score >= 8: return "CRITICAL"
    if score >= 6: return "HIGH"
    if score >= 4: return "MEDIUM"
    if score >= 2: return "LOW"
    return "MINIMAL"