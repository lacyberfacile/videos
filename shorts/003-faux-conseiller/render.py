"""Short #003 — Le faux conseiller bancaire (numéro usurpé)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Ta banque t'appelle, et c'est bien son numéro qui s'affiche. Pourtant, c'est un escroc.",
    "Le numéro affiché peut être falsifié. Comme une fausse adresse d'expéditeur au dos d'une enveloppe.",
    "Il connaît déjà ton nom, ta banque, parfois ton numéro de compte, grâce à des fuites de données.",
    "Il t'annonce une opération suspecte, et te demande de valider quelque chose en urgence pour la bloquer.",
    "En réalité, c'est son opération à lui que tu valides.",
    "Trois réflexes. Un : ne donne jamais un code reçu par SMS.",
    "Deux : ne valide jamais une opération que tu n'as pas faite toi-même.",
    "Trois : raccroche, et rappelle ta banque au numéro habituel.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1000, 0.95)
    dr = D(img)
    cx = (sx0 + sx1) / 2
    for i in range(3):
        ph = ((t * 1.2) + i / 3) % 1
        r = 100 + ph * 160
        dr.ellipse([cx - r, sy0 + 330 - r, cx + r, sy0 + 330 + r], outline=GREEN + (int(200 * (1 - ph)),), width=6)
    rev = ease_out(prog(t, d * 0.6, 0.35))
    if rev < 1:
        dr.ellipse([cx - 100, sy0 + 230, cx + 100, sy0 + 430], fill=CYAN + (int(255 * (1 - rev)),))
        dr.text((cx, sy0 + 330), "MB", font=font(80, "Black"), fill=DARK + (int(255 * (1 - rev)),), anchor="mm")
    if rev > 0:
        hacker(img, cx, sy0 + 380, 0.75, int(255 * rev))
    dr = D(img)
    dr.text((cx, sy0 + 520), "Ma Banque", font=font(58, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    dr.text((cx, sy0 + 590), "01 23 45 67 89", font=font(40, "Medium"), fill=GREY + (255,), anchor="mm")
    # bouton décrocher qui sautille
    by = sy1 - 150 + abs(math.sin(t * 6)) * -12
    dr.ellipse([cx - 70, by - 70, cx + 70, by + 70], fill=GREEN + (255,))
    glyph(dr, cx, by + 4, "☎", 80, WHITE)
    glitch_text(img, W / 2, 300, "C'est ta banque ?", 96, WHITE, t, 0.0)
    stamp(img, W / 2, 1000, "ESCROC", RED, t, d * 0.7, size=130)


def s2(img, t, d):
    dr = D(img)
    k = back_out(prog(t, 0, 0.45))
    w, h = 820 * k, 520 * k
    cx, cy = W / 2, 900
    if w > 10:
        dr.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=(235, 228, 210, 255))
        dr.line([(cx - w / 2, cy - h / 2), (cx, cy + 20 * k), (cx + w / 2, cy - h / 2)], fill=(190, 180, 160, 255), width=6)
    if k > 0.9:
        lk = ease_out(prog(t, 0.4, 0.4))
        lx, ly = cx - 360, cy + 90
        dr.text((lx, ly), "Expéditeur :", font=font(40, "SemiBold"), fill=(90, 90, 100, 255))
        txt = "Ma Banque"[: int(9 * clamp((t - 0.5) / 0.6))]
        dr.text((lx, ly + 60), txt, font=font(60, "ExtraBold"), fill=DARK + (255,))
        # l'étiquette se décolle et révèle le vrai expéditeur
        pk = ease_out(prog(t, d * 0.55, 0.5))
        if pk > 0:
            dr.rounded_rectangle([lx - 20, ly + 50, lx + 420, ly + 140], radius=10, fill=(235, 228, 210, int(255 * pk)))
            dr.text((lx, ly + 60), "??? inconnu", font=font(60, "ExtraBold"), fill=RED + (int(255 * pk),))
    pop_text(img, W / 2, 300, "Numéro falsifié", 96, RED, t, 0.1)
    chip(img, W / 2, 1360, "On peut afficher n'importe quel numéro", RED, prog(t, d * 0.4, 0.4), 40)


def s3(img, t, d):
    hacker(img, W / 2, 1180, 1.1)
    dr = D(img)
    # dossier
    dr.rounded_rectangle([W / 2 - 300, 1260, W / 2 + 300, 1520], radius=24, fill=(234, 179, 8, 255))
    dr.rounded_rectangle([W / 2 - 300, 1230, W / 2 - 80, 1280], radius=14, fill=(234, 179, 8, 255))
    D(img).text((W / 2, 1400), "TON DOSSIER", font=font(56, "Black"), fill=DARK + (255,), anchor="mm")
    infos = ["Ton nom", "Ta banque", "N° de compte"]
    for i, s in enumerate(infos):
        k = prog(t, 0.3 + i * 0.5, 0.6)
        if k <= 0:
            continue
        sx, sy = 180 + i * 360, 560
        x = sx + (W / 2 - sx) * ease_in_out(clamp((k - 0.5) * 2))
        y = sy + (1330 - sy) * ease_in_out(clamp((k - 0.5) * 2))
        if k < 1:
            chip(img, x, y, s, CYAN, min(1, k * 2), 42)
    pop_text(img, W / 2, 300, "Il sait déjà tout", 92, WHITE, t, 0.05)
    chip(img, W / 2, 440, "Fuites de données", RED, prog(t, d * 0.5, 0.4), 48)


def s4(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1020, 0.95)
    dr = D(img)
    cx = (sx0 + sx1) / 2
    k = back_out(prog(t, 0.1, 0.4))
    if k > 0:
        dr.rounded_rectangle([sx0 + 30, sy0 + 180, sx1 - 30, sy0 + 420], radius=26, fill=(60, 20, 26, 255), outline=RED + (255,), width=5)
        dr.text((cx, sy0 + 240), "Opération suspecte", font=font(40, "ExtraBold"), fill=RED + (255,), anchor="mm")
        dr.text((cx, sy0 + 330), "- 980,00 €", font=font(72, "Black"), fill=WHITE + (255,), anchor="mm")
    # compte à rebours
    left = max(0, 60 - int((t - 0.5) * 12)) if t > 0.5 else 60
    tk = prog(t, 0.6, 0.3)
    if tk > 0:
        r = 110
        ang = 360 * (left / 60)
        dr.ellipse([cx - r, sy0 + 470, cx + r, sy0 + 470 + 2 * r], outline=(60, 75, 100, 255), width=12)
        dr.arc([cx - r, sy0 + 470, cx + r, sy0 + 470 + 2 * r], -90, -90 + ang, fill=RED + (255,), width=12)
        dr.text((cx, sy0 + 470 + r), f"0:{left:02d}", font=font(54, "Black"), fill=WHITE + (255,), anchor="mm")
    bk = back_out(prog(t, d * 0.45, 0.4))
    if bk > 0:
        pulse = 1 + 0.05 * math.sin(t * 9)
        bw, bh = 380 * bk * pulse, 110 * bk * pulse
        by = sy1 - 140
        dr.rounded_rectangle([cx - bw / 2, by - bh / 2, cx + bw / 2, by + bh / 2], radius=55, fill=GREEN + (255,))
        if bk > 0.8:
            dr.text((cx, by), "VALIDER", font=font(50, "Black"), fill=DARK + (255,), anchor="mm")
    pop_text(img, W / 2, 300, "Vite, il faut bloquer !", 84, WHITE, t, 0.05)


def s5(img, t, d):
    dr = D(img)
    # compte de la victime (gauche) -> escroc (droite)
    dr.rounded_rectangle([90, 700, 470, 1000], radius=30, fill=(22, 30, 50, 255), outline=CYAN + (255,), width=5)
    D(img).text((280, 760), "Ton compte", font=font(40, "Bold"), fill=GREY + (255,), anchor="mm")
    bal = 2450 - int(980 * ease_in_out(prog(t, 0.3, d * 0.6)))
    D(img).text((280, 880), f"{bal:,} €".replace(",", " "), font=font(70, "Black"), fill=WHITE + (255,), anchor="mm")
    hacker(img, 800, 900, 0.9)
    for i in range(6):
        ph = (t * 0.9 + i / 6) % 1
        if t < 0.3:
            break
        x = 470 + (690 - 470) * ph
        y = 850 - math.sin(ph * math.pi) * 160
        dr = D(img)
        dr.ellipse([x - 34, y - 34, x + 34, y + 34], fill=(234, 179, 8, 255))
        dr.text((x, y), "€", font=font(44, "Black"), fill=DARK + (255,), anchor="mm")
    pop_text(img, W / 2, 330, "Tu valides…", 92, WHITE, t, 0.05)
    pop_text(img, W / 2, 450, "son opération à lui", 80, RED, t, d * 0.35)


ITEMS = ["Ne donne jamais un code reçu par SMS", "Ne valide rien que tu n'as pas fait", "Raccroche et rappelle ta banque"]
SCENES = [s1, s2, s3, s4, s5, reflex_bigslide(ITEMS, 0), reflex_bigslide(ITEMS, 1), reflex_bigslide(ITEMS, 2), outro(1)]
SUBS = [True] * 8 + [False]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS)
