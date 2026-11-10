"""Kit commun La Cyber Facile (Shorts #002+) : rendu, pictos, outro, réflexes.

Usage dans un render.py :
    from kit import *
    run(__file__, SEGMENTS, SCENES, SUBS)
"""
import argparse, json, math, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from lcf import *  # noqa

ROOT = Path(__file__).resolve().parent.parent
LOGO = Image.open(ROOT / "assets/branding/logo_la_cyber_facile_1080.png").convert("RGB")
TAIL = 0.6


# ======================= rendu =======================
def durations(audio_dir, segments):
    if audio_dir:
        out = []
        for i in range(1, len(segments) + 1):
            p = Path(audio_dir) / f"seg{i:02d}.mp3"
            r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                               capture_output=True, text=True, check=True)
            out.append(float(r.stdout.strip()) + 0.15)
        out[-1] += TAIL
        return out
    return [max(2.0, len(s) / 15.5) for s in segments]


def run(script_file, segments, scenes, subs):
    here = Path(script_file).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio-dir")
    ap.add_argument("--out", default=str(here / "out" / "short.mp4"))
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    assert len(segments) == len(scenes) == len(subs)
    (here / "out").mkdir(exist_ok=True)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    durs = durations(a.audio_dir, segments)
    (here / "out" / "timings.json").write_text(json.dumps(durs, indent=1))
    n = len(segments)

    def frame(T, starts):
        i = max(j for j, s in enumerate(starts) if s <= T + 1e-9)
        t, d = T - starts[i], durs[i]
        base = background(T)
        img = base.copy()
        scenes[i](img, t, d)
        if subs[i]:
            subtitle(img, segments[i].split(), t, d)
        img = fade_in_out(img, base, t, d, fin=0.15, fout=0.12 if i < n - 1 else 0.4)
        return zoom(img, 1.0 + 0.035 * ease_in_out(t / d))

    starts = [sum(durs[:i]) for i in range(n)]
    if a.preview:
        for i in range(n):
            frame(starts[i] + durs[i] * 0.75, starts).save(here / "out" / f"preview_{i+1:02d}.png")
        return
    total = sum(durs)
    nframes = int(math.ceil(total * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-"]
    if a.audio_dir:
        concat = here / "out" / "voice.wav"
        inputs, filt = [], []
        for i in range(1, n + 1):
            inputs += ["-i", str(Path(a.audio_dir) / f"seg{i:02d}.mp3")]
            pad = 0.15 + (TAIL if i == n else 0)
            filt.append(f"[{i-1}:a]aresample=48000,apad=pad_dur={pad}[a{i}]")
        filt.append("".join(f"[a{i}]" for i in range(1, n + 1)) + f"concat=n={n}:v=0:a=1[out]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", str(concat)], check=True)
        cmd += ["-i", str(concat), "-filter:a", "apad", "-c:a", "aac", "-b:a", "192k", "-t", f"{nframes / FPS:.3f}"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(nframes):
        p.stdin.write(frame(f / FPS, starts).tobytes())
    p.stdin.close()
    p.wait()
    print(a.out, round(total, 2), "s")


# ======================= pictos =======================
def D(img):
    return ImageDraw.Draw(img, "RGBA")


def wifi_icon(img, cx, cy, r, color, k=1.0, alpha=255):
    """Icône Wi-Fi : 3 arcs + point ; k (0..1) fait apparaître les arcs un par un."""
    d = D(img)
    d.ellipse([cx - r * 0.13, cy - r * 0.13, cx + r * 0.13, cy + r * 0.13], fill=color + (alpha,))
    for i in range(3):
        kk = clamp(k * 3 - i)
        if kk <= 0:
            continue
        rr = r * (0.42 + 0.29 * i)
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 225, 315, fill=color + (int(alpha * kk),), width=max(4, int(r * 0.13)))


def person(img, cx, cy, s, color, alpha=255):
    d = D(img)
    d.ellipse([cx - 45 * s, cy - 150 * s, cx + 45 * s, cy - 60 * s], fill=color + (alpha,))
    d.rounded_rectangle([cx - 80 * s, cy - 45 * s, cx + 80 * s, cy + 90 * s], radius=int(60 * s), fill=color + (alpha,))


def hacker(img, cx, cy, s, alpha=255):
    """Silhouette à capuche (rouge), visage sombre + yeux."""
    d = D(img)
    d.pieslice([cx - 110 * s, cy - 190 * s, cx + 110 * s, cy + 30 * s], 180, 360, fill=RED + (alpha,))
    d.rounded_rectangle([cx - 110 * s, cy - 80 * s, cx + 110 * s, cy + 120 * s], radius=int(50 * s), fill=RED + (alpha,))
    d.ellipse([cx - 62 * s, cy - 140 * s, cx + 62 * s, cy - 10 * s], fill=DARK + (alpha,))
    for ex in (-24, 24):
        d.ellipse([cx + ex * s - 9 * s, cy - 82 * s, cx + ex * s + 9 * s, cy - 64 * s], fill=WHITE + (alpha,))


def laptop(img, cx, cy, s=1.0, color=(60, 75, 100)):
    d = D(img)
    w, h = 760 * s, 470 * s
    x0, y0 = cx - w / 2, cy - h / 2
    glow(img, [x0, y0, x0 + w, y0 + h], CYAN, 50, 40)
    d = D(img)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(26 * s), fill=(22, 30, 50, 255), outline=color + (255,), width=5)
    d.polygon([(x0 - 60 * s, y0 + h + 10 * s), (x0 + w + 60 * s, y0 + h + 10 * s), (x0 + w + 20 * s, y0 + h + 50 * s), (x0 - 20 * s, y0 + h + 50 * s)],
              fill=(40, 52, 76, 255))
    return (x0 + 20 * s, y0 + 20 * s, x0 + w - 20 * s, y0 + h - 20 * s)


def padlock(img, cx, cy, s, color, open_k=0.0, alpha=255):
    d = D(img)
    lift = 40 * s * open_k
    d.arc([cx - 70 * s, cy - 170 * s - lift, cx + 70 * s, cy - 30 * s - lift], 180, 360, fill=color + (alpha,), width=int(26 * s))
    d.line([cx - 57 * s, cy - 100 * s - lift, cx - 57 * s, cy - 30 * s - lift], fill=color + (alpha,), width=int(26 * s))
    if open_k < 0.5:
        d.line([cx + 57 * s, cy - 100 * s - lift, cx + 57 * s, cy - 30 * s], fill=color + (alpha,), width=int(26 * s))
    d.rounded_rectangle([cx - 110 * s, cy - 40 * s, cx + 110 * s, cy + 130 * s], radius=int(30 * s), fill=color + (alpha,))
    d.ellipse([cx - 18 * s, cy + 20 * s, cx + 18 * s, cy + 56 * s], fill=DARK + (alpha,))
    d.rectangle([cx - 7 * s, cy + 40 * s, cx + 7 * s, cy + 90 * s], fill=DARK + (alpha,))


def key(img, cx, cy, s, color, angle=0, alpha=255):
    layer = Image.new("RGBA", (int(420 * s) + 4, int(180 * s) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([0, 0, 170 * s, 170 * s], outline=color + (alpha,), width=int(30 * s))
    d.rectangle([150 * s, 70 * s, 410 * s, 100 * s], fill=color + (alpha,))
    for x in (300, 360):
        d.rectangle([x * s, 100 * s, (x + 30) * s, 150 * s], fill=color + (alpha,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


def qr(img, x, y, size, seed, color=DARK, bg=WHITE, alpha=255):
    """QR code décoratif (pas un vrai QR scannable)."""
    rnd = random.Random(seed)
    n = 21
    c = size / n
    d = D(img)
    d.rounded_rectangle([x - c, y - c, x + size + c, y + size + c], radius=int(c), fill=bg + (alpha,))
    for i in range(n):
        for j in range(n):
            finder = (i < 7 and j < 7) or (i < 7 and j >= n - 7) or (i >= n - 7 and j < 7)
            if finder:
                ii, jj = (i % 14 if i >= n - 7 else i) - (0 if i < 7 else n - 7), j
            if finder:
                fi = i if i < 7 else i - (n - 7)
                fj = j if j < 7 else j - (n - 7)
                on = fi in (0, 6) or fj in (0, 6) or (2 <= fi <= 4 and 2 <= fj <= 4)
            else:
                on = rnd.random() < 0.5
            if on:
                d.rectangle([x + j * c, y + i * c, x + (j + 1) * c, y + (i + 1) * c], fill=color + (alpha,))


def window(img, box, title, color, k=1.0, body=(24, 33, 54)):
    """Fenêtre type navigateur / pop-up qui apparaît en rebond (k)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    s = 0.7 + 0.3 * back_out(k)
    x0, x1 = cx - (cx - x0) * s, cx + (x1 - cx) * s
    y0, y1 = cy - (cy - y0) * s, cy + (y1 - cy) * s
    a = int(255 * clamp(k * 1.5))
    d = D(img)
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=body + (a,), outline=color + (a,), width=6)
    d.rounded_rectangle([x0, y0, x1, y0 + 74], radius=26, fill=color + (int(a * 0.25),))
    for i, c in enumerate([(239, 68, 68), (234, 179, 8), (34, 197, 94)]):
        d.ellipse([x0 + 28 + i * 38, y0 + 26, x0 + 50 + i * 38, y0 + 48], fill=c + (a,))
    if title:
        d.text(((x0 + x1) / 2, y0 + 37), title, font=font(34, "SemiBold"), fill=WHITE + (a,), anchor="mm")
    return (x0, y0 + 74, x1, y1)


def envelope(img, cx, cy, s, color, alpha=255):
    d = D(img)
    w, h = 120 * s, 80 * s
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=color + (alpha,))
    d.line([(cx - w / 2, cy - h / 2), (cx, cy + 6 * s), (cx + w / 2, cy - h / 2)], fill=DARK + (alpha,), width=max(2, int(6 * s)))


def chip(img, cx, cy, txt, color, k=1.0, size=52, fill=None):
    """Étiquette arrondie (pilule) avec texte."""
    if k <= 0:
        return
    f = font(size, "ExtraBold")
    w = f.getlength(txt) + 70
    h = size * 1.7
    s = 0.6 + 0.4 * back_out(k)
    w2, h2 = w * s, h * s
    a = int(255 * clamp(k * 1.6))
    d = D(img)
    d.rounded_rectangle([cx - w2 / 2, cy - h2 / 2, cx + w2 / 2, cy + h2 / 2], radius=int(h2 / 2),
                        fill=(fill or (color[0] // 5, color[1] // 5, color[2] // 5)) + (a,), outline=color + (a,), width=5)
    if k > 0.5:
        d.text((cx, cy), txt, font=font(int(size * s), "ExtraBold"), fill=WHITE + (a,), anchor="mm")


def counter(img, cx, cy, value, size, color, t, start, dur=0.8, suffix="", prefix=""):
    k = ease_out(prog(t, start, dur))
    if t < start:
        return
    v = int(round(value * k))
    D(img).text((cx, cy), f"{prefix}{v:,}{suffix}".replace(",", " "), font=font(size, "Black"), fill=color + (255,), anchor="mm")


def glitch_text(img, cx, cy, txt, size, color, t, start=0.0, maxw=960):
    """Texte qui arrive en « glitch » (décalages rouge/cyan) puis se stabilise."""
    k = prog(t, start, 0.45)
    if k <= 0:
        return
    lines = wrap(txt, size, "Black", maxw)
    lh = int(size * 1.12)
    f = font(size, "Black")
    d = D(img)
    jitter = (1 - k) * 26
    y0 = cy - lh * (len(lines) - 1) / 2
    rnd = random.Random(int(t * 30))
    for i, l in enumerate(lines):
        y = y0 + lh * i
        if k < 1:
            dx = rnd.uniform(-jitter, jitter)
            d.text((cx + dx - 8, y), l, font=f, fill=RED + (150,), anchor="mm")
            d.text((cx - dx + 8, y), l, font=f, fill=CYAN + (150,), anchor="mm")
        d.text((cx, y), l, font=f, fill=color + (int(255 * clamp(k * 2)),), anchor="mm")


def arrow(img, p0, p1, color, k=1.0, width=10, alpha=255):
    if k <= 0:
        return
    x0, y0 = p0
    x1, y1 = x0 + (p1[0] - x0) * k, y0 + (p1[1] - y0) * k
    d = D(img)
    d.line([x0, y0, x1, y1], fill=color + (alpha,), width=width)
    ang = math.atan2(y1 - y0, x1 - x0)
    L = width * 3
    d.polygon([(x1, y1), (x1 - L * math.cos(ang - 0.45), y1 - L * math.sin(ang - 0.45)),
               (x1 - L * math.cos(ang + 0.45), y1 - L * math.sin(ang + 0.45))], fill=color + (alpha,))


def cross(img, cx, cy, r, color, k=1.0, width=22):
    if k <= 0:
        return
    d = D(img)
    a = r * ease_out(k)
    d.line([cx - a, cy - a, cx + a, cy + a], fill=color + (255,), width=width)
    d.line([cx - a, cy + a, cx + a, cy - a], fill=color + (255,), width=width)


# ======================= réflexes (3 mises en scène) =======================
def reflex_checklist(items, n, title="3 réflexes"):
    """Liste à cocher : les réflexes s'empilent, le courant se coche."""
    def s(img, t, d):
        pop_text(img, W / 2, 300, title, 96, GREEN, t, 0 if n == 0 else -1)
        dr = D(img)
        for i in range(n + 1):
            y = 560 + i * 250
            k = 1.0 if i < n else ease_out(prog(t, 0.05, 0.4))
            x = 90 - (1 - k) * 500
            a = int(255 * k)
            cur = i == n
            dr.rounded_rectangle([x, y - 95, x + 900, y + 95], radius=36, fill=(20, 40, 34, a) if cur else (18, 30, 30, a),
                                 outline=(GREEN if cur else (40, 90, 60)) + (a,), width=6 if cur else 3)
            ck = 1.0 if i < n else ease_out(prog(t, 0.5, 0.3))
            dr.ellipse([x + 40, y - 45, x + 130, y + 45], outline=GREEN + (a,), width=6)
            if ck > 0:
                icon_check(dr, x + 85, y, 45 * ck, GREEN)
            lines = wrap(items[i], 54 if cur else 46, "ExtraBold", 680)
            lh = 60 if cur else 52
            for j, l in enumerate(lines):
                dr.text((x + 170, y + (j - (len(lines) - 1) / 2) * lh), l, font=font(54 if cur else 46, "ExtraBold"),
                        fill=(WHITE if cur else (160, 200, 175)) + (a,), anchor="lm")
    return s


def reflex_bigslide(items, n, icons=None):
    """Grand numéro + carte qui glisse depuis la droite (une règle plein écran)."""
    def s(img, t, d):
        dr = D(img)
        k = ease_out(prog(t, 0, 0.45))
        num_x = W / 2 + (1 - k) * 600
        dr.text((num_x, 620), str(n + 1), font=font(420, "Black"), fill=GREEN + (int(70 + 185 * k),), anchor="mm")
        dr.text((W / 2, 300), "Réflexe", font=font(64, "Bold"), fill=GREY + (int(255 * k),), anchor="mm")
        for i in range(3):
            cx = W / 2 + (i - 1) * 60
            col = GREEN if i <= n else (60, 75, 100)
            dr.ellipse([cx - 14, 380 - 14, cx + 14, 380 + 14], fill=col + (255,))
        ck = back_out(prog(t, 0.25, 0.45))
        if ck > 0:
            x = W / 2 + (1 - ck) * 900
            glow(img, [x - 440, 960, x + 440, 1300], GREEN, 60, 50)
            dr = D(img)
            dr.rounded_rectangle([x - 440, 960, x + 440, 1300], radius=40, fill=(20, 40, 34, 255), outline=GREEN + (255,), width=6)
            lines = wrap(items[n], 70, "ExtraBold", 780)
            for j, l in enumerate(lines):
                dr.text((x, 1130 + (j - (len(lines) - 1) / 2) * 82), l, font=font(70, "ExtraBold"), fill=WHITE + (255,), anchor="mm")
    return s


def reflex_trio(items, n, drawers):
    """Trois tuiles côte à côte avec pictos ; la courante grossit, les précédentes cochées."""
    def s(img, t, d):
        pop_text(img, W / 2, 300, "Comment te protéger", 76, GREEN, t, 0 if n == 0 else -1)
        dr = D(img)
        for i in range(3):
            cx = W / 2 + (i - 1) * 330
            cur = i == n
            k = ease_out(prog(t, 0.0, 0.4)) if cur else 1.0
            sc = 1.0 + 0.18 * k if cur else 0.92
            w, h = 250 * sc, 250 * sc
            col = GREEN if i <= n else (60, 75, 100)
            dr.rounded_rectangle([cx - w / 2, 640 - h / 2, cx + w / 2, 640 + h / 2], radius=40,
                                 fill=(20, 40, 34, 255) if i <= n else (22, 30, 50, 255), outline=col + (255,), width=6 if cur else 3)
            drawers[i](img, cx, 640, 0.9 * sc, col)
            if i < n:
                icon_check(D(img), cx + w / 2 - 20, 640 - h / 2 + 20, 34, GREEN)
            dr = D(img)
        pop_text(img, W / 2, 1060, items[n], 80, WHITE, t, 0.3, maxw=920)
        # soulignement animé
        uk = ease_out(prog(t, 0.6, 0.5))
        if uk > 0:
            dr.rounded_rectangle([W / 2 - 300 * uk, 1180, W / 2 + 300 * uk, 1192], radius=6, fill=GREEN + (255,))
    return s


# ======================= outro (variantes) =======================
def outro(variant=0):
    def s(img, t, d):
        k = back_out(prog(t, 0, 0.5))
        size = max(2, int(480 * k))
        logo = LOGO.resize((size, size), Image.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
        cy = 760
        if variant == 1:  # le logo tourne légèrement
            logo = logo.rotate(math.sin(t * 2.5) * 6, resample=Image.BICUBIC)
        if variant == 2:  # anneaux qui pulsent
            dr = D(img)
            for i in range(3):
                ph = ((t * 0.9) + i / 3) % 1
                r = 260 + ph * 260
                dr.ellipse([W / 2 - r, cy - r, W / 2 + r, cy + r], outline=CYAN + (int(160 * (1 - ph)),), width=5)
        img.paste(logo, (int(W / 2 - size / 2), int(cy - size / 2)), mask)
        pop_text(img, W / 2, 1130, "La Cyber Facile", 92, WHITE, t, 0.25)
        pop_text(img, W / 2, 1230, "@lacyberfacile", 56, CYAN, t, 0.4, weight="SemiBold")
        bk = back_out(prog(t, 0.6, 0.4))
        if bk > 0:
            pulse = 1 + 0.04 * math.sin(t * 7)
            bw, bh = 560 * bk * pulse, 130 * bk * pulse
            dr = D(img)
            dr.rounded_rectangle([W / 2 - bw / 2, 1410 - bh / 2, W / 2 + bw / 2, 1410 + bh / 2], radius=65, fill=RED + (255,))
            if bk > 0.8:
                dr.text((W / 2, 1410), "S'ABONNER", font=font(58, "Black"), fill=WHITE + (255,), anchor="mm")
            if variant == 1 and t > 1.2:  # doigt qui tape le bouton
                kk = ease_out(prog(t, 1.2, 0.4))
                fx, fy = W / 2 + 180 + (1 - kk) * 200, 1440 + (1 - kk) * 250
                dr.ellipse([fx - 36, fy - 36, fx + 36, fy + 36], fill=WHITE + (210,))
    return s
