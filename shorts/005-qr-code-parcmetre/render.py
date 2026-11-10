"""Short #005 — Le faux QR code sur le parcmètre (quishing)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Tu scannes le QR code du parcmètre ? Regarde d'abord s'il n'a pas été collé par-dessus.",
    "Des escrocs collent leur propre QR code sur le vrai. Un simple autocollant.",
    "Il t'envoie vers un faux site de paiement, presque identique à l'officiel.",
    "Tu crois payer ton stationnement… et tu donnes ta carte bancaire à l'escroc.",
    "Trois réflexes. Un : touche le QR code. Si c'est un autocollant, méfiance.",
    "Deux : paie plutôt avec l'appli officielle de stationnement, ou directement à la machine.",
    "Trois : avant de payer, vérifie l'adresse du site qui s'ouvre.",
    "Déjà payé sur un faux site ? Fais opposition sur ta carte, tout de suite.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)


def meter(img, cx, cy, s=1.0):
    dr = D(img)
    dr.rounded_rectangle([cx - 60 * s, cy + 300 * s, cx + 60 * s, cy + 700 * s], radius=10, fill=(40, 52, 76, 255))
    dr.rounded_rectangle([cx - 230 * s, cy - 380 * s, cx + 230 * s, cy + 320 * s], radius=int(40 * s), fill=(30, 40, 62, 255), outline=(70, 90, 120, 255), width=6)
    dr.rounded_rectangle([cx - 170 * s, cy - 320 * s, cx + 170 * s, cy - 190 * s], radius=14, fill=(10, 40, 50, 255))
    dr.text((cx, cy - 255 * s), "P  2,40 €/h", font=font(int(44 * s), "Bold"), fill=CYAN + (255,), anchor="mm")
    dr.text((cx, cy + 260 * s), "Scannez pour payer", font=font(int(30 * s), "Medium"), fill=GREY + (255,), anchor="mm")
    return (cx - 120 * s, cy - 140 * s, 240 * s)  # x, y, taille du QR


def s1(img, t, d):
    qx, qy, qs = meter(img, W / 2, 980)
    qr(img, qx, qy, qs, 1)
    # viseur de caméra qui se resserre
    k = ease_out(prog(t, 0.2, 0.6))
    m = 160 - 120 * k
    dr = D(img)
    x0, y0, x1, y1 = qx - m, qy - m, qx + qs + m, qy + qs + m
    L = 60
    for (x, y, sx, sy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        dr.line([x, y, x + L * sx, y], fill=WHITE + (255,), width=10)
        dr.line([x, y, x, y + L * sy], fill=WHITE + (255,), width=10)
    if t > d * 0.5:
        sy = qy + (qs * ((t * 1.5) % 1))
        dr.line([qx - 20, sy, qx + qs + 20, sy], fill=RED + (200,), width=6)
    glitch_text(img, W / 2, 300, "Ce QR code ?", 104, WHITE, t, 0.0)
    pop_text(img, W / 2, 430, "Regarde avant de scanner", 64, CYAN, t, d * 0.45)


def s2(img, t, d):
    qx, qy, qs = meter(img, W / 2, 980)
    qr(img, qx, qy, qs, 1)
    k = ease_out(prog(t, 0.3, 0.7))
    # autocollant qui glisse depuis la droite et se pose
    sx = qx + (1 - k) * 700
    sy = qy - 10 + (1 - k) * -200
    ang = (1 - k) * 25
    layer = Image.new("RGBA", (int(qs + 60), int(qs + 60)), (0, 0, 0, 0))
    qr(layer, 30, 30, qs, 7, color=(60, 10, 14))
    ld = ImageDraw.Draw(layer)
    ld.polygon([(qs + 60, qs + 60), (qs + 60, qs - 10), (qs - 10, qs + 60)], fill=(200, 200, 200, 255))  # coin décollé
    layer = layer.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(sx - 30 - (layer.width - qs - 60) / 2), int(sy - 30 - (layer.height - qs - 60) / 2)), layer)
    pop_text(img, W / 2, 300, "Un autocollant", 100, RED, t, 0.1)
    if k >= 1:
        arrow(img, (qx + qs + 250, qy + qs + 180), (qx + qs + 50, qy + qs + 40), RED, ease_out(prog(t, d * 0.55, 0.3)), 10)
        chip(img, W / 2, 1580 - 120, "collé par-dessus le vrai", RED, prog(t, d * 0.55, 0.4), 46)


def site(img, box, url, col, k):
    inner = window(img, box, "", col, k)
    if k < 0.6:
        return
    dr = D(img)
    x0, y0, x1, y1 = inner
    dr.rounded_rectangle([x0 + 20, y0 - 62, x1 - 20, y0 - 14], radius=20, fill=(14, 20, 34, 255))
    dr.text((x0 + 45, y0 - 38), url, font=font(28, "SemiBold"), fill=col + (255,), anchor="lm")
    dr.text(((x0 + x1) / 2, y0 + 70), "Paiement stationnement", font=font(34, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    for j in range(3):
        dr.rounded_rectangle([x0 + 40, y0 + 130 + j * 85, x1 - 40, y0 + 190 + j * 85], radius=12, fill=(40, 52, 76, 255))
    dr.rounded_rectangle([x0 + 40, y1 - 100, x1 - 40, y1 - 35], radius=30, fill=col + (255,))
    dr.text(((x0 + x1) / 2, y1 - 67), "Payer", font=font(34, "Black"), fill=DARK + (255,), anchor="mm")


def s3(img, t, d):
    site(img, [70, 620, 520, 1250], "ville.fr/parking", GREEN, ease_out(prog(t, 0.1, 0.4)))
    site(img, [560, 620, 1010, 1250], "parking-ville.top", RED, ease_out(prog(t, 0.45, 0.4)))
    chip(img, 295, 1340, "officiel", GREEN, prog(t, d * 0.5, 0.3), 44)
    chip(img, 785, 1340, "faux", RED, prog(t, d * 0.55, 0.3), 44)
    pop_text(img, W / 2, 300, "Presque identique", 96, WHITE, t, 0.05)


def s4(img, t, d):
    dr = D(img)
    k = back_out(prog(t, 0.05, 0.4))
    if k > 0:
        dr.rounded_rectangle([W / 2 - 380 * k, 560 - 110 * k, W / 2 + 380 * k, 560 + 110 * k], radius=30, fill=(24, 33, 54, 255), outline=CYAN + (255,), width=5)
        if k > 0.8:
            dr.text((W / 2, 525), "Stationnement 2 h", font=font(42, "SemiBold"), fill=GREY + (255,), anchor="mm")
            dr.text((W / 2, 600), "4,80 €", font=font(70, "Black"), fill=WHITE + (255,), anchor="mm")
    ck = prog(t, d * 0.35, d * 0.5)
    x = W / 2 + 320 * ease_in_out(ck)
    credit_card(img, x, 1000, 1.0 - 0.6 * ease_in_out(ck), angle=-15 * ck)
    if ck > 0:
        hacker(img, 900, 1300, 0.9, int(255 * clamp(ck * 2)))
    pop_text(img, W / 2, 300, "Ta carte, à l'escroc", 88, RED, t, d * 0.4)


def ico_touch(img, cx, cy, s, col):
    qr(img, cx - 70 * s, cy - 70 * s, 140 * s, 3, color=col, bg=(30, 40, 62))
    D(img).ellipse([cx + 20 * s, cy + 20 * s, cx + 90 * s, cy + 90 * s], fill=WHITE + (230,))


def ico_app(img, cx, cy, s, col):
    dr = D(img)
    dr.rounded_rectangle([cx - 60 * s, cy - 100 * s, cx + 60 * s, cy + 100 * s], radius=int(18 * s), outline=col + (255,), width=int(8 * s))
    dr.text((cx, cy), "P", font=font(int(90 * s), "Black"), fill=col + (255,), anchor="mm")


def ico_url(img, cx, cy, s, col):
    dr = D(img)
    dr.rounded_rectangle([cx - 110 * s, cy - 40 * s, cx + 110 * s, cy + 40 * s], radius=int(40 * s), outline=col + (255,), width=int(7 * s))
    padlock(img, cx - 65 * s, cy + 5 * s, 0.18 * s, col)
    dr.line([cx - 25 * s, cy, cx + 80 * s, cy], fill=col + (255,), width=int(8 * s))


def s8(img, t, d):
    pop_text(img, W / 2, 300, "Déjà payé ?", 100, RED, t, 0.05)
    credit_card(img, W / 2, 900, 1.3, angle=math.sin(t * 3) * 4)
    stamp(img, W / 2, 920, "OPPOSITION", GREEN, t, d * 0.35, size=100, angle=-10)
    pop_text(img, W / 2, 1300, "tout de suite", 80, WHITE, t, d * 0.5)


ITEMS = ["Touche le QR code", "Appli officielle ou machine", "Vérifie l'adresse du site"]
DRAW = [ico_touch, ico_app, ico_url]
SCENES = [s1, s2, s3, s4, reflex_trio(ITEMS, 0, DRAW), reflex_trio(ITEMS, 1, DRAW), reflex_trio(ITEMS, 2, DRAW), s8, outro(2)]
SUBS = [True] * 8 + [False]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS)
