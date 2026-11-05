#!/usr/bin/env python3
"""build_pptx.py — PPTX versions of six social templates, built with python-pptx.
Slide size = the platform's pixels at 96 dpi (1080 px = 11.25 in). Fonts are named Fraunces Light (display),
Inter Tight (eyebrows, wall-label titles) and Inter (body). The project image is embedded as a JPG that Pillow has
already cropped to the frame and darkened with the brand veil (assets/, rebuilt every run); the logo is the production
PNG from 02_LOGO_SYSTEM. Every line of copy is an editable text box. Proof: LibreOffice opens each PPTX and exports
slide 1 to proofs/<name>.png.   Run from this folder:  python3 build_pptx.py"""
import pathlib, subprocess
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn

HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent.parent
IMG = ROOT / '00_ORIGINAL_ASSETS_BACKUP/images/img'
LOGO = ROOT / '02_LOGO_SYSTEM/PNG/sanzeed-primary-wordmark--full-colour-dark-1200w.png'
OUT = HERE / 'PPTX'; ASSETS = OUT / 'assets'; PROOFS = OUT / 'proofs'
for d in (OUT, ASSETS, PROOFS): d.mkdir(exist_ok=True)

WHITE, SILVER, MIST, GOLD = RGBColor(0xF5, 0xF5, 0xF7), RGBColor(0xA1, 0xA1, 0xA6), RGBColor(0x80, 0x80, 0x86), RGBColor(0xE9, 0xB2, 0x5A)
FRAUNCES, TIGHT, INTER = 'Fraunces Light', 'Inter Tight', 'Inter'
px = lambda n: Inches(n / 96)

# ---------- images: cover-crop to the frame and bake the veil (the CSS gradients, as alpha stops) ----------
def gradient(size, stops, horizontal=False):
    n = size[0] if horizontal else size[1]
    strip = Image.new('L', (n, 1))
    for i in range(n):
        t = i / (n - 1)
        for (t0, a0), (t1, a1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                a = a0 + (a1 - a0) * (t - t0) / (t1 - t0) if t1 > t0 else a1; break
        strip.putpixel((i, 0), int(255 * a))
    return strip.resize(size) if horizontal else strip.rotate(90, expand=True).resize(size)

def bake(src, name, w, h, focal=(0.5, 0.5), veils=(), rounded=0, canvas=None):
    im = Image.open(src).convert('RGB'); s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * focal[0]); y = round((im.height - h) * focal[1]); im = im.crop((x, y, x + w, y + h))
    for stops, horizontal in veils:
        im = Image.composite(Image.new('RGB', (w, h), 'black'), im, gradient((w, h), stops, horizontal))
    if rounded:  # the room: rounded plate on a black ground
        mask = Image.new('L', (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), rounded, fill=255)
        im = Image.composite(im, Image.new('RGB', (w, h), 'black'), mask)
    out = ASSETS / f'{name}.jpg'; im.save(out, quality=88, subsampling=0, optimize=True); return out

VEIL_V = [(0, .88), (.14, .72), (.32, .18), (.56, .42), (.80, .90), (1, .96)]
VEIL_YT_H = [(0, .94), (.34, .86), (.60, .45), (1, .15)]; VEIL_YT_V = [(0, .55), (.30, 0), (.70, 0), (1, .60)]
VEIL_FB_H = [(0, .97), (.36, .92), (.60, .62), (1, .30)]; VEIL_FB_V = [(0, .58), (.40, .05), (1, .40)]
VEIL_X_H = [(0, .94), (.42, .88), (.64, .60), (1, .30)]

# ---------- text ----------
def text(slide, x, y, w, h, runs, font, size, color=WHITE, bold=False, italic=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, tracking=0, caps=False):
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h)); tf = tb.text_frame
    tf.word_wrap = True; tf.auto_size = MSO_AUTO_SIZE.NONE; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = align; p.line_spacing = spacing
    for t, c in (runs if isinstance(runs, list) else [(runs, color)]):
        r = p.add_run(); r.text = t.upper() if caps else t; f = r.font
        f.name = font; f.size = Pt(size * 0.75); f.bold = bold; f.italic = italic; f.color.rgb = c
        if tracking: r._r.get_or_add_rPr().set('spc', str(int(tracking * 100)))
    return tb

def headline(slide, x, y, w, h, s, size, lit=False, anchor=MSO_ANCHOR.TOP):
    runs = [(s, WHITE)]
    if lit:
        head, _, last = s.strip().rpartition(' '); runs = [(head + ' ', WHITE), (last, GOLD)]
    return text(slide, x, y, w, h, runs, FRAUNCES, size, spacing=1.04, anchor=anchor)

def eyebrow(slide, x, y, w, s, size=18, align=PP_ALIGN.LEFT): return text(slide, x, y, w, size * 1.4, s, TIGHT, size, GOLD, bold=True, tracking=size * 0.12 * 0.75, caps=True, align=align)
def label(slide, x, y, w, title, place, ts=28, ps=24):
    text(slide, x, y, w, ts * 1.3, title, TIGHT, ts, WHITE, bold=True)
    text(slide, x, y + ts * 1.3 + 4, w, ps * 1.4, place, INTER, ps, SILVER)
def site(slide, x, y, w, s, size=20, align=PP_ALIGN.RIGHT): return text(slide, x, y, w, size * 1.3, s, INTER, size, MIST, align=align)

def deck(w, h):
    prs = Presentation(); prs.slide_width = px(w); prs.slide_height = px(h)
    s = prs.slides.add_slide(prs.slide_layouts[6]); fill = s.background.fill; fill.solid(); fill.fore_color.rgb = RGBColor(0, 0, 0)
    return prs, s
def photo(slide, path, x, y, w, h): return slide.shapes.add_picture(str(path), px(x), px(y), px(w), px(h))
def logo(slide, x, y, w): return slide.shapes.add_picture(str(LOGO), px(x), px(y), width=px(w))

def save(prs, name):
    out = OUT / f'{name}.pptx'; prs.save(out)
    subprocess.run(['soffice', '--headless', '--convert-to', 'png', '--outdir', str(PROOFS), str(out)], check=True, capture_output=True)
    print('  wrote', out.relative_to(ROOT), '· proof', (PROOFS / f'{name}.png').relative_to(ROOT))

# 1 · Instagram post — project 1080×1080
prs, s = deck(1080, 1080)
photo(s, bake(IMG / 'case/prime-minister-museum-03.webp', 'ig-post-project', 1080, 1080, (0.5, 0.5), [(VEIL_V, False)]), 0, 0, 1080, 1080)
logo(s, 72, 72, 220); site(s, 680, 78, 328, 'sanzeed.com/work')
eyebrow(s, 72, 584, 900, 'Case study · Museums & Experience Centres')
headline(s, 72, 620, 900, 290, 'A corridor you walk in order.', 84, anchor=MSO_ANCHOR.BOTTOM)
label(s, 72, 920, 900, 'Prime Minister Museum', 'New Delhi', 24, 22)
save(prs, 'sanzeed-ig-post--project-1080x1080')

# 2 · Instagram story — project 1080×1920 (plate 5:4, copy inside the 1080×1420 centre-safe band)
prs, s = deck(1080, 1920)
photo(s, bake(IMG / 'case/ram-katha-show-08.webp', 'ig-story-project', 920, 736, (0.5, 0.5), rounded=28), 80, 380, 920, 736)
logo(s, 80, 270, 240); eyebrow(s, 600, 276, 400, 'Case study', 20, PP_ALIGN.RIGHT)
headline(s, 80, 1150, 920, 230, 'The building is the screen.', 84, lit=True, anchor=MSO_ANCHOR.BOTTOM)
label(s, 80, 1400, 920, 'Ram Katha Show', 'Ayodhya', 30, 26)
site(s, 80, 1626, 920, 'sanzeed.com/work/ram-katha-show', 22, PP_ALIGN.LEFT)
save(prs, 'sanzeed-ig-story--project-1080x1920')

# 3 · LinkedIn post — project 1200×627
prs, s = deck(1200, 627)
photo(s, bake(IMG / 'army-museum-abu-dhabi.webp', 'li-post-project', 1200, 627, (0.52, 0.5), [(VEIL_V, False)]), 0, 0, 1200, 627)
logo(s, 56, 56, 180); site(s, 800, 60, 344, 'sanzeed.com/#galleries', 16)
eyebrow(s, 56, 360, 900, 'Museums & Experience Centres', 15)
headline(s, 56, 384, 1040, 160, 'One vision, from the brief to opening night.', 56, anchor=MSO_ANCHOR.BOTTOM)
label(s, 56, 552, 900, 'Army Museum Abu Dhabi', 'Abu Dhabi', 24, 20)
save(prs, 'sanzeed-li-post--project-1200x627')

# 4 · YouTube thumbnail — project film 1280×720
prs, s = deck(1280, 720)
photo(s, bake(IMG / 'case/ram-katha-show-08.webp', 'yt-thumb-project', 1280, 720, (0.5, 0.5), [(VEIL_YT_H, True), (VEIL_YT_V, False)]), 0, 0, 1280, 720)
logo(s, 72, 72, 210)
eyebrow(s, 72, 262, 700, 'Project film', 20)
headline(s, 72, 296, 820, 274, 'The building is the screen.', 96, lit=True, anchor=MSO_ANCHOR.BOTTOM)
label(s, 72, 584, 720, 'Ram Katha Show', 'Ayodhya', 32, 26)
save(prs, 'sanzeed-yt-thumbnail--project-1280x720')

# 5 · Facebook cover 1640×624 (copy inside the 1250×463 centre-safe area)
prs, s = deck(1640, 624)
photo(s, bake(IMG / 'case/prime-minister-museum-03.webp', 'fb-cover', 1640, 624, (0.62, 0.5), [(VEIL_FB_H, True), (VEIL_FB_V, False)]), 0, 0, 1640, 624)
logo(s, 195, 104, 230)
headline(s, 195, 236, 940, 212, 'Experiential design you can walk into.', 58, anchor=MSO_ANCHOR.BOTTOM)
label(s, 195, 460, 900, 'Sanzeed Mirza', 'Experiential Design Consultant · New Delhi', 22, 19)
site(s, 1145, 494, 300, 'sanzeed.com', 16)
save(prs, 'sanzeed-fb-cover-1640x624')

# 6 · X header 1500×500 (bottom-left 440×220 kept clear for the avatar)
prs, s = deck(1500, 500)
photo(s, bake(IMG / 'g20-tree-show.webp', 'x-header', 1500, 500, (0.5, 0.45), [(VEIL_X_H, True)]), 0, 0, 1500, 500)
logo(s, 64, 52, 220)
headline(s, 520, 120, 916, 176, 'Experiential design you can walk into.', 58, anchor=MSO_ANCHOR.BOTTOM)
label(s, 520, 306, 916, 'Sanzeed Mirza', 'Experiential Design Consultant · New Delhi · sanzeed.com', 22, 18)
save(prs, 'sanzeed-x-header-1500x500')
print('done.')
