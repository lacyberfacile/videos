"""Short #011 — Les mises à jour : la fenêtre mal fermée."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Tu repousses toujours les mises à jour ? Les pirates adorent ça.",
    "Une mise à jour n'ajoute pas que des nouveautés. Elle corrige aussi des failles de sécurité.",
    "Une faille, c'est comme une fenêtre mal fermée : quelqu'un peut entrer par là.",
    "Une fois la faille connue, les pirates visent les appareils qui ne sont pas à jour.",
    "Ils peuvent alors voler tes données, ou installer un virus sans que tu le voies.",
    "Trois réflexes. Un : active les mises à jour automatiques, sur ton téléphone et ton ordinateur.",
    "Deux : installe-les uniquement depuis les réglages ou la boutique officielle, jamais depuis une pub.",
    "Trois : un appareil qui ne reçoit plus de mises à jour est plus exposé. Pense à le remplacer.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
ITEMS = ["Mises à jour automatiques", "Seulement via les réglages", "Plus de mises à jour ? Remplace-le"]


def house(img, cx, cy, s, open_k, color):
    dr = D(img)
    w, h = 520 * s, 420 * s
    dr.polygon([(cx - w / 2 - 40 * s, cy - h / 2), (cx, cy - h / 2 - 260 * s), (cx + w / 2 + 40 * s, cy - h / 2)], fill=(40, 52, 78, 255))
    dr.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=(26, 35, 56, 255), outline=(60, 75, 100, 255), width=4)
    dr.rectangle([cx + 80 * s, cy - 10 * s, cx + 200 * s, cy + h / 2], fill=(50, 62, 90, 255))  # porte
    # fenêtre : un battant fermé, l'autre qui bat
    wx0, wy0, wx1, wy1 = cx - 210 * s, cy - 130 * s, cx - 10 * s, cy + 60 * s
    dr.rectangle([wx0, wy0, wx1, wy1], fill=(10, 14, 24, 255), outline=color + (255,), width=5)
    mid = (wx0 + wx1) / 2
    dr.rectangle([wx0, wy0, mid, wy1], fill=(40, 70, 100, 255), outline=color + (255,), width=4)
    ow = (wx1 - mid) * (1 - 0.8 * open_k)
    dr.polygon([(mid, wy0), (mid + ow, wy0 - 30 * open_k * s), (mid + ow, wy1 + 30 * open_k * s), (mid, wy1)],
               fill=(40, 70, 100, 255), outline=color + (255,))
    return (mid + ow, (wy0 + wy1) / 2)


def device(img, cx, cy, s, ok, k=1.0, blink=1.0):
    if k <= 0:
        return
    a = int(255 * clamp(k * 1.5))
    sc = s * (0.7 + 0.3 * back_out(k))
    col = GREEN if ok else RED
    dr = D(img)
    dr.rounded_rectangle([cx - 60 * sc, cy - 100 * sc, cx + 60 * sc, cy + 100 * sc], radius=int(18 * sc),
                         fill=(26, 35, 56, a), outline=col + (int(a * (blink if not ok else 1)),), width=5)
    if ok:
        icon_check(dr, cx, cy, 30 * sc, GREEN)
    else:
        glyph(dr, cx, cy, "!", int(70 * sc), RED, int(a * blink))


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1000, 0.95, tilt_y=int(60 * (1 - ease_out(prog(t, 0, 0.5)))))
    k = back_out(prog(t, 0.15, 0.4))
    if k > 0:
        dr = D(img)
        y = sy0 + 260 - (1 - k) * 200
        dr.rounded_rectangle([sx0 + 30, y, sx1 - 30, y + 330], radius=28, fill=(40, 52, 78, 255), outline=CYAN + (255,), width=3)
        dr.text(((sx0 + sx1) / 2, y + 70), "Mise à jour", font=font(46, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
        dr.text(((sx0 + sx1) / 2, y + 125), "disponible", font=font(40, "SemiBold"), fill=GREY + (255,), anchor="mm")
        # bouton « Plus tard » tapé en boucle
        press = (t * 2.2) % 1
        bs = 1 - 0.08 * (press < 0.15)
        bx, by = (sx0 + sx1) / 2, y + 240
        dr.rounded_rectangle([bx - 160 * bs, by - 45 * bs, bx + 160 * bs, by + 45 * bs], radius=40, fill=RED + (255,))
        dr.text((bx, by), "Plus tard", font=font(42, "Black"), fill=WHITE + (255,), anchor="mm")
        n = 1 + int(max(0, t - 0.4) * 2.2)
        dr.text(((sx0 + sx1) / 2, y + 420), f"Reportée {n} fois", font=font(44, "ExtraBold"), fill=RED + (255,), anchor="mm")
    glitch_text(img, W / 2, 290, "Encore plus tard ?", 100, RED, t, d * 0.4)


def s2(img, t, d):
    pop_text(img, W / 2, 330, "Ce que ça corrige", 92, WHITE, t, 0.05)
    padlock(img, W / 2, 850, 1.3, GREEN, open_k=1 - ease_out(prog(t, 1.4, 0.6)))
    chip(img, W / 2, 1180, "+ Nouveautés", CYAN, prog(t, 0.3, 0.4), size=56)
    chip(img, W / 2, 1340, "Failles corrigées", GREEN, prog(t, 1.2, 0.4), size=60)


def s3(img, t, d):
    pop_text(img, W / 2, 330, "Une fenêtre mal fermée", 88, WHITE, t, 0.05)
    open_k = 0.5 + 0.5 * math.sin(t * 2.2)
    ex, ey = house(img, W / 2, 1020, 1.25, open_k, RED)
    hk = ease_out(prog(t, 0.8, 0.8))
    if hk > 0:
        hacker(img, W / 2 - 520 + 260 * hk, 1260, 0.75, alpha=int(255 * hk))
    glow(img, [ex - 40, ey - 60, ex + 40, ey + 60], RED, 40, int(60 + 40 * math.sin(t * 6)))


def s4(img, t, d):
    pop_text(img, W / 2, 330, "Pas à jour = visé", 92, RED, t, 0.05)
    oks = [True, False, True, True, False, True]
    for i, ok in enumerate(oks):
        cx = 230 + (i % 3) * 310
        cy = 760 + (i // 3) * 380
        blink = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 8 + i))
        device(img, cx, cy, 1.1, ok, prog(t, 0.1 + i * 0.12, 0.35), blink)
    # faisceau de recherche qui balaie
    sk = prog(t, 0.9, d - 1.0)
    if sk > 0:
        x = 100 + (W - 200) * (0.5 - 0.5 * math.cos(sk * math.pi * 2))
        dr = D(img)
        dr.rectangle([x - 6, 560, x + 6, 1340], fill=RED + (140,))
        glow(img, [x - 30, 560, x + 30, 1340], RED, 30, 50)


def s5(img, t, d):
    sx0, sy0, sx1, sy1 = laptop(img, 330, 900, 0.9)
    hacker(img, W - 220, 880 + math.sin(t * 3) * 10, 1.0)
    files = ["Photos", "Mails", "Codes"]
    for i, f in enumerate(files):
        k = ease_in_out(prog(t, 0.3 + i * 0.45, 0.9))
        if k > 0:
            x = 330 + (W - 760) * k
            y = 700 - math.sin(k * math.pi) * (120 + 50 * i) + i * 110
            chip(img, x, y, f, RED, min(1, k * 3), size=40)
    vk = back_out(prog(t, 1.9, 0.4))
    if vk > 0:
        dr = D(img)
        cx, cy, r = 330, 1270, 90 * vk
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED + (255,))
        for a in range(8):
            ang = a * math.pi / 4 + t
            dr.line([cx + math.cos(ang) * r, cy + math.sin(ang) * r, cx + math.cos(ang) * r * 1.4, cy + math.sin(ang) * r * 1.4],
                    fill=RED + (255,), width=10)
        chip(img, 690, 1270, "Un virus caché", RED, vk, size=48)
    pop_text(img, W / 2, 330, "Tes données volées", 92, RED, t, 0.05)


SCENES = [s1, s2, s3, s4, s5,
          reflex_bigslide(ITEMS, 0), reflex_bigslide(ITEMS, 1), reflex_bigslide(ITEMS, 2), outro(2)]
SUBS = [True] * 8 + [False]
MUSIC = None  # pas de musique de fond (décision de Néo, 19/11/2026)
# Uniquement le pop discret, rien sur les réflexes (décision de Néo, 19/11/2026)
SFX = [
    (0, 0.15, 'pop', 0.5),  # notification de mise à jour
    (1, 1.2, 'pop', 0.4),   # « Failles corrigées »
    (4, 1.9, 'pop', 0.4),   # virus
    (8, 0.6, 'pop', 0.5),   # bouton S'ABONNER
]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS, sfx=SFX, music=MUSIC, final="short011.mp4")
