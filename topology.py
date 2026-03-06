# topology.py — Network Topology Map (Pure Canvas, NO CDN needed — works offline!)
import os, json

def generate_topology(devices, my_ip, output_file="topology.html"):
    """
    Draws network topology using HTML5 Canvas only.
    No external libraries — works even without internet!
    """
    base       = ".".join(my_ip.split(".")[:3])
    router_ip  = base + ".1"

    # Build node data for JS
    nodes = []

    # Router node (center)
    router_found = any(d["ip"] == router_ip for d in devices)
    nodes.append({
        "id":    "router",
        "ip":    router_ip,
        "label": "🌐 Router",
        "sub":   router_ip,
        "color": "#007AFF",
        "ring":  "#5AC8FA",
        "isMe":  False,
        "risk":  "ROUTER",
        "ports": 0,
        "vulns": 0,
    })

    risk_colors = {
        "CRITICAL": "#FF453A",
        "HIGH":     "#FF9F0A",
        "MEDIUM":   "#FFD60A",
        "LOW":      "#30D158",
        "MINIMAL":  "#8E8E93",
        "ROUTER":   "#007AFF",
    }

    for d in devices:
        ip     = d["ip"]
        rl     = d.get("risk_label", "MINIMAL")
        score  = d.get("risk_score", 0)
        os_n   = (d.get("os_info") or {}).get("os", "Unknown")[:18]
        is_me  = d.get("is_me", ip == my_ip)
        ports  = len(d.get("open_ports", []))
        vulns  = len(d.get("vulnerabilities", []))

        if os_n.lower().startswith("windows"):      icon = "🖥️"
        elif "android" in os_n.lower() or \
             "linux"   in os_n.lower():              icon = "📱"
        elif "router"  in os_n.lower() or \
             "network" in os_n.lower():              icon = "🌐"
        else:                                        icon = "💻"

        nodes.append({
            "id":    ip,
            "ip":    ip,
            "label": f"{'💻 YOU' if is_me else icon}",
            "sub":   ip,
            "os":    os_n,
            "color": risk_colors.get(rl, "#8E8E93"),
            "ring":  "#FF453A" if rl == "CRITICAL" else risk_colors.get(rl, "#8E8E93"),
            "isMe":  is_me,
            "risk":  rl,
            "score": score,
            "ports": ports,
            "vulns": vulns,
        })

    nodes_json = json.dumps(nodes)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NetAudit Pro — Network Map</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:#060608;font-family:-apple-system,'Inter',sans-serif;color:#fff;overflow:hidden;user-select:none;}}
canvas{{display:block;}}
#ui{{position:fixed;top:14px;left:14px;z-index:10;}}
.panel{{background:rgba(14,14,22,.95);border:1px solid rgba(255,255,255,.12);border-radius:14px;
  padding:14px 16px;backdrop-filter:blur(20px);margin-bottom:10px;min-width:200px;}}
.ptitle{{font-size:13px;font-weight:800;color:#007AFF;margin-bottom:8px;}}
.prow{{font-size:10.5px;color:rgba(255,255,255,.55);margin:3px 0;}}
.legend{{display:flex;flex-direction:column;gap:5px;}}
.lrow{{display:flex;align-items:center;gap:7px;font-size:10px;color:rgba(255,255,255,.6);}}
.dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0;}}
#tooltip{{position:fixed;background:rgba(14,14,22,.97);border:1px solid rgba(255,255,255,.15);
  border-radius:12px;padding:12px 14px;pointer-events:none;display:none;z-index:100;
  font-size:10.5px;line-height:1.8;min-width:160px;box-shadow:0 8px 32px rgba(0,0,0,.6);}}
.tip-title{{font-size:12px;font-weight:700;color:#5AC8FA;margin-bottom:5px;}}
.tip-risk{{font-weight:800;font-size:11px;}}
#hint{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);
  font-size:10px;color:rgba(255,255,255,.3);pointer-events:none;}}
</style>
</head>
<body>
<canvas id="c"></canvas>

<div id="ui">
  <div class="panel">
    <div class="ptitle">🛡 NetAudit Pro — Network Map</div>
    <div class="prow">📡 {len(devices)} devices found</div>
    <div class="prow">🌐 Network: {base}.0/24</div>
    <div class="prow">💻 Your IP: {my_ip}</div>
  </div>
  <div class="panel">
    <div class="ptitle">Legend</div>
    <div class="legend">
      <div class="lrow"><div class="dot" style="background:#007AFF"></div>Router / Gateway</div>
      <div class="lrow"><div class="dot" style="background:#FF453A"></div>CRITICAL Risk</div>
      <div class="lrow"><div class="dot" style="background:#FF9F0A"></div>HIGH Risk</div>
      <div class="lrow"><div class="dot" style="background:#FFD60A"></div>MEDIUM Risk</div>
      <div class="lrow"><div class="dot" style="background:#30D158"></div>LOW / Minimal</div>
      <div class="lrow"><div class="dot" style="background:#8E8E93"></div>Unknown</div>
    </div>
  </div>
</div>

<div id="tooltip"></div>
<div id="hint">Hover nodes for details • Drag to move • Scroll to zoom</div>

<script>
const NODES = {nodes_json};

const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');
let W, H, animId;
let zoom = 1, panX = 0, panY = 0;
let dragging = null, dragOffX = 0, dragOffY = 0;
let hovering = null;

// ── LAYOUT: router center, devices in circle ──────────────────────────────
function layout() {{
  const cx = W / 2, cy = H / 2;
  const R  = Math.min(W, H) * 0.32;

  // Router at center
  NODES[0].x = cx;
  NODES[0].y = cy;
  NODES[0].r = 36;

  // Devices in circle around router
  const devNodes = NODES.slice(1);
  devNodes.forEach((n, i) => {{
    const angle = (i / devNodes.length) * Math.PI * 2 - Math.PI / 2;
    n.x = cx + Math.cos(angle) * R;
    n.y = cy + Math.sin(angle) * R;
    n.r = n.isMe ? 30 : 24;
  }});
}}

function resize() {{
  W = canvas.width  = window.innerWidth;
  H = canvas.height = window.innerHeight;
  layout();
}}

// ── DRAW ──────────────────────────────────────────────────────────────────
function draw() {{
  ctx.clearRect(0, 0, W, H);
  ctx.save();
  ctx.translate(panX, panY);
  ctx.scale(zoom, zoom);

  const router = NODES[0];

  // Draw edges first
  NODES.slice(1).forEach(n => {{
    const pulse = (Date.now() / 1000) % 1;
    // Line
    ctx.beginPath();
    ctx.moveTo(router.x, router.y);
    ctx.lineTo(n.x, n.y);
    ctx.strokeStyle = n.color + '40';
    ctx.lineWidth   = 1.5;
    ctx.stroke();

    // Animated dot on edge
    const dx = n.x - router.x, dy = n.y - router.y;
    const px = router.x + dx * pulse;
    const py = router.y + dy * pulse;
    ctx.beginPath();
    ctx.arc(px, py, 3, 0, Math.PI*2);
    ctx.fillStyle = n.color + 'cc';
    ctx.fill();
  }});

  // Draw nodes
  NODES.forEach(n => {{
    const isHov = hovering === n;
    const r = n.r + (isHov ? 4 : 0);

    // Glow
    const grd = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 2.2);
    grd.addColorStop(0, n.color + '30');
    grd.addColorStop(1, 'transparent');
    ctx.beginPath();
    ctx.arc(n.x, n.y, r * 2.2, 0, Math.PI*2);
    ctx.fillStyle = grd;
    ctx.fill();

    // Outer ring (risk color)
    ctx.beginPath();
    ctx.arc(n.x, n.y, r + 4, 0, Math.PI*2);
    ctx.strokeStyle = n.ring + (isHov ? 'ff' : '88');
    ctx.lineWidth   = isHov ? 2.5 : 1.5;
    ctx.stroke();

    // Node circle
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI*2);
    const bg = ctx.createRadialGradient(n.x-r*0.3, n.y-r*0.3, 0, n.x, n.y, r);
    bg.addColorStop(0, n.color + 'dd');
    bg.addColorStop(1, n.color + '88');
    ctx.fillStyle = bg;
    ctx.fill();
    ctx.strokeStyle = n.color;
    ctx.lineWidth   = 1.5;
    ctx.stroke();

    // Emoji icon
    ctx.font        = `${{Math.round(r * 0.75)}}px serif`;
    ctx.textAlign   = 'center';
    ctx.textBaseline= 'middle';
    ctx.fillStyle   = '#fff';
    ctx.fillText(n.label, n.x, n.y);

    // IP label below
    ctx.font        = `bold ${{Math.round(r * 0.38)}}px monospace`;
    ctx.textAlign   = 'center';
    ctx.textBaseline= 'top';
    ctx.fillStyle   = '#ffffffcc';
    ctx.fillText(n.sub, n.x, n.y + r + 6);

    // Risk badge
    if(n.risk && n.risk !== 'ROUTER') {{
      ctx.font        = `bold ${{Math.round(r * 0.32)}}px sans-serif`;
      ctx.textBaseline= 'bottom';
      ctx.fillStyle   = n.color;
      ctx.fillText(n.risk, n.x, n.y - r - 4);
    }}
  }});

  ctx.restore();
  animId = requestAnimationFrame(draw);
}}

// ── TOOLTIP ───────────────────────────────────────────────────────────────
function showTooltip(n, mx, my) {{
  const tip = document.getElementById('tooltip');
  const riskColors = {{
    CRITICAL:'#FF453A', HIGH:'#FF9F0A', MEDIUM:'#FFD60A',
    LOW:'#30D158', MINIMAL:'#8E8E93', ROUTER:'#007AFF'
  }};
  const rc = riskColors[n.risk] || '#8E8E93';
  let html = `<div class="tip-title">${{n.sub}}</div>`;
  if(n.os)    html += `<div>💻 OS: ${{n.os}}</div>`;
  if(n.isMe)  html += `<div style="color:#007AFF;font-weight:700">◀ YOUR MACHINE</div>`;
  if(n.risk && n.risk !== 'ROUTER')
              html += `<div class="tip-risk" style="color:${{rc}}">Risk: ${{n.risk}} ${{n.score !== undefined ? `(${{n.score}}/10)` : ''}}</div>`;
  if(n.ports !== undefined) html += `<div>🚪 Open Ports: ${{n.ports}}</div>`;
  if(n.vulns !== undefined && n.vulns > 0)
              html += `<div style="color:#FF453A">⚠ Vulnerabilities: ${{n.vulns}}</div>`;
  tip.innerHTML = html;
  tip.style.display = 'block';
  tip.style.left = (mx + 14) + 'px';
  tip.style.top  = (my - 10) + 'px';
}}
function hideTooltip() {{
  document.getElementById('tooltip').style.display = 'none';
}}

// ── HIT TEST ──────────────────────────────────────────────────────────────
function hitTest(mx, my) {{
  const wx = (mx - panX) / zoom;
  const wy = (my - panY) / zoom;
  for(let i = NODES.length-1; i >= 0; i--) {{
    const n  = NODES[i];
    const dx = wx - n.x, dy = wy - n.y;
    if(dx*dx + dy*dy <= (n.r+6)*(n.r+6)) return n;
  }}
  return null;
}}

// ── EVENTS ────────────────────────────────────────────────────────────────
canvas.addEventListener('mousemove', e => {{
  const n = hitTest(e.clientX, e.clientY);
  hovering = n;
  canvas.style.cursor = n ? 'grab' : 'default';
  if(n) showTooltip(n, e.clientX, e.clientY);
  else  hideTooltip();
  if(dragging) {{
    dragging.x = (e.clientX - panX) / zoom - dragOffX;
    dragging.y = (e.clientY - panY) / zoom - dragOffY;
  }}
}});

canvas.addEventListener('mousedown', e => {{
  const n = hitTest(e.clientX, e.clientY);
  if(n) {{
    dragging  = n;
    dragOffX  = (e.clientX - panX) / zoom - n.x;
    dragOffY  = (e.clientY - panY) / zoom - n.y;
    canvas.style.cursor = 'grabbing';
  }}
}});
canvas.addEventListener('mouseup',   () => {{ dragging = null; }});
canvas.addEventListener('mouseleave',() => {{ dragging = null; hideTooltip(); }});

canvas.addEventListener('wheel', e => {{
  e.preventDefault();
  const delta = e.deltaY > 0 ? 0.9 : 1.1;
  zoom = Math.min(3, Math.max(0.3, zoom * delta));
}}, {{passive:false}});

// Touch support
canvas.addEventListener('touchmove', e => {{
  e.preventDefault();
  const t  = e.touches[0];
  const n  = hitTest(t.clientX, t.clientY);
  hovering = n;
  if(dragging) {{
    dragging.x = (t.clientX - panX) / zoom - dragOffX;
    dragging.y = (t.clientY - panY) / zoom - dragOffY;
  }}
}}, {{passive:false}});
canvas.addEventListener('touchstart', e => {{
  const t = e.touches[0];
  const n = hitTest(t.clientX, t.clientY);
  if(n) {{
    dragging = n;
    dragOffX = (t.clientX - panX) / zoom - n.x;
    dragOffY = (t.clientY - panY) / zoom - n.y;
  }}
}});
canvas.addEventListener('touchend', () => dragging = null);

window.addEventListener('resize', resize);
resize();
draw();
</script>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    return output_file