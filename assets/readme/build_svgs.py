#!/usr/bin/env python3
"""Build animated README SVGs for ShweMind (SMIL only — no JS, no external refs)."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "readme")
os.makedirs(OUT, exist_ok=True)

TEAL = "#00c9a7"
TEAL_DARK = "#005e62"
BG = "#0a0f14"
PANEL = "#101a22"
TEXT = "#e8eef2"
MUTED = "#93a3b3"
LINE = "#22303c"
SYS = "system-ui, -apple-system, 'Segoe UI', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# ---------------------------------------------------------------- hero.svg ---
def hero():
    particles = []
    import random
    random.seed("shwemind")
    for i in range(16):
        cx = random.randint(40, 1160)
        cy = random.randint(40, 360)
        r = random.randint(2, 5)
        dy = random.randint(-46, -18)
        dur = round(random.uniform(5, 9), 1)
        begin = round(random.uniform(0, 6), 1)
        op = round(random.uniform(0.25, 0.6), 2)
        particles.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{TEAL}" opacity="{op}">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0; 0 {dy}; 0 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op};{op*0.3};{op}" dur="{dur}s" '
            f'begin="{begin}s" repeatCount="indefinite"/></circle>'
        )
    pills = [("zly168 relay ready", 190), ("multi-user auth", 170), ("local-first mode", 170)]
    total = sum(w for _, w in pills) + 24 * (len(pills) - 1)
    x = (1200 - total) / 2
    pill_els = []
    for label, w in pills:
        pill_els.append(
            f'<rect x="{x:.0f}" y="322" width="{w}" height="36" rx="18" fill="{PANEL}" '
            f'stroke="#1e3a3f" stroke-width="1.5"/>'
            f'<circle cx="{x+24:.0f}" cy="340" r="5" fill="{TEAL}">'
            f'<animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></circle>'
            f'<text x="{x+38:.0f}" y="345" font-family="{SYS}" font-size="15" fill="#9fb3c0">{label}</text>'
        )
        x += w + 24
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400" role="img" aria-label="ShweMind — a personal agent with a browser, terminal, files, and work that keeps going">
<defs>
<linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{TEAL}"/><stop offset="0.5" stop-color="#8df5da"/><stop offset="1" stop-color="{TEAL}"/>
</linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.85"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.42" r="0.65">
<stop offset="0" stop-color="{TEAL_DARK}" stop-opacity="0.6"/><stop offset="1" stop-color="{TEAL_DARK}" stop-opacity="0"/>
</radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
<path d="M40 0H0V40" fill="none" stroke="#16222c" stroke-width="1"/>
</pattern>
<clipPath id="tagClip"><rect x="126" y="262" width="0" height="34"><animate attributeName="width" values="0;948;948;0" keyTimes="0;0.32;0.86;1" dur="12s" repeatCount="indefinite"/></rect></clipPath>
<clipPath id="sweepClip"><rect x="0" y="80" width="0" height="140"><animate attributeName="width" values="0;1200;1200;0" keyTimes="0;0.32;0.78;1" dur="7s" repeatCount="indefinite"/></rect></clipPath>
</defs>
<rect width="1200" height="400" fill="{BG}"/>
<rect width="1200" height="400" fill="url(#grid)"/>
<rect width="1200" height="400" fill="url(#glow)"/>
{''.join(particles)}
<text x="600" y="200" text-anchor="middle" font-family="{SYS}" font-size="104" font-weight="800" letter-spacing="3" fill="url(#titleGrad)">ShweMind</text>
<text x="600" y="200" text-anchor="middle" font-family="{SYS}" font-size="104" font-weight="800" letter-spacing="3" fill="url(#sweep)" opacity="0.5" clip-path="url(#sweepClip)">ShweMind</text>
<text x="600" y="238" text-anchor="middle" font-family="{SYS}" font-size="16" letter-spacing="6" fill="{MUTED}">P E R S O N A L&#160;&#160;A I&#160;&#160;A G E N T</text>
<g clip-path="url(#tagClip)"><text x="126" y="290" font-family="{MONO}" font-size="20" fill="#c7d3dc">A personal agent with a browser, terminal, files, and work that keeps going.</text></g>
<rect x="1082" y="268" width="11" height="24" fill="{TEAL}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
{''.join(pill_els)}
</svg>'''
    return svg

# --------------------------------------------------------------- terminal.svg
def terminal():
    T = 14.0
    def kt(t0, fade=0.45):
        return (f"0;0;1;1;0",
                f"0;{t0/T:.4f};{(t0+fade)/T:.4f};0.96;1")
    def typekt(t0, dur, w):
        return (f"0;0;{w};{w};0",
                f"0;{t0/T:.4f};{(t0+dur)/T:.4f};0.96;1")
    lines = []
    y = 92
    # line 1: typed command
    v, k = typekt(0.6, 1.8, 560)
    lines.append(f'''<clipPath id="t1"><rect x="48" y="{y-20}" width="0" height="30"><animate attributeName="width" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>
<g clip-path="url(#t1)"><text x="48" y="{y}" font-family="{MONO}" font-size="15"><tspan fill="{TEAL}">$ </tspan><tspan fill="{TEXT}">shwemind "summarize my inbox"</tspan></text></g>''')
    y += 36
    # line 2-4: fades
    for t0, txt, col in [(2.7, "\u25b8 reading 12 threads\u2026", MUTED),
                         (3.7, "\u25b8 3 need replies: invoice, poster draft, deploy", TEXT),
                         (4.7, "\u2713 drafts ready \u2014 review in Activity", TEAL)]:
        v, k = kt(t0)
        lines.append(f'''<text x="48" y="{y}" font-family="{MONO}" font-size="15" fill="{col}" opacity="0"><animate attributeName="opacity" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite"/>{txt}</text>''')
        y += 36
    # line 5: typed command
    v, k = typekt(6.1, 1.8, 600)
    lines.append(f'''<clipPath id="t2"><rect x="48" y="{y-20}" width="0" height="30"><animate attributeName="width" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>
<g clip-path="url(#t2)"><text x="48" y="{y}" font-family="{MONO}" font-size="15"><tspan fill="{TEAL}">$ </tspan><tspan fill="{TEXT}">shwemind "watch this price and alert me"</tspan></text></g>''')
    y += 36
    v, k = kt(8.1)
    lines.append(f'''<text x="48" y="{y}" font-family="{MONO}" font-size="15" fill="{TEAL}" opacity="0"><animate attributeName="opacity" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite"/>\u2713 goal #42 created: price-watch</text>''')
    y += 36
    v, k = kt(9.1)
    lines.append(f'''<text x="48" y="{y}" font-family="{MONO}" font-size="15" opacity="0"><animate attributeName="opacity" values="{v}" keyTimes="{k}" dur="{T}s" repeatCount="indefinite"/><tspan fill="{TEAL}">$ </tspan><tspan fill="{TEAL}">\u258b<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="1.1s" repeatCount="indefinite"/></tspan></text>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="440" viewBox="0 0 760 440" role="img" aria-label="ShweMind terminal demo session">
<defs><radialGradient id="tglow" cx="0.5" cy="0" r="0.9"><stop offset="0" stop-color="{TEAL_DARK}" stop-opacity="0.35"/><stop offset="1" stop-color="{TEAL_DARK}" stop-opacity="0"/></radialGradient></defs>
<rect width="760" height="440" fill="{BG}" rx="14"/>
<rect width="760" height="440" fill="url(#tglow)" rx="14"/>
<rect x="20" y="20" width="720" height="400" rx="12" fill="#111a21" stroke="{LINE}" stroke-width="1.5"/>
<rect x="20" y="20" width="720" height="46" rx="12" fill="#16212b"/>
<rect x="20" y="50" width="720" height="16" fill="#16212b"/>
<circle cx="48" cy="43" r="7" fill="#e0655f" opacity="0.85"/><circle cx="72" cy="43" r="7" fill="#e0b45f" opacity="0.85"/><circle cx="96" cy="43" r="7" fill="#5fd08a" opacity="0.85"/>
<text x="380" y="48" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">shwemind \u2014 agent session</text>
{''.join(lines)}
</svg>'''
    return svg

# --------------------------------------------------------------- features.svg
def features():
    cards = [
        ("Take-Control Browser",
         "Persistent Chromium. Watch it work inline,",
         "then take over the session yourself.",
         "browser"),
        ("Own Linux Terminal",
         "Its own shell and workspace files,",
         "with saved receipts for every command.",
         "terminal"),
        ("Curated Memory",
         "A MEMORY.md the agent maintains itself \u2014",
         "it remembers across every chat.",
         "memory"),
        ("Multi-User Auth",
         "Real signup and login, scrypt hashing,",
         "per-user data isolation.",
         "users"),
        ("zly168 Relay Ready",
         "Any OpenAI-compatible endpoint",
         "via OPENAI_BASE_URL. Your key, your bill.",
         "bolt"),
        ("Local-First Mode",
         "Runs fully without the Intelligence cloud key.",
         "Your server, your data.",
         "home"),
    ]
    icons = {
        "browser": f'<rect x="-26" y="-20" width="52" height="40" rx="6" fill="none" stroke="{TEAL}" stroke-width="3"/><line x1="-26" y1="-8" x2="26" y2="-8" stroke="{TEAL}" stroke-width="3"/><circle cx="-16" cy="-14" r="2.6" fill="{TEAL}"/>',
        "terminal": f'<rect x="-26" y="-20" width="52" height="40" rx="6" fill="none" stroke="{TEAL}" stroke-width="3"/><text x="-14" y="8" font-family="{MONO}" font-size="20" font-weight="bold" fill="{TEAL}">\u003e_</text>',
        "memory": f'<circle cx="0" cy="-4" r="14" fill="none" stroke="{TEAL}" stroke-width="3"/><circle cx="-24" cy="12" r="6" fill="{TEAL}"/><circle cx="24" cy="12" r="6" fill="{TEAL}"/><line x1="-11" y1="4" x2="-20" y2="10" stroke="{TEAL}" stroke-width="2.5"/><line x1="11" y1="4" x2="20" y2="10" stroke="{TEAL}" stroke-width="2.5"/>',
        "users": f'<circle cx="-10" cy="-8" r="9" fill="none" stroke="{TEAL}" stroke-width="3"/><circle cx="14" cy="-4" r="7" fill="none" stroke="{TEAL}" stroke-width="3"/><path d="M-26 18 Q-10 6 6 18" fill="none" stroke="{TEAL}" stroke-width="3"/><path d="M4 18 Q14 10 26 16" fill="none" stroke="{TEAL}" stroke-width="3"/>',
        "bolt": f'<polygon points="4,-22 -12,4 -2,4 -6,20 12,-4 2,-4" fill="{TEAL}"/>',
        "home": f'<path d="M-24 2 L0 -18 L24 2" fill="none" stroke="{TEAL}" stroke-width="3"/><rect x="-14" y="2" width="28" height="18" fill="none" stroke="{TEAL}" stroke-width="3"/><rect x="-5" y="9" width="10" height="11" fill="{TEAL}"/>',
    }
    els = [f'<text x="600" y="58" text-anchor="middle" font-family="{SYS}" font-size="34" font-weight="800" fill="{TEXT}">Built different, on purpose.</text>',
           f'<text x="600" y="88" text-anchor="middle" font-family="{SYS}" font-size="16" fill="{MUTED}">Everything the alpha ships, and the ShweMind-only upgrades.</text>']
    for i, (title, d1, d2, icon) in enumerate(cards):
        col, row = i % 3, i // 3
        x = 30 + col * 390
        y = 120 + row * 232
        els.append(f'''<g>
<rect x="{x}" y="{y}" width="360" height="200" rx="16" fill="{PANEL}" stroke="{LINE}" stroke-width="1.5"/>
<rect x="{x}" y="{y}" width="360" height="200" rx="16" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0.45" stroke-dasharray="7 9"><animate attributeName="stroke-dashoffset" from="0" to="64" dur="3.2s" begin="{i*0.4}s" repeatCount="indefinite"/></rect>
<g transform="translate({x+56},{y+52})">{icons[icon]}</g>
<circle cx="{x+322}" cy="{y+30}" r="6" fill="{TEAL}"><animate attributeName="opacity" values="1;0.2;1" dur="2.4s" begin="{i*0.3}s" repeatCount="indefinite"/></circle>
<text x="{x+28}" y="{y+116}" font-family="{SYS}" font-size="20" font-weight="700" fill="{TEXT}">{title}</text>
<text x="{x+28}" y="{y+144}" font-family="{SYS}" font-size="14" fill="{MUTED}">{d1}</text>
<text x="{x+28}" y="{y+166}" font-family="{SYS}" font-size="14" fill="{MUTED}">{d2}</text>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600" role="img" aria-label="ShweMind feature highlights">
<rect width="1200" height="600" fill="{BG}" rx="14"/>
{''.join(els)}
</svg>'''
    return svg

# ------------------------------------------------------------ architecture.svg
def architecture():
    def node(x, y, w, title, sub):
        return f'''<g>
<rect x="{x-4}" y="{y-4}" width="{w+8}" height="72" rx="14" fill="none" stroke="{TEAL}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;0.55;0" dur="3s" repeatCount="indefinite"/></rect>
<rect x="{x}" y="{y}" width="{w}" height="64" rx="12" fill="{PANEL}" stroke="#23414a" stroke-width="1.5"/>
<text x="{x+w/2}" y="{y+27}" text-anchor="middle" font-family="{SYS}" font-size="17" font-weight="700" fill="{TEXT}">{title}</text>
<text x="{x+w/2}" y="{y+48}" text-anchor="middle" font-family="{SYS}" font-size="12.5" fill="{MUTED}">{sub}</text>
</g>'''
    def dot(path, dur, begin):
        return f'<circle r="5" fill="{TEAL}" opacity="0.95"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{path}"/></circle>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" role="img" aria-label="ShweMind architecture data flow">
<rect width="1200" height="360" fill="{BG}" rx="14"/>
<text x="600" y="40" text-anchor="middle" font-family="{SYS}" font-size="24" font-weight="800" fill="{TEXT}">How it flows</text>
{node(30, 150, 190, "Apps", "iOS \u00b7 Android \u00b7 Web")}
{node(320, 150, 190, "API Server", "Hono \u00b7 SSE / Intelligence")}
{node(610, 150, 190, "Agent Engine", "tools \u00b7 memory \u00b7 tasks")}
{node(900, 60, 240, "Browser Worker", "Playwright \u00b7 take control")}
{node(900, 240, 240, "Model Relay", "zly168 \u00b7 OpenAI-compatible")}
<path d="M220 182 H320" stroke="#23414a" stroke-width="2.5" fill="none"/>
<path d="M510 182 H610" stroke="#23414a" stroke-width="2.5" fill="none"/>
<path d="M800 170 C 855 170, 855 92, 900 92" stroke="#23414a" stroke-width="2.5" fill="none"/>
<path d="M800 194 C 855 194, 855 272, 900 272" stroke="#23414a" stroke-width="2.5" fill="none"/>
{dot("M220 182 H320", 1.6, 0)}{dot("M220 182 H320", 1.6, 0.8)}
{dot("M510 182 H610", 1.6, 0.4)}{dot("M510 182 H610", 1.6, 1.2)}
{dot("M800 170 C 855 170, 855 92, 900 92", 2.2, 0.2)}{dot("M800 170 C 855 170, 855 92, 900 92", 2.2, 1.3)}
{dot("M800 194 C 855 194, 855 272, 900 272", 2.2, 0.7)}{dot("M800 194 C 855 194, 855 272, 900 272", 2.2, 1.8)}
<text x="270" y="172" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">chat</text>
<text x="560" y="172" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">plan</text>
<text x="862" y="132" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">browse</text>
<text x="862" y="232" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">reason</text>
</svg>'''
    return svg

if __name__ == "__main__":
    for name, fn in [("hero.svg", hero), ("terminal.svg", terminal),
                     ("features.svg", features), ("architecture.svg", architecture)]:
        p = os.path.join(OUT, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(fn())
        print(name, os.path.getsize(p), "bytes")
