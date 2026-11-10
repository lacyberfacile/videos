"""Rendu du Short #001 — Le faux SMS de colis.

Usage : python3 render.py [--audio-dir DIR] [--out FILE] [--preview]
- Avec --audio-dir (seg01.mp3 … seg10.mp3), les durées des plans viennent de l'audio.
- Sans audio, durées estimées (rendu muet pour valider l'animation).
"""
import argparse, json, math, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "engine"))
from lcf import *  # noqa
from PIL import Image, ImageDraw

LOGO = Image.open(HERE.parent.parent / "assets/branding/logo_la_cyber_facile_1080.png").convert("RGB")

SEGMENTS = [
    "Ton colis n'a pas pu être livré ? Attention : ce SMS est un piège.",
    "Il imite un transporteur connu, et te demande de cliquer pour reprogrammer la livraison.",
    "Le lien t'envoie sur un faux site, une copie quasi parfaite du vrai. Comme un faux guichet installé devant la vraie poste.",
    "On te réclame quelques euros de frais… et surtout, ta carte bancaire.",
    "Et ce n'est que le début : quelques jours plus tard, un faux conseiller de ta banque peut t'appeler, avec tes vraies infos.",
    "Trois réflexes. Un : ne clique jamais sur le lien.",
    "Deux : vérifie ton suivi sur l'appli officielle du transporteur.",
    "Trois : transfère le SMS au 33 700. C'est gratuit.",
    "Et si tu as déjà donné ta carte, appelle ta banque tout de suite pour la faire bloquer.",
    "Abonne-toi à La Cyber Facile, pour ne plus te faire avoir.",
]
TAIL = 0.6  # silence ajouté après la dernière phrase


def sms_lines():
    return ["Votre colis n'a pas pu être", "livré. Reprogrammez ici :", "suivi-colis.example"]


# ---------------- scènes ----------------
def s1(img, t, d):  # accroche
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 900, 1.0, tilt_y=int(30 * (1 - ease_out(prog(t, 0, 0.5)))))
    dr = ImageDraw.Draw(img, "RGBA")
    dr.text(((sx0 + sx1) / 2, sy0 + 110), "06 •• •• •• ••", font=font(36, "SemiBold"), fill=GREY + (255,), anchor="mm")
    sms_bubble(img, sx0 + 30, sy0 + 190, sx1 - sx0 - 60, sms_lines(), t, 0.1, link_idx=2)
    stamp(img, W / 2, 1000, "PIÈGE", RED, t, d * 0.55)


def s2(img, t, d):  # imite un transporteur, clique
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1000, 0.95)
    dr = ImageDraw.Draw(img, "RGBA")
    dr.text(((sx0 + sx1) / 2, sy0 + 105), "06 •• •• •• ••", font=font(34, "SemiBold"), fill=GREY + (255,), anchor="mm")
    hot = prog(t, d * 0.45, 0.3)
    link_col = mix(CYAN, RED, hot)
    box = sms_bubble(img, sx0 + 28, sy0 + 180, sx1 - sx0 - 56, sms_lines(), t + 1, 0, link_idx=2, link_col=link_col)
    pop_text(img, W / 2, 300, "Il imite un livreur", 84, WHITE, t, 0.05)
    # doigt qui tape sur le lien
    k = prog(t, d * 0.35, 0.4)
    if k > 0 and box:
        lx, ly = box[0] + 200, box[3] - 40
        fx = lx + (1 - ease_out(k)) * 260
        fy = ly + (1 - ease_out(k)) * 300
        dr.ellipse([fx - 34, fy - 34, fx + 34, fy + 34], fill=WHITE + (200,))
        if k >= 1:
            r = 40 + ((t * 2.2) % 1) * 70
            a = int(200 * (1 - ((t * 2.2) % 1)))
            dr.ellipse([lx - r, ly - r, lx + r, ly + r], outline=RED + (a,), width=6)


def browser(img, x, y, w, h, title, color, k=1.0):
    dr = ImageDraw.Draw(img, "RGBA")
    a = int(255 * k)
    dr.rounded_rectangle([x, y, x + w, y + h], radius=28, fill=(24, 33, 54, a), outline=color + (a,), width=6)
    dr.rounded_rectangle([x, y, x + w, y + 80], radius=28, fill=color + (int(60 * k),))
    for i, c in enumerate([(239, 68, 68), (234, 179, 8), (34, 197, 94)]):
        dr.ellipse([x + 30 + i * 40, y + 28, x + 54 + i * 40, y + 52], fill=c + (a,))
    dr.rounded_rectangle([x + 60, y + 130, x + w - 60, y + 210], radius=16, fill=(50, 62, 88, a))
    dr.rounded_rectangle([x + 60, y + 240, x + w - 160, y + 280], radius=12, fill=(50, 62, 88, a))
    dr.rounded_rectangle([x + 60, y + 300, x + w - 220, y + 340], radius=12, fill=(50, 62, 88, a))
    dr.rounded_rectangle([x + 60, y + h - 130, x + w - 60, y + h - 60], radius=20, fill=color + (a,))
    dr.text((x + w / 2, y + h - 95), title, font=font(40, "ExtraBold"), fill=DARK + (a,), anchor="mm")


def s3(img, t, d):  # faux site / faux guichet
    k1 = ease_out(prog(t, 0, 0.4))
    browser(img, 110, 620 - int(40 * (1 - k1)), 700, 620, "VRAI SITE", CYAN, k1)
    k2 = ease_out(prog(t, d * 0.25, 0.5))
    if k2 > 0:
        x = int(270 + (1 - k2) * 700)
        browser(img, x, 760, 700, 620, "FAUX SITE", RED, k2)
    if t < d * 0.55:
        pop_text(img, W / 2, 330, "Une copie quasi parfaite", 80, WHITE, t, 0.05)
    else:
        pop_text(img, W / 2, 330, "Un faux guichet", 92, RED, t, d * 0.55)


def s4(img, t, d):  # frais + carte bancaire
    dr = ImageDraw.Draw(img, "RGBA")
    k = back_out(prog(t, 0, 0.4))
    bw, bh = int(760 * k), int(220 * k)
    if bw > 10:
        dr.rounded_rectangle([W / 2 - bw / 2, 520 - bh / 2, W / 2 + bw / 2, 520 + bh / 2], radius=30, fill=(24, 33, 54, 255), outline=RED + (255,), width=5)
        if k > 0.8:
            dr.text((W / 2, 490), "Frais de livraison", font=font(44, "SemiBold"), fill=GREY + (255,), anchor="mm")
            dr.text((W / 2, 560), "1,99 €", font=font(72, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    # trou rouge qui aspire la carte
    hk = ease_out(prog(t, d * 0.4, 0.4))
    if hk > 0:
        r = 170 * hk
        for i in range(6, 0, -1):
            rr = r * i / 6
            dr.ellipse([W / 2 - rr, 1230 - rr * 0.45, W / 2 + rr, 1230 + rr * 0.45], fill=mix(RED, BG, i / 7) + (230,))
    ck = prog(t, d * 0.5, d * 0.45)
    cy = 900 + 330 * ease_in_out(ck)
    credit_card(img, W / 2, cy, 1.0 - 0.9 * ease_in_out(ck), angle=ck * 220)
    if t > d * 0.45:
        pop_text(img, W / 2, 300, "Ta carte bancaire", 92, RED, t, d * 0.45)


def s5(img, t, d):  # faux conseiller
    sx0, sy0, sx1, sy1 = phone(img, W / 2, 1000, 0.9)
    dr = ImageDraw.Draw(img, "RGBA")
    cx, cy = (sx0 + sx1) / 2, sy0 + 330
    for i in range(3):
        ph = ((t * 1.3) + i / 3) % 1
        r = 90 + ph * 170
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED + (int(220 * (1 - ph)),), width=6)
    dr.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=RED + (255,))
    # combiné
    glyph(dr, cx, cy + 4, "☎", 110, WHITE)
    dr.text((cx, cy + 190), "Appel entrant", font=font(38, "Medium"), fill=GREY + (255,), anchor="mm")
    dr.text((cx, cy + 250), "« Votre banque »", font=font(50, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    pop_text(img, W / 2, 300, "Puis : un faux conseiller", 80, WHITE, t, 0.1)


REFLEXES = ["Ne clique pas", "Appli officielle", "Transfère au 33700"]


def reflex_scene(n):
    def s(img, t, d):
        dr = ImageDraw.Draw(img, "RGBA")
        pop_text(img, W / 2, 300, "3 réflexes", 96, GREEN, t if n > 0 else t, 0 if n == 0 else -1)
        # pastilles de progression
        for i in range(3):
            cx = W / 2 + (i - 1) * 170
            if i < n:
                icon_check(dr, cx, 470, 50, GREEN)
            elif i == n:
                k = ease_out(prog(t, 0.05, 0.3))
                dr.ellipse([cx - 50, 420, cx + 50, 520], outline=GREEN + (255,), width=6, fill=GREEN + (int(255 * k),))
                dr.text((cx, 470), str(i + 1), font=font(52, "Black"), fill=(DARK if k > 0.5 else GREEN) + (255,), anchor="mm")
            else:
                dr.ellipse([cx - 50, 420, cx + 50, 520], outline=GREY + (120,), width=4)
                dr.text((cx, 470), str(i + 1), font=font(48, "Bold"), fill=GREY + (140,), anchor="mm")
        # grande carte de la règle courante
        k = back_out(prog(t, 0.15, 0.45))
        if k > 0:
            bw, bh = int(900 * k), int(360 * k)
            glow(img, [W / 2 - bw / 2, 1000 - bh / 2, W / 2 + bw / 2, 1000 + bh / 2], GREEN, 60, 60)
            dr = ImageDraw.Draw(img, "RGBA")
            dr.rounded_rectangle([W / 2 - bw / 2, 1000 - bh / 2, W / 2 + bw / 2, 1000 + bh / 2], radius=40, fill=(20, 40, 34, 255), outline=GREEN + (255,), width=6)
        if k > 0.7:
            pop_text(img, W / 2, 1000, REFLEXES[n], 86, WHITE, t, 0.35, maxw=820)
    return s


def s9(img, t, d):
    if t < d * 0.4:
        pop_text(img, W / 2, 700, "Déjà donné ta carte ?", 88, RED, t, 0.05)
    else:
        pop_text(img, W / 2, 620, "Appelle ta banque", 96, GREEN, t, d * 0.4)
        pop_text(img, W / 2, 760, "tout de suite", 72, WHITE, t, d * 0.5)
        dr = ImageDraw.Draw(img, "RGBA")
        k = back_out(prog(t, d * 0.55, 0.4))
        if k > 0:
            r = 120 * k
            wob = math.sin(t * 18) * 6 * k
            dr.ellipse([W / 2 - r, 1100 - r, W / 2 + r, 1100 + r], fill=GREEN + (255,))
            if k > 0.5:
                glyph(dr, W / 2 + wob, 1104, "☎", int(140 * min(k, 1.0)), DARK)


def s10(img, t, d):
    k = back_out(prog(t, 0, 0.5))
    size = max(2, int(520 * k))
    logo = LOGO.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    img.paste(logo, (int(W / 2 - size / 2), int(760 - size / 2)), mask)
    pop_text(img, W / 2, 1150, "La Cyber Facile", 92, WHITE, t, 0.25)
    pop_text(img, W / 2, 1250, "@lacyberfacile", 56, CYAN, t, 0.4, weight="SemiBold")
    bk = back_out(prog(t, 0.6, 0.4))
    if bk > 0:
        pulse = 1 + 0.04 * math.sin(t * 7)
        bw, bh = 560 * bk * pulse, 130 * bk * pulse
        dr = ImageDraw.Draw(img, "RGBA")
        dr.rounded_rectangle([W / 2 - bw / 2, 1420 - bh / 2, W / 2 + bw / 2, 1420 + bh / 2], radius=65, fill=RED + (255,))
        if bk > 0.8:
            dr.text((W / 2, 1420), "S'ABONNER", font=font(58, "Black"), fill=WHITE + (255,), anchor="mm")


SCENES = [s1, s2, s3, s4, s5, reflex_scene(0), reflex_scene(1), reflex_scene(2), s9, s10]
SUBS = [True] * 9 + [False]


def durations(audio_dir):
    if audio_dir:
        out = []
        for i in range(1, 11):
            p = Path(audio_dir) / f"seg{i:02d}.mp3"
            r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True, check=True)
            out.append(float(r.stdout.strip()) + 0.15)
        out[-1] += TAIL
        return out
    return [max(2.0, len(s) / 15.5) for s in SEGMENTS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir")
    ap.add_argument("--out", default=str(HERE / "out" / "short001.mp4"))
    ap.add_argument("--preview", action="store_true", help="exporte une image par scène au lieu de la vidéo")
    a = ap.parse_args()
    durs = durations(a.audio_dir)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    (HERE / "out").mkdir(exist_ok=True)
    (HERE / "out" / "timings.json").write_text(json.dumps(durs, indent=1))

    if a.preview:
        for i, (sc, d) in enumerate(zip(SCENES, durs)):
            t = d * 0.8
            base = background(t)
            img = base.copy()
            sc(img, t, d)
            if SUBS[i]:
                subtitle(img, SEGMENTS[i].split(), t, d)
            img.save(HERE / "out" / f"preview_{i+1:02d}.png")
        return

    total = sum(durs)
    nframes = int(math.ceil(total * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if a.audio_dir:
        concat = HERE / "out" / "voice.wav"
        # concatène les plans avec 0,15 s de silence après chacun (+ fin)
        inputs, filt = [], []
        for i in range(1, 11):
            inputs += ["-i", str(Path(a.audio_dir) / f"seg{i:02d}.mp3")]
            pad = 0.15 + (TAIL if i == 10 else 0)
            filt.append(f"[{i-1}:a]aresample=48000,apad=pad_dur={pad}[a{i}]")
        filt.append("".join(f"[a{i}]" for i in range(1, 11)) + "concat=n=10:v=0:a=1[out]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", str(concat)], check=True)
        # durée fixée sur la vidéo (et non -shortest, qui coupait la fin et cassait le pipe)
        cmd += ["-i", str(concat), "-filter:a", "apad", "-c:a", "aac", "-b:a", "192k", "-t", f"{nframes / FPS:.3f}"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    starts = [sum(durs[:i]) for i in range(len(durs))]
    for f in range(nframes):
        T = f / FPS
        i = max(j for j, s in enumerate(starts) if s <= T + 1e-9)
        t, d = T - starts[i], durs[i]
        base = background(T)
        img = base.copy()
        SCENES[i](img, t, d)
        if SUBS[i]:
            subtitle(img, SEGMENTS[i].split(), t, d)
        img = fade_in_out(img, base, t, d, fin=0.15, fout=0.12 if i < len(durs) - 1 else 0.4)
        img = zoom(img, 1.0 + 0.035 * ease_in_out(t / d))
        p.stdin.write(img.tobytes())
    p.stdin.close()
    p.wait()
    print(a.out, round(total, 2), "s")


if __name__ == "__main__":
    main()
