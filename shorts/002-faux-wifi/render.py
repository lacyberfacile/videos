"""Short #002 — Le faux Wi-Fi public."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Ce Wi-Fi gratuit à la gare ? Il est peut-être tenu par un pirate.",
    "N'importe qui peut créer un réseau avec le même nom que le vrai. Ton téléphone ne voit pas la différence.",
    "Si tu te connectes au sien, tout ton trafic passe par son appareil. Comme un faux bureau de poste qui trie ton courrier.",
    "Il peut voir quels sites tu visites, et t'afficher une fausse page de connexion pour voler ton mot de passe.",
    "Trois réflexes. Un : pour ta banque ou tes achats, passe en 4G ou 5G.",
    "Deux : désactive la connexion automatique aux Wi-Fi ouverts.",
    "Trois : demande le nom exact du réseau, et méfie-toi des doublons.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
VOICE[4] = "Trois réflexes. Un : pour ta banque ou tes achats, passe en quatre G ou cinq G."
NET = "Gare_WiFi_Gratuit"


def wifi_row(img, x, y, w, name, color, k, lock=False):
    if k <= 0:
        return
    dr = D(img)
    dx = (1 - ease_out(k)) * 200
    a = int(255 * clamp(k * 1.5))
    dr.rounded_rectangle([x + dx, y, x + dx + w, y + 96], radius=22, fill=(30, 40, 62, a), outline=color + (a,), width=3)
    wifi_icon(img, x + dx + 60, y + 62, 42, color, 1.0, a)
    D(img).text((x + dx + 115, y + 48), name, font=font(34, "SemiBold"), fill=WHITE + (a,), anchor="lm")


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1040, 0.95, tilt_y=int(40 * (1 - ease_out(prog(t, 0, 0.5)))))
    dr = D(img)
    dr.text(((sx0 + sx1) / 2, sy0 + 110), "Wi-Fi", font=font(46, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    w = sx1 - sx0 - 50
    names = ["Livebox-8F2A", NET, "SFR_WiFi_Mobile", NET]
    for i, n in enumerate(names):
        k = prog(t, 0.15 + i * 0.18, 0.35)
        col = CYAN
        if i == 3 and t > d * 0.45:
            col = mix(CYAN, RED, ease_out(prog(t, d * 0.45, 0.3)))
        wifi_row(img, sx0 + 25, sy0 + 180 + i * 120, w, n, col, k)
    glitch_text(img, W / 2, 300, "Ce Wi-Fi gratuit ?", 96, WHITE, t, 0.0)
    hk = ease_out(prog(t, d * 0.55, 0.4))
    if hk > 0:
        hacker(img, sx1 + 30 - 200 * hk + 200, sy0 + 760, 0.8, int(255 * hk))
        stamp(img, W / 2, 1380, "PIRATE ?", RED, t, d * 0.62, size=110)


def tower(img, cx, cy, color, t, label, k):
    if k <= 0:
        return
    dr = D(img)
    a = int(255 * clamp(k * 1.5))
    dr.rounded_rectangle([cx - 120, cy - 40, cx + 120, cy + 60], radius=20, fill=(30, 40, 62, a), outline=color + (a,), width=4)
    dr.line([cx - 70, cy - 40, cx - 90, cy - 120], fill=color + (a,), width=8)
    dr.line([cx + 70, cy - 40, cx + 90, cy - 120], fill=color + (a,), width=8)
    for i in range(3):
        ph = ((t * 0.9) + i / 3) % 1
        r = 60 + ph * 140
        dr.arc([cx - r, cy - 150 - r, cx + r, cy - 150 + r], 220, 320, fill=color + (int(a * (1 - ph)),), width=7)
    dr.text((cx, cy + 120), label, font=font(34, "Bold"), fill=WHITE + (a,), anchor="mm")


def s2(img, t, d):
    pop_text(img, W / 2, 300, "Même nom", 100, WHITE, t, 0.05)
    pop_text(img, W / 2, 420, "Deux réseaux", 72, CYAN, t, 0.35)
    k1 = ease_out(prog(t, 0.2, 0.4))
    k2 = ease_out(prog(t, 0.45, 0.4))
    rev = ease_out(prog(t, d * 0.5, 0.4))
    tower(img, 280, 820, CYAN, t, NET, k1)
    tower(img, 800, 820, mix(CYAN, RED, rev), t, NET, k2)
    if rev > 0:
        hacker(img, 800, 1180, 0.75, int(255 * rev))
        chip(img, 280, 1180, "le vrai", GREEN, rev, 46)
    # téléphone qui hésite au centre
    dr = D(img)
    px = W / 2 + math.sin(t * 5) * 30 * (1 - rev)
    sx0, sy0, sx1, sy1 = phone(img, px, 1050, 0.32)
    D(img).text(((sx0 + sx1) / 2, (sy0 + sy1) / 2), "?", font=font(110, "Black"), fill=WHITE + (255,), anchor="mm")


def s3(img, t, d):
    # téléphone -> pirate -> internet
    pts = [(200, 900), (W / 2, 900), (880, 900)]
    sx = phone(img, 200, 900, 0.34)
    wifi_icon(img, 200, 920, 60, CYAN, 1.0)
    hacker(img, W / 2, 960, 0.9)
    dr = D(img)
    dr.ellipse([880 - 110, 900 - 110, 880 + 110, 900 + 110], outline=CYAN + (255,), width=8)
    dr.ellipse([880 - 50, 900 - 110, 880 + 50, 900 + 110], outline=CYAN + (255,), width=5)
    dr.line([770, 900, 990, 900], fill=CYAN + (255,), width=5)
    D(img).text((880, 1060), "Internet", font=font(40, "Bold"), fill=WHITE + (255,), anchor="mm")
    arrow(img, (290, 900), (W / 2 - 140, 900), RED, ease_out(prog(t, 0.2, 0.4)), 10)
    arrow(img, (W / 2 + 140, 900), (760, 900), RED, ease_out(prog(t, 0.5, 0.4)), 10)
    # enveloppes qui défilent et marquent un arrêt chez le pirate
    for i in range(4):
        ph = ((t * 0.45) + i / 4) % 1
        if t < 0.8:
            break
        if ph < 0.45:
            x = 290 + (W / 2 - 290) * (ph / 0.45)
        elif ph < 0.6:
            x = W / 2
        else:
            x = W / 2 + (770 - W / 2) * ((ph - 0.6) / 0.4)
        y = 800 if 0.45 <= ph < 0.6 else 900 - 110
        envelope(img, x, y, 0.6, RED if 0.45 <= ph else WHITE)
    pop_text(img, W / 2, 330, "Tout passe par lui", 88, RED, t, 0.1)
    if t > d * 0.5:
        chip(img, W / 2, 1300, "Un faux bureau de poste", RED, prog(t, d * 0.5, 0.4), 50)


def s4(img, t, d):
    scr = laptop(img, W / 2, 760, 1.0)
    x0, y0, x1, y1 = scr
    dr = D(img)
    sites = ["banque", "mail", "réseaux sociaux", "boutique"]
    if t < d * 0.45:
        dr.text((x0 + 30, y0 + 40), "Sites visités :", font=font(40, "Bold"), fill=GREY + (255,))
        for i, s in enumerate(sites):
            k = prog(t, 0.2 + i * 0.22, 0.3)
            if k > 0:
                dr.text((x0 + 40 + (1 - ease_out(k)) * 60, y0 + 110 + i * 70), "• " + s, font=font(44, "SemiBold"), fill=mix(BG, CYAN, k) + (255,))
        pop_text(img, W / 2, 300, "Il voit où tu vas", 88, WHITE, t, 0.05)
    else:
        k = prog(t, d * 0.45, 0.4)
        bx = window(img, [W / 2 - 330, 1050, W / 2 + 330, 1560], "Connexion", RED, k)
        if k > 0.6:
            dr = D(img)
            for j, lab in enumerate(["Identifiant", "Mot de passe"]):
                yy = bx[1] + 60 + j * 140
                dr.text((bx[0] + 50, yy), lab, font=font(32, "Medium"), fill=GREY + (255,))
                dr.rounded_rectangle([bx[0] + 50, yy + 45, bx[2] - 50, yy + 110], radius=14, fill=(40, 52, 76, 255))
            stars = "•" * int(clamp((t - d * 0.6) / (d * 0.25)) * 10)
            dr.text((bx[0] + 75, bx[1] + 60 + 140 + 78), stars, font=font(46, "Bold"), fill=WHITE + (255,), anchor="lm")
        pop_text(img, W / 2, 300, "Fausse page de connexion", 80, RED, t, d * 0.45)
        stamp(img, W / 2 + 180, 1480, "FAUX", RED, t, d * 0.8, size=100)


ITEMS = ["Banque, achats : 4G ou 5G", "Pas de connexion auto", "Nom exact du réseau"]
SCENES = [s1, s2, s3, s4, reflex_checklist(ITEMS, 0), reflex_checklist(ITEMS, 1), reflex_checklist(ITEMS, 2), outro(2)]
SUBS = [True] * 7 + [False]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS)
