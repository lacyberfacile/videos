"""Short #012 — Les faux placements crypto : le distributeur peint sur le mur."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Une star te promet de devenir riche grâce à la crypto ? C'est sûrement une arnaque.",
    "Les escrocs utilisent de fausses vidéos, parfois créées par intelligence artificielle, et de faux articles de presse.",
    "Ils t'envoient sur une plateforme qui affiche des gains énormes, pour te pousser à investir encore plus.",
    "C'est comme un distributeur de billets peint sur un mur : il affiche de l'argent, mais rien n'en sort.",
    "Quand tu veux retirer, on te réclame une fausse taxe pour débloquer ton argent. Et en général, il ne revient jamais.",
    "Trois réflexes. Un : un gros rendement, c'est un gros risque. Le placement miracle n'existe pas.",
    "Deux : vérifie la plateforme sur les listes de l'AMF, le gendarme des marchés financiers.",
    "Trois : ne paie jamais de frais pour récupérer ton argent. Et l'AMF ne t'appellera jamais pour ça.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
VOICE[6] = "Deux : vérifie la plateforme sur les listes de l'A M F, le gendarme des marchés financiers."
VOICE[7] = "Trois : ne paie jamais de frais pour récupérer ton argent. Et l'A M F ne t'appellera jamais pour ça."
ITEMS = ["Pas de placement miracle", "Vérifie sur le site de l'AMF", "Jamais de frais pour retirer"]


def bill(img, cx, cy, s, color, angle=0, alpha=255):
    w, h = int(260 * s), int(130 * s)
    if w < 4:
        return
    tile = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle([2, 2, w + 1, h + 1], radius=int(14 * s), fill=(30, 60, 50, alpha), outline=color + (alpha,), width=max(2, int(5 * s)))
    d.ellipse([w / 2 - h / 3, h / 2 - h / 3, w / 2 + h / 3, h / 2 + h / 3], outline=color + (alpha,), width=max(2, int(4 * s)))
    d.text((w / 2 + 2, h / 2 + 2), "€", font=font(int(60 * s), "Black"), fill=color + (alpha,), anchor="mm")
    tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2))) if img.mode == "RGBA" else \
        img.paste(tile, (int(cx - tile.width / 2), int(cy - tile.height / 2)), tile)


def star_person(img, cx, cy, s, alpha=255):
    gold = (234, 179, 8)
    person(img, cx, cy, s, gold, alpha)
    dr = D(img)
    for i in range(5):  # petites étoiles qui scintillent
        a = i * 1.25
        r = 170 * s
        x, y = cx + math.cos(a) * r, cy - 60 * s + math.sin(a) * r * 0.8
        dr.text((x, y), "✦", font=font(int(34 * s), "Black"), fill=gold + (alpha,), anchor="mm")


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1010, 0.95, tilt_y=int(60 * (1 - ease_out(prog(t, 0, 0.5)))))
    dr = D(img)
    vx0, vy0, vx1, vy1 = sx0 + 25, sy0 + 120, sx1 - 25, sy0 + 620
    dr.rounded_rectangle([vx0, vy0, vx1, vy1], radius=24, fill=(30, 40, 64, 255))
    star_person(img, (vx0 + vx1) / 2, vy0 + 330, 1.3 * ease_out(prog(t, 0.1, 0.4)) + 0.01)
    dr = D(img)
    dr.text((vx0 + 30, vy0 + 40), "Publicité", font=font(30, "SemiBold"), fill=GREY + (255,), anchor="lm")
    k = back_out(prog(t, 0.5, 0.4))
    if k > 0:
        y = vy1 + 40
        dr.rounded_rectangle([sx0 + 30, y, sx1 - 30, y + 150], radius=26, fill=(40, 52, 78, 255), outline=RED + (255,), width=3)
        dr.text(((sx0 + sx1) / 2, y + 50), "Mon secret pour", font=font(38, "Bold"), fill=WHITE + (int(255 * k),), anchor="mm")
        dr.text(((sx0 + sx1) / 2, y + 105), "devenir riche", font=font(44, "Black"), fill=RED + (int(255 * k),), anchor="mm")
    glitch_text(img, W / 2, 290, "Riche grâce à la crypto ?", 92, RED, t, d * 0.4)


def s2(img, t, d):
    pop_text(img, W / 2, 330, "Vidéos et articles bidon", 86, WHITE, t, 0.05)
    # vidéo truquée
    k = ease_out(prog(t, 0.1, 0.4))
    box = [90, 520, 600, 900]
    zx0, zy0, zx1, zy1 = window(img, box, "vidéo", RED, k)
    star_person(img, (zx0 + zx1) / 2, zy1 - 60, 0.9, alpha=int(255 * k))
    chip(img, 520, 560 + math.sin(t * 4) * 6, "IA", RED, prog(t, 0.7, 0.35), size=52)
    # faux article
    ak = ease_out(prog(t, 0.9, 0.4))
    if ak > 0:
        dr = D(img)
        x0 = 470 + (1 - ak) * 400
        dr.rounded_rectangle([x0, 960, x0 + 520, 1380], radius=18, fill=(225, 228, 235, int(255 * ak)))
        dr.text((x0 + 30, 1010), "LE JOURNAL", font=font(40, "Black"), fill=DARK + (int(255 * ak),), anchor="lm")
        for i in range(6):
            dr.rounded_rectangle([x0 + 30, 1070 + i * 46, x0 + 490 - (i % 3) * 60, 1090 + i * 46], radius=8, fill=(150, 155, 170, int(255 * ak)))
    stamp(img, 730, 1170, "FAUX", RED, t, 1.6, size=130)


def s3(img, t, d):
    box = [70, 560, W - 70, 1360]
    zx0, zy0, zx1, zy1 = window(img, box, "super-crypto.xyz", RED, ease_out(prog(t, 0, 0.4)))
    k = prog(t, 0.3, d * 0.7)
    pts = []
    n = 40
    for i in range(int(n * k) + 1):
        u = i / n
        x = zx0 + 60 + (zx1 - zx0 - 120) * u
        y = zy1 - 60 - (zy1 - zy0 - 220) * (u ** 2) + math.sin(u * 20) * 12
        pts.append((x, y))
    if len(pts) > 1:
        D(img).line(pts, fill=CYAN + (255,), width=10, joint="curve")
        glow(img, [pts[-1][0] - 30, pts[-1][1] - 30, pts[-1][0] + 30, pts[-1][1] + 30], CYAN, 30, 90)
    counter(img, (zx0 + zx1) / 2, zy0 + 90, 340, 90, CYAN, t, 0.3, dur=d * 0.6, prefix="+ ", suffix=" %")
    pop_text(img, W / 2, 330, "Des gains énormes…", 92, WHITE, t, 0.05)
    chip(img, W / 2, 1460, "…mais affichés seulement", RED, prog(t, d * 0.65, 0.4), size=48)


def s4(img, t, d):
    pop_text(img, W / 2, 330, "Un distributeur peint", 92, WHITE, t, 0.05)
    dr = D(img)
    # mur de briques
    for r in range(11):
        y = 560 + r * 80
        off = 0 if r % 2 else 90
        for c in range(-1, 7):
            x = 90 + off + c * 180
            if min(W - 70, x + 170) > max(70, x):
                dr.rectangle([max(70, x), y, min(W - 70, x + 170), y + 70], fill=(55, 40, 45, 255))
    # le distributeur (peint) qui « respire »
    cx, cy = W / 2, 1000
    dr.rounded_rectangle([cx - 260, cy - 340, cx + 260, cy + 320], radius=26, fill=(40, 52, 78, 255), outline=CYAN + (255,), width=5)
    dr.rounded_rectangle([cx - 190, cy - 270, cx + 190, cy - 60], radius=14, fill=(14, 20, 34, 255))
    blink = 0.6 + 0.4 * math.sin(t * 5)
    dr.text((cx, cy - 165), "5 000 €", font=font(80, "Black"), fill=CYAN + (int(255 * blink),), anchor="mm")
    for i in range(3):
        for j in range(3):
            dr.rounded_rectangle([cx - 160 + j * 110, cy - 20 + i * 70, cx - 80 + j * 110, cy + 30 + i * 70], radius=8, fill=(70, 85, 115, 255))
    dr.rounded_rectangle([cx - 170, cy + 230, cx + 170, cy + 260], radius=10, fill=(10, 14, 24, 255))
    # rien ne sort : le billet tente de sortir puis disparaît
    ph = (t * 0.8) % 1
    if ph < 0.6:
        bill(img, cx, cy + 245 + ph * 60, 0.6, GREEN, alpha=int(255 * (1 - ph / 0.6)))
    chip(img, W / 2, 1460, "Rien n'en sort", RED, prog(t, d * 0.6, 0.4), size=54)


def s5(img, t, d):
    box = [90, 560, W - 90, 1240]
    zx0, zy0, zx1, zy1 = window(img, box, "Retrait", RED, ease_out(prog(t, 0, 0.4)))
    dr = D(img)
    cx = (zx0 + zx1) / 2
    padlock(img, cx, zy0 + 190, 1.0, RED, open_k=0.0)
    ok = prog(t, 0.6, 0.4)
    if ok > 0:
        dr = D(img)
        dr.text((cx, zy0 + 390), "Retrait bloqué", font=font(64, "Black"), fill=RED + (int(255 * ok),), anchor="mm")
        dr.text((cx, zy0 + 480), "Taxe à payer : 1 500 €", font=font(50, "Bold"), fill=WHITE + (int(255 * ok),), anchor="mm")
    # les billets s'envolent
    for i in range(3):
        k = prog(t, 1.4 + i * 0.35, 1.2)
        if 0 < k < 1:
            bill(img, 250 + i * 290 + math.sin(t * 3 + i) * 30, 1380 - k * 900, 0.55, RED, angle=20 * math.sin(t * 4 + i), alpha=int(255 * (1 - k)))
    pop_text(img, W / 2, 330, "Une fausse taxe", 96, RED, t, 0.05)


def d_chart(img, cx, cy, s, col):
    dr = D(img)
    pts = [(cx - 80 * s, cy + 50 * s), (cx - 20 * s, cy), (cx + 20 * s, cy + 30 * s), (cx + 80 * s, cy - 60 * s)]
    dr.line(pts, fill=col + (255,), width=int(12 * s), joint="curve")
    glyph(dr, cx + 60 * s, cy + 50 * s, "!", int(60 * s), col)


def d_list(img, cx, cy, s, col):
    dr = D(img)
    for i in range(3):
        y = cy - 50 * s + i * 50 * s
        dr.rounded_rectangle([cx - 70 * s, y - 10 * s, cx + 40 * s, y + 10 * s], radius=6, fill=col + (255,))
    dr.ellipse([cx + 10 * s, cy + 10 * s, cx + 80 * s, cy + 80 * s], outline=col + (255,), width=int(9 * s))


def d_nofee(img, cx, cy, s, col):
    dr = D(img)
    dr.text((cx, cy), "€", font=font(int(110 * s), "Black"), fill=col + (255,), anchor="mm")
    dr.line([cx - 70 * s, cy + 70 * s, cx + 70 * s, cy - 70 * s], fill=col + (255,), width=int(12 * s))


DRAWERS = [d_chart, d_list, d_nofee]
SCENES = [s1, s2, s3, s4, s5,
          reflex_trio(ITEMS, 0, DRAWERS), reflex_trio(ITEMS, 1, DRAWERS), reflex_trio(ITEMS, 2, DRAWERS), outro(1)]
SUBS = [True] * 8 + [False]
MUSIC = None  # pas de musique de fond (décision de Néo, 19/11/2026)
# Uniquement le pop discret, rien sur les réflexes (décision de Néo, 19/11/2026)
SFX = [
    (0, 0.5, 'pop', 0.5),   # bulle « mon secret »
    (2, 0.3, 'pop', 0.4),   # compteur de gains
    (4, 0.6, 'pop', 0.4),   # « Retrait bloqué »
    (8, 0.6, 'pop', 0.5),   # bouton S'ABONNER
]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS, sfx=SFX, music=MUSIC, final="short012.mp4")
