# report.py
# HOME NETWORK SECURITY AUDIT TOOL — PDF Report Generator

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import datetime

# ─── COLORS ─────────────────────────────────────
COLOR_DARK      = colors.HexColor('#1a1a2e')
COLOR_BLUE      = colors.HexColor('#0f3460')
COLOR_ACCENT    = colors.HexColor('#e94560')
COLOR_GREEN     = colors.HexColor('#2ecc71')
COLOR_YELLOW    = colors.HexColor('#f39c12')
COLOR_RED       = colors.HexColor('#e74c3c')
COLOR_LIGHT     = colors.HexColor('#f5f5f5')
COLOR_WHITE     = colors.white
COLOR_GRAY      = colors.HexColor('#7f8c8d')

def get_severity_color(severity):
    if '🔴' in severity or 'CRITICAL' in severity:
        return COLOR_RED
    elif '🟡' in severity or 'MEDIUM' in severity:
        return COLOR_YELLOW
    elif '🟢' in severity or 'LOW' in severity:
        return COLOR_GREEN
    else:
        return COLOR_GRAY

def generate_report(devices, all_results, auditor_name="Anonymous", output_file="network_audit_report.pdf"):
    """Generate a professional PDF security audit report"""

    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    story = []

    # ─── CUSTOM STYLES ───────────────────────────
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=COLOR_WHITE,
        backColor=COLOR_DARK,
        alignment=TA_CENTER,
        spaceAfter=5,
        spaceBefore=5,
        fontName='Helvetica-Bold',
        borderPadding=(20, 20, 20, 20)
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_WHITE,
        backColor=COLOR_BLUE,
        alignment=TA_CENTER,
        spaceAfter=3,
        fontName='Helvetica'
    )

    section_style = ParagraphStyle(
        'Section',
        parent=styles['Normal'],
        fontSize=13,
        textColor=COLOR_WHITE,
        backColor=COLOR_BLUE,
        fontName='Helvetica-Bold',
        spaceBefore=15,
        spaceAfter=8,
        borderPadding=(8, 8, 8, 8)
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLOR_DARK,
        fontName='Helvetica',
        spaceAfter=4
    )

    bold_style = ParagraphStyle(
        'Bold',
        parent=styles['Normal'],
        fontSize=9,
        textColor=COLOR_DARK,
        fontName='Helvetica-Bold',
        spaceAfter=4
    )

    # ─── HEADER ──────────────────────────────────
    story.append(Paragraph("HOME NETWORK SECURITY AUDIT", title_style))
    story.append(Paragraph("CONFIDENTIAL SECURITY REPORT", subtitle_style))
    story.append(Spacer(1, 0.3*inch))

    # ─── REPORT INFO TABLE ───────────────────────
    now = datetime.datetime.now()
    info_data = [
        ["Report Date", now.strftime("%Y-%m-%d %H:%M:%S"), "Report Type", "Network Security Audit"],
        ["Auditor", auditor_name, "Classification", "CONFIDENTIAL"],
        ["Devices Scanned", str(len(devices)), "Network Range", f"{devices[0]['ip'].rsplit('.', 1)[0]}.0/24"]
    ]

    info_table = Table(info_data, colWidths=[3.5*cm, 6*cm, 3.5*cm, 6*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), COLOR_BLUE),
        ('BACKGROUND', (2, 0), (2, -1), COLOR_BLUE),
        ('TEXTCOLOR', (0, 0), (0, -1), COLOR_WHITE),
        ('TEXTCOLOR', (2, 0), (2, -1), COLOR_WHITE),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_GRAY),
        ('ROWBACKGROUNDS', (1, 0), (1, -1), [COLOR_LIGHT, COLOR_WHITE]),
        ('ROWBACKGROUNDS', (3, 0), (3, -1), [COLOR_LIGHT, COLOR_WHITE]),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.2*inch))

    # ─── EXECUTIVE SUMMARY ───────────────────────
    story.append(Paragraph("EXECUTIVE SUMMARY", section_style))

    total_vulns = sum(len(r['vulnerabilities']) for r in all_results)
    critical = sum(1 for r in all_results for v in r['vulnerabilities'] if 'CRITICAL' in v['severity'] or '🔴' in v['severity'])
    medium = sum(1 for r in all_results for v in r['vulnerabilities'] if 'MEDIUM' in v['severity'] or '🟡' in v['severity'])
    low = sum(1 for r in all_results for v in r['vulnerabilities'] if 'LOW' in v['severity'] or '🟢' in v['severity'])

    risk_score = min(100, (critical * 25) + (medium * 10) + (low * 5))
    if risk_score >= 75:
        risk_level = "HIGH RISK"
        risk_color = COLOR_RED
    elif risk_score >= 40:
        risk_level = "MEDIUM RISK"
        risk_color = COLOR_YELLOW
    else:
        risk_level = "LOW RISK"
        risk_color = COLOR_GREEN

    summary_data = [
        ["METRIC", "VALUE", "STATUS"],
        ["Devices Scanned", str(len(devices)), "Completed"],
        ["Total Vulnerabilities", str(total_vulns), "Found"],
        ["Critical Issues", str(critical), "Immediate Action Required"],
        ["Medium Issues", str(medium), "Action Recommended"],
        ["Low Issues", str(low), "Monitor"],
        ["Overall Risk Score", f"{risk_score}/100", risk_level],
    ]

    summary_table = Table(summary_data, colWidths=[6*cm, 4*cm, 9*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_LIGHT, COLOR_WHITE]),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TEXTCOLOR', (1, -1), (1, -1), risk_color),
        ('FONTNAME', (1, -1), (1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2, -1), (2, -1), risk_color),
        ('FONTNAME', (2, -1), (2, -1), 'Helvetica-Bold'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))

    # ─── DEVICES FOUND ───────────────────────────
    story.append(Paragraph("DEVICES DISCOVERED", section_style))

    device_data = [["#", "IP Address", "MAC Address", "Type"]]
    for i, device in enumerate(devices, 1):
        dtype = "Audit Machine" if device['ip'] == devices[-1]['ip'] else "Network Device"
        device_data.append([str(i), device['ip'], device['mac'], dtype])

    device_table = Table(device_data, colWidths=[1*cm, 5*cm, 6*cm, 7*cm])
    device_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_LIGHT, COLOR_WHITE]),
        ('PADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(device_table)
    story.append(Spacer(1, 0.2*inch))

    # ─── VULNERABILITY DETAILS ───────────────────
    story.append(Paragraph("DETAILED VULNERABILITY REPORT", section_style))

    for result in all_results:
        ip = result['ip']
        vulns = result['vulnerabilities']

        story.append(Paragraph(f"Device: {ip}", bold_style))

        if not vulns:
            story.append(Paragraph("No vulnerabilities found on this device.", body_style))
            story.append(Spacer(1, 0.1*inch))
            continue

        for v in vulns:
            sev_color = get_severity_color(v['severity'])

            vuln_header = [[
                Paragraph(f"Port {v['port']} — {v['name']}", ParagraphStyle('vh', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_WHITE)),
                Paragraph(f"CVSS: {v['cvss_score']}/10", ParagraphStyle('cvss', fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_WHITE, alignment=TA_CENTER))
            ]]
            header_table = Table(vuln_header, colWidths=[14*cm, 5*cm])
            header_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), sev_color),
                ('PADDING', (0, 0), (-1, -1), 7),
            ]))
            story.append(header_table)

            hacker_text = "<br/>".join([f"• {h}" for h in v['hacker_can']])
            fix_text = "<br/>".join([f"• {f}" for f in v['fix']])

            detail_data = [
                [Paragraph("What is it:", bold_style), Paragraph(v['what_is_it'], body_style)],
                [Paragraph("Attacker can:", bold_style), Paragraph(hacker_text, body_style)],
                [Paragraph("Remediation:", bold_style), Paragraph(fix_text, body_style)],
            ]
            detail_table = Table(detail_data, colWidths=[3*cm, 16*cm])
            detail_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), COLOR_LIGHT),
                ('GRID', (0, 0), (-1, -1), 0.3, COLOR_GRAY),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(detail_table)
            story.append(Spacer(1, 0.1*inch))

    # ─── RECOMMENDATIONS ─────────────────────────
    story.append(Paragraph("TOP RECOMMENDATIONS", section_style))

    recommendations = [
        ["Priority", "Action", "Impact"],
        ["1 - URGENT", "Disable SMBv1 and block port 445 on firewall", "Prevents ransomware attacks"],
        ["2 - URGENT", "Disable RDP or enable NLA + VPN", "Prevents remote takeover"],
        ["3 - HIGH", "Block RPC port 135 on firewall", "Prevents remote code execution"],
        ["4 - HIGH", "Disable NetBIOS over TCP/IP", "Prevents user enumeration"],
        ["5 - MEDIUM", "Enable Windows Defender Firewall", "Blocks unauthorized access"],
        ["6 - MEDIUM", "Keep Windows fully updated", "Patches known vulnerabilities"],
        ["7 - LOW", "Run this audit monthly", "Maintains security posture"],
    ]

    rec_table = Table(recommendations, colWidths=[3.5*cm, 9*cm, 6.5*cm])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, COLOR_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_LIGHT, COLOR_WHITE]),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('TEXTCOLOR', (0, 1), (0, 2), COLOR_RED),
        ('TEXTCOLOR', (0, 3), (0, 4), COLOR_YELLOW),
        ('FONTNAME', (0, 1), (0, 4), 'Helvetica-Bold'),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 0.3*inch))

    # ─── FOOTER ──────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BLUE))
    story.append(Spacer(1, 0.1*inch))
    footer_text = f"Generated by Home Network Security Audit Tool v1.0 | Auditor: {auditor_name} | {now.strftime('%Y-%m-%d %H:%M:%S')} | CONFIDENTIAL"
    story.append(Paragraph(footer_text, ParagraphStyle('footer', fontName='Helvetica', fontSize=8, textColor=COLOR_GRAY, alignment=TA_CENTER)))

    # ─── BUILD PDF ───────────────────────────────
    doc.build(story)
    print(f"\n  ✅ PDF Report saved as: {output_file}")
    return output_file
