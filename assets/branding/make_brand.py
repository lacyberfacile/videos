"""Génère le logo et la bannière YouTube de La Cyber Facile (SVG -> PNG via rsvg-convert)."""
import subprocess, random
from pathlib import Path

OUT = Path(__file__).parent
BG, BG2 = "#0A0F1C", "#111A2E"
CYAN, GREEN, RED, WHITE, GREY = "#22D3EE", "#22C55E", "#EF4444", "#F8FAFC", "#94A3B8"


def padlock(cx, cy, s):
    """Cadenas cyan + coche verte, centré en (cx, cy), taille s (hauteur totale ~ s)."""
    bw, bh = 0.78 * s, 0.56 * s              # corps
    bx, by = cx - bw / 2, cy - s / 2 + 0.44 * s
    sw = 0.085 * s                           # épaisseur anse
    r = 0.25 * s                             # rayon anse
    top = cy - s / 2 + sw / 2
    return f'''
  <path d="M {cx-r} {by+2} V {top+r} A {r} {r} 0 0 1 {cx+r} {top+r} V {by+2}"
        fill="none" stroke="{CYAN}" stroke-width="{sw}" stroke-linecap="round"/>
  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{0.12*s}" fill="url(#lockgrad)"/>
  <path d="M {cx-0.17*s} {by+bh*0.52} L {cx-0.04*s} {by+bh*0.72} L {cx+0.19*s} {by+bh*0.30}"
        fill="none" stroke="{BG}" stroke-width="{0.075*s}" stroke-linecap="round" stroke-linejoin="round"/>
'''


def defs():
    return f'''<defs>
  <linearGradient id="lockgrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{GREEN}"/>
  </linearGradient>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.35"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="bggrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>
  </linearGradient>
</defs>'''


def logo_svg(size=1080):
    c = size / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
{defs()}
  <rect width="{size}" height="{size}" fill="url(#bggrad)"/>
  <circle cx="{c}" cy="{c}" r="{size*0.42}" fill="url(#glow)"/>
  <circle cx="{c}" cy="{c}" r="{size*0.40}" fill="none" stroke="{CYAN}" stroke-opacity="0.25" stroke-width="{size*0.008}"/>
  {padlock(c, c, size*0.52)}
</svg>'''


def circuit_lines(w, h, seed=7):
    """Pistes de circuit discrètes en arrière-plan, hors zone de sécurité."""
    random.seed(seed)
    out = []
    for _ in range(46):
        left = random.random() < 0.5
        x = random.uniform(0, 380) if left else random.uniform(2180, w)
        y = random.uniform(80, h - 80)
        L1, L2 = random.uniform(60, 220), random.uniform(40, 160)
        d = -1 if left else 1
        col = random.choice([CYAN, CYAN, CYAN, GREEN])
        out.append(f'<path d="M {x} {y} h {L1*d} l {30*d} {30*random.choice([-1,1])} h {L2*d}" '
                   f'fill="none" stroke="{col}" stroke-opacity="0.18" stroke-width="3"/>'
                   f'<circle cx="{x}" cy="{y}" r="6" fill="{col}" fill-opacity="0.35"/>')
    return "\n  ".join(out)


def pill(x, y, text, color):
    w = 30 + len(text) * 17.5
    return (f'<rect x="{x}" y="{y}" width="{w}" height="52" rx="26" fill="{color}" fill-opacity="0.14" '
            f'stroke="{color}" stroke-width="2.5"/>'
            f'<text x="{x+w/2}" y="{y+35}" text-anchor="middle" font-family="Inter" font-weight="600" '
            f'font-size="28" fill="{color}">{text}</text>'), w


def banner_svg(w=2560, h=1440):
    # zone de sécurité 1546x423 centrée : x 507-2053, y 508-931
    p1, w1 = pill(970, 790, "Comprendre", CYAN)
    p2, w2 = pill(970 + w1 + 20, 790, "Repérer", RED)
    p3, _ = pill(970 + w1 + w2 + 40, 790, "Se protéger", GREEN)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
{defs()}
  <rect width="{w}" height="{h}" fill="url(#bggrad)"/>
  {circuit_lines(w, h)}
  <ellipse cx="{w/2}" cy="{h/2}" rx="900" ry="360" fill="url(#glow)" opacity="0.6"/>
  <circle cx="760" cy="720" r="190" fill="{BG}" stroke="{CYAN}" stroke-opacity="0.35" stroke-width="5"/>
  {padlock(760, 720, 250)}
  <text x="970" y="700" font-family="Inter" font-weight="800" font-size="118" fill="{WHITE}">La <tspan fill="{CYAN}">Cyber</tspan> Facile</text>
  <text x="972" y="758" font-family="Inter" font-weight="500" font-size="36" fill="{GREY}">La cybersécurité expliquée simplement, sans jargon.</text>
  {p1}{p2}{p3}
</svg>'''


def render(svg, name, w, h):
    s = OUT / f"{name}.svg"
    s.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), str(s), "-o", str(OUT / f"{name}.png")], check=True)


if __name__ == "__main__":
    render(logo_svg(), "logo_la_cyber_facile_1080", 1080, 1080)
    render(banner_svg(), "banniere_youtube_2560x1440", 2560, 1440)
