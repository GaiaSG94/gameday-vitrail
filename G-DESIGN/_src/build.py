#!/usr/bin/env python3
"""Build des planches Vitrail.

Chaque planche source (`_src/*.src.html`) contient des jetons [[NOM cle=valeur ...]].
Ce script les remplace par : polices embarquees (base64), vitrail SVG, pieces de verre,
habillage neutre du feed (desktop / mobile). Sortie : `planches/v1/*.html`, autonomes,
ouvrables en double-clic, sans aucune requete reseau.

Usage : python3 G-DESIGN/_src/build.py
"""
import base64
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "planches" / "v1"

# ---------------------------------------------------------------- polices (OFL)
FONTS = {
    "inter": ("Inter", "inter-latin.woff2", "100 900", "normal"),
    "jbm": ("JetBrains Mono", "jetbrainsmono-latin.woff2", "100 800", "normal"),
    "nsd": ("Noto Serif Display", "noto-serif-display-regular.woff2", "400", "normal"),
    "nsdi": ("Noto Serif Display", "noto-serif-display-italic.woff2", "400", "italic"),
    "fraunces": ("Fraunces", "fraunces-latin-600-normal.woff2", "600", "normal"),
    "sg4": ("Space Grotesk", "space-grotesk-latin-400-normal.woff2", "400", "normal"),
    "sg5": ("Space Grotesk", "space-grotesk-latin-500-normal.woff2", "500", "normal"),
    "sg7": ("Space Grotesk", "space-grotesk-latin-700-normal.woff2", "700", "normal"),
    "archivo": ("Archivo", "archivo.woff2", "100 900", "normal"),
}


def tok_fonts(names):
    css = []
    for n in names.split(","):
        fam, f, w, s = FONTS[n]
        b64 = base64.b64encode((SRC / "fonts" / f).read_bytes()).decode()
        extra = "font-stretch:62% 125%;" if n == "archivo" else ""
        css.append(
            f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b64}) format('woff2');"
            f"font-weight:{w};font-style:{s};{extra}font-display:block}}"
        )
    return "\n".join(css)


# ---------------------------------------------------------------- le vitrail du jour
# Lancette 300 x 520, 8 cases (motif « The Lily »). Les polygones debordent et sont
# rognes par la silhouette de la fenetre.
OUTLINE = "M8,520 L8,205 C8,112 68,42 150,8 C232,42 292,112 292,205 L292,520 Z"
CELLS = {
    "A": [(0, 0), (300, 0), (300, 170), (150, 120), (0, 170)],          # arc
    "B": [(0, 170), (150, 120), (110, 290), (0, 300)],                  # petale gauche
    "C": [(300, 170), (150, 120), (190, 290), (300, 300)],              # petale droit
    "D": [(150, 120), (190, 290), (150, 330), (110, 290)],              # bouton
    "E": [(0, 300), (110, 290), (150, 330), (150, 400), (0, 410)],      # feuille gauche
    "F": [(300, 300), (190, 290), (150, 330), (150, 400), (300, 410)],  # feuille droite
    "G": [(0, 410), (150, 400), (150, 520), (0, 520)],                  # socle gauche
    "H": [(300, 410), (150, 400), (150, 520), (300, 520)],              # socle droit
}
SOLUTION = dict(A="ruby", B="cobalt", C="emerald", D="amber",
                E="emerald", F="ruby", G="cobalt", H="amber")
# faisceau : droite y = 180 + 1.23 (x - 20) ; points de passage dans B, E, F, H
BEAM_MARKS = [("B", 60, 229, "cobalt"), ("E", 128, 313, "emerald"),
              ("F", 185, 383, "ruby"), ("H", 255, 469, "amber")]

STATES = {
    "empty": {},
    "play": {k: SOLUTION[k] for k in "ABDEF"},
    "done": dict(SOLUTION),
    "conflict": {**{k: SOLUTION[k] for k in "ABCDEFH"}, "G": "amber"},
    "three": {k: SOLUTION[k] for k in "ABD"},
}

DIRS = {
    "nef": dict(
        tints=dict(ruby="#b3122e", cobalt="#1f4fd1", emerald="#0f8a5f", amber="#e89a14"),
        lead="#2b2f36", lead_hi="#4b515b", empty="#1b1e24", empty_line="rgba(255,255,255,.035)",
        lead_w=7, out_w=12, light="#f4d58d", beam="#fff2d2", err="#ff5a4e",
        style="lead"),
    "atelier": dict(
        tints=dict(ruby="#d81f43", cobalt="#2c5fe0", emerald="#12a476", amber="#f6b326"),
        lead="#2b2925", lead_hi="#5a564e", empty="#fffdf7", empty_line="rgba(43,41,37,.10)",
        lead_w=6, out_w=8, light="#2b2925", beam="#fff7dc", err="#d4352a",
        style="pencil"),
    "nocturne": dict(
        tints=dict(ruby="#e2314f", cobalt="#3d6bff", emerald="#1fc28a", amber="#ffb42e"),
        lead="#0b0e15", lead_hi="#1f2533", empty="#232a3a", empty_line="rgba(190,205,235,.05)",
        lead_w=6, out_w=10, light="#ffd59e", beam="#ffe6bf", err="#ff5a4e",
        style="seam"),
}

_uid = [0]


def pts(poly):
    return " ".join(f"{x},{y}" for x, y in poly)


def centroid(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def tok_win(dir="nef", w="360", state="play", beam="1", target="", marks="1", glow="0", nums="0"):
    d = DIRS[dir]
    _uid[0] += 1
    u = f"w{_uid[0]}"
    placed = STATES[state]
    T = d["tints"]
    W = float(w)
    H = W * 560 / 340
    glow = glow == "1" or state == "done"
    o = []
    o.append(f'<svg class="win" viewBox="-20 -20 340 560" width="{W:.0f}" height="{H:.0f}" '
             f'xmlns="http://www.w3.org/2000/svg" style="overflow:visible">')
    o.append("<defs>")
    o.append(f'<clipPath id="{u}c"><path d="{OUTLINE}"/></clipPath>')
    o.append(f'<filter id="{u}t" x="0" y="0" width="100%" height="100%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.045 0.03" numOctaves="3" seed="23"/>'
             '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.6 -0.55"/></filter>')
    o.append(f'<filter id="{u}b" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="16"/></filter>')
    o.append(f'<filter id="{u}s" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3.2"/></filter>')
    o.append(f'<linearGradient id="{u}g" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="#fff" stop-opacity=".30"/>'
             '<stop offset=".45" stop-color="#fff" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>')
    o.append(f'<linearGradient id="{u}beam" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{d["beam"]}" stop-opacity=".0"/>'
             f'<stop offset=".25" stop-color="{d["beam"]}" stop-opacity=".55"/>'
             f'<stop offset="1" stop-color="{d["beam"]}" stop-opacity=".15"/></linearGradient>')
    o.append(f'<pattern id="{u}h" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             f'<line x1="0" y1="0" x2="0" y2="9" stroke="{d["empty_line"]}" stroke-width="3"/></pattern>')
    o.append("</defs>")

    # halo derriere le verre pose (lumiere qui deborde)
    if placed and (glow or d["style"] == "seam"):
        op = ".85" if glow else ".45"
        o.append(f'<g filter="url(#{u}b)" opacity="{op}">')
        for k, t in placed.items():
            o.append(f'<polygon points="{pts(CELLS[k])}" fill="{T[t]}" clip-path="url(#{u}c)"/>')
        o.append("</g>")

    o.append(f'<g clip-path="url(#{u}c)">')
    o.append(f'<rect x="0" y="0" width="300" height="520" fill="{d["empty"]}"/>')
    o.append(f'<rect x="0" y="0" width="300" height="520" fill="url(#{u}h)"/>')
    for k, t in placed.items():
        o.append(f'<polygon points="{pts(CELLS[k])}" fill="{T[t]}"/>')
    if target:
        t = target.split(":")
        o.append(f'<polygon points="{pts(CELLS[t[0]])}" fill="{T[t[1]]}" opacity=".38"/>')
    if placed:
        o.append('<g>')
        for k in placed:
            o.append(f'<polygon points="{pts(CELLS[k])}" fill="#fff" filter="url(#{u}t)" '
                     'opacity=".42" style="mix-blend-mode:overlay"/>')
            o.append(f'<polygon points="{pts(CELLS[k])}" fill="url(#{u}g)"/>')
        o.append('</g>')
    if glow:
        o.append(f'<rect x="0" y="0" width="300" height="520" fill="#fff" opacity=".07"/>')
    if beam == "1" and d["style"] == "pencil":
        o.append(f'<line x1="-40" y1="107" x2="340" y2="575" stroke="{d["lead"]}" stroke-width="2" '
                 'stroke-dasharray="2 7" stroke-linecap="round" opacity=".55"/>')
    elif beam == "1":
        o.append(f'<polygon points="-90,96 -38,52 390,580 338,628" fill="url(#{u}beam)" '
                 'style="mix-blend-mode:screen" opacity=".32"/>')
    o.append("</g>")

    # plomb
    if d["style"] == "seam":
        # la lumiere passe par les joints
        o.append(f'<g clip-path="url(#{u}c)" filter="url(#{u}s)" opacity="{".95" if placed else ".25"}">')
        for k in CELLS:
            o.append(f'<polygon points="{pts(CELLS[k])}" fill="none" stroke="{d["light"]}" '
                     f'stroke-width="{d["lead_w"] + 7}" stroke-linejoin="round"/>')
        o.append("</g>")
    o.append(f'<g clip-path="url(#{u}c)" fill="none" stroke-linejoin="round">')
    for k in CELLS:
        if d["style"] == "pencil" and k not in placed:
            o.append(f'<polygon points="{pts(CELLS[k])}" stroke="#8d877b" stroke-width="1.6" '
                     'stroke-dasharray="1 0"/>')
        else:
            o.append(f'<polygon points="{pts(CELLS[k])}" stroke="{d["lead"]}" stroke-width="{d["lead_w"]}"/>')
    if d["style"] != "pencil":
        for k in CELLS:
            o.append(f'<polygon points="{pts(CELLS[k])}" stroke="{d["lead_hi"]}" stroke-width="1.2" '
                     'transform="translate(-1,-1)" opacity=".7"/>')
    o.append("</g>")
    if d["style"] == "pencil" and not placed:
        o.append(f'<path d="{OUTLINE}" fill="none" stroke="#8d877b" stroke-width="2"/>')
    else:
        o.append(f'<path d="{OUTLINE}" fill="none" stroke="{d["lead"]}" stroke-width="{d["out_w"]}" stroke-linejoin="round"/>')

    if nums == "1":
        names = dict(A="1", B="2", C="3", D="4", E="5", F="6", G="7", H="8")
        for k in CELLS:
            if k in placed:
                continue
            cx, cy = centroid(CELLS[k])
            if k == "A":
                cy = 95
            o.append(f'<text x="{cx:.0f}" y="{cy + 5:.0f}" text-anchor="middle" font-size="15" '
                     f'font-family="Space Grotesk" font-weight="500" fill="#8d877b">{names[k]}</text>')

    if target:
        t = target.split(":")
        o.append(f'<polygon points="{pts(CELLS[t[0]])}" fill="none" stroke="{d["light"]}" stroke-width="3.5" '
                 f'stroke-dasharray="9 7" clip-path="url(#{u}c)" stroke-linejoin="round">'
                 '<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.4s" repeatCount="indefinite"/></polygon>')
    if state == "conflict":
        o.append(f'<line x1="150" y1="400" x2="150" y2="520" stroke="{d["err"]}" stroke-width="{d["lead_w"] + 2}" '
                 'stroke-linecap="round"/>')
        o.append(f'<line x1="150" y1="400" x2="150" y2="520" stroke="{d["err"]}" stroke-width="18" '
                 f'opacity=".35" filter="url(#{u}s)"/>')
    if beam == "1" and marks == "1":
        for k, x, y, t in BEAM_MARKS:
            lit = k in placed and placed[k] == t
            mk = d["lead"] if d["style"] == "pencil" else d["beam"]
            if lit:
                o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{mk}" stroke="{"#fff" if d["style"] == "pencil" else d["lead"]}" stroke-width="2.5"/>')
            else:
                o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{mk}" stroke-width="2.5" '
                         'stroke-dasharray="3 3" opacity=".9"/>')
    o.append("</svg>")
    return "".join(o)


def tok_chip(dir="nef", tint="ruby", w="56", state="ok"):
    """Une piece de verre taillee (eclat)."""
    d = DIRS[dir]
    _uid[0] += 1
    u = f"c{_uid[0]}"
    W = float(w)
    H = W * 56 / 64
    path = "M8,15 L31,4 L57,11 L61,39 L37,53 L5,45 Z"
    if state == "gone":
        stroke = "#8d877b" if dir == "atelier" else d["lead_hi"]
        return (f'<svg class="chip" viewBox="0 0 66 58" width="{W:.0f}" height="{H:.0f}">'
                f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="1.6" stroke-dasharray="4 4"/></svg>')
    c = d["tints"][tint]
    edge = "none" if dir == "atelier" else d["lead"]
    o = [f'<svg class="chip" viewBox="0 0 66 58" width="{W:.0f}" height="{H:.0f}" style="overflow:visible">',
         f'<defs><filter id="{u}t" x="0" y="0" width="100%" height="100%">'
         '<feTurbulence type="fractalNoise" baseFrequency="0.09 0.06" numOctaves="2" seed="7"/>'
         '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.6 -0.55"/></filter>'
         f'<linearGradient id="{u}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".38"/>'
         '<stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>'
         f'<filter id="{u}b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter></defs>']
    if state in ("held", "glow") or dir in ("atelier", "nocturne"):
        op = ".9" if state == "held" else ".45"
        o.append(f'<path d="{path}" fill="{c}" filter="url(#{u}b)" opacity="{op}"/>')
    o.append(f'<path d="{path}" fill="{c}"/>')
    o.append(f'<path d="{path}" fill="#fff" filter="url(#{u}t)" opacity=".6" style="mix-blend-mode:overlay"/>')
    o.append(f'<path d="{path}" fill="url(#{u}g)" stroke="{edge}" stroke-width="3" stroke-linejoin="round"/>')
    o.append("</svg>")
    return "".join(o)


# ---------------------------------------------------------------- habillage neutre
def tok_feed(theme="dark"):
    """Feed generique en arriere-plan du cadre desktop. Aucune marque, aucun logo."""
    cards = "".join(
        f'<div class="fc"><div class="fc-h"><i></i><b style="width:{a}px"></b></div>'
        f'<b class="fc-t" style="width:{t}px"></b><div class="fc-m" style="height:{h}px"></div>'
        f'<div class="fc-f"><b></b><b></b><b></b></div></div>'
        for a, t, h in [(120, 420, 220), (90, 360, 160), (140, 300, 260)])
    rail = "".join(f'<b style="width:{w}px"></b>' for w in (130, 96, 150, 110, 84, 140, 120, 90))
    return (f'<div class="feed feed-{theme}"><div class="ft"><span class="ft-a"></span>'
            f'<span class="ft-s"></span><span class="ft-r"><i></i><i></i><i></i></span></div>'
            f'<div class="fr">{rail}</div><div class="fcol">{cards}</div></div>')


def tok_dbar(theme="dark", title="Window Nº 23 — The Lily"):
    return (f'<div class="pbar pbar-{theme}"><i class="av"></i><span class="sub">r/vitrail</span>'
            f'<span class="dot">·</span><span class="pt">{title}</span><span class="x" aria-label="Close">'
            '<svg viewBox="0 0 16 16" width="14" height="14"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round"/></svg></span></div>')


def tok_mtop(theme="dark", title="Window Nº 23 — The Lily"):
    return (f'<div class="mst mst-{theme}"><span>9:41</span><span class="mst-r"><i></i><i></i><i></i></span></div>'
            f'<div class="mpb mpb-{theme}"><svg viewBox="0 0 16 16" width="16" height="16"><path d="M10 3L5 8l5 5" '
            'stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            f'<i class="av"></i><span class="mpb-t"><b>r/vitrail</b><span>{title}</span></span></div>')


BASECSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{min-width:1980px}
.board{padding:40px 48px 64px;min-height:100vh}
.bh{display:flex;align-items:flex-end;justify-content:space-between;gap:40px;margin-bottom:28px}
.bh h1{font-size:30px;line-height:1.1}
.bh p{font-size:14px;line-height:1.5;max-width:760px;opacity:.75;margin-top:8px}
.bh .meta{font:500 12px/1.6 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.04em;text-align:right;opacity:.7}
.frames{display:flex;gap:48px;align-items:flex-start}
.flabel{font:500 12px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin-bottom:12px}
.fd{position:relative;width:1440px;height:900px;overflow:hidden;border-radius:12px;box-shadow:0 30px 80px -30px rgba(0,0,0,.55),0 0 0 1px rgba(127,127,127,.25)}
.fm{position:relative;width:390px;height:844px;overflow:hidden;border-radius:46px;box-shadow:0 30px 80px -30px rgba(0,0,0,.55),0 0 0 10px #0b0b0d,0 0 0 11px rgba(127,127,127,.35)}
/* feed neutre */
.feed{position:absolute;inset:0}
.feed-dark{background:#0f1012}.feed-light{background:#eceae6}
.ft{height:56px;display:flex;align-items:center;gap:24px;padding:0 20px;border-bottom:1px solid rgba(127,127,127,.18)}
.ft-a{width:32px;height:32px;border-radius:50%;background:rgba(127,127,127,.35)}
.ft-s{width:520px;height:36px;border-radius:18px;background:rgba(127,127,127,.16);margin-left:180px}
.ft-r{margin-left:auto;display:flex;gap:12px}.ft-r i{width:32px;height:32px;border-radius:50%;background:rgba(127,127,127,.22)}
.fr{position:absolute;left:0;top:56px;bottom:0;width:260px;padding:24px;display:flex;flex-direction:column;gap:18px;border-right:1px solid rgba(127,127,127,.14)}
.fr b{height:10px;border-radius:5px;background:rgba(127,127,127,.22)}
.fcol{position:absolute;left:380px;top:80px;width:720px;display:flex;flex-direction:column;gap:16px}
.fc{border-radius:14px;padding:16px;background:rgba(127,127,127,.08)}
.fc-h{display:flex;gap:8px;align-items:center}.fc-h i{width:22px;height:22px;border-radius:50%;background:rgba(127,127,127,.3)}
.fc-h b,.fc-t,.fc-f b{display:block;height:9px;border-radius:5px;background:rgba(127,127,127,.25)}
.fc-t{height:14px;margin:12px 0}.fc-m{border-radius:10px;background:rgba(127,127,127,.14)}
.fc-f{display:flex;gap:10px;margin-top:12px}.fc-f b{width:64px;height:24px;border-radius:12px}
.scrim{position:absolute;inset:0;background:rgba(0,0,0,.62);backdrop-filter:blur(2px)}
.xp{position:absolute;left:200px;top:44px;width:1040px;height:812px;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 40px 90px -20px rgba(0,0,0,.7)}
.pbar{height:44px;flex:none;display:flex;align-items:center;gap:8px;padding:0 16px;font:500 13px/1 Inter,system-ui,sans-serif}
.pbar-dark{background:#0f1012;color:#c9c7c2;border-bottom:1px solid rgba(255,255,255,.07)}
.pbar-light{background:#fbfaf8;color:#45433f;border-bottom:1px solid rgba(0,0,0,.08)}
.pbar .av,.mpb .av{width:22px;height:22px;border-radius:50%;background:rgba(127,127,127,.4);flex:none}
.pbar .sub{font-weight:600}.pbar .dot{opacity:.5}.pbar .pt{opacity:.8}.pbar .x{margin-left:auto;opacity:.7;display:flex}
.game{position:relative;flex:1;overflow:hidden}
/* mobile */
.mst{height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;font:600 15px/1 Inter,system-ui,sans-serif}
.mst-r{display:flex;gap:5px}.mst-r i{width:16px;height:10px;border-radius:2px;background:currentColor;opacity:.8}
.mst-dark{background:#0f1012;color:#eee}.mst-light{background:#fbfaf8;color:#222}
.mpb{height:48px;display:flex;align-items:center;gap:10px;padding:0 14px;font:400 12px/1.25 Inter,system-ui,sans-serif}
.mpb-dark{background:#0f1012;color:#c9c7c2;border-bottom:1px solid rgba(255,255,255,.07)}
.mpb-light{background:#fbfaf8;color:#45433f;border-bottom:1px solid rgba(0,0,0,.08)}
.mpb-t{display:flex;flex-direction:column}.mpb-t b{font-weight:600}.mpb-t span{opacity:.75}
.mgame{position:relative;height:752px;overflow:hidden}
.states{margin-top:48px}
.states h2{font:500 12px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.06em;text-transform:uppercase;opacity:.6;margin-bottom:16px}
.srow{display:flex;gap:20px;flex-wrap:wrap}
.st{border-radius:12px;padding:18px;display:flex;flex-direction:column;gap:12px;align-items:flex-start}
.st .cap{font:500 11px/1.4 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.04em;opacity:.65}
"""

TOKENS = {
    "FONTS": tok_fonts, "WIN": tok_win, "CHIP": tok_chip, "FEED": tok_feed,
    "DBAR": tok_dbar, "MTOP": tok_mtop, "BASECSS": lambda: BASECSS,
}


def render(text):
    def rep(m):
        name, args = m.group(1), m.group(2).strip()
        kw = dict(re.findall(r'(\w+)=("[^"]*"|\S+)', args))
        kw = {k: v.strip('"') for k, v in kw.items()}
        if name == "FONTS":
            return tok_fonts(kw["names"])
        if name in ("GOTH", "GCHIP", "GTAB", "FLEURON"):
            import gothic  # import tardif (gothic importe build)
            return {"GOTH": gothic.tok_goth, "GCHIP": gothic.tok_gchip, "GTAB": gothic.tok_gtab, "FLEURON": gothic.tok_fleuron}[name](**kw)
        return TOKENS[name](**kw)
    return re.sub(r"\[\[([A-Z]+)((?:\s+\w+=(?:\"[^\"]*\"|[^\s\]]+))*)\s*\]\]", rep, text)


def main():
    jobs = [(p, OUT) for p in sorted(SRC.glob("*.src.html"))]
    jobs += [(p, SRC.parent / "planches" / "v2") for p in sorted((SRC / "v2").glob("*.src.html"))]
    for src, out in jobs:
        out.mkdir(parents=True, exist_ok=True)
        _uid[0] = 0
        html = render(src.read_text())
        assert "[[" not in html, f"jeton non remplace dans {src.name}"
        dst = out / src.name.replace(".src.html", ".html")
        dst.write_text(html)
        print(f"{dst.relative_to(SRC.parent.parent)}  {len(html) // 1024} Ko")


if __name__ == "__main__":
    main()
