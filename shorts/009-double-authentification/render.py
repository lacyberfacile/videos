"""Short #009 — La double authentification (deux serrures sur la porte)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Ton mot de passe a fuité ? Un seul réglage peut encore bloquer le pirate.",
    "Ce réglage, c'est la double authentification. En plus du mot de passe, le site te demande une confirmation.",
    "C'est comme une porte avec deux serrures : voler une seule clé ne suffit plus.",
    "Cette confirmation, c'est un code reçu par SMS, une validation dans une appli, une clé de sécurité ou ton empreinte.",
    "Résultat : toi seul peux autoriser un nouvel appareil à se connecter à ton compte.",
    "Trois réflexes. Un : active-la d'abord sur ta boîte mail, car elle sert à récupérer tes autres comptes.",
    "Deux : active-la ensuite sur tes réseaux sociaux, tes messageries et tes sites d'achat.",
    "Trois : ne donne jamais ce code de confirmation à personne, même au téléphone.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
ITEMS = ["D'abord ta boîte mail", "Puis réseaux et achats", "Garde ce code pour toi"]


def field(img, x0, y0, x1, label, value, color, k=1.0):
    if k <= 0:
        return
    a = int(255 * clamp(k * 1.5))
    dr = D(img)
    dr.text((x0, y0 - 40), label, font=font(34, "SemiBold"), fill=GREY + (a,), anchor="lm")
    dr.rounded_rectangle([x0, y0, x1, y0 + 100], radius=22, fill=(12, 17, 30, a), outline=color + (a,), width=4)
    dr.text((x0 + 30, y0 + 50), value, font=font(46, "Bold"), fill=WHITE + (a,), anchor="lm")


def fingerprint(img, cx, cy, s, color):
    dr = D(img)
    for i in range(5):
        r = (18 + i * 16) * s
        dr.arc([cx - r, cy - r * 1.2, cx + r, cy + r * 1.2], 200 - i * 6, 340 + i * 6, fill=color + (255,), width=max(3, int(6 * s)))
        dr.arc([cx - r, cy - r * 1.2, cx + r, cy + r * 1.2], 20, 160, fill=color + (255,), width=max(3, int(6 * s)))


def s1(img, t, d):
    win = window(img, (110, 560, 970, 1260), "Connexion", CYAN, ease_out(prog(t, 0.0, 0.4)))
    field(img, 170, 720, 910, "E-mail", "toi@mail.fr", CYAN, prog(t, 0.2, 0.3))
    field(img, 170, 930, 910, "Mot de passe", "••••••••••", RED, prog(t, 0.35, 0.3))
    if t > 0.7:
        stamp(img, W / 2 + 160, 1000, "FUITE", RED, t, 0.7, size=110, angle=-10)
    gk = back_out(prog(t, d * 0.5, 0.45))
    if gk > 0:
        glow(img, [W / 2 - 160, 1250, W / 2 + 160, 1520], GREEN, 50, 70)
        padlock(img, W / 2, 1400, 0.75 * gk, GREEN)
    glitch_text(img, W / 2, 300, "Mot de passe volé ?", 96, WHITE, t, 0.0)


def s2(img, t, d):
    pop_text(img, W / 2, 330, "2 étapes pour entrer", 84, WHITE, t, 0.05)
    k1 = back_out(prog(t, 0.2, 0.4))
    if k1 > 0:
        chip(img, W / 2, 620, "1. Mot de passe  ✓", CYAN, k1, size=52)
    arrow(img, (W / 2, 700), (W / 2, 820), GREY, prog(t, 0.7, 0.3), width=8)
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1180 + (1 - ease_out(prog(t, 0.9, 0.5))) * 500, 0.55)
    k2 = prog(t, 1.3, 0.4)
    if k2 > 0:
        dr = D(img)
        a = int(255 * clamp(k2 * 2))
        cy = (sy0 + sy1) / 2
        dr.text(((sx0 + sx1) / 2, cy - 80), "C'est toi ?", font=font(44, "ExtraBold"), fill=WHITE + (a,), anchor="mm")
        pulse = 1 + 0.05 * math.sin(t * 7)
        dr.rounded_rectangle([sx0 + 30, cy + 10, sx1 - 30, cy + 100 * pulse], radius=24, fill=GREEN + (a,))
        dr.text(((sx0 + sx1) / 2, cy + 55), "Oui", font=font(40, "Black"), fill=DARK + (a,), anchor="mm")


def s3(img, t, d):
    pop_text(img, W / 2, 330, "Deux serrures", 104, WHITE, t, 0.05)
    dr = D(img)
    dr.rounded_rectangle([W / 2 - 230, 560, W / 2 + 230, 1420], radius=20, fill=(40, 52, 76, 255), outline=(70, 85, 110, 255), width=6)
    ok = ease_out(prog(t, 0.8, 0.4))
    padlock(img, W / 2, 800, 0.8, mix(CYAN, RED, ok), open_k=ok)
    padlock(img, W / 2, 1180, 0.8, GREEN)
    kk = ease_out(prog(t, 0.2, 0.6))
    key(img, 120 + 230 * kk, 820, 0.6, RED, angle=0, alpha=int(255 * clamp(kk * 2)))
    if t > 1.4:
        shake = math.sin(t * 40) * 8 if t < 1.9 else 0
        hacker(img, 170 + shake, 1250, 0.7)
        cross(img, W / 2 + 330, 1180, 80, RED, prog(t, 1.6, 0.3), 18)
        chip(img, W / 2 + 330, 1330, "Bloqué", GREEN, prog(t, 1.8, 0.3), size=40)


def s4(img, t, d):
    pop_text(img, W / 2, 330, "Ton 2e verrou", 100, WHITE, t, 0.05)
    tiles = ["SMS", "Appli", "Clé", "Empreinte"]
    for i, lab in enumerate(tiles):
        r, c = divmod(i, 2)
        cx, cy = W / 2 + (c - 0.5) * 420, 760 + r * 480
        k = back_out(prog(t, 0.2 + i * 0.6, 0.4))
        if k <= 0:
            continue
        w = 360 * k
        dr = D(img)
        cur = 0.2 + i * 0.6 <= t < 0.2 + (i + 1) * 0.6 + 0.4
        dr.rounded_rectangle([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], radius=40, fill=(20, 40, 34, 255),
                             outline=GREEN + (255,), width=7 if cur else 3)
        s = k
        if i == 0:
            envelope(img, cx, cy - 30, 1.4 * s, GREEN)
        elif i == 1:
            dr.rounded_rectangle([cx - 45 * s, cy - 110 * s, cx + 45 * s, cy + 50 * s], radius=12, outline=GREEN + (255,), width=6)
            icon_check(D(img), cx, cy - 30 * s, 30 * s, GREEN)
        elif i == 2:
            key(img, cx, cy - 30, 0.55 * s, GREEN, angle=-30)
        else:
            fingerprint(img, cx, cy - 30, 1.0 * s, GREEN)
        D(img).text((cx, cy + 120 * s), lab, font=font(int(46 * s) + 1, "ExtraBold"), fill=WHITE + (255,), anchor="mm")


def s5(img, t, d):
    pop_text(img, W / 2, 330, "Toi seul décides", 100, WHITE, t, 0.05)
    laptop(img, 300, 820, 0.45)
    D(img).text((300, 820), "Nouvel appareil", font=font(26, "Bold"), fill=GREY + (255,), anchor="mm")
    sx0, sy0, sx1, sy1 = phone(img, 800, 1050, 0.5)
    arrow(img, (480, 860), (690, 960), CYAN, prog(t, 0.4, 0.4), width=8)
    k = prog(t, 0.9, 0.3)
    if k > 0:
        dr = D(img)
        cy = (sy0 + sy1) / 2
        dr.text((800, cy - 60), "Autoriser ?", font=font(36, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
        icon_check(dr, 800, cy + 60, 50 * ease_out(prog(t, 1.3, 0.3)), GREEN)
    person(img, 800, 1420, 0.6, GREEN)


SCENES = [s1, s2, s3, s4, s5,
          reflex_trio(ITEMS, 0, None), reflex_trio(ITEMS, 1, None), reflex_trio(ITEMS, 2, None), outro(1)]


def _d_mail(img, cx, cy, s, col):
    envelope(img, cx, cy, 1.3 * s, col)


def _d_apps(img, cx, cy, s, col):
    for i, (dx, dy) in enumerate([(-35, -35), (35, -35), (-35, 35), (35, 35)]):
        D(img).rounded_rectangle([cx + dx * s - 28 * s, cy + dy * s - 28 * s, cx + dx * s + 28 * s, cy + dy * s + 28 * s], radius=10, fill=col + (255,))


def _d_secret(img, cx, cy, s, col):
    padlock(img, cx, cy + 10 * s, 0.45 * s, col)


DRAW = [_d_mail, _d_apps, _d_secret]
SCENES[5:8] = [reflex_trio(ITEMS, n, DRAW) for n in range(3)]
SUBS = [True] * 8 + [False]
MUSIC = None  # pas de musique de fond (décision de Néo, 19/11/2026)
# (segment, offset s ou -fraction, son, gain)
# Sons doux uniquement (pop, success) : pas de whoosh, stamp, alert, glitch, type (décision de Néo, 19/11/2026)
SFX = [
    (0, -0.5, 'success', 0.4),
    (1, 1.3, 'success', 0.35),
    (2, 1.8, 'success', 0.4),
    (3, 0.2, 'pop', 0.4),
    (3, 1.4, 'pop', 0.4),
    (4, 1.3, 'success', 0.4),
    (5, 0.4, 'success', 0.4),
    (6, 0.4, 'success', 0.4),
    (7, 0.4, 'success', 0.4),
    (8, 0.6, 'pop', 0.5),
]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS, sfx=SFX, music=MUSIC, final="short009.mp4")
