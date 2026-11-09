"""Moteur d'animation La Cyber Facile — primitives PIL pour Shorts 1080x1920.

Chaque scène est une fonction draw(img, t, d) où t = temps local (s) et d = durée de la scène.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FPS = 30
BG, BG2 = (10, 15, 28), (17, 26, 46)
CYAN, GREEN, RED = (34, 211, 238), (34, 197, 94), (239, 68, 68)
WHITE, GREY, DARK = (248, 250, 252), (148, 163, 184), (8, 12, 22)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
_fonts = {}


def font(size, weight="Bold"):
    key = (size, weight)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f"{FONT_DIR}Inter-{weight}.otf", size)
    return _fonts[key]


# ---------- easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x):
    x = clamp(x)
    return 3 * x * x - 2 * x * x * x


def back_out(x, s=1.7):
    x = clamp(x)
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def prog(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else float(t >= start)


def mix(c1, c2, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))


# ---------- background ----------
_bg_cache = None


def background(t):
    """Fond sombre + grille de points qui dérive (jamais figé)."""
    global _bg_cache
    if _bg_cache is None:
        g = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(g)
        for y in range(H):
            d.line([(0, y), (W, y)], fill=mix(BG2, BG, y / H))
        _bg_cache = g
    img = _bg_cache.copy()
    d = ImageDraw.Draw(img, "RGBA")
    off = (t * 18) % 90
    for gx in range(-90, W + 90, 90):
        for gy in range(-90, H + 90, 90):
            x, y = gx + off, gy + off * 0.6
            a = int(28 + 18 * math.sin((gx + gy) * 0.01 + t * 1.5))
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=CYAN + (a,))
    return img


def glow(img, box, color, radius=60, alpha=90):
    """Halo flou derrière une zone."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box, radius=40, fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(radius))
    img.paste(layer, (0, 0), layer)


# ---------- texte ----------
def text_center(d, cx, cy, txt, size, color, weight="ExtraBold", alpha=255, anchor="mm"):
    f = font(size, weight)
    d.text((cx, cy), txt, font=f, fill=color + (alpha,), anchor=anchor)


def wrap(txt, size, weight, maxw):
    f = font(size, weight)
    words, lines, cur = txt.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if f.getlength(test) <= maxw:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def pop_text(img, cx, cy, txt, size, color, t, start=0.0, weight="ExtraBold", maxw=940):
    """Texte qui apparaît avec un léger rebond (scale) + fondu."""
    k = prog(t, start, 0.35)
    if k <= 0:
        return
    s = 0.6 + 0.4 * back_out(k)
    lines = wrap(txt, size, weight, maxw)
    f = font(size, weight)
    lh = int(size * 1.15)
    tw = int(max(f.getlength(l) for l in lines)) + 40
    th = lh * len(lines) + 30
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, l in enumerate(lines):
        ld.text((tw / 2, 15 + lh * i + lh / 2), l, font=f, fill=color + (255,), anchor="mm")
    nw, nh = max(1, int(tw * s)), max(1, int(th * s))
    layer = layer.resize((nw, nh), Image.LANCZOS)
    if k < 1:
        a = layer.getchannel("A").point(lambda v: int(v * ease_out(k)))
        layer.putalpha(a)
    img.paste(layer, (int(cx - nw / 2), int(cy - nh / 2)), layer)


def subtitle(img, words, t, d, y=1640):
    """Sous-titres : 2 à 4 mots à la fois, mot courant surligné.
    Le timing est réparti au prorata de la longueur des mots (approximation)."""
    if not words:
        return
    # rattache la ponctuation isolée (« ? », « : », « … ») au mot précédent
    merged = []
    for w in words:
        if merged and all(c in "?!:;…»" for c in w):
            merged[-1] += " " + w
        else:
            merged.append(w)
    words = merged
    total = sum(len(w) + 2 for w in words)
    acc, times = 0, []
    for w in words:
        times.append(acc / total * d)
        acc += len(w) + 2
    cur = max(i for i, s in enumerate(times) if s <= t) if t >= 0 else 0
    chunk = 3
    c0 = (cur // chunk) * chunk
    group = words[c0:c0 + chunk]
    f = font(64, "ExtraBold")
    spacing = 22
    widths = [f.getlength(w) for w in group]
    total_w = sum(widths) + spacing * (len(group) - 1)
    pad = 28
    dr = ImageDraw.Draw(img, "RGBA")
    dr.rounded_rectangle([W / 2 - total_w / 2 - pad, y - 60, W / 2 + total_w / 2 + pad, y + 60],
                         radius=30, fill=(0, 0, 0, 150))
    x = W / 2 - total_w / 2
    for i, w in enumerate(group):
        col = CYAN if c0 + i == cur else WHITE
        dr.text((x, y), w, font=f, fill=col, anchor="lm")
        x += widths[i] + spacing


# ---------- objets ----------
def phone(img, cx, cy, scale=1.0, tilt_y=0):
    """Téléphone stylisé ; renvoie la boîte de l'écran."""
    pw, ph = int(560 * scale), int(1040 * scale)
    x0, y0 = int(cx - pw / 2), int(cy - ph / 2 + tilt_y)
    d = ImageDraw.Draw(img, "RGBA")
    glow(img, [x0, y0, x0 + pw, y0 + ph], CYAN, radius=50, alpha=50)
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=int(70 * scale), fill=(22, 30, 50), outline=(60, 75, 100), width=4)
    sx0, sy0, sx1, sy1 = x0 + int(22 * scale), y0 + int(22 * scale), x0 + pw - int(22 * scale), y0 + ph - int(22 * scale)
    d.rounded_rectangle([sx0, sy0, sx1, sy1], radius=int(52 * scale), fill=(12, 17, 30))
    d.rounded_rectangle([cx - 60 * scale, sy0 + 14 * scale, cx + 60 * scale, sy0 + 44 * scale], radius=16, fill=(0, 0, 0))
    return (sx0, sy0, sx1, sy1)


def sms_bubble(img, x, y, maxw, lines, t, start, color_bg=(38, 48, 70), link_idx=None, link_col=CYAN):
    """Bulle SMS qui glisse depuis la gauche."""
    k = ease_out(prog(t, start, 0.4))
    if k <= 0:
        return None
    f = font(34, "Medium")
    lh = 46
    bw = int(max(f.getlength(l) for l in lines)) + 50
    bw = min(bw, maxw)
    bh = lh * len(lines) + 36
    dx = int((1 - k) * -120)
    d = ImageDraw.Draw(img, "RGBA")
    a = int(255 * k)
    d.rounded_rectangle([x + dx, y, x + dx + bw, y + bh], radius=30, fill=color_bg + (a,))
    for i, l in enumerate(lines):
        col = link_col if i == link_idx else WHITE
        d.text((x + dx + 25, y + 18 + lh * i), l, font=f, fill=col + (a,))
        if i == link_idx:
            lw = f.getlength(l)
            d.line([x + dx + 25, y + 18 + lh * i + 40, x + dx + 25 + lw, y + 18 + lh * i + 40], fill=col + (a,), width=3)
    return (x + dx, y, x + dx + bw, y + bh)


def stamp(img, cx, cy, txt, color, t, start, size=150, angle=-12):
    """Tampon qui s'écrase sur l'écran (scale 2.2 -> 1) + tremblement."""
    k = prog(t, start, 0.25)
    if k <= 0:
        return
    f = font(size, "Black")
    tw = int(f.getlength(txt)) + 80
    th = int(size * 1.4)
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([6, 6, tw - 6, th - 6], radius=24, outline=color + (255,), width=12)
    ld.text((tw / 2, th / 2), txt, font=f, fill=color + (255,), anchor="mm")
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    s = 2.2 - 1.2 * ease_out(k)
    nw, nh = int(layer.width * s), int(layer.height * s)
    layer = layer.resize((nw, nh), Image.LANCZOS)
    if k < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * k)))
    shake = 0
    since = t - start - 0.25
    if 0 < since < 0.3:
        shake = int(14 * math.sin(since * 80) * (1 - since / 0.3))
    img.paste(layer, (int(cx - nw / 2 + shake), int(cy - nh / 2)), layer)


def glyph(d, cx, cy, ch, size, color, alpha=255):
    """Pictogramme Unicode (DejaVu Sans), ex. ☎ U+260E."""
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    d.text((cx, cy), ch, font=f, fill=color + (alpha,), anchor="mm")


def icon_check(d, cx, cy, r, color, k=1.0):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (int(255 * k),))
    if k > 0.3:
        w = max(4, int(r * 0.22))
        pts = [(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)]
        d.line(pts, fill=DARK + (255,), width=w, joint="curve")


def credit_card(img, cx, cy, scale, angle, alpha=255):
    cw, ch = int(520 * scale), int(330 * scale)
    if cw < 4:
        return
    layer = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=int(30 * scale), fill=(40, 60, 100, alpha))
    ld.rounded_rectangle([int(40 * scale), int(80 * scale), int(120 * scale), int(140 * scale)], radius=int(10 * scale), fill=(230, 190, 90, alpha))
    if scale > 0.3:
        ld.text((int(40 * scale), int(200 * scale)), "•••• •••• •••• ••••", font=font(max(8, int(40 * scale)), "Bold"), fill=WHITE + (alpha,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


def fade_in_out(img, base, t, d, fin=0.18, fout=0.18):
    """Transition : fondu depuis/vers le fond (appliqué en fin de rendu de scène)."""
    k = min(prog(t, 0, fin), 1 - prog(t, d - fout, fout))
    if k >= 1:
        return img
    return Image.blend(base, img, k)


def zoom(img, s):
    """Zoom caméra centré (s >= 1)."""
    if abs(s - 1) < 1e-3:
        return img
    nw, nh = int(W * s), int(H * s)
    big = img.resize((nw, nh), Image.BILINEAR)
    x0, y0 = (nw - W) // 2, (nh - H) // 2
    return big.crop((x0, y0, x0 + W, y0 + H))
