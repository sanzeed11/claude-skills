#!/usr/bin/env python3
"""Presentation template — PPTX 16:9 (13.333 × 7.5 in) built with python-pptx. Fourteen real slides, one per
layout, so each can be duplicated: title · section divider · agenda · statement · full-bleed image · image + text ·
two-column · three-column cards · stats · timeline · method · quote · team/contact · end card.
Slide master background: Gallery Black. Fonts: Fraunces Light / Inter Tight SemiBold / Inter (install from 04_TYPOGRAPHY)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image, ImageDraw
import numpy as np

D = f'{OUT}/Presentation_Template'
SRC = f'{D}/src'
AS = f'{SRC}/assets'
os.makedirs(AS, exist_ok=True)

BLACK = RGBColor(0, 0, 0); NIGHT = RGBColor(0x0D, 0x0D, 0x0F); CHARCOAL = RGBColor(0x1C, 0x1C, 0x1E); GRAPHITE = RGBColor(0x2A, 0x2A, 0x2D)
GWHITE = RGBColor(0xF5, 0xF5, 0xF7); SILVER = RGBColor(0xA1, 0xA1, 0xA6); MIST = RGBColor(0x80, 0x80, 0x86); LAMP = RGBColor(0xE9, 0xB2, 0x5A)
F_DISPLAY, F_HEAD, F_TEXT = 'Fraunces Light', 'Inter Tight SemiBold', 'Inter'
SW, SH = Inches(13.333), Inches(7.5)
M = Inches(0.9)  # margin

# ------------------------------------------------------------------ assets
def lamp_bg(path, w=1920, h=1080, cx=0.5, cy=0.44, strength=0.46):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = (xx - w * cx) / (w * 0.58); dy = (yy - h * cy) / (h * 0.60)
    d = np.sqrt(dx * dx + dy * dy)
    a = np.interp(d, [0, 0.28, 0.72, 2], [strength, 0.12, 0.0, 0.0])
    rng = np.random.default_rng(7)
    grain = (rng.random((h, w)).astype(np.float32) - 0.5) * 0.035
    col = np.array([233, 178, 90], np.float32)
    img = np.clip(col[None, None, :] * a[..., None] + grain[..., None] * 255, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(path, quality=88, subsampling=0)
    return path

LAMP_BG = lamp_bg(f'{AS}/sanzeed-slide-bg--lamp.jpg')
LAMP_BG_END = lamp_bg(f'{AS}/sanzeed-slide-bg--lamp-end.jpg', cx=0.5, cy=0.5, strength=0.34)

def veil_image(name, out, bottom=0.78):
    im = Image.open(f'{IMG_DIR}/{name}.webp').convert('RGB').resize((1920, 1080), Image.LANCZOS)
    arr = np.asarray(im).astype(np.float32)
    h = arr.shape[0]
    t = np.linspace(0, 1, h)[:, None, None]
    f = 1 - bottom * np.clip((t - 0.35) / 0.65, 0, 1) ** 1.2
    arr = arr * f
    Image.fromarray(arr.astype(np.uint8)).save(out, quality=88, subsampling=0)
    return out

IMG_PM = veil_image('prime-minister-museum', f'{AS}/sanzeed-slide-img--prime-minister-museum-veil.jpg')
IMG_RK = jpg_from_webp('ram-katha-show', f'{AS}/sanzeed-slide-img--ram-katha-show.jpg', crop='4:3')
IMG_BP = jpg_from_webp('buddha-park', f'{AS}/sanzeed-slide-img--buddha-park.jpg', crop='16:9')
im = Image.open(f'{IMG_DIR}/portrait.webp').convert('RGB'); w0, h0 = im.size; nh = int(w0 * 5 / 4); y0 = int((h0 - nh) * 0.35)
im.crop((0, y0, w0, y0 + nh)).resize((640, 800), Image.LANCZOS).save(f'{AS}/sanzeed-portrait--4x5.jpg', quality=88, subsampling=0)
PORTRAIT = f'{AS}/sanzeed-portrait--4x5.jpg'
# wordmark PNGs (transparent) for the dark slides
for variant, px in (('primary-wordmark', 2400), ('symbol', 600), ('horizontal-descriptor', 2400)):
    inkscape([f'{LOGO_DIR}/sanzeed-{variant}--full-colour-dark.svg', '--export-type=png', f'--export-width={px}', f'--export-filename={AS}/sanzeed-{variant}--full-colour-dark.png'])
WM = f'{AS}/sanzeed-primary-wordmark--full-colour-dark.png'; SYM = f'{AS}/sanzeed-symbol--full-colour-dark.png'; LOCK = f'{AS}/sanzeed-horizontal-descriptor--full-colour-dark.png'

# ------------------------------------------------------------------ helpers
prs = Presentation()
prs.slide_width, prs.slide_height = SW, SH
master = prs.slide_master
master.background.fill.solid(); master.background.fill.fore_color.rgb = BLACK
BLANK = prs.slide_layouts[6]
# the master's placeholders are not used; make sure the blank layout is black too
BLANK.background.fill.solid(); BLANK.background.fill.fore_color.rgb = BLACK


def new_slide(name):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = BLACK
    s.name = name
    return s


def tb(slide, x, y, w, h, anchor='top'):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {'top': MSO_ANCHOR.TOP, 'middle': MSO_ANCHOR.MIDDLE, 'bottom': MSO_ANCHOR.BOTTOM}[anchor]
    return box, tf


def run(p, text, font=F_TEXT, size=18, color=GWHITE, bold=False, italic=False, spacing=None):
    r = p.add_run(); r.text = text
    f = r.font; f.name = font; f.size = Pt(size); f.color.rgb = color; f.bold = bold; f.italic = italic
    if spacing is not None:
        rPr = r._r.get_or_add_rPr(); rPr.set('spc', str(int(spacing * 100)))
    return r


def para(tf, first=False, align='left', line=1.0, before=0, after=0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = {'left': PP_ALIGN.LEFT, 'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT}[align]
    p.line_spacing = line; p.space_before = Pt(before); p.space_after = Pt(after)
    return p


def eyebrow(slide, x, y, text, w=Inches(6), color=LAMP):
    b, tf = tb(slide, x, y, w, Inches(0.3)); p = para(tf, True)
    run(p, text.upper(), F_HEAD, 11, color, spacing=1.3)
    return b


def headline(slide, x, y, w, h, text, size=54, lit=None, align='left', anchor='top', line=1.02, color=GWHITE):
    """Fraunces Light headline; the last word (or `lit`) in Lamp Gold, full stop included."""
    b, tf = tb(slide, x, y, w, h, anchor)
    p = para(tf, True, align, line)
    if lit:
        head = text[: text.rfind(lit)]
        run(p, head, F_DISPLAY, size, color)
        run(p, lit, F_DISPLAY, size, LAMP)
    else:
        run(p, text, F_DISPLAY, size, color)
    return b


def body(slide, x, y, w, h, text, size=16, color=SILVER, line=1.35, font=F_TEXT, align='left'):
    b, tf = tb(slide, x, y, w, h); p = para(tf, True, align, line)
    run(p, text, font, size, color)
    return b


def hairline(slide, x, y, w, color=GRAPHITE):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Emu(9525))
    s.fill.solid(); s.fill.fore_color.rgb = color; s.line.fill.background(); s.shadow.inherit = False
    return s


def point(slide, cx, cy, r=Inches(0.07)):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - r, cy - r, 2 * r, 2 * r)
    s.fill.solid(); s.fill.fore_color.rgb = LAMP; s.line.fill.background(); s.shadow.inherit = False
    return s


def room(slide, x, y, w, h, fill=CHARCOAL):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    s.adjustments[0] = min(0.5, Inches(0.3) / min(w, h))
    s.fill.solid(); s.fill.fore_color.rgb = fill; s.line.color.rgb = GRAPHITE; s.line.width = Pt(0.75); s.shadow.inherit = False
    return s


def wall_label(slide, x, y, title, place, line3=None, w=Inches(6)):
    b, tf = tb(slide, x, y, w, Inches(0.8)); p = para(tf, True, line=1.3)
    run(p, title, F_HEAD, 13, GWHITE); run(p, '  ·  ' + place, F_TEXT, 13, MIST)
    if line3:
        p2 = para(tf, line=1.3); run(p2, line3, F_TEXT, 13, MIST)
    return b


def footer(slide, counter=None):
    b, tf = tb(slide, M, SH - Inches(0.62), Inches(8), Inches(0.3)); p = para(tf, True)
    run(p, 'Sanzeed Mirza  ·  Experiential Design Consultant', F_TEXT, 10, MIST)
    if counter:
        b2, tf2 = tb(slide, SW - M - Inches(2), SH - Inches(0.62), Inches(2), Inches(0.3)); p2 = para(tf2, True, 'right')
        run(p2, counter, F_HEAD, 10, LAMP, spacing=0.8)


# ------------------------------------------------------------------ 1 · title
s = new_slide('01 Title — dark, lamp, wordmark')
s.shapes.add_picture(LAMP_BG, 0, 0, SW, SH)
s.shapes.add_picture(WM, (SW - Inches(6.2)) / 2, Inches(2.35), width=Inches(6.2))
headline(s, M, Inches(4.4), SW - 2 * M, Inches(1.2), 'Experiential design you can walk into.', 40, lit='into.', align='center')
body(s, M, Inches(5.65), SW - 2 * M, Inches(0.5), 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  New Delhi  ·  [Date]', 14, SILVER, align='center')

# ------------------------------------------------------------------ 2 · section divider
s = new_slide('02 Section divider — counter + title')
eyebrow(s, M, Inches(2.6), '001  ·  Now showing')
headline(s, M, Inches(3.0), Inches(11), Inches(2), 'Eight rooms, lit.', 72, lit='lit.')
footer(s, '001')

# ------------------------------------------------------------------ 3 · agenda
s = new_slide('03 Agenda')
eyebrow(s, M, M, 'Agenda')
headline(s, M, Inches(1.25), Inches(6), Inches(1.4), 'The route.', 44, lit='route.')
items = ['The room', 'The one central story', 'Method', 'Scope', 'Team', 'Next step']
for i, it in enumerate(items):
    y = Inches(1.3) + i * Inches(0.8)
    b, tf = tb(s, Inches(7.2), y, Inches(1), Inches(0.5)); p = para(tf, True); run(p, f'{i + 1:03d}', F_HEAD, 12, LAMP, spacing=0.8)
    b, tf = tb(s, Inches(8.1), y - Inches(0.06), Inches(4.4), Inches(0.6)); p = para(tf, True); run(p, it, F_DISPLAY, 24, GWHITE)
    hairline(s, Inches(7.2), y + Inches(0.62), Inches(5.3))
footer(s, '003')

# ------------------------------------------------------------------ 4 · statement
s = new_slide('04 Statement — one line, lit word')
headline(s, M, 0, SW - 2 * M, SH, 'Between two points of light.', 64, lit='light.', align='center', anchor='middle')
footer(s, '004')

# ------------------------------------------------------------------ 5 · full-bleed image with wall label
s = new_slide('05 Full-bleed image + wall label')
s.shapes.add_picture(IMG_PM, 0, 0, SW, SH)
wall_label(s, M, SH - Inches(1.5), 'Prime Minister Museum', 'New Delhi', 'One Prime Minister at a time, in order.', w=Inches(8))
s.shapes.add_picture(SYM, SW - M - Inches(0.5), SH - Inches(1.35), width=Inches(0.5))

# ------------------------------------------------------------------ 6 · image + text
s = new_slide('06 Image + text')
room(s, M, M, Inches(6.0), SH - 2 * M)
pic = s.shapes.add_picture(IMG_RK, M + Inches(0.12), M + Inches(0.12), Inches(5.76), Inches(4.32))
wall_label(s, M + Inches(0.3), SH - M - Inches(1.1), 'Ram Katha Show', 'Ayodhya', 'The building is the screen.', w=Inches(5.4))
eyebrow(s, Inches(7.5), M + Inches(0.3), 'Case study  ·  Projection mapping & shows')
headline(s, Inches(7.5), M + Inches(0.75), Inches(5), Inches(1.6), 'The building is the screen.', 36, lit='screen.')
body(s, Inches(7.5), M + Inches(2.5), Inches(5.1), Inches(2.4), 'Every dome, arch and column of the hall was mapped and painted with light, so the story seems to rise from the stone. Scenes move from the central shrine outwards along the galleries; the gilded ceiling becomes sky, then forest, then fire.', 15)
body(s, Inches(7.5), M + Inches(5.0), Inches(5.1), Inches(0.9), 'Visitors sit in the dark and watch a building they know by day become the story by night.', 15, GWHITE)
footer(s, '006')

# ------------------------------------------------------------------ 7 · two-column
s = new_slide('07 Two-column')
eyebrow(s, M, M, 'Case study  ·  Buddha Park, Uttarakhand')
headline(s, M, M + Inches(0.45), Inches(11), Inches(1.2), 'A garden of gestures.', 40, lit='gestures.')
colw = (SW - 2 * M - Inches(0.8)) / 2
for i, (h, t) in enumerate([('The brief', 'A park in Uttarakhand around a reclining Buddha, with a stupa, shrines and gardens — a landscape that must work as a place of calm for pilgrims and a day out for families.'),
                            ('The idea', 'The park is laid out as one loop: from the gate past the shrines to the stupa, around the reclining Buddha and back to a fountain court ringed by sculpted hands in the mudras. The walk itself is the meditation; nothing is read, everything is passed.')]):
    x = M + i * (colw + Inches(0.8))
    hairline(s, x, Inches(2.75), colw)
    b, tf = tb(s, x, Inches(2.95), colw, Inches(0.5)); p = para(tf, True); run(p, h, F_HEAD, 18, GWHITE)
    body(s, x, Inches(3.5), colw, Inches(3), t, 16)
footer(s, '007')

# ------------------------------------------------------------------ 8 · three-column cards (services)
s = new_slide('08 Three-column cards — services')
eyebrow(s, M, M, 'Experiential design  ·  Seven ways to carry the light across')
headline(s, M, M + Inches(0.45), Inches(11), Inches(1.2), 'Between two points of light.', 36, lit='light.')
cards = [('01', 'Experiential Design & Creative Direction', 'One vision from brief to opening night: narrative, space, media and the team that builds it.'),
         ('02', 'Museum & Cultural Exhibition Planning', 'Galleries planned as a route, not a floor plan. Objects, stories and dwell time, in order.'),
         ('03', 'Immersive Storytelling & Narrative Architecture', 'The script comes first. Every room, screen and surface carries a line of it.')]
cw = (SW - 2 * M - 2 * Inches(0.4)) / 3
for i, (n, h, t) in enumerate(cards):
    x = M + i * (cw + Inches(0.4)); y = Inches(2.7); ch = Inches(3.6)
    room(s, x, y, cw, ch)
    b, tf = tb(s, x + Inches(0.4), y + Inches(0.4), Inches(1), Inches(0.3)); p = para(tf, True); run(p, n, F_HEAD, 12, LAMP, spacing=0.8)
    b, tf = tb(s, x + Inches(0.4), y + Inches(0.85), cw - Inches(0.8), Inches(1.1)); p = para(tf, True, line=1.15); run(p, h, F_HEAD, 19, GWHITE)
    body(s, x + Inches(0.4), y + Inches(2.0), cw - Inches(0.8), Inches(1.5), t, 14)
footer(s, '008')

# ------------------------------------------------------------------ 9 · stats
s = new_slide('09 Stats')
eyebrow(s, M, M, 'About  ·  Fifteen years, one through-line')
stats = [('15', 'Years of experience'), ('8', 'Years experiential & museum'), ('90', 'Projects directed'), ('60', 'Museums & centres')]
sw_ = (SW - 2 * M) / 4
for i, (n, l) in enumerate(stats):
    x = M + i * sw_
    b, tf = tb(s, x, Inches(2.5), sw_ - Inches(0.3), Inches(1.5)); p = para(tf, True, line=1.0)
    run(p, n, F_DISPLAY, 88, GWHITE); run(p, '+', F_DISPLAY, 88, LAMP)
    hairline(s, x, Inches(4.25), sw_ - Inches(0.5))
    body(s, x, Inches(4.4), sw_ - Inches(0.5), Inches(0.6), l, 14, SILVER)
body(s, M, Inches(5.6), SW - 2 * M, Inches(0.6), 'Trusted by PwC, Microsoft, Discovery and National Museums, from concept to public unveiling.', 15, MIST)
footer(s, '009')

# ------------------------------------------------------------------ 10 · timeline (the career)
s = new_slide('10 Timeline — journey')
eyebrow(s, M, M, 'Journey')
headline(s, M, M + Inches(0.45), Inches(11), Inches(1.2), 'Fifteen years, one through-line.', 36, lit='through-line.')
steps = [('2011', 'Lead Concept Artist', 'Broadcast2world · VFX Artist, Prime Focus'), ('2017', 'Creative Director', 'SocioPixels'),
         ('2018', 'Creative Head', 'Digital Web Solutions'), ('2018 – 2026', 'Creative Director', 'Tagbin'), ('Aug 2026', 'Experiential Design Consultant', 'Independent, New Delhi')]
ly = Inches(3.6)
hairline(s, M, ly, SW - 2 * M)
n = len(steps); gap = (SW - 2 * M) / n
for i, (yr, role, org) in enumerate(steps):
    x = M + i * gap
    point(s, x + Inches(0.07), ly + Emu(4762), Inches(0.07) if i < n - 1 else Inches(0.09))
    b, tf = tb(s, x, ly - Inches(0.5), gap - Inches(0.2), Inches(0.35)); p = para(tf, True); run(p, yr, F_HEAD, 12, LAMP, spacing=0.6)
    b, tf = tb(s, x, ly + Inches(0.3), gap - Inches(0.25), Inches(0.8)); p = para(tf, True, line=1.15); run(p, role, F_HEAD, 15, GWHITE)
    body(s, x, ly + Inches(1.0), gap - Inches(0.25), Inches(0.9), org, 13, MIST)
footer(s, '010')

# ------------------------------------------------------------------ 11 · method
s = new_slide('11 Method — four steps')
eyebrow(s, M, M, 'Method')
headline(s, M, M + Inches(0.45), Inches(11), Inches(1.2), 'A method for the monumental.', 36, lit='monumental.')
method = [('STEP 01', 'Discover', 'Immersion in the subject — its history, intent and audience — until the central story reveals itself.', 'A research deck and the one central story'),
          ('STEP 02', 'Direct', 'A unifying creative vision that aligns designers, architects, writers, producers and technologists toward one outcome.', 'A concept book and a walkthrough film'),
          ('STEP 03', 'Craft', 'Space, light, motion and interaction composed into environments that engage intellectually, emotionally and physically.', 'Detail drawings, media scripts and a prototype room'),
          ('STEP 04', 'Deliver', 'Concept to launch — balancing creative ambition with operational discipline. On scale, on story, on time.', 'A built, tested and opened experience')]
mw = (SW - 2 * M - 3 * Inches(0.35)) / 4
ry = Inches(2.75)
hairline(s, M, ry - Inches(0.15), SW - 2 * M)
for i, (st, name, desc, deliv) in enumerate(method):
    x = M + i * (mw + Inches(0.35))
    point(s, x + Inches(0.06), ry - Inches(0.15) + Emu(4762), Inches(0.06))
    b, tf = tb(s, x, ry + Inches(0.15), mw, Inches(0.3)); p = para(tf, True); run(p, st, F_HEAD, 11, LAMP, spacing=1.0)
    b, tf = tb(s, x, ry + Inches(0.5), mw, Inches(0.7)); p = para(tf, True); run(p, name, F_DISPLAY, 30, GWHITE)
    body(s, x, ry + Inches(1.3), mw, Inches(1.8), desc, 13, SILVER)
    body(s, x, ry + Inches(3.0), mw, Inches(0.9), 'You receive ' + deliv[0].lower() + deliv[1:] + '.', 13, GWHITE)
footer(s, '011')

# ------------------------------------------------------------------ 12 · quote
s = new_slide('12 Quote')
b, tf = tb(s, M + Inches(0.5), Inches(1.6), SW - 2 * M - Inches(1), Inches(3.4), 'middle'); p = para(tf, True, 'left', 1.25)
run(p, 'The most powerful stories aren\'t just told — they\'re felt, lived, and remembered through the spaces we design and the moments we shape.', F_DISPLAY, 34, GWHITE, italic=True)
body(s, M + Inches(0.5), Inches(5.3), Inches(8), Inches(0.5), '— Sanzeed Mirza', 15, LAMP, font=F_HEAD)
footer(s, '012')

# ------------------------------------------------------------------ 13 · team / contact
s = new_slide('13 Team / contact')
room(s, M, M, Inches(3.6), Inches(4.5))
s.shapes.add_picture(PORTRAIT, M + Inches(0.1), M + Inches(0.1), Inches(3.4), Inches(4.25))
wall_label(s, M, M + Inches(4.75), 'Sanzeed Mirza', 'New Delhi', w=Inches(4))
eyebrow(s, Inches(5.3), M, 'Get in touch')
headline(s, Inches(5.3), M + Inches(0.45), Inches(7.2), Inches(1.6), 'Strategy, craft and calm leadership, in one person.', 32, lit='person.')
body(s, Inches(5.3), M + Inches(2.3), Inches(7), Inches(1.6), 'I lead the whole room — story, space, graphics, media and the team that builds it. The work I want to make is calm to run and impossible to forget once you have walked through it.', 15)
contact = [('Email', 'sanzeed@gmail.com'), ('Call / WhatsApp', '+91 7827051270'), ('Web', 'sanzeed.com'), ('LinkedIn', 'linkedin.com/in/sanzeed')]
for i, (k, v) in enumerate(contact):
    y = M + Inches(3.95) + i * Inches(0.42)
    b, tf = tb(s, Inches(5.3), y, Inches(2), Inches(0.3)); p = para(tf, True); run(p, k.upper(), F_HEAD, 10, MIST, spacing=0.8)
    b, tf = tb(s, Inches(7.4), y - Inches(0.03), Inches(5), Inches(0.35)); p = para(tf, True); run(p, v, F_TEXT, 15, GWHITE)
    hairline(s, Inches(5.3), y + Inches(0.36), Inches(7.1))
footer(s, '013')

# ------------------------------------------------------------------ 14 · end card
s = new_slide('14 End card — Tell me about the room.')
s.shapes.add_picture(LAMP_BG_END, 0, 0, SW, SH)
headline(s, M, Inches(2.3), SW - 2 * M, Inches(1.6), 'Tell me about the room.', 60, lit='room.', align='center')
body(s, M, Inches(4.1), SW - 2 * M, Inches(0.5), 'A few lines are enough. The first conversation is always free.', 16, SILVER, align='center')
body(s, M, Inches(4.65), SW - 2 * M, Inches(0.5), 'sanzeed@gmail.com  ·  +91 7827051270  ·  sanzeed.com  ·  linkedin.com/in/sanzeed', 14, GWHITE, align='center')
s.shapes.add_picture(WM, (SW - Inches(2.2)) / 2, Inches(6.1), width=Inches(2.2))

prs.core_properties.author = 'Sanzeed Mirza'; prs.core_properties.title = 'Sanzeed — presentation template'
prs.core_properties.comments = 'Fonts: Fraunces Light, Inter Tight SemiBold, Inter — install from 04_TYPOGRAPHY/Font_Files before editing.'
PPTX = f'{SRC}/sanzeed-presentation-template.pptx'
prs.save(PPTX)

tmpd = tempfile.mkdtemp()
pdf = soffice_pdf(PPTX, tmpd); shutil.move(pdf, f'{D}/sanzeed-presentation-template.pdf')
pages = pdf_pages_to_png(f'{D}/sanzeed-presentation-template.pdf', f'{D}/sanzeed-presentation-template--slide', dpi=96)
print('slides:', len(pages), pdfinfo(f'{D}/sanzeed-presentation-template.pdf').split('Page size:')[1].split('\n')[0].strip())
print('presentation done')
