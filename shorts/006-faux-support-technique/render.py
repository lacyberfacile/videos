"""Short #006 — Le faux support technique (« virus détecté, appelez ce numéro »)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Ton écran affiche : virus détecté, appelez ce numéro. Surtout, n'appelle pas.",
    "Ce message ne vient pas de ton ordinateur. C'est une simple page web, faite pour te faire peur.",
    "Au téléphone, un faux technicien te demande de le laisser prendre le contrôle de ton PC à distance.",
    "Ensuite, il te fait payer une réparation inutile, et peut fouiller dans tes fichiers.",
    "Et Microsoft le rappelle : il ne t'appelle jamais de lui-même.",
    "Trois réflexes. Un : n'appelle jamais le numéro affiché.",
    "Deux : ferme ton navigateur. S'il est bloqué, ferme-le avec le gestionnaire des tâches.",
    "Trois : ne laisse jamais un inconnu prendre le contrôle de ton ordinateur.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)


def alert(img, box, t, k, flash=True):
    x0, y0, x1, y1 = box
    if k <= 0:
        return
    on = (int(t * 4) % 2 == 0) if flash else True
    dr = D(img)
    a = int(255 * clamp(k * 1.5))
    dr.rectangle([x0, y0, x1, y1], fill=(RED if on else (150, 30, 30)) + (a,))
    cx = (x0 + x1) / 2
    h = y1 - y0
    glyph(dr, cx, y0 + h * 0.22, "⚠", int(h * 0.26), WHITE, a)
    dr.text((cx, y0 + h * 0.5), "VIRUS DÉTECTÉ", font=font(int(h * 0.12), "Black"), fill=WHITE + (a,), anchor="mm")
    dr.text((cx, y0 + h * 0.66), "Appelez le support :", font=font(int(h * 0.065), "SemiBold"), fill=WHITE + (a,), anchor="mm")
    dr.text((cx, y0 + h * 0.8), "09 •• •• •• ••", font=font(int(h * 0.1), "Black"), fill=(255, 230, 120) + (a,), anchor="mm")


def s1(img, t, d):
    x0, y0, x1, y1 = laptop(img, W / 2, 900, 1.05)
    alert(img, (x0, y0, x1, y1), t, ease_out(prog(t, 0.1, 0.25)))
    glitch_text(img, W / 2, 300, "Virus détecté ?", 104, WHITE, t, 0.0)
    if t > d * 0.62:
        k = back_out(prog(t, d * 0.62, 0.35))
        dr = D(img)
        r = 130 * k
        dr.ellipse([W / 2 - r, 1420 - r, W / 2 + r, 1420 + r], fill=(22, 30, 50, 255), outline=RED + (255,), width=8)
        if k > 0.5:
            glyph(dr, W / 2, 1424, "☎", int(130 * min(k, 1)), WHITE)
        cross(img, W / 2, 1420, 120, RED, prog(t, d * 0.7, 0.25), 20)


def s2(img, t, d):
    # dézoom : l'alerte n'est qu'un onglet de navigateur
    k = ease_in_out(prog(t, 0.2, 0.9))
    box_full = (60, 520, 1020, 1300)
    inner = window(img, [80, 560, 1000, 1360], "", CYAN, k) if k > 0 else None
    if inner:
        x0, y0, x1, y1 = inner
        dr = D(img)
        dr.rounded_rectangle([x0 + 20, y0 - 62, x1 - 20, y0 - 14], radius=20, fill=(14, 20, 34, 255))
        dr.text((x0 + 45, y0 - 38), "alerte-securite-pc.xyz", font=font(30, "SemiBold"), fill=RED + (255,), anchor="lm")
        alert(img, (x0 + 30, y0 + 30, x1 - 30, y1 - 30), t, 1.0)
    else:
        alert(img, box_full, t, 1.0)
    pop_text(img, W / 2, 300, "Juste une page web", 92, CYAN, t, 0.3)
    chip(img, W / 2, 1500, "Faite pour te faire peur", RED, prog(t, d * 0.55, 0.4), 50)


def s3(img, t, d):
    x0, y0, x1, y1 = laptop(img, W / 2, 1000, 1.0)
    dr = D(img)
    for j in range(3):
        dr.rounded_rectangle([x0 + 40, y0 + 40 + j * 120, x0 + 300, y0 + 130 + j * 120], radius=14, fill=(40, 52, 76, 255))
        dr.text((x0 + 170, y0 + 85 + j * 120), ["Photos", "Documents", "Banque"][j], font=font(34, "Bold"), fill=WHITE + (255,), anchor="mm")
    # curseur qui bouge tout seul
    if t > 0.4:
        cx = x0 + 420 + math.sin(t * 2.3) * 160
        cy = y0 + 200 + math.cos(t * 1.7) * 110
        dr.polygon([(cx, cy), (cx, cy + 70), (cx + 18, cy + 52), (cx + 34, cy + 86), (cx + 46, cy + 80), (cx + 30, cy + 46), (cx + 54, cy + 46)],
                   fill=RED + (255,), outline=WHITE + (255,))
    hacker(img, 900, 560, 0.7, int(255 * ease_out(prog(t, 0.2, 0.4))))
    arrow(img, (820, 620), (x1 - 120, y0 + 90), RED, ease_out(prog(t, 0.5, 0.4)), 8)
    pop_text(img, W / 2, 300, "Contrôle à distance", 92, RED, t, 0.05)


def s4(img, t, d):
    dr = D(img)
    k = back_out(prog(t, 0.05, 0.45))
    if k > 0:
        w, h = 620 * k, 560 * k
        cx, cy = 360, 900
        dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=24, fill=(240, 240, 235, 255))
        if k > 0.8:
            dr.text((cx, cy - 200), "FACTURE", font=font(56, "Black"), fill=DARK + (255,), anchor="mm")
            dr.text((cx - 250, cy - 90), "Réparation", font=font(40, "SemiBold"), fill=(80, 80, 90, 255), anchor="lm")
            dr.text((cx - 250, cy - 20), "Antivirus « pro »", font=font(40, "SemiBold"), fill=(80, 80, 90, 255), anchor="lm")
            counter(img, cx, cy + 140, 299, 96, DARK, t, 0.5, 0.8, suffix=" €")
    stamp(img, 360, 1220, "INUTILE", RED, t, d * 0.4, size=90)
    # fichiers aspirés vers le pirate
    hacker(img, 850, 1200, 0.8)
    for i in range(4):
        ph = (t * 0.7 + i / 4) % 1
        if t < d * 0.45:
            break
        x = 700 + (850 - 700) * ph
        y = 700 + (1080 - 700) * ph
        dr = D(img)
        dr.rounded_rectangle([x - 40, y - 30, x + 40, y + 30], radius=8, fill=(234, 179, 8, int(255 * (1 - ph))))
    pop_text(img, W / 2, 300, "Il te fait payer", 96, WHITE, t, 0.05)


def s5(img, t, d):
    pop_text(img, W / 2, 300, "Bon à savoir", 92, CYAN, t, 0.0)
    dr = D(img)
    k = back_out(prog(t, 0.05, 0.45))
    if k > 0:
        glow(img, [W / 2 - 440 * k, 700 - 260 * k, W / 2 + 440 * k, 700 + 260 * k], CYAN, 60, 50)
        dr = D(img)
        dr.rounded_rectangle([W / 2 - 440 * k, 700 - 260 * k, W / 2 + 440 * k, 700 + 260 * k], radius=40, fill=(18, 30, 50, 255), outline=CYAN + (255,), width=6)
    if k > 0.8:
        pop_text(img, W / 2, 620, "Microsoft", 80, CYAN, t, 0.3)
        pop_text(img, W / 2, 760, "ne t'appelle jamais de lui-même", 62, WHITE, t, 0.5, maxw=800)
    # téléphone qui sonne puis barré
    sk = prog(t, d * 0.4, 0.3)
    if sk > 0:
        r = 120
        wob = math.sin(t * 25) * 8 * (1 - prog(t, d * 0.65, 0.2))
        dr = D(img)
        dr.ellipse([W / 2 - r + wob, 1240 - r, W / 2 + r + wob, 1240 + r], fill=(22, 30, 50, 255), outline=GREY + (255,), width=6)
        glyph(dr, W / 2 + wob, 1244, "☎", 130, WHITE)
        cross(img, W / 2, 1240, 110, RED, prog(t, d * 0.65, 0.25), 18)


REFLEX = ["N'appelle jamais le numéro", "Ferme le navigateur", "Personne ne prend le contrôle"]


def reflex(n):
    """Mise en scène propre à #006 : l'élément du piège est barré, puis la règle s'affiche en vert."""
    def s(img, t, d):
        dr = D(img)
        for i in range(3):
            cx = W / 2 + (i - 1) * 90
            dr.rounded_rectangle([cx - 30, 395, cx + 30, 410], radius=7, fill=(GREEN if i <= n else (60, 75, 100)) + (255,))
        pop_text(img, W / 2, 300, f"Réflexe {n + 1}", 92, GREEN, t, 0.0)
        cy = 820
        if n == 0:
            dr.rounded_rectangle([W / 2 - 360, cy - 110, W / 2 + 360, cy + 110], radius=30, fill=(60, 20, 26, 255), outline=RED + (255,), width=5)
            dr.text((W / 2, cy), "09 •• •• •• ••", font=font(84, "Black"), fill=WHITE + (255,), anchor="mm")
        elif n == 1:
            window(img, [W / 2 - 360, cy - 230, W / 2 + 360, cy + 230], "alerte-securite-pc.xyz", RED, 1.0)
            D(img).text((W / 2 + 330, cy - 193), "✕", font=font(40, "Black"), fill=WHITE + (255,), anchor="mm")
            if t > d * 0.45:  # raccourci clavier
                kk = back_out(prog(t, d * 0.45, 0.3))
                for j, kname in enumerate(["Ctrl", "Maj", "Échap"]):
                    kx = W / 2 + (j - 1) * 230
                    dr = D(img)
                    dr.rounded_rectangle([kx - 100 * kk, 1120 - 55 * kk, kx + 100 * kk, 1120 + 55 * kk], radius=18, fill=(40, 52, 76, 255), outline=WHITE + (255,), width=4)
                    if kk > 0.8:
                        dr.text((kx, 1120), kname, font=font(44, "Black"), fill=WHITE + (255,), anchor="mm")
        else:
            x0, y0, x1, y1 = laptop(img, W / 2, cy, 0.8)
            ccx = (x0 + x1) / 2 + math.sin(t * 2) * 100
            dr = D(img)
            dr.polygon([(ccx, y0 + 120), (ccx, y0 + 190), (ccx + 18, y0 + 172), (ccx + 54, y0 + 166)], fill=RED + (255,))
        cross(img, W / 2, cy, 230 if n else 180, RED, prog(t, 0.35, 0.3), 24)
        ck = back_out(prog(t, 0.6, 0.4))
        if ck > 0:
            yb = 1330 if n == 1 else 1180
            dr = D(img)
            dr.rounded_rectangle([W / 2 - 440 * ck, yb - 100 * ck, W / 2 + 440 * ck, yb + 100 * ck], radius=40, fill=(20, 40, 34, 255), outline=GREEN + (255,), width=6)
            if ck > 0.8:
                dr.text((W / 2, yb), REFLEX[n], font=font(52, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    return s


SCENES = [s1, s2, s3, s4, s5, reflex(0), reflex(1), reflex(2), outro(1)]
SUBS = [True] * 8 + [False]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS)
