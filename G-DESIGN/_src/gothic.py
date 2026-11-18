"""Scene gothique (V2) : baie en pierre, archivoltes, colonnettes, verre detaille,
faisceaux volumetriques, poussiere, projection coloree sur le dallage.

Tout est du SVG statique. La pierre est eclairee par feDiffuseLighting (lumiere
distante venant du haut-gauche, comme le soleil qui traverse le vitrail).
Le vitrail reprend la geometrie et la solution de build.py (memes 8 cases).
"""
import random

from build import CELLS, STATES, BEAM_MARKS

TINTS = dict(ruby="#a3112b", cobalt="#1b42b8", emerald="#0b7d55", amber="#dc8c0c")
STONE = "#77705f"
GOLD = "#d8b26a"
SUN = "#ffe9bf"


def _hex(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    A, B = _hex(a), _hex(b)
    return "#" + "".join(f"{round(A[i] + (B[i] - A[i]) * t):02x}" for i in range(3))


def lancet(o=0.0, bottom=520.0, closed=True):
    L, R, S = 8 - o, 292 + o, 205
    c1y = 112 - o * 0.55
    c2x, c2y = 68 - o * 0.95, 42 - o * 1.05
    ay = 8 - o * 1.25
    p = (f"M{L:.1f},{bottom:.1f} L{L:.1f},{S} C{L:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} 150,{ay:.1f} "
         f"C{300 - c2x:.1f},{c2y:.1f} {R:.1f},{c1y:.1f} {R:.1f},{S} L{R:.1f},{bottom:.1f}")
    return p + (" Z" if closed else "")


def pts(poly):
    return " ".join(f"{x},{y}" for x, y in poly)


def inside_poly(x, y, poly):
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def inside_lancet(x, y, m=10):
    if y >= 205:
        return 8 + m < x < 292 - m and y < 520 - m
    return ((x - 150) / (142 - m)) ** 2 + ((205 - y) / (197 - m)) ** 2 < 0.92


# peinture de grisaille (traits peints sur le verre), coordonnees du vitrail
def _mirror(d):
    """Miroir gauche/droite d'un chemin ecrit en 'Cx,y' (x -> 300 - x)."""
    res = []
    for part in d.split():
        cmd = ""
        if part[0].isalpha():
            cmd, part = part[0], part[1:]
        if not part:
            res.append(cmd)
            continue
        x, y = part.split(",")
        res.append(f"{cmd}{300 - float(x):g},{y}")
    return " ".join(res)


PAINT = {
    "B": ["M128,146 Q78,190 18,232", "M124,168 Q84,226 30,282", "M120,196 Q100,244 86,284",
          "M60,214 Q52,236 40,250", "M92,236 Q86,256 72,270"],
    "D": ["M150,140 L150,318", "M150,196 Q134,236 126,284", "M150,196 Q166,236 174,284",
          "M150,240 Q142,262 140,292", "M150,240 Q158,262 160,292"],
    "E": ["M14,398 Q72,332 142,338", "M44,372 Q46,352 36,336", "M80,352 Q86,330 80,312",
          "M112,342 Q120,326 120,310", "M60,384 Q80,396 100,392"],
    "G": ["M20,470 Q75,438 130,470 Q75,502 20,470 Z", "M75,452 L75,488", "M50,470 L100,470"],
}
PAINT["C"] = [_mirror(d) for d in PAINT["B"]]
PAINT["F"] = [_mirror(d) for d in PAINT["E"]]
PAINT["H"] = [_mirror(d) for d in PAINT["G"]]

SOLDER = [(150, 120), (110, 290), (190, 290), (150, 330), (150, 400), (10, 168), (290, 168),
          (10, 300), (290, 300), (10, 409), (290, 409), (150, 514)]

_uid = [0]


def _defs(u, placed):
    d = [f'<clipPath id="{u}lc"><path d="{lancet()}"/></clipPath>']
    # pierre : bruit + lumiere diffuse distante (haut-gauche)
    d.append(
        f'<filter id="{u}st" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="5" seed="4" result="n"/>'
        '<feDiffuseLighting in="n" surfaceScale="2.6" diffuseConstant="1.15" lighting-color="#fff4e2" result="l">'
        '<feDistantLight azimuth="225" elevation="52"/></feDiffuseLighting>'
        '<feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.25" k2="0" k3="0" k4="0" result="m"/>'
        '<feComposite in="m" in2="SourceAlpha" operator="in"/></filter>')
    d.append(
        f'<filter id="{u}sf" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.11" numOctaves="4" seed="9" result="n"/>'
        '<feDiffuseLighting in="n" surfaceScale="1.4" diffuseConstant="1.2" lighting-color="#fff2dc" result="l">'
        '<feDistantLight azimuth="225" elevation="58"/></feDiffuseLighting>'
        '<feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.2" k2="0" k3="0" k4="0" result="m"/>'
        '<feComposite in="m" in2="SourceAlpha" operator="in"/></filter>')
    # verre : stries (etirees) + petites irregularites
    d.append(f'<filter id="{u}gs" x="0" y="0" width="100%" height="100%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.004 0.075" numOctaves="3" seed="11"/>'
             '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 2.2 -0.9"/></filter>')
    d.append(f'<filter id="{u}gm" x="0" y="0" width="100%" height="100%">'
             '<feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="3"/>'
             '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.4 -0.55"/></filter>')
    for b in (2, 5, 9, 16, 28):
        d.append(f'<filter id="{u}b{b}" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="{b}"/></filter>')
    for name, c in TINTS.items():
        d.append(f'<radialGradient id="{u}t{name}" cx=".42" cy=".38" r=".75">'
                 f'<stop offset="0" stop-color="{mix(c, "#fff6dc", .55)}"/>'
                 f'<stop offset=".25" stop-color="{mix(c, "#fff6dc", .18)}"/>'
                 f'<stop offset=".55" stop-color="{c}"/>'
                 f'<stop offset="1" stop-color="{mix(c, "#000", .42)}"/></radialGradient>')
    d.append(f'<radialGradient id="{u}clear" cx=".45" cy=".35" r=".8"><stop offset="0" stop-color="#2c3038"/>'
             '<stop offset="1" stop-color="#121418"/></radialGradient>')
    d.append(f'<radialGradient id="{u}sol" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#cfd3d9"/>'
             '<stop offset=".6" stop-color="#7c818a"/><stop offset="1" stop-color="#2c2f35"/></radialGradient>')
    d.append(f'<linearGradient id="{u}shaft" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{SUN}" stop-opacity=".42"/>'
             f'<stop offset=".55" stop-color="{SUN}" stop-opacity=".16"/>'
             f'<stop offset="1" stop-color="{SUN}" stop-opacity="0"/></linearGradient>')
    d.append(f'<linearGradient id="{u}col" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#26231e"/><stop offset=".22" stop-color="#9a927f"/>'
             '<stop offset=".38" stop-color="#c9bfa7"/><stop offset=".62" stop-color="#6e6757"/>'
             '<stop offset="1" stop-color="#1c1a16"/></linearGradient>')
    d.append(f'<linearGradient id="{u}beam" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0" stop-color="{SUN}" stop-opacity="0"/><stop offset=".3" stop-color="{SUN}" stop-opacity=".5"/>'
             f'<stop offset="1" stop-color="{SUN}" stop-opacity=".12"/></linearGradient>')
    d.append(f'<pattern id="{u}diaper" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             '<path d="M0,0 L0,22 M0,0 L22,0" stroke="#2a1a10" stroke-width="1.1" fill="none"/>'
             '<circle cx="11" cy="11" r="1.6" fill="#2a1a10"/></pattern>')
    return "".join(d)


def _glass(u, placed, target, beam, marks, rnd, empty_paint=True):
    """Vitrail en coordonnees 300 x 520."""
    o = []
    # halo de lumiere transmise sur la feuillure
    o.append(f'<g clip-path="url(#{u}lc)">')
    o.append(f'<rect width="300" height="520" fill="url(#{u}clear)"/>')
    # verre clair non pose : givre leger
    o.append(f'<rect width="300" height="520" fill="#9aa3b2" filter="url(#{u}gs)" opacity=".10"/>')
    for k, t in placed.items():
        o.append(f'<polygon points="{pts(CELLS[k])}" fill="url(#{u}t{t})"/>')
    if target:
        k, t = target.split(":")
        o.append(f'<polygon points="{pts(CELLS[k])}" fill="url(#{u}t{t})" opacity=".34"/>')
    # stries + marbrures uniquement sur le verre colore
    for k in placed:
        o.append(f'<polygon points="{pts(CELLS[k])}" fill="#fff" filter="url(#{u}gs)" opacity=".30" style="mix-blend-mode:soft-light"/>')
        o.append(f'<polygon points="{pts(CELLS[k])}" fill="#000" filter="url(#{u}gm)" opacity=".2"/>')
    # bulles (seeds)
    for k in placed:
        poly = CELLS[k]
        n = 0
        tries = 0
        while n < 9 and tries < 400:
            tries += 1
            x, y = rnd.uniform(0, 300), rnd.uniform(0, 520)
            if inside_poly(x, y, poly) and inside_lancet(x, y, 14):
                r = rnd.uniform(.7, 2.1)
                o.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r * 1.4:.1f}" ry="{r:.1f}" fill="#fff" fill-opacity=".18" '
                         'stroke="#fff" stroke-opacity=".55" stroke-width=".5"/>')
                n += 1
    # grisaille peinte
    for k, paths in PAINT.items():
        on = k in placed
        if not on and not empty_paint:
            continue
        col, op, w = ("#2a1a10", ".55", "2.2") if on else ("#d9d2c2", ".10", "1.6")
        o.append(f'<g stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" fill="none" stroke-linecap="round">')
        o.append("".join(f'<path d="{p}"/>' for p in paths))
        o.append("</g>")
    on_a = "A" in placed
    o.append(f'<polygon points="{pts(CELLS["A"])}" fill="url(#{u}diaper)" opacity="{".42" if on_a else ".07"}" '
             f'style="{"" if on_a else "filter:invert(1)"}"/>')
    # reflet de surface + assombrissement en bas (epaisseur)
    if beam:
        o.append(f'<polygon points="-90,96 -38,52 390,580 338,628" fill="url(#{u}beam)" style="mix-blend-mode:screen" opacity=".42"/>')
    o.append("</g>")

    # plomb : profil en H (sombre, arete claire, ombre)
    o.append(f'<g clip-path="url(#{u}lc)" fill="none" stroke-linejoin="round">')
    for k in CELLS:
        o.append(f'<polygon points="{pts(CELLS[k])}" stroke="#000" stroke-opacity=".55" stroke-width="9" transform="translate(1.5,2)"/>')
    for k in CELLS:
        o.append(f'<polygon points="{pts(CELLS[k])}" stroke="#1d1f24" stroke-width="7.5"/>')
    for k in CELLS:
        o.append(f'<polygon points="{pts(CELLS[k])}" stroke="#4f555f" stroke-width="1.4" transform="translate(-1.2,-1.2)" opacity=".8"/>')
    for k in CELLS:
        o.append(f'<polygon points="{pts(CELLS[k])}" stroke="#c9ccd2" stroke-width=".6" transform="translate(-1.8,-1.8)" opacity=".35"/>')
    o.append("</g>")
    # soudures
    for x, y in SOLDER:
        o.append(f'<circle cx="{x}" cy="{y}" r="5.4" fill="url(#{u}sol)" stroke="#111" stroke-width=".8"/>')
    # cadre / feuillure
    o.append(f'<path d="{lancet()}" fill="none" stroke="#14130f" stroke-width="13"/>')
    o.append(f'<path d="{lancet(-5)}" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="5" filter="url(#{u}b2)"/>')

    if target:
        k, t = target.split(":")
        o.append(f'<polygon points="{pts(CELLS[k])}" fill="none" stroke="{GOLD}" stroke-width="3.2" stroke-dasharray="9 7" '
                 f'clip-path="url(#{u}lc)" stroke-linejoin="round">'
                 '<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.4s" repeatCount="indefinite"/></polygon>')
    if placed.get("G") == "amber" and placed.get("H") == "amber":
        o.append('<line x1="150" y1="400" x2="150" y2="520" stroke="#ff5a4e" stroke-width="8" stroke-linecap="round"/>')
        o.append(f'<line x1="150" y1="400" x2="150" y2="520" stroke="#ff5a4e" stroke-width="22" opacity=".45" filter="url(#{u}b5)"/>')
    if beam and marks:
        for k, x, y, t in BEAM_MARKS:
            lit = placed.get(k) == t
            if lit:
                o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{SUN}" opacity=".5" filter="url(#{u}b5)"/>')
                o.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{SUN}" stroke="#1d1f24" stroke-width="2"/>')
            else:
                o.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="none" stroke="{SUN}" stroke-width="2" stroke-dasharray="3 3"/>')
    return "".join(o)


def _mouldings(u, s):
    """Archivoltes (3 rouleaux), larmier et ombres portees, coordonnees du vitrail."""
    o = []
    orders = [(18, 16), (44, 18), (70, 16)]  # (decalage, largeur)
    # fond de l'embrasure (ebrasement) : du plus profond au plus clair
    o.append(f'<path d="{lancet(84, 548)}" fill="#24211c" filter="url(#{u}sf)"/>')
    for i, (off, w) in enumerate(reversed(orders)):
        p = lancet(off, 532 + off * .2, closed=False)
        o.append(f'<path d="{p}" fill="none" stroke="#0e0d0b" stroke-width="{w + 7}" stroke-linecap="butt"/>')
        o.append(f'<path d="{p}" fill="none" stroke="{STONE}" stroke-width="{w}" filter="url(#{u}sf)" stroke-linecap="butt"/>')
        o.append(f'<path d="{p}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="{w * .55}" transform="translate({w * .2:.1f},{w * .2:.1f})" stroke-linecap="butt" filter="url(#{u}b2)"/>')
        o.append(f'<path d="{p}" fill="none" stroke="#efe4cc" stroke-opacity=".38" stroke-width="{w * .22:.1f}" transform="translate({-w * .22:.1f},{-w * .22:.1f})" stroke-linecap="butt"/>')
    # gorges profondes entre les rouleaux
    for off in (31, 57):
        o.append(f'<path d="{lancet(off, 540, closed=False)}" fill="none" stroke="#070605" stroke-width="5"/>')
    # larmier (hood mould) avec culots
    hp = lancet(92, 205, closed=False)
    o.append(f'<path d="{hp}" fill="none" stroke="#0e0d0b" stroke-width="15"/>')
    o.append(f'<path d="{hp}" fill="none" stroke="{STONE}" stroke-width="10" filter="url(#{u}sf)"/>')
    o.append(f'<path d="{hp}" fill="none" stroke="#f3e8d0" stroke-opacity=".45" stroke-width="2.4" transform="translate(-2.5,-2.5)"/>')
    for x in (-84, 384):
        leaves = "".join(
            f'<ellipse cx="0" cy="-8" rx="6" ry="9" transform="rotate({a})" fill="{STONE}" stroke="#0e0d0b" stroke-width="1.6"/>'
            for a in (0, 90, 180, 270))
        o.append(f'<g transform="translate({x},214)"><circle r="17" fill="#000" opacity=".55" filter="url(#{u}b2)" transform="translate(3,4)"/>'
                 f'<g filter="url(#{u}sf)">{leaves}</g>'
                 '<path d="M-5,-15 Q0,-19 5,-15 M-15,-5 Q-19,0 -15,5" stroke="#f3e8d0" stroke-opacity=".5" stroke-width="1.4" fill="none"/>'
                 f'<circle r="4.5" fill="#cbbf9f" stroke="#0e0d0b" stroke-width="1.4"/></g>')
    # appui (glacis) sous la baie
    o.append(f'<path d="M-20,522 L320,522 L344,556 L-44,556 Z" fill="{STONE}" filter="url(#{u}sf)"/>')
    o.append('<path d="M-20,522 L320,522" stroke="#f3e8d0" stroke-opacity=".5" stroke-width="2"/>')
    o.append('<path d="M-44,556 L344,556" stroke="#050404" stroke-width="3"/>')
    o.append(f'<path d="M-44,558 L344,558 L344,570 L-44,570 Z" fill="#000" opacity=".55" filter="url(#{u}b5)"/>')
    return "".join(o)


def _column(u, x, top, bottom, w):
    """Colonnette : base, fut avec bague, chapiteau a crochets."""
    o = [f'<g transform="translate({x},0)">']
    h = bottom - top
    o.append(f'<rect x="{-w / 2}" y="{top}" width="{w}" height="{h}" fill="url(#{u}col)"/>')
    o.append(f'<rect x="{-w / 2}" y="{top}" width="{w}" height="{h}" fill="#888" filter="url(#{u}sf)" opacity=".35" style="mix-blend-mode:multiply"/>')
    mid = top + h * .52
    o.append(f'<rect x="{-w * .78}" y="{mid - 4}" width="{w * 1.56}" height="8" rx="4" fill="url(#{u}col)" stroke="#0e0d0b" stroke-width="1"/>')
    # chapiteau
    o.append(f'<path d="M{-w / 2},{top} L{-w * 1.25},{top - 22} L{w * 1.25},{top - 22} L{w / 2},{top} Z" fill="url(#{u}col)" stroke="#0e0d0b" stroke-width="1"/>')
    for sx in (-1, 1):
        o.append(f'<path d="M{sx * w * .3},{top - 2} Q{sx * w * 1.6},{top - 10} {sx * w * 1.2},{top - 24} Q{sx * w * .9},{top - 16} {sx * w * 1.05},{top - 13}" '
                 'fill="none" stroke="#141210" stroke-width="2.2"/>')
        o.append(f'<circle cx="{sx * w * 1.18}" cy="{top - 21}" r="3" fill="#bdb39b" stroke="#141210" stroke-width="1.2"/>')
    o.append(f'<rect x="{-w * 1.45}" y="{top - 30}" width="{w * 2.9}" height="9" fill="{STONE}" filter="url(#{u}sf)" stroke="#0e0d0b" stroke-width="1"/>')
    o.append(f'<line x1="{-w * 1.45}" y1="{top - 30}" x2="{w * 1.45}" y2="{top - 30}" stroke="#f3e8d0" stroke-opacity=".5" stroke-width="1.4"/>')
    # base
    for i, (ww, hh) in enumerate([(1.35, 7), (1.6, 8), (1.9, 12)]):
        yb = bottom + sum(v[1] for v in [(1.35, 7), (1.6, 8), (1.9, 12)][:i])
        o.append(f'<rect x="{-w * ww / 2 * 1.2}" y="{yb}" width="{w * ww * 1.2}" height="{hh}" rx="{3 if i < 2 else 0}" fill="url(#{u}col)" stroke="#0e0d0b" stroke-width="1"/>')
    o.append("</g>")
    return "".join(o)


def tok_goth(w="1040", h="768", gx="404", gy="110", gw="232", fy="566", state="play", target="",
             beam="1", marks="1", cols="1", motes="70", projx="0", mode="scene", seed="23"):
    _uid[0] += 1
    u = f"g{_uid[0]}"
    W, H, GX, GY, GW, FY = map(float, (w, h, gx, gy, gw, fy))
    s = GW / 300
    placed = STATES[state]
    rnd = random.Random(int(seed))
    beam_on = beam == "1"
    o = [f'<svg class="goth" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" xmlns="http://www.w3.org/2000/svg">',
         f"<defs>{_defs(u, placed)}"]
    o.append(f'<radialGradient id="{u}vig" cx="{(GX + GW / 2) / W:.3f}" cy="{(GY + GW * .9) / H:.3f}" r=".85">'
             '<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".32" stop-color="#000" stop-opacity=".42"/><stop offset=".7" stop-color="#000" stop-opacity=".8"/>'
             '<stop offset="1" stop-color="#000" stop-opacity=".93"/></radialGradient>')
    o.append(f'<linearGradient id="{u}fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".6"/>'
             '<stop offset=".25" stop-color="#000" stop-opacity=".1"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient>')
    o.append(f'<clipPath id="{u}floor"><rect x="0" y="{FY}" width="{W}" height="{H - FY}"/></clipPath>')
    o.append("</defs>")
    gt = f"translate({GX:.1f},{GY:.1f}) scale({s:.4f})"

    if mode == "glass":
        o.append(f'<rect width="{W}" height="{H}" fill="#14120f"/>')
        o.append(f'<g transform="{gt}">{_glass(u, placed, target, beam_on, marks == "1", rnd)}</g>')
        if state == "done":
            o.append(f'<g transform="{gt}" filter="url(#{u}b16)" opacity=".7" style="mix-blend-mode:screen">')
            o.append("".join(f'<polygon points="{pts(CELLS[k])}" fill="{TINTS[t]}" clip-path="url(#{u}lc)"/>' for k, t in placed.items()))
            o.append("</g>")
        o.append("</svg>")
        return "".join(o)

    # 1. mur en appareil de pierre
    o.append(f'<rect width="{W}" height="{FY}" fill="#47423a" filter="url(#{u}st)"/>')
    rows = []
    ch = 30 * max(s, .55) / .77
    y = FY - ch
    r2 = random.Random(5)
    row = 0
    while y > -ch:
        rows.append(f'M0,{y:.1f} L{W},{y:.1f}')
        x = -r2.uniform(0, 80) - (40 if row % 2 else 0)
        while x < W:
            x += r2.uniform(70, 120) * max(s, .55) / .77
            rows.append(f'M{x:.1f},{y:.1f} L{x:.1f},{y + ch:.1f}')
        y -= ch
        row += 1
    jd = " ".join(rows)
    o.append(f'<path d="{jd}" stroke="#14110d" stroke-opacity=".75" stroke-width="2" fill="none"/>')
    o.append(f'<path d="{jd}" stroke="#f3e6cc" stroke-opacity=".10" stroke-width="1" fill="none" transform="translate(1,1.6)"/>')
    # bandeaux horizontaux (cordons) au niveau des chapiteaux et de l'appui
    for yy, hh in ((GY + 205 * s - 30 * s - 10, 12), (GY + 556 * s, 16)):
        o.append(f'<rect x="0" y="{yy:.1f}" width="{W}" height="{hh}" fill="{STONE}" filter="url(#{u}sf)"/>')
        o.append(f'<line x1="0" y1="{yy:.1f}" x2="{W}" y2="{yy:.1f}" stroke="#f3e8d0" stroke-opacity=".35" stroke-width="1.5"/>')
        o.append(f'<rect x="0" y="{yy + hh:.1f}" width="{W}" height="7" fill="#000" opacity=".6" filter="url(#{u}b2)"/>')

    # 2. rebond colore sur la pierre autour de la baie
    if placed:
        o.append(f'<g transform="translate({GX + GW / 2:.1f},{GY + 260 * s:.1f}) scale(1.55) translate({-GW / 2:.1f},{-260 * s:.1f}) {f"scale({s:.4f})"}" '
                 f'filter="url(#{u}b28)" opacity=".6" style="mix-blend-mode:screen">')
        o.append("".join(f'<polygon points="{pts(CELLS[k])}" fill="{TINTS[t]}" clip-path="url(#{u}lc)"/>' for k, t in placed.items()))
        o.append("</g>")

    # 3. baie : moulures + colonnettes + vitrail
    o.append(f'<g transform="{gt}">{_mouldings(u, s)}</g>')
    if cols == "1":
        cw = 22 * s
        for cx in (GX - 108 * s, GX + 408 * s):
            o.append(_column(u, cx, GY + 205 * s, GY + 548 * s, cw))
    o.append(f'<g transform="{gt}">{_glass(u, placed, target, beam_on, marks == "1", rnd)}</g>')
    # lumiere transmise qui deborde du verre (bloom)
    if placed:
        o.append(f'<g transform="{gt}" filter="url(#{u}b9)" opacity="{".95" if state == "done" else ".62"}" style="mix-blend-mode:screen">')
        o.append("".join(f'<polygon points="{pts(CELLS[k])}" fill="{mix(TINTS[t], "#fff", .25)}" clip-path="url(#{u}lc)"/>' for k, t in placed.items()))
        o.append("</g>")

    # 4. sol dalle en perspective
    o.append(f'<g clip-path="url(#{u}floor)">')
    o.append(f'<rect x="0" y="{FY}" width="{W}" height="{H - FY}" fill="#3a362f" filter="url(#{u}st)"/>')
    cx = GX + GW / 2
    vy = FY - (H - FY) * 1.6
    lines = []
    for i in range(-14, 15):
        lines.append(f'M{cx:.1f},{vy:.1f} L{cx + i * 120 * s / .77:.1f},{H + 400}')
    n = 7
    for k in range(1, n + 1):
        yy = FY + (H - FY) * (k / n) ** 1.7
        lines.append(f'M0,{yy:.1f} L{W},{yy:.1f}')
    fl = " ".join(lines)
    o.append(f'<path d="{fl}" stroke="#0c0a08" stroke-opacity=".8" stroke-width="2" fill="none"/>')
    o.append(f'<path d="{fl}" stroke="#f0e2c4" stroke-opacity=".08" stroke-width="1" fill="none" transform="translate(0,1.5)"/>')
    # projection du vitrail sur le dallage (miroir vertical, cisaille vers la droite)
    k1, k2 = .62, .30
    x0 = GX + float(projx)
    a, c, d = s, -k1 * s, -k2 * s
    e, f = x0 + 520 * k1 * s, FY + 6 + 520 * k2 * s
    mat = f"matrix({a:.4f},0,{c:.4f},{d:.4f},{e:.1f},{f:.1f})"
    o.append(f'<g transform="{mat}" style="mix-blend-mode:screen">')
    o.append(f'<g filter="url(#{u}b9)" opacity=".9">')
    o.append(f'<path d="{lancet()}" fill="{SUN}" opacity=".16"/>')
    o.append("".join(f'<polygon points="{pts(CELLS[kk])}" fill="{mix(TINTS[t], "#fff", .15)}" clip-path="url(#{u}lc)"/>' for kk, t in placed.items()))
    o.append("</g>")
    o.append(f'<g clip-path="url(#{u}lc)" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="7" filter="url(#{u}b2)">')
    o.append("".join(f'<polygon points="{pts(CELLS[kk])}"/>' for kk in CELLS))
    o.append("</g></g>")
    o.append(f'<rect x="0" y="{FY}" width="{W}" height="{H - FY}" fill="url(#{u}fl)"/>')
    o.append("</g>")
    # plinthe (pied de mur) + ombre de contact
    o.append(f'<rect x="0" y="{FY - 12}" width="{W}" height="12" fill="{STONE}" filter="url(#{u}sf)"/>')
    o.append(f'<line x1="0" y1="{FY - 12}" x2="{W}" y2="{FY - 12}" stroke="#f3e8d0" stroke-opacity=".3" stroke-width="1.2"/>')
    o.append(f'<rect x="0" y="{FY}" width="{W}" height="10" fill="#000" opacity=".7" filter="url(#{u}b5)"/>')

    # 6. vignettage (la nef est sombre, seule la baie eclaire)
    o.append(f'<rect width="{W}" height="{H}" fill="url(#{u}vig)"/>')
    # 5. faisceaux volumetriques, du vitrail vers le sol
    if beam_on:
        o.append(f'<g style="mix-blend-mode:screen">')
        shafts = [(.02, .42, 1.0), (.3, .78, .85), (.58, 1.0, .7), (.12, .22, .6), (.66, .74, .55)]
        top_y0 = GY + 330 * s
        for (u0, u1, op) in shafts:
            xa = GX + 300 * s * u0
            xb = GX + 300 * s * u1
            ya, yb = top_y0 + 300 * s * u0 * .6, top_y0 + 300 * s * u1 * .6
            dx, dy = (H - FY) * 1.05 + 120 * s, H - top_y0 + 40
            o.append(f'<polygon points="{xa:.1f},{ya:.1f} {xb:.1f},{yb:.1f} {xb + dx:.1f},{yb + dy:.1f} {xa + dx * .92:.1f},{ya + dy:.1f}" '
                     f'fill="url(#{u}shaft)" opacity="{op}" filter="url(#{u}b9)"/>')
        # tintes : le rayon emporte la couleur des pieces traversees
        for kk, t in placed.items():
            ccx = sum(p[0] for p in CELLS[kk]) / len(CELLS[kk])
            ccy = sum(p[1] for p in CELLS[kk]) / len(CELLS[kk])
            xa, ya = GX + ccx * s, GY + ccy * s
            o.append(f'<polygon points="{xa - 10:.1f},{ya:.1f} {xa + 10:.1f},{ya:.1f} {xa + 170 * s + 30:.1f},{ya + 260 * s + 60:.1f} {xa + 130 * s:.1f},{ya + 260 * s + 60:.1f}" '
                     f'fill="{mix(TINTS[t], "#fff", .2)}" opacity=".3" filter="url(#{u}b16)"/>')
        o.append("</g>")
        # poussiere en suspension
        nm = int(motes)
        for i in range(nm):
            t = rnd.random()
            xx = GX + rnd.uniform(0, 300 * s) + t * ((H - FY) * 1.05 + 120 * s)
            yy = GY + 120 * s + t * (H - GY - 80)
            r = rnd.uniform(.5, 1.9) * max(s, .6) / .77
            op = rnd.uniform(.25, .85) * (1 - t * .6)
            bl = f' filter="url(#{u}b2)"' if r > 1.4 else ""
            o.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="{r:.2f}" fill="{SUN}" opacity="{op:.2f}"{bl}/>')

    o.append("</svg>")
    return "".join(o)


def tok_gchip(tint="ruby", w="52", state="ok"):
    """Eclat de verre pose sur la pierre, avec son ombre coloree."""
    _uid[0] += 1
    u = f"q{_uid[0]}"
    W = float(w)
    H = W * 64 / 72
    path = "M10,18 L33,6 L60,13 L64,41 L39,56 L7,48 Z"
    if state == "gone":
        return (f'<svg class="chip" viewBox="0 0 72 64" width="{W:.0f}" height="{H:.0f}">'
                f'<path d="{path}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="1.4" stroke-dasharray="3 4"/></svg>')
    c = TINTS[tint]
    lift = -6 if state == "held" else 0
    return (
        f'<svg class="chip" viewBox="0 0 72 64" width="{W:.0f}" height="{H:.0f}" style="overflow:visible">'
        f'<defs><radialGradient id="{u}g" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="{mix(c, "#fff6dc", .45)}"/>'
        f'<stop offset=".55" stop-color="{c}"/><stop offset="1" stop-color="{mix(c, "#000", .45)}"/></radialGradient>'
        f'<filter id="{u}b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>'
        f'<filter id="{u}s" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.01 0.18" numOctaves="2" seed="11"/>'
        '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 2.2 -0.9"/></filter></defs>'
        # ombre coloree (la lumiere traverse la piece et teinte la pierre)
        f'<path d="{path}" fill="{c}" opacity="{".85" if state == "held" else ".6"}" filter="url(#{u}b)" transform="translate(10,{12 - lift})"/>'
        f'<g transform="translate(0,{lift})">'
        f'<path d="{path}" fill="url(#{u}g)" stroke="#0b0a08" stroke-width="2.4" stroke-linejoin="round"/>'
        f'<path d="{path}" fill="#fff" filter="url(#{u}s)" opacity=".35" style="mix-blend-mode:soft-light"/>'
        '<path d="M14,19 L33,9 L56,15" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>'
        '<circle cx="40" cy="34" r="1.6" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width=".6"/>'
        '<circle cx="26" cy="38" r="1" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width=".5"/>'
        '</g></svg>')


def tok_gtab(w="262", h="500", arch="1"):
    """Plaque de pierre gravee (fond de panneau), sommet en arc brise ou droit."""
    _uid[0] += 1
    u = f"p{_uid[0]}"
    W, H = float(w), float(h)
    if arch == "1":
        sp = W * .36
        d = (f"M0,{H} L0,{sp:.1f} C0,{sp * .45:.1f} {W * .22:.1f},{sp * .12:.1f} {W / 2:.1f},0 "
             f"C{W * .78:.1f},{sp * .12:.1f} {W},{sp * .45:.1f} {W},{sp:.1f} L{W},{H} Z")
        i = 9
        spi = sp + 2
        di = (f"M{i},{H - i} L{i},{spi:.1f} C{i},{spi * .5:.1f} {W * .24:.1f},{sp * .2 + i:.1f} {W / 2:.1f},{i * 1.6:.1f} "
              f"C{W * .76:.1f},{sp * .2 + i:.1f} {W - i},{spi * .5:.1f} {W - i},{spi:.1f} L{W - i},{H - i} Z")
    else:
        d = f"M0,0 L{W},0 L{W},{H} L0,{H} Z"
        i = 9
        di = f"M{i},{i} L{W - i},{i} L{W - i},{H - i} L{i},{H - i} Z"
    return (
        f'<svg class="tabbg" viewBox="-6 -6 {W + 12:.0f} {H + 12:.0f}" width="{W + 12:.0f}" height="{H + 12:.0f}" '
        'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
        f'<defs><filter id="{u}f" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="5" seed="17" result="n"/>'
        '<feDiffuseLighting in="n" surfaceScale="1.8" diffuseConstant="1.1" lighting-color="#fff2dc" result="l">'
        '<feDistantLight azimuth="225" elevation="55"/></feDiffuseLighting>'
        '<feComposite in="l" in2="SourceGraphic" operator="arithmetic" k1="1.2" k2="0" k3="0" k4="0" result="m"/>'
        '<feComposite in="m" in2="SourceAlpha" operator="in"/></filter>'
        f'<linearGradient id="{u}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".45"/></linearGradient>'
        f'<filter id="{u}b" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter></defs>'
        f'<path d="{d}" fill="#000" opacity=".75" filter="url(#{u}b)" transform="translate(5,12)"/>'
        f'<path d="{d}" fill="#3a352d" filter="url(#{u}f)"/>'
        f'<path d="{d}" fill="url(#{u}g)"/>'
        f'<path d="{d}" fill="none" stroke="#f3e6c8" stroke-opacity=".28" stroke-width="1.5" transform="translate(-.6,-.6)"/>'
        f'<path d="{d}" fill="none" stroke="#000" stroke-opacity=".7" stroke-width="1.5" transform="translate(.9,.9)"/>'
        # filet grave et dore
        f'<path d="{di}" fill="none" stroke="#000" stroke-opacity=".6" stroke-width="1.6" transform="translate(.8,.8)"/>'
        f'<path d="{di}" fill="none" stroke="{GOLD}" stroke-opacity=".55" stroke-width="1"/>'
        '</svg>')


def tok_fleuron(w="200"):
    W = float(w)
    m = W / 2
    return (f'<svg class="fleuron" viewBox="0 0 {W:.0f} 18" width="{W:.0f}" height="18" aria-hidden="true">'
            f'<g stroke="{GOLD}" stroke-opacity=".7" fill="none" stroke-width="1">'
            f'<line x1="0" y1="9" x2="{m - 16:.0f}" y2="9"/><line x1="{m + 16:.0f}" y1="9" x2="{W:.0f}" y2="9"/>'
            f'<circle cx="{m - 5:.1f}" cy="9" r="4.2"/><circle cx="{m + 5:.1f}" cy="9" r="4.2"/>'
            f'<circle cx="{m:.1f}" cy="4" r="4.2"/><circle cx="{m:.1f}" cy="14" r="4.2"/></g>'
            f'<circle cx="{m:.1f}" cy="9" r="1.6" fill="{GOLD}"/></svg>')
