"""Short #010 — Les faux sites de promo (Black Friday) : la vitrine en carton."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Une promo à moins 80 % ? Attention, c'est peut-être un faux site.",
    "Pendant le Black Friday, des escrocs créent de fausses boutiques, avec des prix trop beaux pour être vrais.",
    "C'est comme une vitrine en carton : belle de l'extérieur, mais vide derrière.",
    "Leur adresse imite parfois une vraie marque, avec juste une lettre changée.",
    "Tu paies, le colis n'arrive jamais, et tes coordonnées bancaires sont entre leurs mains.",
    "Trois réflexes. Un : tape le nom du site suivi du mot arnaque dans un moteur de recherche.",
    "Deux : lis les mentions légales. Pas de société ni d'adresse ? Passe ton chemin.",
    "Trois : privilégie un paiement sécurisé, comme la carte bancaire, plutôt qu'un virement.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
VOICE[0] = "Une promo à moins quatre-vingts pour cent ? Attention, c'est peut-être un faux site."
ITEMS = ["Cherche « nom du site + arnaque »", "Lis les mentions légales", "Paie par carte, pas par virement"]


def product_card(img, cx, cy, s, price, old, k=1.0, accent=RED):
    if k <= 0:
        return
    sc = s * (0.75 + 0.25 * back_out(k))
    w, h = 300 * sc, 400 * sc
    a = int(255 * clamp(k * 1.5))
    dr = D(img)
    dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(26 * sc), fill=(26, 35, 56, a))
    # mini téléphone en guise de produit
    dr.rounded_rectangle([cx - 55 * sc, cy - h / 2 + 35 * sc, cx + 55 * sc, cy - h / 2 + 215 * sc], radius=int(16 * sc),
                         fill=(60, 75, 100, a), outline=CYAN + (a,), width=3)
    dr.text((cx, cy + 70 * sc), old, font=font(int(36 * sc), "SemiBold"), fill=GREY + (a,), anchor="mm")
    ow = font(int(36 * sc), "SemiBold").getlength(old)
    dr.line([cx - ow / 2, cy + 70 * sc, cx + ow / 2, cy + 70 * sc], fill=GREY + (a,), width=3)
    dr.text((cx, cy + 135 * sc), price, font=font(int(60 * sc), "Black"), fill=accent + (a,), anchor="mm")


def badge(img, cx, cy, txt, t, start, r=110):
    k = back_out(prog(t, start, 0.4))
    if k <= 0:
        return
    rr = r * k * (1 + 0.06 * math.sin(t * 8))
    glow(img, [cx - rr, cy - rr, cx + rr, cy + rr], RED, 40, 70)
    dr = D(img)
    dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=RED + (255,))
    dr.text((cx, cy), txt, font=font(int(64 * k), "Black"), fill=WHITE + (255,), anchor="mm")


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1010, 0.95, tilt_y=int(60 * (1 - ease_out(prog(t, 0, 0.5)))))
    dr = D(img)
    dr.rectangle([sx0, sy0 + 50, sx1, sy0 + 150], fill=(22, 30, 50, 255))
    dr.text(((sx0 + sx1) / 2, sy0 + 100), "BLACK FRIDAY", font=font(44, "Black"), fill=WHITE + (255,), anchor="mm")
    product_card(img, (sx0 + sx1) / 2, sy0 + 480, 1.1, "199 €", "999 €", prog(t, 0.15, 0.4))
    badge(img, sx1 - 60, sy0 + 260, "-80%", t, 0.5)
    # compte à rebours qui défile
    rem = max(0, 179 - int(t * 7))
    ck = prog(t, 0.8, 0.3)
    if ck > 0:
        dr = D(img)
        dr.rounded_rectangle([sx0 + 40, sy1 - 190, sx1 - 40, sy1 - 90], radius=24, fill=(60, 20, 30, int(255 * ck)))
        dr.text(((sx0 + sx1) / 2, sy1 - 140), f"Fin dans 0{rem // 60}:{rem % 60:02d}", font=font(46, "ExtraBold"),
                fill=RED + (int(255 * ck),), anchor="mm")
    glitch_text(img, W / 2, 290, "-80 % ? Méfie-toi", 104, RED, t, d * 0.4)


def s2(img, t, d):
    box = [70, 560, W - 70, 1380]
    zx0, zy0, zx1, zy1 = window(img, box, "promo-boutique.xyz", RED, ease_out(prog(t, 0, 0.4)))
    prices = [("49 €", "450 €"), ("19 €", "220 €"), ("89 €", "790 €")]
    for i, (p, o) in enumerate(prices):
        cx = zx0 + (zx1 - zx0) * (i + 0.5) / 3
        cy = (zy0 + zy1) / 2 + math.sin(t * 2.5 + i) * 10
        product_card(img, cx, cy, 0.85, p, o, prog(t, 0.35 + i * 0.3, 0.4))
    pop_text(img, W / 2, 330, "Une fausse boutique", 92, WHITE, t, 0.05)
    chip(img, W / 2, 1480, "Prix trop beaux pour être vrais", RED, prog(t, 1.5, 0.4), size=46)


def s3(img, t, d):
    pop_text(img, W / 2, 330, "Une vitrine en carton", 92, WHITE, t, 0.05)
    cx, cy = W / 2, 1000
    # la façade pivote : elle se révèle plate (épaisseur d'un carton)
    turn = ease_in_out(prog(t, d * 0.45, 0.9))
    fw = 640 * (1 - 0.93 * turn)
    dr = D(img)
    # derrière : vide
    if turn > 0.3:
        a = int(255 * (turn - 0.3) / 0.7)
        dr.rounded_rectangle([cx - 320, cy - 300, cx + 320, cy + 330], radius=20, outline=GREY + (a // 2,), width=4)
        dr.text((cx + 120, cy + 10), "rien", font=font(60, "Bold"), fill=GREY + (a,), anchor="mm")
    col = mix(CYAN, RED, turn)
    dr.rectangle([cx - fw / 2 - 160 * turn, cy - 300, cx + fw / 2 - 160 * turn, cy + 330], fill=(26, 35, 56, 255), outline=col + (255,), width=5)
    if fw > 200:
        ox = -160 * turn
        # store bandes de l'auvent
        for i in range(6):
            x0 = cx + ox - fw / 2 + i * fw / 6
            dr.rectangle([x0, cy - 300, x0 + fw / 6, cy - 200], fill=(RED if i % 2 else WHITE) + (255,))
        dr.rectangle([cx + ox - fw / 2 + 50, cy - 140, cx + ox + fw / 2 - 50, cy + 160], fill=(40, 60, 90, 255))
        dr.text((cx + ox, cy + 10), "SOLDES", font=font(int(80 * fw / 640), "Black"), fill=WHITE + (255,), anchor="mm")
        dr.text((cx + ox, cy + 250), "-80%", font=font(int(70 * fw / 640), "Black"), fill=RED + (255,), anchor="mm")
    chip(img, W / 2, 1450, "Vide derrière", RED, prog(t, d * 0.7, 0.4), size=50)


def s4(img, t, d):
    pop_text(img, W / 2, 330, "Une lettre changée", 92, WHITE, t, 0.05)
    k = ease_out(prog(t, 0.2, 0.4))
    dr = D(img)
    y = 860
    dr.rounded_rectangle([90 - (1 - k) * 600, y - 75, W - 90 - (1 - k) * 600, y + 75], radius=75, fill=(22, 30, 50, 255), outline=GREY + (255,), width=3)
    sw = ease_in_out(prog(t, 1.2, 0.5))
    f = font(64, "Bold")
    pre, good, bad, post = "grandemarq", "u", "v", "e.fr"
    total = f.getlength(pre + good + post)
    x = W / 2 - total / 2 - (1 - k) * 600
    dr.text((x, y), pre, font=f, fill=WHITE + (int(255 * k),), anchor="lm")
    x2 = x + f.getlength(pre)
    lw = f.getlength(good)
    if sw < 0.5:
        dr.text((x2, y - sw * 160), good, font=f, fill=CYAN + (int(255 * k * (1 - sw * 2)),), anchor="lm")
    else:
        dr.text((x2, y - (1 - sw) * 160), bad, font=f, fill=RED + (255,), anchor="lm")
        pulse = 0.5 + 0.5 * math.sin(t * 7)
        dr.ellipse([x2 - 18, y - 60, x2 + lw + 18, y + 60], outline=RED + (int(150 + 100 * pulse),), width=6)
    dr.text((x2 + lw, y), post, font=f, fill=WHITE + (int(255 * k),), anchor="lm")
    # vraie / fausse
    chip(img, W / 2 - 230, 1150, "Vraie : u", CYAN, prog(t, 0.6, 0.4), size=48)
    chip(img, W / 2 + 230, 1150, "Fausse : v", RED, prog(t, 1.7, 0.4), size=48)


def s5(img, t, d):
    person(img, 230, 820, 1.1, CYAN)
    hacker(img, W - 230, 860 + math.sin(t * 3) * 10, 1.1)
    k = ease_in_out(prog(t, 0.3, 1.0))
    if k > 0:  # la carte part chez l'escroc et se pose à côté de lui
        x = 230 + (W - 680) * k
        credit_card(img, x, 640 - math.sin(k * math.pi) * 140, 0.45, 15 * math.sin(t * 4))
    # colis barré
    ck = prog(t, 1.5, 0.4)
    if ck > 0:
        dr = D(img)
        bx, by = W / 2, 1150
        dr.rectangle([bx - 100, by - 80, bx + 100, by + 80], fill=(120, 90, 60, int(255 * ck)))
        dr.line([bx, by - 80, bx, by + 80], fill=(80, 60, 40, int(255 * ck)), width=8)
        cross(img, bx, by, 120, RED, ck)
    pop_text(img, W / 2, 330, "Pas de colis", 96, RED, t, 0.05)
    chip(img, W / 2, 1420, "Tes données bancaires", RED, prog(t, 2.0, 0.4), size=50)


SCENES = [s1, s2, s3, s4, s5,
          reflex_checklist(ITEMS, 0), reflex_checklist(ITEMS, 1), reflex_checklist(ITEMS, 2), outro(0)]
SUBS = [True] * 8 + [False]
MUSIC = None  # pas de musique de fond (décision de Néo, 19/11/2026)
# Uniquement le pop discret, rien sur les réflexes (décision de Néo, 19/11/2026)
SFX = [
    (0, 0.5, 'pop', 0.5),   # badge -80 %
    (3, 1.2, 'pop', 0.4),   # la lettre change
    (4, 1.5, 'pop', 0.4),   # colis barré
    (8, 0.6, 'pop', 0.5),   # bouton S'ABONNER
]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS, sfx=SFX, music=MUSIC, final="short010.mp4")
