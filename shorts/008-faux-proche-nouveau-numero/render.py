"""Short #008 — L'arnaque au faux proche (« Coucou maman, j'ai changé de numéro »)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Coucou maman, j'ai cassé mon téléphone, voici mon nouveau numéro. Si tu reçois ça, méfie-toi.",
    "Ce n'est pas ton enfant. C'est un escroc qui envoie ce message en masse, en espérant tomber sur un parent.",
    "C'est comme quelqu'un qui frappe à ta porte en criant : c'est moi, ouvre ! Sans jamais montrer son visage.",
    "Très vite, il invente une urgence : une facture à payer, un téléphone à racheter. Et il demande un virement.",
    "Et il a toujours une excuse pour ne pas t'appeler : micro cassé, plus de crédit.",
    "Trois réflexes. Un : appelle ton proche sur son numéro habituel, celui que tu connais.",
    "Deux : ne réponds pas au message suspect.",
    "Trois : n'envoie jamais d'argent sur un simple message, même si c'est urgent.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
ITEMS = ["Appelle son numéro habituel", "Ne réponds pas au message", "Jamais d'argent sur un message"]


def sms(img, x, y, lines, t, start, color=(38, 48, 70), size=36):
    k = ease_out(prog(t, start, 0.35))
    if k <= 0:
        return
    f = font(size, "Medium")
    bw = int(max(f.getlength(l) for l in lines)) + 56
    bh = int(size * 1.4) * len(lines) + 34
    dx = (1 - k) * -140
    a = int(255 * k)
    dr = D(img)
    dr.rounded_rectangle([x + dx, y, x + dx + bw, y + bh], radius=30, fill=color + (a,))
    for i, l in enumerate(lines):
        dr.text((x + dx + 28, y + 17 + int(size * 1.4) * i), l, font=f, fill=WHITE + (a,))


def door(img, cx, cy, s, knock):
    dr = D(img)
    w, h = 380 * s, 700 * s
    shake = math.sin(knock * 60) * 6 if knock > 0 else 0
    x0 = cx - w / 2 + shake
    dr.rectangle([x0 - 30, cy - h / 2 - 30, x0 + w + 30, cy + h / 2], fill=(30, 40, 62, 255))
    dr.rectangle([x0, cy - h / 2, x0 + w, cy + h / 2], fill=(70, 50, 40, 255), outline=(110, 80, 60, 255), width=6)
    for yy in (cy - h / 4, cy + h / 6):
        dr.rounded_rectangle([x0 + 40, yy - 110 * s, x0 + w - 40, yy + 90 * s], radius=10, outline=(110, 80, 60, 255), width=5)
    dr.ellipse([x0 + w - 70, cy - 15, x0 + w - 40, cy + 15], fill=(230, 190, 90, 255))


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1010, 0.95, tilt_y=int(50 * (1 - ease_out(prog(t, 0, 0.5)))))
    dr = D(img)
    dr.text(((sx0 + sx1) / 2, sy0 + 115), "06 •• •• •• ••", font=font(40, "Bold"), fill=WHITE + (255,), anchor="mm")
    dr.text(((sx0 + sx1) / 2, sy0 + 165), "Numéro inconnu", font=font(28, "Medium"), fill=GREY + (255,), anchor="mm")
    sms(img, sx0 + 30, sy0 + 240, ["Coucou maman, j'ai", "cassé mon téléphone"], t, 0.1)
    sms(img, sx0 + 30, sy0 + 400, ["Voici mon nouveau", "numéro, écris-moi ici"], t, 0.6)
    glitch_text(img, W / 2, 300, "« Coucou maman… »", 86, WHITE, t, 0.0)
    if t > d * 0.55:
        stamp(img, W / 2, 1300, "MÉFIANCE", RED, t, d * 0.55, size=120)


def s2(img, t, d):
    pop_text(img, W / 2, 330, "Envoyé en masse", 100, WHITE, t, 0.05)
    hacker(img, W / 2, 760, 0.9)
    for i in range(12):
        r, c = divmod(i, 4)
        cx, cy = 210 + c * 220, 1050 + r * 150
        k = prog(t, 0.4 + i * 0.12, 0.3)
        col = RED if k >= 1 else (60, 75, 100)
        dr = D(img)
        dr.rounded_rectangle([cx - 38, cy - 60, cx + 38, cy + 60], radius=14, fill=(22, 30, 50, 255), outline=col + (255,), width=4)
        if 0 < k < 1:
            envelope(img, W / 2 + (cx - W / 2) * k, 820 + (cy - 820) * k, 0.45, RED)
        if k >= 1 and i in (5, 10):
            glyph(dr, cx, cy, "?", 50, WHITE)


def s3(img, t, d):
    pop_text(img, W / 2, 330, "Sans montrer son visage", 76, WHITE, t, 0.05)
    knock = (t % 1.2) if t > 0.3 else 0
    door(img, W / 2 - 120, 1000, 1.0, knock if knock < 0.25 else 0)
    if knock < 0.25 and t > 0.3:
        dr = D(img)
        for i in range(3):
            r = 60 + i * 45 + knock * 200
            dr.arc([W / 2 + 90 - r, 900 - r, W / 2 + 90 + r, 900 + r], -40, 40, fill=GREY + (int(200 * (1 - knock * 4)),), width=6)
    k = back_out(prog(t, 0.5, 0.4))
    if k > 0:
        dr = D(img)
        bx, by = W / 2 + 230, 600
        dr.rounded_rectangle([bx - 230 * k, by - 80 * k, bx + 200 * k, by + 80 * k], radius=36, fill=(22, 30, 50, 255), outline=RED + (255,), width=5)
        if k > 0.8:
            dr.text((bx - 15, by), "C'est moi, ouvre !", font=font(44, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    sk = prog(t, 1.1, 0.4)
    if sk > 0:
        person(img, W / 2 + 330, 1220, 1.0, (60, 75, 100), int(255 * sk))
        glyph(D(img), W / 2 + 330, 1110, "?", int(80 * ease_out(sk)) + 1, RED)


def s4(img, t, d):
    pop_text(img, W / 2, 330, "L'urgence = le piège", 92, WHITE, t, 0.05)
    window(img, (120, 520, 960, 1060), "Message", RED, ease_out(prog(t, 0.1, 0.4)))
    if t > 0.4:
        dr = D(img)
        dr.text((W / 2, 700), "Facture à payer", font=font(56, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
        dr.text((W / 2, 790), "aujourd'hui !", font=font(48, "SemiBold"), fill=GREY + (255,), anchor="mm")
    counter(img, W / 2, 930, 650, 110, RED, t, 0.8, suffix=" €")
    # minuteur qui tourne
    dr = D(img)
    a = (t * 120) % 360
    dr.ellipse([W / 2 - 110, 1180, W / 2 + 110, 1400], outline=RED + (255,), width=10)
    dr.pieslice([W / 2 - 90, 1200, W / 2 + 90, 1380], -90, -90 + a, fill=RED + (120,))
    chip(img, W / 2, 1460, "Virement", RED, prog(t, 1.4, 0.4), size=46)


def s5(img, t, d):
    pop_text(img, W / 2, 330, "Jamais d'appel", 100, WHITE, t, 0.05)
    k = back_out(prog(t, 0.1, 0.4))
    r = 170 * k
    dr = D(img)
    if r > 1:
        dr.ellipse([W / 2 - r, 820 - r, W / 2 + r, 820 + r], fill=(22, 30, 50, 255), outline=GREY + (255,), width=6)
        glyph(dr, W / 2, 820, "☎", int(170 * k) + 1, WHITE)
    cross(img, W / 2, 820, 200, RED, prog(t, 0.6, 0.3), 26)
    chip(img, W / 2 - 200 + math.sin(t * 2) * 10, 1150, "Micro cassé", RED, prog(t, 1.0, 0.4), size=50)
    chip(img, W / 2 + 180 - math.sin(t * 2) * 10, 1310, "Plus de crédit", RED, prog(t, 1.6, 0.4), size=50)


SCENES = [s1, s2, s3, s4, s5,
          reflex_bigslide(ITEMS, 0), reflex_bigslide(ITEMS, 1), reflex_bigslide(ITEMS, 2), outro(2)]
SUBS = [True] * 8 + [False]
MUSIC = None  # pas de musique de fond (décision de Néo, 19/11/2026)
# (segment, offset s ou -fraction, son, gain)
# Uniquement le pop discret : pas de success, whoosh, stamp, alert, glitch, type (décision de Néo, 19/11/2026)
SFX = [
    (0, 0.1, 'pop', 0.5),
    (0, 0.6, 'pop', 0.4),
    (1, 0.4, 'pop', 0.35),
    (2, 0.5, 'pop', 0.45),
    (8, 0.6, 'pop', 0.5),
]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS, sfx=SFX, music=MUSIC, final="short008.mp4")
