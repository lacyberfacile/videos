"""Short #004 — Le même mot de passe partout."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Tu utilises le même mot de passe partout ? Alors un seul piratage suffit.",
    "Un site se fait pirater, et les mots de passe de ses clients fuitent.",
    "Les pirates les essaient automatiquement sur des centaines d'autres sites. C'est comme une seule clé pour ta maison, ta voiture et ton casier.",
    "Mail, réseaux sociaux, compte de jeu : tout tombe en même temps.",
    "Trois réflexes. Un : un mot de passe différent pour chaque site.",
    "Deux : laisse un gestionnaire de mots de passe les retenir pour toi.",
    "Trois : active la double authentification. Même avec ton mot de passe, il manquera un code au pirate.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
APPS = ["Mail", "Insta", "Jeu", "Cloud", "Achats", "Banque"]


def tile(img, cx, cy, s, label, color, a=255):
    dr = D(img)
    w = 230 * s
    dr.rounded_rectangle([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], radius=int(46 * s), fill=(22, 30, 50, a), outline=color + (a,), width=5)
    dr.text((cx, cy), label, font=font(int(46 * s), "ExtraBold"), fill=WHITE + (a,), anchor="mm")


def pw_field(img, cx, cy, w, color, k=1.0):
    dr = D(img)
    a = int(255 * clamp(k * 1.5))
    dr.rounded_rectangle([cx - w / 2, cy - 60, cx + w / 2, cy + 60], radius=24, fill=(30, 40, 62, a), outline=color + (a,), width=5)
    dr.text((cx, cy), "Soleil2004!", font=font(56, "ExtraBold"), fill=WHITE + (a,), anchor="mm")


def s1(img, t, d):
    glitch_text(img, W / 2, 320, "Même mot de passe partout ?", 88, WHITE, t, 0.0)
    pw_field(img, W / 2, 700, 620, CYAN, ease_out(prog(t, 0.1, 0.4)))
    for i, a in enumerate(APPS):
        k = ease_out(prog(t, 0.6 + i * 0.12, 0.45))
        if k <= 0:
            continue
        tx, ty = W / 2 + ((i % 3) - 1) * 300, 1060 + (i // 3) * 300
        x, y = W / 2 + (tx - W / 2) * k, 700 + (ty - 700) * k
        tile(img, x, y, 0.4 + 0.6 * k, a, CYAN)
        if k > 0.9:
            D(img).text((x, y + 80), "Soleil2004!", font=font(26, "SemiBold"), fill=GREY + (255,), anchor="mm")


def s2(img, t, d):
    dr = D(img)
    cx, cy = W / 2, 760
    crack = ease_out(prog(t, d * 0.25, 0.4))
    shake = math.sin(t * 60) * 8 * (1 - crack) if t > d * 0.2 else 0
    dr.rounded_rectangle([cx - 260 + shake, cy - 260, cx + 260 + shake, cy + 260], radius=40, fill=(22, 30, 50, 255),
                         outline=mix(CYAN, RED, crack) + (255,), width=8)
    for j in range(4):
        dr.rounded_rectangle([cx - 200 + shake, cy - 200 + j * 105, cx + 200 + shake, cy - 130 + j * 105], radius=14, fill=(40, 52, 76, 255))
        dr.ellipse([cx + 140 + shake, cy - 180 + j * 105, cx + 170 + shake, cy - 150 + j * 105], fill=mix(GREEN, RED, crack) + (255,))
    if crack > 0:
        pts = [(cx - 40, cy - 260), (cx + 10, cy - 120), (cx - 30, cy), (cx + 30, cy + 120), (cx - 10, cy + 260)]
        dr.line(pts, fill=RED + (255,), width=int(10 * crack))
    # fuite : lignes identifiant/mot de passe qui tombent
    for i in range(7):
        ph = (t * 0.6 + i / 7) % 1
        if t < d * 0.35:
            break
        y = cy + 280 + ph * 650
        x = cx + (i - 3) * 110
        dr.text((x, y), "•••••", font=font(36, "Bold"), fill=RED + (int(255 * (1 - ph)),), anchor="mm")
    pop_text(img, W / 2, 300, "Un site piraté", 96, WHITE, t, 0.05)
    stamp(img, W / 2, 1300, "FUITE", RED, t, d * 0.4, size=120)


def s3(img, t, d):
    dr = D(img)
    doors = [("Maison", 220), ("Voiture", W / 2), ("Casier", 860)]
    for i, (lab, x) in enumerate(doors):
        open_k = ease_out(prog(t, d * (0.45 + i * 0.15), 0.3))
        padlock(img, x, 1000, 0.75, mix(CYAN, RED, open_k), open_k)
        D(img).text((x, 1180), lab, font=font(44, "Bold"), fill=WHITE + (255,), anchor="mm")
    # la clé passe de cadenas en cadenas
    kt = prog(t, d * 0.4, d * 0.5)
    if kt > 0:
        x = 220 + (860 - 220) * ease_in_out(kt)
        key(img, x, 800 + math.sin(kt * math.pi * 3) * -40, 0.55, (234, 179, 8))
    pop_text(img, W / 2, 300, "Testé partout", 96, RED, t, 0.05)
    pop_text(img, W / 2, 470, "sur des centaines de sites", 64, WHITE, t, 0.4)
    chip(img, W / 2, 1400, "Une seule clé pour tout", RED, prog(t, d * 0.6, 0.4), 50)


def s4(img, t, d):
    for i, a in enumerate(APPS):
        x, y = W / 2 + ((i % 3) - 1) * 300, 760 + (i // 3) * 320
        k = ease_out(prog(t, 0.25 + i * 0.22, 0.25))
        col = mix(CYAN, RED, k)
        tile(img, x, y + 18 * k, 1.0 - 0.05 * k, a, col)
        if k > 0:
            cross(img, x + 80, y - 80, 30, RED, k, 12)
    pop_text(img, W / 2, 330, "Tout tombe", 110, RED, t, 0.05)


def ico_keys(img, cx, cy, s, col):
    for j, c in enumerate([CYAN, GREEN, (234, 179, 8)]):
        key(img, cx, cy - 60 * s + j * 60 * s, 0.32 * s, c if col != (60, 75, 100) else col)


def ico_vault(img, cx, cy, s, col):
    dr = D(img)
    dr.rounded_rectangle([cx - 85 * s, cy - 85 * s, cx + 85 * s, cy + 85 * s], radius=int(18 * s), outline=col + (255,), width=int(10 * s))
    dr.ellipse([cx - 45 * s, cy - 45 * s, cx + 45 * s, cy + 45 * s], outline=col + (255,), width=int(8 * s))
    dr.line([cx, cy - 45 * s, cx, cy + 45 * s], fill=col + (255,), width=int(6 * s))


def ico_code(img, cx, cy, s, col):
    dr = D(img)
    dr.rounded_rectangle([cx - 60 * s, cy - 100 * s, cx + 60 * s, cy + 100 * s], radius=int(18 * s), outline=col + (255,), width=int(8 * s))
    dr.text((cx, cy), "482\n913", font=font(int(38 * s), "Black"), fill=col + (255,), anchor="mm", align="center")


ITEMS = ["Un mot de passe par site", "Un gestionnaire de mots de passe", "La double authentification"]
DRAW = [ico_keys, ico_vault, ico_code]
SCENES = [s1, s2, s3, s4, reflex_trio(ITEMS, 0, DRAW), reflex_trio(ITEMS, 1, DRAW), reflex_trio(ITEMS, 2, DRAW), outro(0)]
SUBS = [True] * 7 + [False]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS)
