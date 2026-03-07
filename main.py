# ============================================================
# NetAudit Pro - Home Network Security Audit Tool
# Copyright (c) 2026 SaiDinesh Andekar
# GitHub  : github.com/SaiDinesh200214
# Email   : saidineshandekar1402@gmail.com
# License : MIT with Attribution (see LICENSE file)
# ============================================================

import datetime, os, sys, json, time

R  = '\033[0m'
B  = '\033[94m'
BC = '\033[96m'
BG = '\033[92m'
BY = '\033[93m'
BR = '\033[91m'
BM = '\033[95m'
DM = '\033[2m'
BD = '\033[1m'
OR = '\033[38;5;208m'
W  = '\033[97m'

def col(c, t): return c + str(t) + R

def supports_color():
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
            return True
        except: return False
    return True

if not supports_color():
    R=B=BC=BG=BY=BR=BM=DM=BD=OR=W=''

def TW():
    try:
        import shutil
        w = shutil.get_terminal_size((70,20)).columns
        return max(50, min(w-2, 90))
    except: return 68

def is_termux():
    import os as _os
    return ("com.termux" in _os.environ.get("PREFIX","") or
            "com.termux" in _os.environ.get("HOME","") or
            _os.path.exists("/data/data/com.termux"))

def print_banner():
    print()
    if is_termux():
        # Compact banner for narrow mobile screen
        w = TW()
        inner = w - 2
        print(col(BC+BD, '+' + '='*inner + '+'))
        # Line 1 - tool name centered
        name  = '  NETAUDIT PRO  '
        pad_l = (inner - len(name)) // 2
        pad_r = inner - len(name) - pad_l
        print(col(BC+BD, '|') + ' '*pad_l + col(BC+BD, name) + ' '*pad_r + col(BC+BD, '|'))
        # Line 2 - version centered
        ver   = '  v2.3  |  Network Security Tool  '
        pad_l = (inner - len(ver)) // 2
        pad_r = inner - len(ver) - pad_l
        if pad_l < 0: pad_l = 0
        if pad_r < 0: pad_r = 0
        print(col(BC+BD, '|') + ' '*pad_l + col(W, ver) + ' '*pad_r + col(BC+BD, '|'))
        # Line 3 - author centered
        auth  = '  By SaiDinesh Andekar  '
        pad_l = (inner - len(auth)) // 2
        pad_r = inner - len(auth) - pad_l
        print(col(BC+BD, '|') + ' '*pad_l + col(BY, auth) + ' '*pad_r + col(BC+BD, '|'))
        print(col(BC+BD, '+' + '='*inner + '+'))
        print()
    else:
        # Full ASCII art banner for PC/laptop
        print(BC+BD + r"  ███╗   ██╗███████╗████████╗ █████╗ ██╗   ██╗██████╗ ██╗████████╗   ██████╗ ██████╗  ██████╗ " +R)
        print(BC+BD + r"  ████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║   ██║██╔══██╗██║╚══██╔══╝   ██╔══██╗██╔══██╗██╔═══██╗" +R)
        print(BC+BD + r"  ██╔██╗ ██║█████╗     ██║   ███████║██║   ██║██║  ██║██║   ██║       ██████╔╝██████╔╝██║   ██║" +R)
        print(BC+BD + r"  ██║╚██╗██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║██║   ██║       ██╔═══╝ ██╔══██╗██║   ██║" +R)
        print(BC+BD + r"  ██║ ╚████║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝██║   ██║       ██║     ██║  ██║╚██████╔╝" +R)
        print(BC+BD + r"  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝" +R)
        print(BC + '  ' + chr(9472)*95 + R)
        print(BC+BD + '  HOME NETWORK SECURITY AUDIT TOOL  .  v2.3  .  By SaiDinesh Andekar' + R)
        print(BC + '  ' + chr(9472)*95 + R)
        print()

def divider(char='=', color=BC):
    return col(color, char * TW())

def section(title, plain_title, color=BC):
    w = TW()
    inner = w - 2
    pad_l = (inner - len(plain_title) - 2) // 2
    pad_r = inner - len(plain_title) - 2 - pad_l
    if pad_l < 0: pad_l = 0
    if pad_r < 0: pad_r = 0
    print()
    print(col(color+BD, '+' + '-'*inner + '+'))
    print(col(color+BD, '|') + ' '*pad_l + '  ' + col(W+BD, plain_title) + ' '*pad_r + col(color+BD, '|'))
    print(col(color+BD, '+' + '-'*inner + '+'))

def info_box(plain_lines, colored_lines, color=B):
    w = TW()
    inner = w - 2
    print(col(color+BD, '+' + '-'*inner + '+'))
    for plain, colored in zip(plain_lines, colored_lines):
        pad = inner - len(plain) - 2
        if pad < 0: pad = 0
        print(col(color+BD, '|') + '  ' + colored + ' '*pad + col(color+BD, '|'))
    print(col(color+BD, '+' + '-'*inner + '+'))

def device_box(ip, label, color=B):
    w = TW()
    inner = w - 2
    plain = '  ' + ip + '  --  ' + label
    pad = inner - len(plain) - 2
    if pad < 0: pad = 0
    lc = BY+BD if label == 'YOUR MACHINE' else W+BD
    print()
    print(col(color+BD, '+' + '-'*inner + '+'))
    print(col(color+BD, '|') + '  ' + col(lc, ip) + col(W, '  --  ') + col(lc, label) + ' '*pad + col(color+BD, '|'))
    print(col(color+BD, '+' + '-'*inner + '+'))

def spinner(msg, duration=0.8):
    frames = ['-','\\','|','/']
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print('\r  ' + col(BC, '['+frames[i%4]+']') + '  ' + col(W, msg) + '   ', end='', flush=True)
        time.sleep(0.1)
        i += 1
    print('\r  ' + col(BG+BD, '[OK]') + '  ' + col(W, msg) + '   ')

def progress_bar(label, width=40, color=BC):
    print('\n  ' + col(W+BD, label))
    for i in range(width+1):
        filled = col(color, '#'*i)
        empty  = col(DM, '.'*(width-i))
        pct    = col(BY+BD, str(int((i/width)*100))+'%')
        print('\r  [' + filled + empty + '] ' + pct, end='', flush=True)
        time.sleep(0.018)
    print('  ' + col(BG+BD, ' DONE'))

def risk_col(label):
    return {'CRITICAL':BR+BD,'HIGH':OR+BD,'MEDIUM':BY+BD,'LOW':BG+BD,'MINIMAL':BC+BD}.get(label, W+BD)

def risk_icon(label):
    return {'CRITICAL':'[!!]','HIGH':'[! ]','MEDIUM':'[~ ]','LOW':'[. ]','MINIMAL':'[  ]'}.get(label,'[  ]')

def setup_logging():
    os.makedirs('scan_logs', exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join('scan_logs', 'scan_'+ts+'.log'), ts

def write_log(log_file, message):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write('['+ts+'] '+message+'\n')

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    plain_lines = [
        'Version 2.3  |  Home Network Security Audit Tool',
        '-'*46,
        '>> By SaiDinesh Andekar',
        '>> saidineshandekar1402@gmail.com',
        '>> github.com/SaiDinesh200214',
    ]
    colored_lines = [
        col(BC+BD,'Version 2.3') + '  |  ' + col(W+BD,'Home Network Security Audit Tool'),
        col(DM,'-'*46),
        '>> By ' + col(BC+BD,'SaiDinesh Andekar'),
        '>> ' + col(W,'saidineshandekar1402@gmail.com'),
        '>> ' + col(W,'github.com/SaiDinesh200214'),
    ]
    print()
    info_box(plain_lines, colored_lines)

    print('\n' + col(BC+BD,'  WHAT THIS TOOL DOES:'))
    features = [
        (BC,  '  Discover all devices on your network'),
        (B,   '  Detect OS via TTL analysis'),
        (BM,  '  Scan 20 critical ports per device'),
        (BY,  '  Analyze vulnerabilities with CVSS scores'),
        (BG,  '  Calculate 0-10 risk score per device'),
        (BR,  '  Generate professional PDF report'),
        (W,   '  Save detailed logs to scan_logs/'),
    ]
    for color, text in features:
        print('  >>  ' + col(color, text))

    print('\n' + divider())
    log_file, timestamp = setup_logging()

    print('\n' + col(BC+BD,'  SCAN CONFIGURATION') + '\n')
    auditor_name = input('  >> Your name for the report: ').strip()
    if not auditor_name: auditor_name = 'Anonymous Auditor'

    report_name = input('  >> Report filename (Enter for default): ').strip()
    if not report_name:
        report_name = 'network_audit_'+timestamp+'.pdf'
    elif not report_name.endswith('.pdf'):
        report_name += '.pdf'

    print('\n  ' + col(BG,'[OK]') + '  ' + col(W,'Auditor  : ') + col(BC+BD, auditor_name))
    print('  ' + col(BG,'[OK]') + '  ' + col(W,'Report   : ') + col(BC+BD, report_name))
    print('  ' + col(BG,'[OK]') + '  ' + col(W,'Log      : ') + col(DM, 'scan_logs/scan_'+timestamp+'.log'))
    print('\n' + divider())
    input('\n  ' + col(BY+BD,'[>>] Press Enter to begin scan...'))

    write_log(log_file, '=== NETAUDIT PRO SCAN STARTED ===')
    write_log(log_file, 'Auditor: '+auditor_name+' | Report: '+report_name)

    from scanner import (scan_network, scan_ports, check_vulnerabilities,
                         detect_os, calculate_risk_score, get_risk_label)
    from report import generate_report

    # MODULE 1
    section('MODULE 1 -- DEVICE DISCOVERY', 'MODULE 1 -- DEVICE DISCOVERY', BC)
    write_log(log_file, 'MODULE 1: Device discovery')
    spinner('Scanning network for devices...', 1.0)
    devices, my_ip = scan_network()
    write_log(log_file, 'Found '+str(len(devices))+' device(s). My IP: '+my_ip)

    if not devices:
        print('\n  ' + col(BR+BD,'[!!] No devices found!') + ' Run as Administrator/root.')
        sys.exit(1)

    print('\n  ' + col(BG+BD, 'Found '+str(len(devices))+' device(s):') + '\n')
    print('  ' + col(DM, '-'*58))
    print('  ' + col(BC+BD,'#  ') + col(BC+BD,'IP ADDRESS          ') + col(BC+BD,'MAC ADDRESS           ') + col(BC+BD,'NOTE'))
    print('  ' + col(DM, '-'*58))
    for i, device in enumerate(devices, 1):
        if device['ip'] == my_ip:
            note  = col(BG+BD, '<-- YOU')
            ipcol = col(BY+BD, device['ip'])
        else:
            note  = col(DM, 'Device')
            ipcol = col(W, device['ip'])
        maccol = col(DM, device['mac'])
        print('  '+col(BC,str(i))+'  '+ipcol+' '*(20-len(device['ip']))+maccol+' '*(22-len(device['mac']))+note)
        write_log(log_file, 'Device '+str(i)+': '+device['ip']+' | MAC: '+device['mac'])
    print('  ' + col(DM, '-'*58))

    all_results = []

    for device in devices:
        ip    = device['ip']
        mac   = device['mac']
        label = 'YOUR MACHINE' if ip == my_ip else 'Network Device'

        device_box(ip, label, B)

        # OS
        spinner('Detecting OS on '+ip+'...', 0.5)
        os_info = detect_os(ip)
        os_name = os_info['os']
        os_color = BG if 'Windows' in os_name else BC if 'Linux' in os_name or 'Android' in os_name else DM
        print('  OS: ' + col(os_color+BD, os_name) + '  ' + col(DM, 'TTL:'+str(os_info['ttl'])+' . '+os_info['confidence']+' confidence'))
        write_log(log_file, 'OS: '+os_name+' | TTL: '+str(os_info['ttl']))

        # PORT SCAN
        print('\n  ' + col(BM+BD, '[>>] MODULE 2 -- PORT SCAN'))
        write_log(log_file, 'MODULE 2: Port scan')
        spinner('Scanning ports on '+ip+'...', 1.2)
        open_ports = scan_ports(ip)

        if open_ports:
            print('\n  ' + col(DM,'-'*62))
            print('  ' + col(BC+BD,'PORT    SERVICE      RISK              CVSS   DESCRIPTION'))
            print('  ' + col(DM,'-'*62))
            for p in open_ports:
                rc   = risk_col(p['risk'])
                ri   = risk_icon(p['risk'])
                print('  ' + col(BY+BD,str(p['port'])) + ' '*(8-len(str(p['port']))) +
                      col(W+BD,p['service']) + ' '*(13-len(p['service'])) +
                      col(rc, ri+' '+p['risk']) + ' '*(18-len(ri+' '+p['risk'])) +
                      col(rc,str(p['cvss'])) + ' '*(7-len(str(p['cvss']))) +
                      col(DM,p['desc']))
                write_log(log_file, 'Port '+str(p['port'])+': '+p['service']+' | '+p['risk']+' | CVSS '+str(p['cvss']))
            print('  ' + col(DM,'-'*62))
        else:
            print('  ' + col(BG+BD,'[OK] No risky open ports found!'))
            write_log(log_file, 'No open ports found')

        # VULN ANALYSIS
        print('\n  ' + col(BY+BD,'[!!] MODULE 3 -- VULNERABILITY ANALYSIS'))
        write_log(log_file, 'MODULE 3: Vulnerability analysis')
        vulns = check_vulnerabilities(open_ports)

        if vulns:
            for v in vulns:
                rc = risk_col(v['severity'])
                print('\n  ' + col(rc,'+--') + ' Port ' + col(BY+BD,str(v['port'])) + ' -- ' + col(W+BD,v['name']))
                print('  ' + col(rc,'|') + '  Severity: ' + col(rc,v['severity']) + '  ' + col(DM,'CVSS '+str(v['cvss_score'])+'/10'))
                print('  ' + col(rc,'|'))
                print('  ' + col(rc,'|') + '  ' + col(BR+BD,'Attacker Can:'))
                for h in v['hacker_can']:
                    print('  ' + col(rc,'|') + '    ' + col(BR,'X') + ' ' + col(W,h))
                print('  ' + col(rc,'|'))
                print('  ' + col(rc,'|') + '  ' + col(BG+BD,'How to Fix:'))
                for fix in v['fix']:
                    print('  ' + col(rc,'|') + '    ' + col(BG,'V') + ' ' + col(W,fix))
                print('  ' + col(rc,'+' + '-'*50))
                write_log(log_file, 'VULN Port '+str(v['port'])+': '+v['severity']+' CVSS '+str(v['cvss_score']))
        else:
            print('  ' + col(BG+BD,'[OK] No vulnerabilities found!'))
            write_log(log_file, 'No vulnerabilities found')

        # RISK SCORE
        risk_score = calculate_risk_score(open_ports, vulns)
        risk_label = get_risk_label(risk_score)
        rc = risk_col(risk_label)
        ri = risk_icon(risk_label)
        score_int = int(risk_score * 4)
        bar = col(rc, '#'*score_int) + col(DM, '.'*(40-score_int))
        print('\n  ' + col(BC+BD,'DEVICE RISK SCORE:'))
        print('\n  [' + bar + ']')
        print('  ' + ri + '  ' + col(rc, str(risk_score)+'/10 -- '+risk_label) + '\n')
        write_log(log_file, 'Risk Score: '+str(risk_score)+'/10 -- '+risk_label)

        all_results.append({'ip':ip,'mac':mac,'os_info':os_info,'open_ports':open_ports,
                            'vulnerabilities':vulns,'risk_score':risk_score,'risk_label':risk_label})

    # SUMMARY
    total_vulns    = sum(len(r['vulnerabilities']) for r in all_results)
    total_critical = sum(1 for r in all_results for v in r['vulnerabilities'] if 'CRITICAL' in v['severity'])
    max_risk       = max(r['risk_score'] for r in all_results)
    net_risk_lbl   = get_risk_label(max_risk)
    rc             = risk_col(net_risk_lbl)

    section('FINAL NETWORK SUMMARY', 'FINAL NETWORK SUMMARY', BC)
    print()
    stats = [
        (BC,  'Devices Scanned',      str(len(devices))),
        (BY,  'Total Vulnerabilities', str(total_vulns)),
        (BR,  'Critical Issues',       str(total_critical)),
        (rc,  'Network Risk Level',    str(max_risk)+'/10 -- '+net_risk_lbl),
    ]
    for color, label, value in stats:
        dots = col(DM, '.'*(35-len(label)))
        print('  >>  ' + col(W+BD, label) + ' ' + dots + ' ' + col(color, value))

    write_log(log_file, '=== SUMMARY: '+str(len(devices))+' devices | '+str(total_vulns)+' vulns | '+str(total_critical)+' critical | Risk '+net_risk_lbl+' ===')

    # PDF
    section('MODULE 4 -- GENERATING PDF REPORT', 'MODULE 4 -- GENERATING PDF REPORT', BM)
    write_log(log_file, 'MODULE 4: Generating PDF report...')
    progress_bar('Building PDF report...', color=BM)

    try:
        generate_report(devices, all_results, auditor_name=auditor_name, output_file=report_name)
        print('\n  ' + col(BG+BD,'[OK] Report saved: ') + col(BC+BD, report_name))
        write_log(log_file, 'PDF saved: '+report_name)
    except Exception as e:
        print('  ' + col(BR+BD,'[!!] PDF Error: ') + str(e))
        write_log(log_file, 'PDF Error: '+str(e))

    json_log = os.path.join('scan_logs', 'scan_'+timestamp+'.json')
    try:
        with open(json_log, 'w') as f:
            json.dump({'timestamp':timestamp,'auditor':auditor_name,'devices':all_results,
                       'summary':{'total_devices':len(devices),'total_vulns':total_vulns,
                                  'critical':total_critical,'risk_label':net_risk_lbl}},
                      f, indent=2, default=str)
        write_log(log_file, 'JSON saved: '+json_log)
    except: pass

    write_log(log_file, '=== SCAN COMPLETE ===')

    print('\n' + divider(color=BG))
    print('\n  ' + col(BG+BD,'[OK]') + '  Log  : ' + col(DM, 'scan_logs/scan_'+timestamp+'.log'))
    print('  '   + col(BG+BD,'[OK]') + '  JSON : ' + col(DM, json_log))
    print('  '   + col(BG+BD,'[OK]') + '  PDF  : ' + col(BC+BD, report_name))

    w = TW(); inner = w - 2
    msg = '  ALL MODULES COMPLETE! YOUR NETWORK HAS BEEN AUDITED.  '
    pad = max(0, inner - len(msg) - 2)
    print()
    print(col(BG+BD, '+' + '-'*inner + '+'))
    print(col(BG+BD, '|') + col(BY+BD, '  '+msg) + ' '*pad + col(BG+BD, '|'))
    print(col(BG+BD, '+' + '-'*inner + '+') + '\n')

if __name__ == '__main__':
    main()