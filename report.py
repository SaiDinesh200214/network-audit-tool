# report.py — NetAudit Pro PDF Generator — Premium Design
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame
import datetime, io

# ── BRAND COLORS ─────────────────────────────────────────────────────────────
BG       = colors.HexColor("#060608")
BG2      = colors.HexColor("#0d0d18")
BG3      = colors.HexColor("#1a1a2e")
BLUE     = colors.HexColor("#007AFF")
BLUE2    = colors.HexColor("#5856D6")
GREEN    = colors.HexColor("#30D158")
RED      = colors.HexColor("#FF453A")
ORANGE   = colors.HexColor("#FF9F0A")
PURPLE   = colors.HexColor("#BF5AF2")
TEAL     = colors.HexColor("#5AC8FA")
WHITE    = colors.white
GRAY     = colors.HexColor("#8E8E93")
GRAY2    = colors.HexColor("#3A3A4C")
LIGHT    = colors.HexColor("#F2F2F7")
LIGHT2   = colors.HexColor("#AEAEB2")

W, H = A4
LMARGIN = 18*mm
RMARGIN = 18*mm
TMARGIN = 20*mm
BMARGIN = 20*mm
CONTENT_W = W - LMARGIN - RMARGIN

# ── STYLES ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

STYLES = {
    "h_main":  S("hm", fontName="Helvetica-Bold",   fontSize=30, textColor=WHITE,  alignment=TA_CENTER, leading=36),
    "h_sub":   S("hs", fontName="Helvetica",         fontSize=13, textColor=TEAL,   alignment=TA_CENTER, leading=17),
    "h_badge": S("hb", fontName="Helvetica-Bold",    fontSize=9,  textColor=BLUE,   alignment=TA_CENTER, leading=12),
    "h1":      S("h1", fontName="Helvetica-Bold",    fontSize=13, textColor=WHITE,  leading=18, spaceBefore=8, spaceAfter=5),
    "h2":      S("h2", fontName="Helvetica-Bold",    fontSize=11, textColor=TEAL,   leading=15, spaceBefore=6, spaceAfter=3),
    "h3":      S("h3", fontName="Helvetica-Bold",    fontSize=10, textColor=BLUE,   leading=14),
    "body":    S("bd", fontName="Helvetica",          fontSize=9,  textColor=LIGHT,  leading=13),
    "body2":   S("b2", fontName="Helvetica",          fontSize=8,  textColor=LIGHT2, leading=12),
    "mono":    S("mn", fontName="Courier",            fontSize=8,  textColor=TEAL,   leading=11),
    "caption": S("cp", fontName="Helvetica",          fontSize=7.5,textColor=GRAY,   alignment=TA_CENTER, leading=10),
    "att":     S("at", fontName="Helvetica",          fontSize=8,  textColor=colors.HexColor("#FF6B6B"), leading=11),
    "fix":     S("fx", fontName="Helvetica",          fontSize=8,  textColor=colors.HexColor("#5DDE7A"), leading=11),
    "crit_hdr":S("ch", fontName="Helvetica-Bold",    fontSize=9,  textColor=RED,    leading=12),
    "high_hdr":S("hh", fontName="Helvetica-Bold",    fontSize=9,  textColor=ORANGE, leading=12),
    "med_hdr": S("mh", fontName="Helvetica-Bold",    fontSize=9,  textColor=colors.HexColor("#FFD60A"), leading=12),
    "label":   S("lb", fontName="Helvetica-Bold",    fontSize=8,  textColor=BLUE,   leading=11),
    "value":   S("vl", fontName="Helvetica",          fontSize=9,  textColor=LIGHT,  leading=13),
    "ok":      S("ok", fontName="Helvetica-Bold",    fontSize=9,  textColor=GREEN,  leading=12),
    "footer":  S("ft", fontName="Helvetica",          fontSize=7,  textColor=GRAY,   alignment=TA_CENTER, leading=9),
    "white_c": S("wc", fontName="Helvetica-Bold",    fontSize=9,  textColor=WHITE,  alignment=TA_CENTER, leading=12),
    "white_bold":S("wb",fontName="Helvetica-Bold",   fontSize=10, textColor=WHITE,  leading=14),
    "teal_c":  S("tc", fontName="Helvetica-Bold",    fontSize=9,  textColor=TEAL,   alignment=TA_CENTER, leading=12),
    "r_right": S("rr", fontName="Helvetica-Bold",    fontSize=9,  textColor=RED,    alignment=TA_RIGHT,  leading=12),
    "o_right": S("or", fontName="Helvetica-Bold",    fontSize=9,  textColor=ORANGE, alignment=TA_RIGHT,  leading=12),
    "g_right": S("gr", fontName="Helvetica-Bold",    fontSize=9,  textColor=GREEN,  alignment=TA_RIGHT,  leading=12),
    "b_right": S("br", fontName="Helvetica-Bold",    fontSize=9,  textColor=BLUE,   alignment=TA_RIGHT,  leading=12),
}

def P(text, style="body"):
    return Paragraph(str(text), STYLES[style])

# ── LOGO (drawn with canvas) ─────────────────────────────────────────────────
def draw_shield_logo(c, x, y, size=28):
    """Draw a shield logo using basic shapes"""
    sw = size * 0.7
    sh = size
    cx = x + sw/2
    # Shield background
    c.setFillColor(BLUE)
    c.roundRect(x, y - sh + size*0.15, sw, sh*0.85, radius=4, fill=1, stroke=0)
    # Shield bottom point
    c.setFillColor(BLUE)
    path = c.beginPath()
    path.moveTo(x, y - sh*0.3)
    path.lineTo(cx, y - sh + size*0.02)
    path.lineTo(x + sw, y - sh*0.3)
    path.close()
    c.drawPath(path, fill=1, stroke=0)
    # Inner highlight
    c.setFillColor(BLUE2)
    c.roundRect(x+2, y - sh + size*0.18, sw-4, sh*0.75, radius=3, fill=1, stroke=0)
    # Lock icon in center
    c.setFillColor(WHITE)
    lx = cx - size*0.08
    ly = y - sh*0.52
    lw = size*0.16
    lh = size*0.13
    c.rect(lx - lw*0.3, ly, lw*0.6+lw*0.6, lh, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1.5)
    c.circle(cx, ly + lh + size*0.05, size*0.06, fill=0, stroke=1)

# ── PAGE BACKGROUND ───────────────────────────────────────────────────────────
class AuditDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        frame = Frame(LMARGIN, BMARGIN, CONTENT_W, H - TMARGIN - BMARGIN,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        template = PageTemplate(id="main", frames=[frame], onPage=self._draw_page)
        self.addPageTemplates([template])
        self.page_count = 0

    def _draw_page(self, canv, doc):
        canv.saveState()

        # Full dark background
        canv.setFillColor(BG)
        canv.rect(0, 0, W, H, fill=1, stroke=0)

        # Subtle gradient bands
        canv.setFillColor(BG2)
        canv.rect(0, H - 12*mm, W, 12*mm, fill=1, stroke=0)
        canv.rect(0, 0, W, 8*mm, fill=1, stroke=0)

        # Top accent line (blue to purple gradient effect)
        canv.setFillColor(BLUE)
        canv.rect(0, H - 1.5*mm, W*0.5, 1.5*mm, fill=1, stroke=0)
        canv.setFillColor(BLUE2)
        canv.rect(W*0.5, H - 1.5*mm, W*0.5, 1.5*mm, fill=1, stroke=0)

        # Bottom line
        canv.setFillColor(GRAY2)
        canv.rect(0, 8*mm, W, 0.3*mm, fill=1, stroke=0)

        # Header: logo + title
        draw_shield_logo(canv, LMARGIN, H - 3*mm, size=22)
        canv.setFont("Helvetica-Bold", 11)
        canv.setFillColor(WHITE)
        canv.drawString(LMARGIN + 22, H - 7*mm, "NetAudit Pro")
        canv.setFont("Helvetica", 7.5)
        canv.setFillColor(GRAY)
        canv.drawString(LMARGIN + 22, H - 10*mm, "Network Security Audit Report")

        # Page number
        canv.setFont("Helvetica", 7.5)
        canv.setFillColor(GRAY)
        pg = f"Page {doc.page}"
        canv.drawRightString(W - RMARGIN, 3.5*mm, pg)
        canv.drawString(LMARGIN, 3.5*mm, "CONFIDENTIAL — FOR AUTHORIZED USE ONLY")

        # Corner decorations
        canv.setStrokeColor(BLUE)
        canv.setLineWidth(0.5)
        canv.line(LMARGIN, H - 14*mm, LMARGIN + 8*mm, H - 14*mm)
        canv.line(LMARGIN, H - 14*mm, LMARGIN, H - 14*mm - 8*mm)
        canv.line(W - RMARGIN, H - 14*mm, W - RMARGIN - 8*mm, H - 14*mm)
        canv.line(W - RMARGIN, H - 14*mm, W - RMARGIN, H - 14*mm - 8*mm)

        canv.restoreState()


# ── HELPER: colored rounded box ───────────────────────────────────────────────
def section_header(title, icon="", color=BLUE):
    data = [[Paragraph(f"{icon}  {title}" if icon else title,
                       ParagraphStyle("sh", fontName="Helvetica-Bold", fontSize=11,
                                      textColor=WHITE, leading=14))]]
    t = Table(data, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [6,6,0,0]),
    ]))
    return t

def section_body(*rows_content, bg=BG3):
    """Wraps content in a dark rounded box"""
    # This is just for visual grouping via Table
    content = list(rows_content)
    t = Table([[c] for c in content], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [0,0,6,6]),
        ("BOX",           (0,0),(-1,-1), 0.5, GRAY2),
    ]))
    return t

def kv_table(pairs, cols=2):
    """Key-value table. MAC addresses rendered in Courier so they never line-wrap."""
    cw   = CONTENT_W / (cols * 2)
    row  = []
    rows = []
    for k, v in pairs:
        # Use Courier for MAC — it's fixed-width so 17-char MAC always fits on one line
        val_para = (
            Paragraph(str(v), ParagraphStyle("mac", fontName="Courier", fontSize=8,
                                             textColor=TEAL, leading=11))
            if k == "MAC Address"
            else P(v, "value")
        )
        row.extend([P(k, "label"), val_para])
        if len(row) == cols * 2:
            rows.append(row)
            row = []
    if row:
        while len(row) < cols * 2:
            row.extend([P("", "label"), P("", "value")])
        rows.append(row)

    t     = Table(rows, colWidths=[cw] * cols * 2)
    style = [
        ("BACKGROUND",    (0, 0), (-1, -1), BG3),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, GRAY2),
        ("BOX",           (0, 0), (-1, -1), 0.5, GRAY2),
    ]
    for col in range(0, cols * 2, 2):
        style.append(("BACKGROUND", (col, 0), (col, -1), colors.HexColor("#0a0a18")))
        style.append(("TEXTCOLOR",  (col, 0), (col, -1), BLUE))
    t.setStyle(TableStyle(style))
    return t

def risk_color(label):
    return {"CRITICAL":RED,"HIGH":ORANGE,"MEDIUM":colors.HexColor("#FFD60A"),
            "LOW":GREEN,"MINIMAL":GRAY}.get(label,GRAY)

def severity_style(sev):
    m = {"CRITICAL":"crit_hdr","HIGH":"high_hdr","MEDIUM":"med_hdr"}
    return m.get(sev, "body")

def sev_badge(sev, cvss):
    color_map = {"CRITICAL":RED,"HIGH":ORANGE,"MEDIUM":colors.HexColor("#FFD60A"),"LOW":GREEN}
    c = color_map.get(sev, GRAY)
    data = [[Paragraph(f"{sev}  CVSS {cvss}/10",
                       ParagraphStyle("sb", fontName="Helvetica-Bold", fontSize=8,
                                      textColor=WHITE, leading=10, alignment=TA_CENTER))]]
    t = Table(data, colWidths=[38*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), c),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
        ("TOPPADDING",    (0,0),(-1,-1), 3),
        ("BOTTOMPADDING", (0,0),(-1,-1), 3),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [4,4,4,4]),
    ]))
    return t

# ── MAIN GENERATOR ────────────────────────────────────────────────────────────
def generate_report(devices, all_results, auditor_name="Anonymous", output_file="report.pdf"):
    doc = AuditDocTemplate(
        output_file, pagesize=A4,
        leftMargin=LMARGIN, rightMargin=RMARGIN,
        topMargin=TMARGIN + 4*mm, bottomMargin=BMARGIN + 6*mm
    )

    story = []
    now = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    total_vulns    = sum(len(r.get("vulnerabilities",[])) for r in all_results)
    total_critical = sum(1 for r in all_results
                         for v in r.get("vulnerabilities",[])
                         if "CRITICAL" in v.get("severity",""))
    max_risk  = max((r.get("risk_score",0) for r in all_results), default=0)
    risk_label = ("CRITICAL" if max_risk>=8 else "HIGH" if max_risk>=6 else
                  "MEDIUM"   if max_risk>=4 else "LOW"  if max_risk>=2 else "MINIMAL")

    # ══ COVER HERO ══════════════════════════════════════════════════════
    story.append(Spacer(1, 8*mm))

    # Big logo area
    logo_data = [[
        Paragraph("🛡", ParagraphStyle("logo", fontName="Helvetica-Bold", fontSize=42,
                                       textColor=BLUE, alignment=TA_CENTER, leading=50)),
    ]]
    logo_t = Table(logo_data, colWidths=[CONTENT_W])
    logo_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), BG2),
        ("TOPPADDING",    (0,0),(-1,-1), 18),
        ("BOTTOMPADDING", (0,0),(-1,-1), 12),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [12,12,0,0]),
    ]))
    story.append(logo_t)

    # Title block
    title_data = [
        [P("NetAudit Pro","h_main")],
        [P("Network Security Audit Report","h_sub")],
        [P("PROFESSIONAL EDITION  ·  v1.0  ·  CONFIDENTIAL","h_badge")],
    ]
    title_t = Table(title_data, colWidths=[CONTENT_W])
    title_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), BG2),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
    ]))
    story.append(title_t)

    # Blue separator line
    sep = Table([[""]], colWidths=[CONTENT_W])
    sep.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 1),
        ("BOTTOMPADDING", (0,0),(-1,-1), 1),
    ]))
    story.append(sep)
    story.append(Spacer(1, 4*mm))

    # Scan meta info — 4 columns
    rc = risk_color(risk_label)
    meta_rows = [[
        P("AUDITOR",   "caption"), P("SCAN DATE",  "caption"),
        P("DEVICES",   "caption"), P("OVERALL RISK","caption"),
    ],[
        P(auditor_name, "white_bold"), P(now, "white_bold"),
        P(str(len(devices)), "white_bold"),
        Paragraph(f"{risk_label}  {max_risk}/10",
                  ParagraphStyle("rc", fontName="Helvetica-Bold", fontSize=10,
                                 textColor=rc, leading=14)),
    ]]
    meta_t = Table(meta_rows, colWidths=[CONTENT_W/4]*4)
    meta_t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), BG3),
        ("BACKGROUND",    (0,0),(-1,0),  colors.HexColor("#0a0a18")),
        ("TEXTCOLOR",     (0,0),(-1,0),  BLUE),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("LINEAFTER",     (0,0),(2,-1),  0.5, GRAY2),
        ("LINEBELOW",     (0,0),(-1,0),  0.5, GRAY2),
        ("BOX",           (0,0),(-1,-1), 0.5, GRAY2),
        ("ROUNDEDCORNERS",(0,0),(-1,-1), [0,0,8,8]),
    ]))
    story.append(meta_t)
    story.append(Spacer(1, 5*mm))

    # ── 4 STAT CARDS ───────────────────────────────────────────────────
    total_ports = sum(len(r.get("open_ports",[])) for r in all_results)
    stats = [
        (str(len(devices)),    "Total Devices",   BLUE),
        (str(total_ports),     "Open Ports",      TEAL),
        (str(total_vulns),     "Vulnerabilities", ORANGE),
        (str(total_critical),  "Critical Issues", RED),
    ]
    stat_cells = []
    for val, label, col in stats:
        cell_data = [
            [Paragraph(val, ParagraphStyle("sv", fontName="Helvetica-Bold", fontSize=26,
                                            textColor=col, alignment=TA_CENTER, leading=30))],
            [Paragraph(label, ParagraphStyle("sl", fontName="Helvetica-Bold", fontSize=8,
                                              textColor=GRAY, alignment=TA_CENTER,
                                              leading=10, letterSpacing=0.5))],
        ]
        cell_t = Table(cell_data, colWidths=[(CONTENT_W-9*mm)/4])
        cell_t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), BG3),
            ("TOPPADDING",    (0,0),(-1,-1), 10),
            ("BOTTOMPADDING", (0,0),(-1,-1), 10),
            ("LINEABOVE",     (0,0),(-1,0),  2, col),
            ("BOX",           (0,0),(-1,-1), 0.5, GRAY2),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), [4,4,4,4]),
        ]))
        stat_cells.append(cell_t)

    stats_t = Table([stat_cells], colWidths=[(CONTENT_W-9*mm)/4]*4,
                    hAlign='LEFT', spaceAfter=5*mm)
    stats_t.setStyle(TableStyle([("LEFTPADDING",(0,0),(-1,-1),3),
                                  ("RIGHTPADDING",(0,0),(-1,-1),3)]))
    story.append(stats_t)

    # ══ NETWORK SUMMARY TABLE ═══════════════════════════════════════════
    story.append(KeepTogether([
        section_header("Network Summary", "01"),
        Spacer(1, 0),
        Table([
            [P("Metric","white_c"), P("Value","white_c"), P("Status","white_c")],
            [P("Total Devices Scanned","label"), P(str(len(devices)),"value"),
             P("Complete","ok")],
            [P("Total Open Ports","label"), P(str(total_ports),"value"),
             P("Reviewed","body2")],
            [P("Total Vulnerabilities","label"), P(str(total_vulns),"value"),
             P("Action Needed" if total_vulns else "Clean","ok" if not total_vulns else "body")],
            [P("Critical Vulnerabilities","label"), P(str(total_critical),"value"),
             P("IMMEDIATE ACTION" if total_critical else "None Found",
               "crit_hdr" if total_critical else "ok")],
            [P("Overall Risk Score","label"),
             P(f"{max_risk}/10","value"),
             Paragraph(f"<b>{risk_label}</b>",
                       ParagraphStyle("rl2", fontName="Helvetica-Bold", fontSize=9,
                                      textColor=risk_color(risk_label), leading=12))],
        ], colWidths=[75*mm, 55*mm, CONTENT_W-130*mm],
           style=TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),  BLUE),
            ("BACKGROUND",    (0,1),(-1,-1), BG3),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [BG3, colors.HexColor("#111120")]),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("GRID",          (0,0),(-1,-1), 0.3, GRAY2),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), [0,0,6,6]),
        ])),
    ]))
    story.append(Spacer(1, 6*mm))

    # ══ DEVICE ANALYSIS ═════════════════════════════════════════════════
    story.append(section_header("Device Analysis", "02"))
    story.append(Spacer(1, 1*mm))

    for idx, result in enumerate(all_results):
        ip        = result.get("ip","Unknown")
        mac       = result.get("mac","Unknown")
        os_info   = result.get("os_info",{}) or {}
        ports     = result.get("open_ports",[])
        vulns     = result.get("vulnerabilities",[])
        rscore    = result.get("risk_score",0)
        rlabel    = result.get("risk_label","MINIMAL")
        is_me     = result.get("is_me", False)
        rc2       = risk_color(rlabel)

        # Device header row
        dev_hdr = Table([[
            Paragraph(f"Device {idx+1}  |  {ip}",
                      ParagraphStyle("dh", fontName="Helvetica-Bold", fontSize=11,
                                     textColor=TEAL, leading=14)),
            Paragraph(f"{'YOUR MACHINE' if is_me else 'Network Device'}  |  Risk: {rlabel}  ({rscore}/10)",
                      ParagraphStyle("dr", fontName="Helvetica-Bold", fontSize=9,
                                     textColor=rc2, alignment=TA_RIGHT, leading=12)),
        ]], colWidths=[CONTENT_W*0.55, CONTENT_W*0.45])
        dev_hdr.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), BG2),
            ("TOPPADDING",    (0,0),(-1,-1), 8),
            ("BOTTOMPADDING", (0,0),(-1,-1), 8),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 10),
            ("LINEABOVE",     (0,0),(-1,-1), 2, rc2),
            ("BOX",           (0,0),(-1,-1), 0.5, GRAY2),
        ]))
        story.append(dev_hdr)

        # Device info grid
        os_name = os_info.get("os","Unknown")
        ttl_val = str(os_info.get("ttl","—"))
        story.append(kv_table([
            ("IP Address",  ip),
            ("MAC Address", mac),
            ("OS Detected", os_name),
            ("TTL Value",   ttl_val),
            ("Open Ports",  str(len(ports))),
            ("Vulnerabilities", str(len(vulns))),
        ], cols=3))

        # Open Ports Table
        if ports:
            story.append(Spacer(1, 3*mm))
            port_rows = [[
                P("PORT","white_c"), P("SERVICE","white_c"),
                P("RISK","white_c"), P("CVSS","white_c"), P("DESCRIPTION","white_c"),
            ]]
            for p in ports:
                risk = p.get("risk","")
                cmap = {"CRITICAL":RED,"HIGH":ORANGE,"MEDIUM":colors.HexColor("#FFD60A"),"LOW":GREEN}
                rc3  = cmap.get(risk, GRAY)
                port_rows.append([
                    Paragraph(str(p["port"]),
                              ParagraphStyle("pn",fontName="Courier-Bold",fontSize=9,
                                             textColor=TEAL,leading=12,alignment=TA_CENTER)),
                    P(p.get("service",""),  "body"),
                    Paragraph(risk, ParagraphStyle("rk",fontName="Helvetica-Bold",fontSize=8,
                                                    textColor=rc3,leading=11,alignment=TA_CENTER)),
                    Paragraph(str(p.get("cvss","")),
                              ParagraphStyle("cv",fontName="Helvetica-Bold",fontSize=9,
                                             textColor=rc3,leading=12,alignment=TA_CENTER)),
                    P(p.get("desc","")[:50], "body2"),
                ])

            pt = Table(port_rows, colWidths=[16*mm, 24*mm, 22*mm, 14*mm,
                                              CONTENT_W-76*mm])
            pt.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,0),  BG),
                ("BACKGROUND",    (0,1),(-1,-1), BG3),
                ("ROWBACKGROUNDS",(0,1),(-1,-1), [BG3, colors.HexColor("#111120")]),
                ("TOPPADDING",    (0,0),(-1,-1), 6),
                ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                ("LEFTPADDING",   (0,0),(-1,-1), 8),
                ("RIGHTPADDING",  (0,0),(-1,-1), 8),
                ("GRID",          (0,0),(-1,-1), 0.3, GRAY2),
                ("BOX",           (0,0),(-1,-1), 0.5, GRAY2),
            ]))
            story.append(pt)

        # Vulnerability Details
        for v in vulns:
            sev   = v.get("severity","")
            cvss  = v.get("cvss_score",0)
            sev_c = {"CRITICAL":RED,"HIGH":ORANGE,"MEDIUM":colors.HexColor("#FFD60A")}.get(sev, GRAY)
            bg_c  = {"CRITICAL":colors.HexColor("#1a0a0a"),
                     "HIGH":    colors.HexColor("#1a100a"),
                     "MEDIUM":  colors.HexColor("#141408")}.get(sev, BG3)
            bd_c  = {"CRITICAL":colors.HexColor("#3a1515"),
                     "HIGH":    colors.HexColor("#3a2010"),
                     "MEDIUM":  colors.HexColor("#2a2008")}.get(sev, GRAY2)

            story.append(Spacer(1, 2*mm))

            # Vuln header
            vh = Table([[
                Paragraph(f"Port {v['port']}  —  {v.get('name','')[:60]}",
                          ParagraphStyle("vh", fontName="Helvetica-Bold", fontSize=9,
                                         textColor=sev_c, leading=12)),
                sev_badge(sev, cvss),
            ]], colWidths=[CONTENT_W - 42*mm, 38*mm])
            vh.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), bg_c),
                ("TOPPADDING",    (0,0),(-1,-1), 7),
                ("BOTTOMPADDING", (0,0),(-1,-1), 7),
                ("LEFTPADDING",   (0,0),(-1,-1), 10),
                ("RIGHTPADDING",  (0,0),(-1,-1), 8),
                ("LINEABOVE",     (0,0),(-1,-1), 1.5, sev_c),
                ("BOX",           (0,0),(-1,-1), 0.5, bd_c),
            ]))
            story.append(vh)

            # Attack + Fix content
            hacker_items = "\n".join([f"  x  {h}" for h in v.get("hacker_can",[])])
            fix_items    = "\n".join([f"  v  {f}" for f in v.get("fix",[])])

            vbody = Table([
                [Paragraph("ATTACKER CAN",
                           ParagraphStyle("at_hdr", fontName="Helvetica-Bold", fontSize=7.5,
                                          textColor=GRAY, leading=10, letterSpacing=0.5)),
                 Paragraph("REMEDIATION",
                           ParagraphStyle("fx_hdr", fontName="Helvetica-Bold", fontSize=7.5,
                                          textColor=GRAY, leading=10, letterSpacing=0.5))],
                [Paragraph("\n".join([f"<font color='#FF6B6B'>x</font>  {h}"
                                      for h in v.get("hacker_can",[])]),
                           ParagraphStyle("ac", fontName="Helvetica", fontSize=8.5,
                                          textColor=colors.HexColor("#FF9090"),
                                          leading=13)),
                 Paragraph("\n".join([f"<font color='#5DDE7A'>v</font>  {f}"
                                      for f in v.get("fix",[])]),
                           ParagraphStyle("fc", fontName="Helvetica", fontSize=8.5,
                                          textColor=colors.HexColor("#90E8A0"),
                                          leading=13))],
            ], colWidths=[CONTENT_W/2, CONTENT_W/2])
            vbody.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), bg_c),
                ("BACKGROUND",    (0,0),(-1,0),  colors.HexColor("#0e0e1a")),
                ("TOPPADDING",    (0,0),(-1,-1), 6),
                ("BOTTOMPADDING", (0,0),(-1,-1), 8),
                ("LEFTPADDING",   (0,0),(-1,-1), 10),
                ("RIGHTPADDING",  (0,0),(-1,-1), 10),
                ("LINEAFTER",     (0,0),(0,-1),  0.3, bd_c),
                ("BOX",           (0,0),(-1,-1), 0.5, bd_c),
            ]))
            story.append(vbody)

        story.append(Spacer(1, 5*mm))

    # ══ SECURITY RECOMMENDATIONS ════════════════════════════════════════
    story.append(PageBreak())
    story.append(section_header("Security Recommendations", "03"))
    story.append(Spacer(1, 1*mm))

    all_vulns = [(r.get("ip",""),v)
                 for r in all_results
                 for v in r.get("vulnerabilities",[])]

    if all_vulns:
        rec_rows = [[
            P("DEVICE","white_c"), P("PORT","white_c"), P("SERVICE","white_c"),
            P("RECOMMENDED ACTION","white_c"), P("PRIORITY","white_c"),
        ]]
        seen = set()
        for ip, v in sorted(all_vulns, key=lambda x: x[1]["cvss_score"], reverse=True):
            sev = v.get("severity","")
            sev_c = {"CRITICAL":RED,"HIGH":ORANGE,"MEDIUM":colors.HexColor("#FFD60A")}.get(sev,GRAY)
            for fix in v.get("fix",[]):
                key = (v["port"], fix)
                if key in seen: continue
                seen.add(key)
                rec_rows.append([
                    P(ip, "mono"),
                    Paragraph(str(v["port"]),
                              ParagraphStyle("rp",fontName="Courier-Bold",fontSize=8,
                                             textColor=TEAL,leading=11,alignment=TA_CENTER)),
                    P(v.get("name","").split(" - ")[0], "body"),
                    P(fix, "body"),
                    Paragraph(sev, ParagraphStyle("rs",fontName="Helvetica-Bold",fontSize=7.5,
                                                   textColor=sev_c,leading=10,alignment=TA_CENTER)),
                ])

        rec_t = Table(rec_rows,
                      colWidths=[28*mm, 14*mm, 22*mm,
                                  CONTENT_W - 88*mm, 24*mm])
        rec_t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,0),  BLUE),
            ("BACKGROUND",    (0,1),(-1,-1), BG3),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [BG3, colors.HexColor("#111120")]),
            ("TOPPADDING",    (0,0),(-1,-1), 6),
            ("BOTTOMPADDING", (0,0),(-1,-1), 6),
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ("GRID",          (0,0),(-1,-1), 0.3, GRAY2),
            ("BOX",           (0,0),(-1,-1), 0.5, GRAY2),
            ("ROUNDEDCORNERS",(0,0),(-1,-1), [0,0,6,6]),
        ]))
        story.append(rec_t)
    else:
        story.append(Table([[P("No critical vulnerabilities found. Your network appears secure!","ok")]],
                           colWidths=[CONTENT_W],
                           style=TableStyle([
                               ("BACKGROUND",(0,0),(-1,-1),BG3),
                               ("TOPPADDING",(0,0),(-1,-1),15),
                               ("BOTTOMPADDING",(0,0),(-1,-1),15),
                               ("LEFTPADDING",(0,0),(-1,-1),10),
                           ])))

    story.append(Spacer(1, 8*mm))

    # ══ FOOTER ══════════════════════════════════════════════════════════
    footer_t = Table([[
        Paragraph("Generated by NetAudit Pro", STYLES["footer"]),
        Paragraph(f"Auditor: {auditor_name}", STYLES["footer"]),
        Paragraph(now, STYLES["footer"]),
        Paragraph("github.com/SaiDinesh200214", STYLES["footer"]),
    ]], colWidths=[CONTENT_W/4]*4)
    footer_t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), BG2),
        ("TOPPADDING",  (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LINEABOVE",   (0,0),(-1,-1), 0.5, BLUE),
        ("GRID",        (0,0),(-1,-1), 0.3, GRAY2),
        ("ROUNDEDCORNERS",(0,0),(-1,-1),[6,6,6,6]),
    ]))
    story.append(footer_t)

    doc.build(story)
    return output_file