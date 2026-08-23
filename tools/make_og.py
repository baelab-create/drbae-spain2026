# -*- coding: utf-8 -*-
"""Dr.BAE Spain 2026 — 4-product lineup thumbnail (og:image + links-hub thumb)."""
import os, sys, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import base64, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'index.html')
OUT  = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'assets')

def embedded(alt):
    """First inline base64 image in index.html whose alt attribute is `alt`."""
    html = embedded._html
    m = re.search(r'alt="%s"[^>]*?src="data:image/(\w+);base64,([A-Za-z0-9+/=]+)"'
                  % re.escape(alt), html)
    if not m:
        raise SystemExit('image not found in index.html: ' + alt)
    return Image.open(io.BytesIO(base64.b64decode(m.group(2)))).convert('RGBA')
embedded._html = io.open(PAGE, encoding='utf-8').read()

W, H  = 1200, 630
BG    = (251, 250, 248)
SANDL = (243, 240, 235)
HAIR  = (218, 213, 203)
NAVY  = (31, 58, 92)
SLATE = (78, 114, 144)
TAUPE = (179, 166, 149)
SUB   = (110, 107, 101)
INK   = (38, 38, 36)

F = 'C:/Windows/Fonts/'
def f(name, size): return ImageFont.truetype(F + name, size)
REG, SB, BOLD, ITAL = 'segoeui.ttf', 'seguisb.ttf', 'segoeuib.ttf', 'segoeuii.ttf'

PRODUCTS = [
    ('Exotokine BLUE',        'EXOTOKINE',  'BLUE',        'Skin Core Booster'),
    ('Exotokine TOCOFORTE',   'EXOTOKINE',  'TOCOFORTE',   'Skin & Scalp Finishing'),
    ('Exotokine BLACK SCALP', 'EXOTOKINE',  'BLACK SCALP', 'Scalp Booster'),
    ('PIDIROENNE PINK',       'PIDIROENNE', 'PINK',        'Soothing & Finishing'),
]

def tracked(d, y, text, font, fill, track=0.0, x=None, cx=None):
    """Letter-spaced text; pass cx to centre it, x to left-align it."""
    ws = [d.textlength(c, font=font) for c in text]
    total = sum(ws) + track * (len(text) - 1)
    px = (cx - total / 2) if cx is not None else x
    for c, w in zip(text, ws):
        d.text((px, y), c, font=font, fill=fill)
        px += w + track
    return total

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

BAND_Y = 292
d.rectangle([0, BAND_Y, W, H], fill=SANDL)
d.line([(0, BAND_Y), (W, BAND_Y)], fill=HAIR, width=1)
d.rectangle([0, 0, W, 5], fill=NAVY)

# ---------- logo ----------
logo = embedded('Dr. BAE')
lw = 236
logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
img.paste(logo, (64, 50), logo)

# ---------- headline ----------
tracked(d, 130, 'PROFESSIONAL AESTHETIC SCIENCE  \u00b7  SPAIN 2026',
        f(BOLD, 15), TAUPE, track=1.9, x=66)
d.text((64, 164), 'Exosomes in Professional Aesthetic Care', font=f(BOLD, 41), fill=NAVY)
d.text((64, 220), 'La verdad sobre los exosomas', font=f(ITAL, 25), fill=SLATE)

# ---------- right meta ----------
y = 168
for text, font, col in [('Viernes 28 de agosto  \u00b7  11:00 h (CEST)', f(SB, 16), INK),
                        ('Zoom cient\u00edfico  \u00b7  Peanilla Cosmetics', f(REG, 15), SUB)]:
    d.text((W - 64 - d.textlength(text, font=font), y), text, font=font, fill=col)
    y += 26
d.line([(W - 314, 230), (W - 64, 230)], fill=HAIR, width=1)
t, ft = 'Won-Gyu BAE, Ph.D.  \u00b7  BAE LAB', f(SB, 15)
d.text((W - 64 - d.textlength(t, font=ft), 242), t, font=ft, fill=SLATE)

# ---------- band caption ----------
tracked(d, 316, 'THE PROFESSIONAL LINEUP  \u2014  4 BOOSTERS',
        f(BOLD, 14), TAUPE, track=2.2, cx=W / 2)

# ---------- product row ----------
BH, GAP, TOP = 190, 66, 342
BASE = TOP + BH
loaded = []
for alt, brand, variant, role in PRODUCTS:
    p = embedded(alt)
    p = p.resize((round(p.width * BH / p.height), BH), Image.LANCZOS)
    loaded.append((p, brand, variant, role))

total = sum(p.width for p, *_ in loaded) + GAP * (len(loaded) - 1)
x0 = round((W - total) / 2)

# soft contact shadows
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
cx = x0
for p, *_ in loaded:
    c = cx + p.width / 2
    sd.ellipse([c - p.width * 0.46, BASE - 7, c + p.width * 0.46, BASE + 9], fill=(31, 58, 92, 46))
    cx += p.width + GAP
img = Image.alpha_composite(img.convert('RGBA'),
                            shadow.filter(ImageFilter.GaussianBlur(7))).convert('RGB')
d = ImageDraw.Draw(img)

x = x0
for p, brand, variant, role in loaded:
    img.paste(p, (x, TOP), p)
    c = x + p.width / 2
    tracked(d, 550, brand, f(SB, 11), TAUPE, track=1.6, cx=c)
    tracked(d, 567, variant, f(BOLD, 16), NAVY, track=0.4, cx=c)
    fr = f(REG, 14)
    d.text((c - d.textlength(role, font=fr) / 2, 592), role, font=fr, fill=SUB)
    x += p.width + GAP

os.makedirs(OUT, exist_ok=True)
big = os.path.join(OUT, 'og-spain2026.jpg')
img.save(big, 'JPEG', quality=90, optimize=True, progressive=True)
img.resize((800, 420), Image.LANCZOS).save(os.path.join(OUT, 'thumb-spain2026.jpg'),
                                           'JPEG', quality=88, optimize=True, progressive=True)
print('saved ->', OUT, os.path.getsize(big), 'bytes')
