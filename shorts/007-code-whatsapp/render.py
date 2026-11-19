"""Short #007 — L'arnaque au code WhatsApp (« tu peux me renvoyer le code ? »)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "engine"))
from kit import *  # noqa

SEGMENTS = [
    "Un ami t'écrit : je t'ai envoyé un code par erreur, tu peux me le renvoyer ? Surtout, ne fais pas ça.",
    "Ce code, c'est la clé de ton compte WhatsApp. Le pirate essaie de se connecter avec ton numéro.",
    "Lui donner ce code, c'est comme laisser un inconnu faire un double de la clé de chez toi.",
    "Il prend ton compte, lit tes conversations, et écrit à tes contacts pour leur demander de l'argent.",
    "Et souvent, ton ami s'est lui-même fait pirater de cette façon. C'est une chaîne.",
    "Trois réflexes. Un : ne transmets jamais un code reçu par SMS, même à un proche.",
    "Deux : active la vérification en deux étapes, dans les paramètres de WhatsApp, rubrique Compte.",
    "Trois : en cas de doute, appelle ton ami pour vérifier que c'est bien lui.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
VOICE = list(SEGMENTS)
ITEMS = ["Ne transmets jamais un code", "Active la vérification en deux étapes", "Appelle ton ami pour vérifier"]
CODE = "482 913"


def chat_bubble(img, x, y, lines, t, start, left=True, color=(38, 48, 70)):
    k = ease_out(prog(t, start, 0.35))
    if k <= 0:
        return
    f = font(36, "Medium")
    bw = int(max(f.getlength(l) for l in lines)) + 56
    bh = 50 * len(lines) + 34
    dx = (1 - k) * (-140 if left else 140)
    x0 = x + dx if left else x - bw + dx
    a = int(255 * k)
    dr = D(img)
    dr.rounded_rectangle([x0, y, x0 + bw, y + bh], radius=30, fill=color + (a,))
    for i, l in enumerate(lines):
        dr.text((x0 + 28, y + 17 + 50 * i), l, font=f, fill=WHITE + (a,))


def code_box(img, cx, cy, s, color, k=1.0, txt=CODE):
    if k <= 0:
        return
    sc = s * (0.7 + 0.3 * back_out(k))
    w, h = 520 * sc, 170 * sc
    glow(img, [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], color, 40, 60)
    dr = D(img)
    dr.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(30 * sc), fill=(22, 30, 50, 255), outline=color + (255,), width=6)
    dr.text((cx, cy), txt, font=font(int(110 * sc), "Black"), fill=WHITE + (255,), anchor="mm")


def s1(img, t, d):
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1000, 0.95, tilt_y=int(50 * (1 - ease_out(prog(t, 0, 0.5)))))
    dr = D(img)
    dr.rounded_rectangle([sx0, sy0 + 60, sx1, sy0 + 170], radius=0, fill=(22, 30, 50, 255))
    dr.ellipse([sx0 + 30, sy0 + 80, sx0 + 100, sy0 + 150], fill=CYAN + (255,))
    dr.text((sx0 + 65, sy0 + 115), "L", font=font(40, "Black"), fill=DARK + (255,), anchor="mm")
    dr.text((sx0 + 125, sy0 + 115), "Léa", font=font(40, "Bold"), fill=WHITE + (255,), anchor="lm")
    chat_bubble(img, sx0 + 30, sy0 + 240, ["Coucou ! Je t'ai envoyé", "un code par erreur"], t, 0.15)
    chat_bubble(img, sx0 + 30, sy0 + 400, ["Tu peux me le", "renvoyer stp ?"], t, 0.7)
    # notif SMS qui tombe du haut
    nk = back_out(prog(t, 1.2, 0.45))
    if nk > 0:
        y = sy0 + 560 - (1 - nk) * 400
        dr = D(img)
        dr.rounded_rectangle([sx0 + 20, y, sx1 - 20, y + 150], radius=26, fill=(48, 60, 88, 255), outline=CYAN + (255,), width=3)
        dr.text((sx0 + 50, y + 42), "SMS · WhatsApp", font=font(30, "SemiBold"), fill=GREY + (255,), anchor="lm")
        dr.text((sx0 + 50, y + 100), f"Ton code : {CODE}", font=font(42, "ExtraBold"), fill=WHITE + (255,), anchor="lm")
    glitch_text(img, W / 2, 300, "Ne le renvoie pas !", 104, RED, t, d * 0.45)


def s2(img, t, d):
    hacker(img, 230, 820, 1.1)
    code_box(img, W / 2 + 120, 820, 0.85, CYAN, prog(t, 0.2, 0.4))
    k = prog(t, 1.0, 0.6)
    if k > 0:  # le code se transforme en clé
        key(img, W / 2 + 120, 1150 + math.sin(t * 3) * 10, 1.1 * ease_out(k), CYAN, angle=-20 + 10 * math.sin(t * 2))
    pop_text(img, W / 2, 330, "Ce code = ta clé", 96, WHITE, t, 0.05)
    chip(img, W / 2, 1420, "Ton compte WhatsApp", CYAN, prog(t, 1.6, 0.4), size=48)


def s3(img, t, d):
    pop_text(img, W / 2, 330, "Un double de ta clé", 92, WHITE, t, 0.05)
    key(img, W / 2 - 230, 900, 1.15, CYAN, angle=-15)
    k = ease_out(prog(t, 0.6, 0.7))
    if k > 0:
        key(img, W / 2 - 230 + 460 * k, 900 + math.sin(t * 4) * 8, 1.15, RED, angle=-15 + 30 * k, alpha=int(255 * k))
        arrow(img, (W / 2 - 60, 1100), (W / 2 + 120, 1100), GREY, k, width=8)
    if t > d * 0.5:
        hacker(img, W / 2 + 230, 1350, 0.8 * ease_out(prog(t, d * 0.5, 0.4)))


def s4(img, t, d):
    hacker(img, W / 2, 680 + math.sin(t * 3) * 10, 1.2)
    labels = ["Tes conversations", "Tes contacts", "« Prête-moi 300 € »"]
    for i, lab in enumerate(labels):
        k = prog(t, 0.3 + i * 0.6, 0.45)
        x = W / 2 + (1 - ease_out(k)) * (500 if i % 2 else -500)
        chip(img, x, 1020 + i * 160, lab, RED, k, size=50)
    pulse = 0.5 + 0.5 * math.sin(t * 6)
    D(img).ellipse([W / 2 - 220, 850, W / 2 + 220, 880], fill=RED + (int(70 * pulse),))


def s5(img, t, d):
    pop_text(img, W / 2, 330, "Un piratage en chaîne", 90, WHITE, t, 0.05)
    n = 4
    for i in range(n):
        cx = 170 + i * 250
        cy = 1000 + (i % 2) * 140
        k = prog(t, 0.3 + i * 0.55, 0.3)
        col = mix(CYAN, RED, ease_out(k))
        person(img, cx, cy, 0.9, col)
        if i < n - 1:
            arrow(img, (cx + 70, cy - 40), (cx + 180, cy + (140 if i % 2 == 0 else -140) - 40), RED, prog(t, 0.45 + i * 0.55, 0.4), width=8)
        if k > 0.5:
            dr = D(img)
            envelope(img, cx + 70, cy - 170, 0.7, RED)


SCENES = [s1, s2, s3, s4, s5,
          reflex_checklist(ITEMS, 0), reflex_checklist(ITEMS, 1), reflex_checklist(ITEMS, 2), outro(0)]
SUBS = [True] * 8 + [False]
MUSIC = None  # pas de musique de fond (décision de Néo, 19/11/2026)
# (segment, offset s ou -fraction, son, gain)
SFX = [
    (0, 0.15, "pop", 0.5), (0, 1.2, "alert", 0.35), (0, -0.45, "glitch", 0.45),
    (1, 0.0, "whoosh", 0.35), (1, 1.6, "pop", 0.45),
    (2, 0.0, "whoosh", 0.35), (2, 0.6, "pop", 0.4),
    (3, 0.0, "whoosh", 0.35), (3, 1.5, "alert", 0.35),
    (4, 0.0, "whoosh", 0.35),
    (5, 0.0, "whoosh", 0.35), (5, 0.5, "success", 0.4), (6, 0.5, "success", 0.4), (7, 0.5, "success", 0.4),
    (8, 0.6, "pop", 0.5),
]

if __name__ == "__main__":
    run(__file__, SEGMENTS, SCENES, SUBS, sfx=SFX, music=MUSIC, final="short007.mp4")
