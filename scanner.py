# scanner.py
# Home Network Security Audit Tool — Scanner Module

from scapy.all import ARP, Ether, srp
import socket
import concurrent.futures

# ─── MODULE 1 — DEVICE SCANNER ──────────────────

def get_my_ip():
    """Get our own IP address on the network"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def scan_network():
    """Scan the network and return list of connected devices"""
    my_ip = get_my_ip()
    network = my_ip.rsplit('.', 1)[0] + '.1/24'

    print(f"\n🔍 Your IP Address : {my_ip}")
    print(f"🌐 Scanning Network: {network}")
    print(f"⏳ Please wait...\n")

    arp_request = ARP(pdst=network)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast / arp_request

    answered, _ = srp(arp_broadcast, timeout=3, verbose=False)

    devices = []
    for sent, received in answered:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc
        })

    return devices, my_ip


# ─── MODULE 2 — PORT SCANNER ────────────────────

COMMON_PORTS = {
    21:   ("FTP",         "🔴 HIGH",   "File Transfer — often exploited"),
    22:   ("SSH",         "🔴 HIGH",   "Remote access — brute force target"),
    23:   ("Telnet",      "🔴 HIGH",   "Unencrypted remote access — dangerous"),
    25:   ("SMTP",        "🟡 MEDIUM", "Email server"),
    53:   ("DNS",         "🟢 LOW",    "Domain name resolution"),
    80:   ("HTTP",        "🟡 MEDIUM", "Unencrypted web traffic"),
    110:  ("POP3",        "🟡 MEDIUM", "Email retrieval"),
    135:  ("RPC",         "🔴 HIGH",   "Windows RPC — common attack vector"),
    139:  ("NetBIOS",     "🔴 HIGH",   "Windows file sharing — exploitable"),
    143:  ("IMAP",        "🟡 MEDIUM", "Email access"),
    443:  ("HTTPS",       "🟢 LOW",    "Encrypted web traffic — safe"),
    445:  ("SMB",         "🔴 HIGH",   "Windows sharing — WannaCry target"),
    1433: ("MSSQL",       "🔴 HIGH",   "Microsoft SQL Server"),
    1883: ("MQTT",        "🔴 HIGH",   "IoT protocol — often unsecured"),
    3306: ("MySQL",       "🔴 HIGH",   "Database — should never be public"),
    3389: ("RDP",         "🔴 HIGH",   "Remote Desktop — brute force target"),
    5432: ("PostgreSQL",  "🔴 HIGH",   "Database port"),
    5900: ("VNC",         "🔴 HIGH",   "Remote desktop — often unencrypted"),
    8080: ("HTTP-Alt",    "🟡 MEDIUM", "Alternative web port"),
    8443: ("HTTPS-Alt",   "🟡 MEDIUM", "Alternative secure web port"),
    27017:("MongoDB",     "🔴 HIGH",   "Database — often left open by mistake"),
}

def check_port(ip, port, timeout=1):
    """Check if a single port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(ip):
    """Scan all common ports on a given IP"""
    print(f"\n  🚪 Scanning ports on {ip}...")

    open_ports = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_port = {
            executor.submit(check_port, ip, port): port
            for port in COMMON_PORTS
        }

        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            is_open = future.result()

            if is_open:
                service, risk, description = COMMON_PORTS[port]
                open_ports.append({
                    'port': port,
                    'service': service,
                    'risk': risk,
                    'description': description
                })

    open_ports.sort(key=lambda x: x['port'])
    return open_ports

# ─── MODULE 3 — VULNERABILITY CHECKER ───────────

VULNERABILITY_DB = {
    21: {
        "name": "FTP - File Transfer Protocol",
        "severity": "🔴 CRITICAL",
        "what_is_it": "FTP is an old protocol used to transfer files between computers.",
        "hacker_can": [
            "Intercept files being transferred (no encryption)",
            "Brute force weak passwords",
            "Use anonymous login if misconfigured",
            "Upload malicious files to the server"
        ],
        "fix": [
            "Disable FTP if not needed",
            "Use SFTP instead (encrypted version)",
            "Enforce strong passwords",
            "Disable anonymous login"
        ],
        "cvss_score": 9.8
    },
    22: {
        "name": "SSH - Secure Shell",
        "severity": "🟡 MEDIUM",
        "what_is_it": "SSH allows secure remote access to a computer.",
        "hacker_can": [
            "Brute force weak passwords",
            "Exploit outdated SSH versions",
            "Try stolen credentials"
        ],
        "fix": [
            "Use SSH keys instead of passwords",
            "Disable root login",
            "Change default port 22",
            "Use fail2ban to block brute force"
        ],
        "cvss_score": 5.5
    },
    23: {
        "name": "Telnet",
        "severity": "🔴 CRITICAL",
        "what_is_it": "Telnet is an old remote access protocol with NO encryption.",
        "hacker_can": [
            "Intercept ALL data including passwords (plain text)",
            "Hijack active sessions",
            "Perform man-in-the-middle attacks"
        ],
        "fix": [
            "Disable Telnet immediately",
            "Use SSH instead",
            "Block port 23 on firewall"
        ],
        "cvss_score": 9.8
    },
    80: {
        "name": "HTTP - Web Server",
        "severity": "🟡 MEDIUM",
        "what_is_it": "An unencrypted web server is running on this device.",
        "hacker_can": [
            "Intercept web traffic (no encryption)",
            "Inject malicious content",
            "Steal login credentials sent over HTTP"
        ],
        "fix": [
            "Redirect all HTTP to HTTPS",
            "Install SSL certificate",
            "Enable HSTS header"
        ],
        "cvss_score": 5.0
    },
    135: {
        "name": "RPC - Remote Procedure Call",
        "severity": "🔴 CRITICAL",
        "what_is_it": "Windows RPC allows programs to request services from other computers.",
        "hacker_can": [
            "Exploit RPC vulnerabilities (used in famous Blaster worm)",
            "Execute remote code on your machine",
            "Crash your system remotely"
        ],
        "fix": [
            "Block port 135 on firewall",
            "Keep Windows updated",
            "Disable unnecessary RPC services"
        ],
        "cvss_score": 9.8
    },
    139: {
        "name": "NetBIOS - Network Basic Input/Output System",
        "severity": "🔴 CRITICAL",
        "what_is_it": "NetBIOS allows computers to share files and printers on a network.",
        "hacker_can": [
            "Enumerate users and shares on your PC",
            "Exploit null sessions to access data",
            "Use it for lateral movement in a network attack"
        ],
        "fix": [
            "Disable NetBIOS over TCP/IP",
            "Block ports 137-139 on firewall",
            "Use modern file sharing instead"
        ],
        "cvss_score": 8.1
    },
    443: {
        "name": "HTTPS - Secure Web Server",
        "severity": "🟢 LOW",
        "what_is_it": "An encrypted web server is running — this is normal and safe.",
        "hacker_can": [
            "Exploit outdated SSL/TLS versions",
            "Use expired certificates"
        ],
        "fix": [
            "Keep SSL certificates updated",
            "Use TLS 1.2 or higher",
            "Disable old SSL versions"
        ],
        "cvss_score": 2.0
    },
    445: {
        "name": "SMB - Server Message Block",
        "severity": "🔴 CRITICAL",
        "what_is_it": "SMB is used for Windows file sharing. Famous for WannaCry ransomware.",
        "hacker_can": [
            "Deploy WannaCry or NotPetya ransomware",
            "Access shared files without authentication",
            "Move laterally across the entire network",
            "Execute remote code (EternalBlue exploit)"
        ],
        "fix": [
            "Block port 445 on firewall immediately",
            "Disable SMBv1",
            "Keep Windows fully updated",
            "Never expose SMB to the internet"
        ],
        "cvss_score": 10.0
    },
    3306: {
        "name": "MySQL Database",
        "severity": "🔴 CRITICAL",
        "what_is_it": "A MySQL database is exposed on the network.",
        "hacker_can": [
            "Access all your database data",
            "Brute force database credentials",
            "Dump entire database contents",
            "Inject malicious SQL queries"
        ],
        "fix": [
            "Never expose database to public network",
            "Bind MySQL to localhost only",
            "Use strong passwords",
            "Enable firewall rules"
        ],
        "cvss_score": 9.8
    },
    3389: {
        "name": "RDP - Remote Desktop Protocol",
        "severity": "🔴 CRITICAL",
        "what_is_it": "RDP allows remote desktop access to your Windows machine.",
        "hacker_can": [
            "Brute force your Windows password",
            "Exploit BlueKeep vulnerability (no auth needed)",
            "Take complete control of your desktop",
            "Install ransomware or malware"
        ],
        "fix": [
            "Disable RDP if not needed",
            "Use VPN before allowing RDP",
            "Enable Network Level Authentication",
            "Change default RDP port",
            "Use strong passwords + 2FA"
        ],
        "cvss_score": 9.8
    },
    5900: {
        "name": "VNC - Virtual Network Computing",
        "severity": "🔴 CRITICAL",
        "what_is_it": "VNC provides remote desktop access, often with weak security.",
        "hacker_can": [
            "View your screen in real time",
            "Control your mouse and keyboard",
            "Brute force weak VNC passwords"
        ],
        "fix": [
            "Add strong VNC password",
            "Use VPN tunnel for VNC",
            "Disable if not needed"
        ],
        "cvss_score": 9.8
    },
    8080: {
        "name": "HTTP Alternate Port",
        "severity": "🟡 MEDIUM",
        "what_is_it": "An alternate web server port — often used for dev servers or proxies.",
        "hacker_can": [
            "Access development servers with debug info",
            "Find exposed admin panels",
            "Exploit misconfigured proxy servers"
        ],
        "fix": [
            "Secure or disable if not needed",
            "Add authentication",
            "Use HTTPS instead"
        ],
        "cvss_score": 5.0
    },
    27017: {
        "name": "MongoDB Database",
        "severity": "🔴 CRITICAL",
        "what_is_it": "A MongoDB database is exposed — historically left open with no auth.",
        "hacker_can": [
            "Access ALL database records with no password",
            "Delete or encrypt your data for ransom",
            "Exfiltrate sensitive information"
        ],
        "fix": [
            "Enable MongoDB authentication immediately",
            "Bind to localhost only",
            "Block port 27017 on firewall"
        ],
        "cvss_score": 10.0
    }
}

def check_vulnerabilities(open_ports):
    """Check vulnerabilities for each open port"""
    
    vulnerabilities = []
    
    for port_info in open_ports:
        port = port_info['port']
        
        if port in VULNERABILITY_DB:
            vuln = VULNERABILITY_DB[port].copy()
            vuln['port'] = port
            vulnerabilities.append(vuln)
        else:
            # Generic entry for unknown ports
            vulnerabilities.append({
                'port': port,
                'name': port_info['service'],
                'severity': port_info['risk'],
                'what_is_it': "Unknown service running on this port.",
                'hacker_can': ["Exploit unknown services"],
                'fix': ["Investigate and close if not needed"],
                'cvss_score': 5.0
            })
    
    # Sort by CVSS score — most dangerous first
    vulnerabilities.sort(key=lambda x: x['cvss_score'], reverse=True)
    return vulnerabilities