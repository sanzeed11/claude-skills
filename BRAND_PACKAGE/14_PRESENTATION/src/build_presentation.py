#!/usr/bin/env python3
"""
Brand_Presentation — the final-delivery reveal deck for the Sanzeed identity.

One slide model → two outputs:
  • src/Brand_Presentation.html  (one <section> per slide, 1920 × 1080 CSS px, @page 508 × 285.75 mm)
    rendered to Brand_Presentation.pdf with the brand kit's render.js, then pdftoppm → slide PNGs
  • Editable_Presentation/Brand_Presentation.pptx (python-pptx, 16:9, every text an editable text box,
    every image a real embedded picture) → Brand_Presentation--pptx-export.pdf through LibreOffice

Every element is laid out once in a 1920 × 1080 px coordinate system; the HTML renderer writes absolute
positioned divs, the PPTX renderer converts px → EMU (× 6350) and px → pt (× 0.5).

Usage:  python3 build_presentation.py            # HTML + PPTX + PDFs + PNGs
        python3 build_presentation.py --html-only
"""
import os, sys, re, json, subprocess, shutil, hashlib, html as H
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)                                   # 14_PRESENTATION
B = os.path.dirname(OUT)                                      # BRAND_PACKAGE
EP = f'{OUT}/Editable_Presentation'
ASSETS = f'{EP}/assets'
SLIDES_DIR = f'{EP}/slides'
KIT = f'{B}/15_SOURCE_FILES/Project_Files/brand-kit'
for d in (EP, ASSETS, SLIDES_DIR):
    os.makedirs(d, exist_ok=True)

W, Hh = 1920, 1080
M = 96                      # side margin
EMU = 6350                  # EMU per px at 13.333 in / 1920 px

# ----------------------------------------------------------------------------- colour tokens (03_COLOUR_SYSTEM)
C = dict(black='#000000', night='#0D0D0F', charcoal='#1C1C1E', graphite='#2A2A2D', mist='#808086', silver='#A1A1A6',
         gwhite='#F5F5F7', plaster='#F5F0E7', paper='#FBF8F2', stone='#ECE7DC', umber='#665F55', soot='#1A1816',
         lamp='#E9B25A', lamplight='#F4C97A', oldgold='#B8863B', amber='#D9A64A', goldink='#8A6124',
         moss='#3D8B5E', mossdeep='#2E6E48', ochre='#D4862B', ochredeep='#A8651B', red='#D64540', brick='#C0392B',
         slate='#4A86C8', slatedeep='#2F62A0')
# hairlines as flat colours (10 % white on Night / 10 % Soot on Plaster) so PPTX and HTML match
LINE_D, LINE_L = '#262628', '#DFDAD1'

THEMES = {
    'dark':  dict(bg=C['night'], fg=C['gwhite'], fg2=C['silver'], fg3=C['mist'], card=C['charcoal'], line=LINE_D,
                  accent=C['lamp'], accent_text=C['lamp'], logo='full-colour-dark', sig='white'),
    'black': dict(bg=C['black'], fg=C['gwhite'], fg2=C['silver'], fg3=C['mist'], card=C['charcoal'], line=LINE_D,
                  accent=C['lamp'], accent_text=C['lamp'], logo='full-colour-dark', sig='white'),
    'light': dict(bg=C['plaster'], fg=C['soot'], fg2=C['umber'], fg3='#6D665C', card=C['paper'], line=LINE_L,
                  accent=C['oldgold'], accent_text=C['goldink'], logo='full-colour-light', sig='ink'),
}
F_DISPLAY, F_HEAD, F_TEXT = 'Fraunces', 'Inter Tight', 'Inter'          # HTML families
P_DISPLAY, P_HEAD, P_TEXT = 'Fraunces Light', 'Inter Tight SemiBold', 'Inter'   # PPTX font names

# ----------------------------------------------------------------------------- package paths
LOGO_SVG = f'{B}/02_LOGO_SYSTEM/SVG'
LOGO_PNG = f'{B}/02_LOGO_SYSTEM/PNG'
SIG = f'{B}/02_LOGO_SYSTEM/Signature'
GUIDE = f'{B}/02_LOGO_SYSTEM/Guidelines'
IMG = f'{B}/06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/JPG'
MOCK = f'{B}/13_BRAND_MOCKUPS'
LAMP_TEX = f'{B}/05_GRAPHIC_ASSETS/Textures/sanzeed-texture-lamp-glow--2048.png'
ILL = f'{B}/05_GRAPHIC_ASSETS/Illustrations/png'

LOGO_PNG_NAME = {   # variant → largest transparent PNG stem width available
    'primary-wordmark': 1200, 'wordmark-plain': 1200, 'secondary-symbol-wordmark': 1200, 'horizontal-descriptor': 1200,
    'vertical-stacked': 1000, 'symbol': 512, 'symbol-small-size': 128, 'monogram': 800, 'simplified-small-size': 400}


def logo(variant, colour):
    """(svg path for HTML, png path for PPTX) of a production logo."""
    svg = f'{LOGO_SVG}/sanzeed-{variant}--{colour}.svg'
    png = f'{LOGO_PNG}/sanzeed-{variant}--{colour}-{LOGO_PNG_NAME[variant]}w.png'
    for p in (svg, png):
        assert os.path.exists(p), p
    return svg, png


def tile(colour):
    p = f'{LOGO_PNG}/sanzeed-symbol-tile--{colour}-1024w.png'; assert os.path.exists(p); return p, p


def signature(colour):
    svg = f'{SIG}/sanzeed-signature--{colour}.svg'; png = f'{SIG}/sanzeed-signature--{colour}-2400w.png'
    assert os.path.exists(svg) and os.path.exists(png); return svg, png


def P(rel):
    p = f'{B}/{rel}'
    assert os.path.exists(p), p
    return p


_size_cache = {}
def imsize(path):
    if path not in _size_cache:
        if path.endswith('.svg'):
            m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', open(path).read(4000))
            _size_cache[path] = (float(m.group(3)), float(m.group(4)))
        else:
            _size_cache[path] = Image.open(path).size
    return _size_cache[path]


def ar(path):
    """Height / width of an asset (SVG viewBox or raster) — logos are never placed at a hard-coded ratio."""
    iw, ih = imsize(path)
    return ih / iw


ORIG_SVG = f'{B}/00_ORIGINAL_ASSETS_BACKUP/logo/wordmark-inline-original.svg'
DERIVED = f'{HERE}/derived'


def original_wordmark():
    """The live-site wordmark exactly as found (00_ORIGINAL_ASSETS_BACKUP), given the site's dark-theme colours:
    the inline SVG carries no fills of its own (sanzeed.com colours it with CSS), so a colour style is added and the
    site's animated beam-dot (a loader element, not part of the mark) is hidden. Geometry untouched.
    Returns (svg for HTML, png for PPTX)."""
    os.makedirs(DERIVED, exist_ok=True)
    svg = f'{DERIVED}/sanzeed-original-wordmark--live-site--full-colour-dark.svg'
    png = f'{DERIVED}/sanzeed-original-wordmark--live-site--full-colour-dark-2400w.png'
    src = open(ORIG_SVG).read()
    style = (f'<style>.wm-letters{{fill:{C["gwhite"]}}}.wm-dot{{fill:{C["lamp"]}}}.beam-dot{{display:none}}</style>')
    out = re.sub(r'(<svg[^>]*>)', r'\1' + style, src, count=1)
    open(svg, 'w').write(out)
    # rasterise in Chromium — the browser the live site is seen in. The traced path has unclosed, overlapping
    # sub-paths that cairo / Inkscape fill differently (the Z's bottom bar comes out tapered there).
    pw = 2400; ph = round(pw * ar(svg))
    wrap = f'{DERIVED}/_rasterise-original.html'
    open(wrap, 'w').write(f'<!DOCTYPE html><html><head><style>html,body{{margin:0;background:transparent}}img{{display:block;width:{pw}px;height:{ph}px}}</style></head>'
                          f'<body><img src="{os.path.basename(svg)}" alt=""></body></html>')
    run(['node', f'{KIT}/render.js', '--in', wrap, '--out', png, '--width', str(pw), '--height', str(ph), '--scale', '1', '--transparent'])
    os.remove(wrap)
    return svg, png


def fit(src, x, y, w, h, align='center'):
    """Contain-fit rectangle for src inside (x,y,w,h); align: center | left | top | bottom."""
    iw, ih = imsize(src)
    s = min(w / iw, h / ih); fw, fh = iw * s, ih * s
    fx = x + (w - fw) / 2 if align in ('center', 'top', 'bottom') else x
    fy = y + (h - fh) / 2 if align in ('center', 'left') else (y if align == 'top' else y + h - fh)
    return fx, fy, fw, fh


# ----------------------------------------------------------------------------- slide model
class Slide:
    def __init__(self, theme, name, notes=''):
        self.theme = theme; self.T = THEMES[theme]; self.name = name; self.notes = notes
        self.els = []; self.grain = theme != 'light'

    def add(self, **e):
        self.els.append(e); return e

    # primitives ---------------------------------------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, line=None, radius=0, lw=1, gradient=None):
        return self.add(t='rect', x=x, y=y, w=w, h=h, fill=fill, line=line, radius=radius, lw=lw, gradient=gradient)

    def ellipse(self, cx, cy, r, fill=None, line=None, lw=1, glow=False):
        return self.add(t='ellipse', x=cx - r, y=cy - r, w=2 * r, h=2 * r, fill=fill, line=line, lw=lw, glow=glow)

    def hline(self, x, y, w, color=None):
        return self.rect(x, y, w, 1, fill=color or self.T['line'])

    def img(self, src, x, y, w, h, mode='cover', focal=(0.5, 0.5), radius=0, border=None, png=None, alpha=None, crop=None):
        """src: path for HTML (svg or raster); png: path for PPTX when src is an SVG. crop: (l,t,r,b) fractions of
        the source to use before fitting (used for sheet details)."""
        return self.add(t='img', src=src, png=png or src, x=x, y=y, w=w, h=h, mode=mode, focal=focal, radius=radius,
                        border=border, alpha=alpha, crop=crop)

    def text(self, x, y, w, h, runs, size=18, font='text', color=None, weight=None, align='left', anchor='top',
             line=1.4, tracking=0, caps=False, italic=False, opsz=None):
        """runs: str or list of (text, overrides-dict). font: display | head | text."""
        if isinstance(runs, str):
            runs = [(runs, {})]
        if x >= M and x + w > W - M:
            w = W - M - x
        return self.add(t='text', x=x, y=y, w=w, h=h, runs=runs, size=size, font=font, color=color or self.T['fg'],
                        weight=weight, align=align, anchor=anchor, line=line, tracking=tracking, caps=caps,
                        italic=italic, opsz=opsz)

    # brand components -----------------------------------------------------------------------------------
    def eyebrow(self, x, y, text, w=900, size=16, align='left', color=None):
        return self.text(x, y, w, size * 1.6, text, size=size, font='head', color=color or self.T['accent_text'],
                         tracking=0.12, caps=True, align=align, line=1.2)

    def title(self, text, y=116, size=76, x=M, w=1500, lit=True, color=None, line=1.06, align='left', anchor='top', h=None):
        words = text.split(' ')
        if lit and len(words) > 1:
            runs = [(' '.join(words[:-1]) + ' ', {}), (words[-1], {'color': self.T['accent']})]
        else:
            runs = text
        return self.text(x, y, w, h or size * line * 2.1, runs, size=size, font='display', color=color, line=line,
                         align=align, anchor=anchor)

    def point(self, cx, cy, r=5, glow=True):
        return self.ellipse(cx, cy, r, fill=self.T['accent'], glow=glow)

    def beam(self, x, y, w, point_at=0.0):
        self.hline(x, y, w)
        self.point(x + w * point_at, y + 0.5)

    def wall_label(self, x, y, counter, title, place='', w=700, size=15, align='left'):
        T = self.T
        runs = []
        if counter:
            runs.append((f'{counter}  ', {'font': 'head', 'color': T['accent_text'], 'tracking': 0.08}))
        runs.append((title, {'font': 'head', 'color': T['fg']}))
        if place:
            runs.append((f'  {place}', {'font': 'text', 'color': T['fg3']}))
        return self.text(x, y, w, size * 1.6, runs, size=size, font='text', color=T['fg'], line=1.3, align=align)

    def room(self, x, y, w, h, fill=None, radius=28):
        return self.rect(x, y, w, h, fill=fill or self.T['card'], line=self.T['line'], radius=radius)

    def plate(self, src, x, y, w, h, counter, title, place='', mode='cover', focal=(0.5, 0.5), radius=20, png=None,
              fill=None, pad=0, label=True, crop=None, align='center'):
        """An image in the room with its wall label beneath. For contain mode the image sits in a card."""
        if mode == 'contain':
            self.room(x, y, w, h, fill=fill, radius=radius)
            fx, fy, fw, fh = fit(src, x + pad, y + pad, w - 2 * pad, h - 2 * pad, align=align)
            self.img(src, fx, fy, fw, fh, mode='contain', png=png, radius=0 if pad else radius, crop=crop)
        else:
            self.img(src, x, y, w, h, mode='cover', focal=focal, radius=radius, border=self.T['line'], png=png, crop=crop)
        if label:
            self.wall_label(x, y + h + 14, counter, title, place, w=w)

    def chrome(self, section, name, page, total, wordmark=True):
        """Eyebrow, small wordmark, footer beam and folios shared by every content slide."""
        T = self.T
        self.eyebrow(M, 64, f'{section:02d}  ·  {name}')
        if wordmark:
            svg, png = logo('primary-wordmark', T['logo'])
            lw = 200; lh = lw * ar(svg)
            self.img(svg, W - M - lw, 62, lw, lh, mode='contain', png=png)
        self.hline(M, 1002, W - 2 * M)
        self.point(M, 1002.5, r=4)
        self.text(M, 1018, 900, 24, 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  Brand identity  ·  November 2026',
                  size=13, color=T['fg3'], line=1.3)
        self.text(W - M - 300, 1018, 300, 24, f'{page:02d}  /  {total:02d}', size=13, font='head', color=T['fg3'],
                  align='right', line=1.3, tracking=0.06)

    def lamp(self, cx, cy, size=1500, strength=1.0):
        """The lamp glow — the real texture from 05_GRAPHIC_ASSETS/Textures, centred on (cx, cy)."""
        self.img(LAMP_TEX, cx - size / 2, cy - size / 2, size, size, mode='contain', alpha=strength)


# ----------------------------------------------------------------------------- the deck
SECTIONS = [
    (1, 'The brief and the audit', 'What existed on 5 November 2026, what was strong, what was missing.'),
    (2, 'Strategy on a page', 'The one idea, the promise, the pillars, the archetype and the audience.'),
    (3, 'Three routes considered', 'Developed to the same depth before choosing. Route A was chosen.'),
    (4, 'The idea', 'The point of light, the beam it travels, the room it crosses.'),
    (5, 'The logo family', 'Your own wordmark, refined: eleven variants, each on its right background.'),
    (6, 'Construction and rules', 'The refined letters on their grid, clear space, minimum sizes and the twelve things never to do.'),
    (7, 'Colour system', 'Dark is the gallery, cream is the label, one gold accent.'),
    (8, 'Typography', 'Fraunces 300 speaks; Inter Tight and Inter work.'),
    (9, 'Graphic language', 'Patterns, icons, illustrations and textures from seven words.'),
    (10, 'Photography and art direction', 'The lit room: one light source, blacks that hold, warm highlights.'),
    (11, 'Website', 'sanzeed.com rebuilt with the identity applied — nothing else changed.'),
    (12, 'Digital assets', 'Share images, email, favicons and app icons.'),
    (13, 'Social media', 'Profiles, covers, posts and stories for six platforms.'),
    (14, 'Stationery', 'Cards, letterhead, envelopes, documents, ID and the folder.'),
    (15, 'Marketing and signage', 'Posters, brochures, wayfinding and the totem.'),
    (16, 'Motion', 'Light, not bounce: the reveal, the intro and the pieces between.'),
    (17, 'Applications', 'The identity, applied.'),
    (18, 'What you receive', 'Sixteen folders, every format, every editable source.'),
    (19, 'Next steps', 'Deploy, proof, register, install — and what Sanzeed must supply.'),
]
SEC = {n: (name, line) for n, name, line in SECTIONS}


def build_deck():
    S = []
    total = [0]   # patched later for folios

    def content(theme, section, name, wordmark=True):
        s = Slide(theme, f'{section:02d} · {name}')
        s._chrome = (section, SEC[section][0], wordmark)
        S.append(s); return s

    def divider(n):
        name, line = SEC[n]
        s = Slide('black', f'Divider {n:02d} · {name}')
        s.lamp(1380, 560, 1500, 0.9)
        s.eyebrow(M, 64, f'Section {n:02d} of {len(SECTIONS):02d}  ·  Brand identity')
        s.text(M, 286, 700, 300, f'{n:02d}', size=260, font='display', color=s.T['fg'], line=1.0)
        s.title(name + '.', y=640, size=84, w=1300, lit=True, line=1.04)
        s.text(M, 860, 1100, 60, line, size=22, color=s.T['fg2'], line=1.45)
        s.beam(M, 1002, W - 2 * M, point_at=(n - 1) / (len(SECTIONS) - 1))
        S.append(s); return s

    # 00 — cover ------------------------------------------------------------------------------------------
    s = Slide('black', 'Cover')
    s.lamp(1180, 520, 1700, 1.0)
    s.eyebrow(M, 64, 'Brand identity  ·  November 2026')
    s.text(W - M - 500, 60, 500, 30, 'Final delivery  ·  Version 1.0', size=14, color=s.T['fg3'], align='right', line=1.5)
    s.text(M, 318, 1400, 420, [('Carry the light ', {}), ('across.', {'color': s.T['accent']})], size=150,
           font='display', line=1.0)
    s.text(M, 690, 1000, 40, 'The identity of Sanzeed Mirza, Experiential Design Consultant, New Delhi.', size=24,
           color=s.T['fg2'], line=1.45)
    svg, png = logo('primary-wordmark', 'full-colour-dark')
    s.img(svg, M, 880, 560, 560 * ar(svg), mode='contain', png=png)
    s.text(W - M - 700, 896, 700, 60, 'Sanzeed Mirza  ·  Experiential Design Consultant\nsanzeed.com  ·  New Delhi, India',
           size=15, color=s.T['fg3'], align='right', line=1.6)
    S.append(s)

    # 01 — the brief and the audit --------------------------------------------------------------------------
    divider(1)
    s = content('dark', 1, 'What existed')
    s.title('What existed.', size=72)
    s.text(M + 560, 136, 1000, 60, 'The live site at sanzeed.com, fetched 5 November 2026 — the only source of truth for this package.',
           size=18, color=s.T['fg2'], line=1.5)
    hero = P('01_BRAND_STRATEGY/src/figures/site-desktop-hero.jpg')
    s.plate(hero, M, 250, 1040, 636, '001', 'Home — hero', 'sanzeed.com · desktop 1440 px · three.js lit object, master line', mode='contain', pad=0)
    mob = P('01_BRAND_STRATEGY/src/figures/site-mobile-hero.jpg')
    s.plate(mob, 1184, 250, 264, 636, '002', 'Mobile', '390 px', mode='contain', pad=0)
    serv = P('01_BRAND_STRATEGY/src/figures/site-desktop-services.jpg')
    s.plate(serv, 1488, 250, 336, 133, '003', 'Services', 'seven, named', mode='contain', pad=0)
    s.text(1488, 440, 336, 440,
           'Measured on the site\n\n'
           'Wordmark: hand-traced inline SVG, 3729 × 561, stroke drifting between letters.\n\n'
           'Symbol: a 64 px favicon only.\n\n'
           'Signature: raster PNG, two sizes.\n\n'
           'Colour: black / cream / gold tokens, no print values.\n\n'
           'Type: Fraunces 300 · Inter Tight · Inter, no documented scale.',
           size=15, color=s.T['fg2'], line=1.45)

    s = content('light', 1, 'Strengths and gaps')
    s.title('Strengths, and the gaps.', size=72)
    cols = [
        ('Strengths', [
            ('A real idea, already in the copy', '"Between two points of light. Seven ways to carry the light across."'),
            ('Premium restraint', 'Black, cream, one gold accent, a light serif, generous space.'),
            ('A voice with a point of view', 'First person, short declaratives, spatial vocabulary, named deliverables.'),
            ('Proof at scale', '90 catalogued projects, three deep case studies, a 15-year timeline.'),
            ('A working dark / light token system', 'CSS custom properties already in place — a head start.'),
        ]),
        ('Gaps', [
            ('Wordmark hand-traced, not constructed', 'No lockups, no monogram, no clear space, no print formats.'),
            ('Symbol exists only as a favicon', 'No construction, no colour versions, no app or social set.'),
            ('Signature is raster only', 'Unusable for print at size; inconsistent with the vector system.'),
            ('Colour and type without production values', 'No CMYK or Pantone guidance; sizes ad hoc in CSS.'),
            ('No application system', 'Nothing for social, stationery, documents, decks, motion, signage.'),
            ('Digital hygiene', 'No favicon.ico, no manifest, one OG image for every page.'),
        ]),
    ]
    for ci, (head, items) in enumerate(cols):
        x = M + ci * 880
        s.eyebrow(x, 250, head)
        yy = 296
        for i, (a, b) in enumerate(items):
            s.hline(x, yy, 816)
            s.text(x, yy + 18, 60, 30, f'{i + 1:03d}', size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
            s.text(x + 64, yy + 14, 752, 30, a, size=19, font='head', color=s.T['fg'], line=1.3)
            s.text(x + 64, yy + 44, 752, 50, b, size=15, color=s.T['fg2'], line=1.45)
            yy += 100 if ci == 0 else 108
        s.hline(x, yy, 816)

    # 02 — strategy on a page -------------------------------------------------------------------------------
    divider(2)
    s = content('light', 2, 'Strategy on a page')
    s.title('Strategy on a page.', size=72)
    gx, gy, gw, gh = M, 236, 552, 720
    # card 1 — idea + promise
    s.room(gx, gy, gw, gh)
    s.eyebrow(gx + 36, gy + 32, 'The one idea')
    s.text(gx + 36, gy + 64, gw - 72, 160, [('Carry the light ', {}), ('across.', {'color': s.T['accent']})], size=56, font='display', line=1.06)
    s.text(gx + 36, gy + 210, gw - 72, 150,
           'A brief on one side, a visitor on the other. The gold point of light travels the beam through the dark room — everything in between is the work.',
           size=16, color=s.T['fg2'], line=1.5)
    s.hline(gx + 36, gy + 350, gw - 72)
    s.eyebrow(gx + 36, gy + 376, 'Promise')
    s.text(gx + 36, gy + 408, gw - 72, 100, 'One vision, carried across — from the brief to opening night.', size=26, font='display', line=1.2)
    s.text(gx + 36, gy + 500, gw - 72, 100, 'Backed by three confirmed commitments: the first conversation is free · a reply within two working days · a named deliverable at every step.',
           size=15, color=s.T['fg2'], line=1.5)
    s.hline(gx + 36, gy + 596, gw - 72)
    s.eyebrow(gx + 36, gy + 620, 'Master line')
    s.text(gx + 36, gy + 648, gw - 72, 50, 'Experiential design you can walk into.', size=22, font='display', line=1.2)
    # card 2 — pillars + archetype + personality
    x2 = gx + gw + 36
    s.room(x2, gy, gw, gh)
    s.eyebrow(x2 + 36, gy + 32, 'Pillars')
    for i, (p, e) in enumerate([('Strategic Vision', 'the beam — one line from brief to visitor'),
                                ('Immersive Craft', 'the room — dark field, single lit object, large serif'),
                                ('Calm Leadership', 'restraint — one accent, measured motion, precise labels')]):
        yy = gy + 68 + i * 84
        s.text(x2 + 36, yy, 40, 30, f'{i + 1:02d}', size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
        s.text(x2 + 76, yy - 4, gw - 112, 34, p, size=22, font='head', line=1.3)
        s.text(x2 + 76, yy + 28, gw - 112, 40, e, size=15, color=s.T['fg2'], line=1.45)
    s.hline(x2 + 36, gy + 330, gw - 72)
    s.eyebrow(x2 + 36, gy + 356, 'Archetype')
    s.text(x2 + 36, gy + 388, gw - 72, 60, 'The Creator, tempered by the Sage.', size=26, font='display', line=1.2)
    s.text(x2 + 36, gy + 436, gw - 72, 80, 'A maker who thinks before building and stays composed while building at monumental scale. Not the Magician: spectacle held in a steady hand.',
           size=15, color=s.T['fg2'], line=1.5)
    s.hline(x2 + 36, gy + 540, gw - 72)
    s.eyebrow(x2 + 36, gy + 566, 'Personality')
    s.text(x2 + 36, gy + 598, gw - 72, 60, 'Calm  ·  Precise  ·  Monumental  ·  Warm  ·  Curious', size=20, font='display', line=1.3)
    # card 3 — audience + positioning
    x3 = x2 + gw + 36
    s.room(x3, gy, gw, gh)
    s.eyebrow(x3 + 36, gy + 32, 'Audience')
    for i, (p, e) in enumerate([('Institutional commissioners', 'ministries, museum authorities, cultural trusts, tourism boards'),
                                ('Corporate experience owners', 'brands building centres, pavilions, launches'),
                                ('Delivery partners', 'architects, fabricators, AV integrators, event agencies'),
                                ('Former-employer ecosystem', 'studios needing a senior independent director')]):
        yy = gy + 68 + i * 78
        s.text(x3 + 36, yy, 40, 30, f'{i + 1:02d}', size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
        s.text(x3 + 76, yy - 4, gw - 112, 34, p, size=19, font='head', line=1.3)
        s.text(x3 + 76, yy + 26, gw - 112, 40, e, size=14, color=s.T['fg2'], line=1.45)
    s.hline(x3 + 36, gy + 390, gw - 72)
    s.eyebrow(x3 + 36, gy + 416, 'Positioning')
    s.text(x3 + 36, gy + 448, gw - 72, 200,
           'For institutions and brands that must open a public experience at national scale, Sanzeed Mirza is the independent experiential design consultant who carries one creative vision from the brief to opening night — narrative, space, media and the team — in one person.',
           size=15, color=s.T['fg2'], line=1.55)
    s.hline(x3 + 36, gy + 628, gw - 72)
    s.text(x3 + 36, gy + 648, gw - 72, 40, [('Proof  ', {'font': 'head', 'color': s.T['accent_text']}),
                                            ('15+ years · 8+ years museums · 90+ projects · 60+ museums & centres', {'color': s.T['fg2']})],
           size=15, line=1.5)

    # 03 — three routes ---------------------------------------------------------------------------------------
    divider(3)
    s = content('light', 3, 'Three routes')
    s.title('Three routes, one decision.', size=72)
    s.text(M + 900, 136, 824, 60, 'Each developed to the same depth before choosing. Route A refines the wordmark that already existed and adds the swooping Z; the other two would have replaced it.',
           size=17, color=s.T['fg2'], line=1.5)
    routes = [
        ('A', 'The Point of Light', 'Chosen', [C['black'], C['plaster'], C['lamp'], C['oldgold']],
         'Evolve what exists: black and cream with the gold accent; your own wordmark refined letter by letter, keeping its shapes, with a new swooping Z and a third point of light; the S-and-dot promoted to a brand mark; a graphic language built from the dot, the beam and the room; Fraunces, Inter Tight and Inter kept.',
         'Keeps the logo the client already owns, cleaned rather than replaced · the idea is already in the copy · premium, institutional · survives print, signage and motion.',
         'Less of a "big reveal" · dark-first systems need careful light-mode and print rules — solved in the colour system.'),
        ('B', 'The Plan', 'Not chosen', [C['paper'], C['soot'], C['slatedeep'], C['red']],
         'Architectural drawing language: monochrome ink on paper, blueprint grids, floor-plan diagrams as graphic devices, a signal-red accent, a grotesque typeface.',
         'Distinctive in the museum-design category · highly systematic.',
         'Reads as an architecture practice rather than a storyteller · discards the gold "light" idea and the existing wordmark · cold where the brand is warm.'),
        ('C', 'Spectacle', 'Not chosen', ['#B5338A', '#2BB3C0', C['amber'], C['black']],
         'Projection-mapping energy: saturated light gradients, motion-blur typography, full-bleed show photography, heavy display type.',
         'Dramatic, social-media friendly · communicates the show work instantly.',
         'Contradicts "calm leadership" · dates quickly · weak on paper and in institutional proposals · makes national-museum work look like event marketing.'),
    ]
    for i, (k, nm, status, sw, desc, pro, con) in enumerate(routes):
        x = M + i * 588; y = 236; w = 552; h = 720
        s.room(x, y, w, h, fill=s.T['card'])
        s.eyebrow(x + 36, y + 32, f'Route {k}')
        if k == 'A':
            s.point(x + w - 56, y + 44, r=6, glow=False)
            s.text(x + w - 200, y + 32, 136, 26, status, size=13, font='head', color=s.T['accent_text'], align='right', tracking=0.08, line=1.6)
        else:
            s.text(x + w - 200, y + 32, 164, 26, status, size=13, font='head', color=s.T['fg3'], align='right', tracking=0.08, line=1.6)
        s.text(x + 36, y + 64, w - 72, 60, nm + '.', size=40, font='display', line=1.1)
        for j, col in enumerate(sw):
            s.rect(x + 36 + j * 60, y + 136, 48, 48, fill=col, line=s.T['line'], radius=10)
        if k == 'A':
            svg, png = logo('primary-wordmark', 'full-colour-light')
            s.img(svg, x + 300, y + 148, 216, 216 * ar(svg), mode='contain', png=png)
        s.text(x + 36, y + 212, w - 72, 170, desc, size=15, color=s.T['fg2'], line=1.5)
        s.hline(x + 36, y + 392, w - 72)
        s.text(x + 36, y + 412, w - 72, 20, 'For', size=13, font='head', color=s.T['accent_text'], tracking=0.12, caps=True, line=1.3)
        s.text(x + 36, y + 440, w - 72, 110, pro, size=15, color=s.T['fg'], line=1.5)
        s.text(x + 36, y + 552, w - 72, 20, 'Against', size=13, font='head', color=s.T['fg3'], tracking=0.12, caps=True, line=1.3)
        s.text(x + 36, y + 580, w - 72, 120, con, size=15, color=s.T['fg2'], line=1.5)

    # 04 — the idea -------------------------------------------------------------------------------------------
    divider(4)
    s = content('dark', 4, 'The point, the beam, the room')
    s.title('The point, the beam, the room.', size=72)
    s.text(M + 1060, 136, 764, 60, 'Three things, drawn from the wordmark itself. Every asset in the package is made of them and nothing else.',
           size=17, color=s.T['fg2'], line=1.5)
    colw = 544
    for i, (nm, cap) in enumerate([
            ('The point', 'A gold dot, r = 0.7 × the stroke of its context. It sits in the A, the Z and the D of the wordmark, ends the signature, closes headlines ("lit.") and becomes the symbol. On dark it may glow.'),
            ('The beam', 'The 1 px hairline the point travels along: the route through a museum, the timeline of a career, the rule in a document, the wipe in motion.'),
            ('The room', 'A rounded rectangle, radius 28 (20 small), hairline border, Charcoal on dark / Paper on light. Cards, frames, image plates and these slides.')]):
        x = M + i * (colw + 48)
        s.room(x, 250, colw, 440, fill=C['night'])
        if i == 0:
            s.point(x + colw / 2, 470, r=22)
        elif i == 1:
            s.hline(x + 64, 470, colw - 128, color=C['graphite'])
            s.point(x + 64 + (colw - 128) * 0.62, 470.5, r=8)
            s.ellipse(x + 64, 470.5, 3, fill=s.T['fg3'], glow=False)
            s.ellipse(x + colw - 64, 470.5, 3, fill=s.T['fg3'], glow=False)
        else:
            s.rect(x + 112, 330, colw - 224, 280, fill=C['charcoal'], line=LINE_D, radius=28)
            s.point(x + 112 + 28, 330 + 280 - 28, r=5)
        s.wall_label(x, 712, f'{i + 1:03d}', nm, '')
        s.text(x, 746, colw, 200, cap, size=16, color=s.T['fg2'], line=1.55)

    s = content('dark', 4, 'Between two points of light')
    s.title('Between two points of light.', size=72)
    s.text(M + 1000, 136, 824, 60, 'The diagrams the system is drawn with — monoline at the wordmark\'s stroke weight, gold points, the dotted route.',
           size=17, color=s.T['fg2'], line=1.5)
    btp = f'{ILL}/sanzeed-illustration-between-two-points--dark.png'
    s.img(btp, M, 250, 1040, 520, mode='contain')
    s.wall_label(M, 790, '001', 'Between two points of light', 'the brief, the visitor, seven ways across · 05_GRAPHIC_ASSETS/Illustrations', w=1040)
    s.text(M, 846, 1040, 120, '"Between two points of light. A brief on one side, a visitor on the other. Seven ways to carry the light across." — the line already on sanzeed.com that the whole identity is built from.',
           size=16, color=s.T['fg2'], line=1.55)
    route = f'{ILL}/sanzeed-illustration-museum-route--dark.png'
    s.img(route, 1184, 250, 640, 416, mode='contain')
    s.wall_label(1184, 672, '002', 'The museum route', 'eight rooms, one dotted route, a point of light in each', w=640)
    meth = f'{ILL}/sanzeed-illustration-method-diagram--dark.png'
    s.img(meth, 1184, 740, 640, 203, mode='contain')
    s.wall_label(1184, 950, '003', 'The method', 'Discover · Direct · Craft · Deliver as four points on one beam', w=640)

    # 05 — logo family ----------------------------------------------------------------------------------------
    divider(5)
    s = content('black', 5, 'Primary logo', wordmark=False)
    s.lamp(960, 540, 1700, 1.0)
    svg, png = logo('primary-wordmark', 'full-colour-dark')
    lw = 1200; lh = lw * ar(svg)
    s.img(svg, (W - lw) / 2, 540 - lh / 2, lw, lh, mode='contain', png=png)
    s.wall_label(M, 940, '001', 'Primary logo — your wordmark, refined',
                 'full-colour-dark · three points of light: A, Z, D · the Z point in its open ring · 02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg', w=1728)

    # your original → refined (the client chose to keep their own logo)
    s = content('dark', 5, 'Your original, refined')
    s.title('Your original, refined.', size=72)
    s.text(M + 800, 136, 1024, 60, 'You chose to keep your own logo. The hand-drawn SANZEED from sanzeed.com was cleaned letter by letter, not redrawn on a new geometry; only the Z is new.',
           size=17, color=s.T['fg2'], line=1.5)
    osvg, opng = original_wordmark()
    nsvg, npng = logo('primary-wordmark', 'full-colour-dark')
    u = 960 / imsize(osvg)[0]                         # one scale for both: units of the live site's 3729 × 561 box
    rw, rh = 1160, 300
    # the original is placed as its Chromium raster in both renderers: its traced path fills differently once
    # converted to PDF vector (the Z's tapered bottom bar is straightened), and the raster is what the site shows
    for k, (sv, pn, yy, ctr, nm, pl) in enumerate([
            (opng, opng, 236, '001', 'Your original', 'sanzeed.com as found, 5 November 2026 · inline SVG 3729 × 561 · 00_ORIGINAL_ASSETS_BACKUP/logo/wordmark-inline-original.svg'),
            (nsvg, npng, 610, '002', 'Refined', 'the primary wordmark, full-colour-dark · 02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg')]):
        s.rect(M, yy, rw, rh, fill=C['black'], line=LINE_D, radius=28)
        iw, ih = imsize(osvg if k == 0 else sv); lw, lh = iw * u, ih * u
        s.img(sv, M + (rw - lw) / 2, yy + (rh - lh) / 2, lw, lh, mode='contain', png=pn)
        s.wall_label(M, yy + rh + 14, ctr, nm, pl, w=rw, size=14)
    cx = M + rw + 64; cw_ = W - M - cx
    s.eyebrow(cx, 236, 'What changed, letter by letter')
    yy = 276
    for i, (a, b) in enumerate([
            ('S, A, N and D — yours', 'Your shapes re-traced with smooth edges; the lines you drew straight made exactly straight.'),
            ('E — exact bars', 'Each bar an exact rectangle, at the size you drew it.'),
            ('A and D points — kept', 'The two original points of light, at their original size and position.'),
            ('Z — new', 'Straight top and bottom bars; the diagonal swoops like the right leg of your N.'),
            ('A third point of light', 'At the height of the D point, inside a thin ring that always shows the background. Three points: A, Z, D.')]):
        s.hline(cx, yy, cw_)
        s.text(cx, yy + 18, 50, 24, f'{i + 1:03d}', size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
        s.text(cx + 56, yy + 14, cw_ - 56, 30, a, size=19, font='head', line=1.3)
        s.text(cx + 56, yy + 44, cw_ - 56, 80, b, size=15, color=s.T['fg2'], line=1.5)
        yy += 136
    s.hline(cx, yy, cw_)

    s = content('dark', 5, 'The family')
    s.title('The family.', size=72)
    s.text(M + 420, 136, 1300, 60, 'One refined master, eleven variants. Each shown here on the background it is paired with: full-colour-dark on Gallery Black, full-colour-light on Plaster.',
           size=17, color=s.T['fg2'], line=1.5)
    fam = [
        ('secondary-symbol-wordmark', 'dark', '002', 'Secondary logo', 'symbol + wordmark · partner lockups', 0.78),
        ('horizontal-descriptor', 'light', '003', 'Horizontal logo', 'wordmark + descriptor · stationery, proposals, press', 0.78),
        ('vertical-stacked', 'dark', '004', 'Vertical / stacked logo', 'square and centred layouts, end cards, stamps', 0.62),
        ('symbol', 'light', '005', 'Symbol', 'your hooked S with its full stop · avatars, favicons, watermarks', 0.42),
        ('monogram', 'dark', '006', 'Monogram', 'SM. — the M built from two of the wordmark\'s N · seals, embossing, ID reverse', 0.44),
        ('signature', 'light', '007', 'Signature mark', 'the personal layer · letters, thank-you cards, sign-offs', 0.56),
    ]
    tw, th = 544, 296
    for i, (var, ground, ctr, nm, use, frac) in enumerate(fam):
        x = M + (i % 3) * (tw + 48); y = 244 + (i // 3) * (th + 60)
        fill = C['black'] if ground == 'dark' else C['plaster']
        s.rect(x, y, tw, th, fill=fill, line=LINE_D if ground == 'dark' else LINE_L, radius=28)
        if var == 'signature':
            sv, pn = signature('white' if ground == 'dark' else 'ink')
        else:
            sv, pn = logo(var, 'full-colour-dark' if ground == 'dark' else 'full-colour-light')
        iw, ih = imsize(sv)
        lw = tw * frac; lh = lw * ih / iw
        if lh > th * 0.62:
            lh = th * 0.62; lw = lh * iw / ih
        s.img(sv, x + (tw - lw) / 2, y + (th - lh) / 2, lw, lh, mode='contain', png=pn)
        s.wall_label(x, y + th + 14, ctr, nm, use, w=tw)

    s = content('dark', 5, 'Colourways and small sizes')
    s.title('Colourways, and the small sizes.', size=72)
    cw, ch = 408, 220
    ways = [
        ('full-colour-dark', C['black'], 'Full colour · dark', 'Gallery White + Lamp Gold · screens'),
        ('full-colour-light', C['plaster'], 'Full colour · light', 'Soot + Old Gold · documents, print'),
        ('white', C['charcoal'], 'White', 'reversed out of dark photography or solid colour'),
        ('black', C['paper'], 'Black', 'single-ink print, fax, engraving'),
        ('grayscale-inverted', C['night'], 'Grayscale inverted', 'mono print on dark'),
        ('grayscale', '#FFFFFF', 'Grayscale', 'mono print on light'),
        ('single-colour-gold', C['plaster'], 'Single colour gold', 'spot colour or foil'),
        ('black', C['oldgold'], 'Black on the gold tile', 'the only logo allowed on gold'),
    ]
    for i, (colour, ground, nm, use) in enumerate(ways):
        x = M + (i % 4) * (cw + 32); y = 244 + (i // 4) * (ch + 62)
        s.rect(x, y, cw, ch, fill=ground, line=LINE_D, radius=20)
        sv, pn = logo('primary-wordmark', colour)
        lw = cw * 0.72; lh = lw * ar(sv)
        s.img(sv, x + (cw - lw) / 2, y + (ch - lh) / 2, lw, lh, mode='contain', png=pn)
        s.wall_label(x, y + ch + 12, f'{i + 1:03d}', nm, use, w=cw, size=13)
    # small sizes strip
    sy = 820
    s.hline(M, sy, W - 2 * M)
    s.eyebrow(M, sy + 20, 'Below 120 px / 28 mm')
    sv, pn = logo('simplified-small-size', 'full-colour-dark')
    s.img(sv, M, sy + 56, 120, 120 * ar(sv), mode='contain', png=pn)
    s.text(M + 140, sy + 50, 540, 60, [('Simplified small-size logo', {'font': 'head', 'color': s.T['fg']}),
                                       ('  strokes 10 units heavier per side, rings opened around larger points · 24–120 px', {'color': s.T['fg3']})], size=14, line=1.5)
    s.eyebrow(M + 700, sy + 20, 'Below 24 px / 6 mm')
    sv, pn = logo('symbol-small-size', 'full-colour-dark')
    s.img(sv, M + 700, sy + 56, 36, 36 * ar(sv), mode='contain', png=pn)
    s.img(sv, M + 752, sy + 60, 20, 20 * ar(sv), mode='contain', png=pn)
    s.text(M + 800, sy + 50, 420, 60, [('Small-size symbol', {'font': 'head', 'color': s.T['fg']}),
                                       ('  favicon 16 px, list icons, stamps', {'color': s.T['fg3']})], size=14, line=1.5)
    s.eyebrow(M + 1260, sy + 20, 'Tiles')
    for j, col in enumerate(['dark', 'light', 'gold']):
        sv, pn = tile(col)
        s.img(sv, M + 1260 + j * 80, sy + 50, 64, 64, mode='contain', png=pn)
    s.text(M + 1510, sy + 50, 260, 60, [('Symbol tiles', {'font': 'head', 'color': s.T['fg']}),
                                        ('  app icons, profile images', {'color': s.T['fg3']})], size=14, line=1.5)

    # 06 — construction and rules -----------------------------------------------------------------------------
    divider(6)
    s = content('dark', 6, 'Construction and clear space')
    s.title('Refined on a grid, kept in the clear.', size=72)
    cons = f'{GUIDE}/logo-construction.png'
    ccrop = (0, 0, 1, 0.66)                              # the sheet's drawing; its lower third is empty
    cw_ = 1160; chh = cw_ * imsize(cons)[1] * ccrop[3] / imsize(cons)[0]
    s.img(cons, M, 236, cw_, chh, mode='contain', radius=20, border=LINE_D, crop=ccrop)
    s.wall_label(M, 236 + chh + 14, '001', 'Construction', 'the refined original wordmark on a 20-unit grid · cap line, point line, baseline · 02_LOGO_SYSTEM/Guidelines/logo-construction.png', w=cw_)
    clear = f'{GUIDE}/logo-clear-space.png'
    s.img(clear, 1304, 236, 520, 325, mode='contain', radius=20, border=LINE_D)
    s.wall_label(1304, 575, '002', 'Clear space', 'x = ½ cap height on all sides; symbol alone ¼ of its height', w=520, size=14)
    s.text(1304, 640, 520, 200, 'The ring around the Z point is part of the mark. On photography or colour it shows the background through it, never a fill. The Z and D points share one height; the S overshoots the cap line, as in your original.',
           size=15, color=s.T['fg2'], line=1.55)
    for j, (n, l) in enumerate([('3', 'points of light — A, Z, D'), ('45', 'unit point radius'), ('14', 'unit clear ring around each point'), ('20', 'unit construction grid')]):
        x = M + j * 290
        s.text(x, 690, 270, 80, n, size=64, font='display', line=1.0)
        s.text(x, 770, 260, 50, l, size=14, color=s.T['fg3'], line=1.4)
    s.text(M, 860, 1160, 100, 'Minimum sizes: wordmark 120 px / 28 mm · horizontal lockup 220 px / 50 mm · vertical stack 90 px / 22 mm · symbol 16 px / 6 mm · signature 160 px / 32 mm. Below those, the simplified and small-size versions take over.',
           size=15, color=s.T['fg2'], line=1.55)

    s = content('dark', 6, 'Minimum sizes, placement and misuse')
    s.title('Twelve things never to do.', size=72)
    mis = f'{GUIDE}/logo-incorrect-usage.png'
    s.img(mis, M, 236, 760, 697, mode='contain', radius=20, border=LINE_D)
    s.wall_label(M, 948, '001', 'Incorrect usage', '02_LOGO_SYSTEM/Guidelines/logo-incorrect-usage.svg', w=760)
    mins = f'{GUIDE}/logo-minimum-sizes@2x.png'
    s.img(mins, 904, 236, 440, 314, mode='contain', radius=20, border=LINE_D)
    s.wall_label(904, 564, '002', 'Minimum sizes', 'screen and print', w=440)
    plc = f'{GUIDE}/logo-placement.png'
    s.img(plc, 1376, 236, 448, 243, mode='contain', radius=20, border=LINE_D)
    s.wall_label(1376, 494, '003', 'Placement', 'top-left or centred; documents at 20 mm', w=448)
    s.text(904, 630, 920, 320,
           'Never stretch, rotate, outline, add shadows, bevels or glows to the letters (the dots may glow in motion only), recolour the dots a non-gold colour, change the letter spacing, set the name in a typeface instead of the wordmark, pair it with the old raster signature, place the descriptor in another font or case, or crop the S.\n\n'
           'Backgrounds: flat brand colours, or photography darkened with the veil so the logo sits on ≥ 80 % black. Never on busy imagery, never on gold (except the black logo on the gold tile), never on gradients other than dusk and lamp.',
           size=16, color=s.T['fg2'], line=1.55)

    # 07 — colour ---------------------------------------------------------------------------------------------
    divider(7)
    s = content('dark', 7, 'Colour system')
    s.title('Dark is the gallery, cream is the label.', size=72)
    s.text(M + 1240, 136, 584, 60, '25 colours in three groups. One gold accent per composition — never two, never tints of gold.',
           size=16, color=s.T['fg2'], line=1.5)
    groups = [
        ('Core · dark', [('Gallery Black', 'black'), ('Night', 'night'), ('Charcoal', 'charcoal'), ('Graphite', 'graphite'), ('Mist', 'mist'), ('Silver', 'silver'), ('Gallery White', 'gwhite')]),
        ('Core · light', [('Plaster', 'plaster'), ('Paper', 'paper'), ('Stone', 'stone'), ('Umber', 'umber'), ('Soot', 'soot')]),
        ('Accent', [('Lamp Gold', 'lamp'), ('Lamp Light', 'lamplight'), ('Old Gold', 'oldgold'), ('Amber', 'amber'), ('Gold Ink', 'goldink')]),
        ('Functional', [('Moss', 'moss'), ('Moss Deep', 'mossdeep'), ('Ochre', 'ochre'), ('Ochre Deep', 'ochredeep'), ('Signal Red', 'red'), ('Brick', 'brick'), ('Slate Blue', 'slate'), ('Slate Deep', 'slatedeep')]),
    ]
    yy = 236
    for gname, items in groups:
        s.eyebrow(M, yy, gname, size=13)
        n = len(items); sw = (W - 2 * M - (n - 1) * 16) / n
        swh = 96 if gname.startswith('Core') else 72
        for j, (nm, key) in enumerate(items):
            x = M + j * (sw + 16)
            s.rect(x, yy + 26, sw, swh, fill=C[key], line=LINE_D, radius=12)
            s.text(x + 14, yy + 34, sw - 28, 24, nm, size=13, font='head', color=C['gwhite'] if key in ('black', 'night', 'charcoal', 'graphite', 'mist', 'umber', 'soot', 'goldink', 'mossdeep', 'brick', 'slatedeep', 'ochredeep', 'red', 'slate', 'moss', 'oldgold', 'ochre') else C['soot'], line=1.3)
            s.text(x + 14, yy + 26 + swh - 28, sw - 28, 22, C[key], size=12, color=C['silver'] if key in ('black', 'night', 'charcoal', 'graphite', 'mist', 'umber', 'soot', 'goldink', 'mossdeep', 'brick', 'slatedeep', 'ochredeep', 'red', 'slate', 'moss', 'oldgold', 'ochre') else C['umber'], line=1.3)
        yy += 26 + swh + 22
    # gradients strip
    s.eyebrow(M, yy + 6, 'Gradients', size=13)
    gy2 = yy + 32; gw2 = (W - 2 * M - 4 * 16) / 5; gh2 = 1002 - 34 - gy2
    grads = [('Lamp', None, P('05_GRAPHIC_ASSETS/Backgrounds/sanzeed-bg-lamp--dark-1920x1080.jpg')),
             ('Dusk', ('linear', 180, [(0, C['black']), (1, C['charcoal'])]), None),
             ('Plaster', ('linear', 180, [(0, C['paper']), (1, C['stone'])]), None),
             ('Foil', ('linear', 135, [(0, C['oldgold']), (0.5, C['lamplight']), (1, C['oldgold'])]), None),
             ('Veil', None, P('05_GRAPHIC_ASSETS/Backgrounds/sanzeed-bg-photo-plate--prime-minister-museum-1920x1080.jpg'))]
    for j, (nm, grad, im) in enumerate(grads):
        x = M + j * (gw2 + 16)
        if im:
            s.img(im, x, gy2, gw2, gh2, mode='cover', radius=12, border=LINE_D, focal=(0.5, 0.55))
        else:
            s.rect(x, gy2, gw2, gh2, gradient=grad, line=LINE_D, radius=12)
        dark_text = nm in ('Lamp', 'Dusk', 'Veil')
        s.text(x + 14, gy2 + 8, gw2 - 28, 24, nm, size=13, font='head', color=C['gwhite'] if dark_text else C['soot'], line=1.3)

    # 08 — typography -----------------------------------------------------------------------------------------
    divider(8)
    s = content('light', 8, 'Three families')
    s.title('Serif speaks, sans works.', size=72)
    fams = [
        ('Fraunces 300', 'display', 'Display, headlines, stats, quotes', 'Aa', 'Vision you can walk into.',
         'Light weight only, optical size 144 above 48 px, 72 for 24–48, 36 below; italic for quotes. Never letter-spaced, never below 16 px / 9 pt. Headlines in sentence case ending with a full stop; the last word may be gold.'),
        ('Inter Tight 600', 'head', 'H3, H4, eyebrows, labels, data', 'Aa', 'Immersive Storytelling & Narrative Architecture',
         'Headings that work rather than speak. Eyebrows in caps at +0.12 em in gold; counters 001; Medium 500 with tabular numerals for tables and figures.'),
        ('Inter 400', 'text', 'Body, captions, UI', 'Aa', 'I lead the whole room — story, space, graphics, media and the team that builds it.',
         'The reading face. 400 for body at a measure of 60–72 characters, 500 for buttons and inputs, 13 px for wall labels (Title in Inter Tight 600 · Place in Inter 400).'),
    ]
    for i, (nm, font, role, aa, sample, rule) in enumerate(fams):
        x = M + i * 588; y = 236; w = 552; h = 720
        s.room(x, y, w, h)
        s.eyebrow(x + 36, y + 32, role)
        s.text(x + 36, y + 56, w - 72, 240, aa, size=200, font=font, line=1.0, color=s.T['fg'])
        s.text(x + 36, y + 300, w - 72, 40, nm, size=22, font='head', line=1.3)
        s.hline(x + 36, y + 352, w - 72)
        if font == 'display':
            s.text(x + 36, y + 376, w - 72, 140, [('Vision you can walk ', {}), ('into.', {'color': s.T['accent']})], size=44, font=font, line=1.08)
        elif font == 'head':
            s.text(x + 36, y + 376, w - 72, 140, sample, size=28, font=font, line=1.25)
        else:
            s.text(x + 36, y + 376, w - 72, 140, sample, size=20, font=font, line=1.55, color=s.T['fg'])
        s.hline(x + 36, y + 540, w - 72)
        s.text(x + 36, y + 562, w - 72, 150, rule, size=14, color=s.T['fg2'], line=1.55)

    s = content('light', 8, 'The hierarchy')
    s.title('The scale, in order.', size=72)
    s.text(M + 740, 136, 1084, 60, 'Three of the ten specimen sheets in 04_TYPOGRAPHY: the display and heading hierarchy, the pairing, and the Fraunces specimen. Sizes in px for screen and pt for print live in typography-tokens.json.',
           size=16, color=s.T['fg2'], line=1.5)
    sheets = [('sanzeed-type-hierarchy-1.png', '001', 'Hierarchy', 'display-1 to H4'),
              ('sanzeed-type-pairing.png', '002', 'Pairing', 'serif and sans together'),
              ('sanzeed-type-specimen--fraunces-1.png', '003', 'Fraunces specimen', 'weights, axes, italics')]
    for i, (f, ctr, nm, pl) in enumerate(sheets):
        src = P(f'04_TYPOGRAPHY/Typography_Specimens/{f}')
        sh = 700; sw = sh * imsize(src)[0] / imsize(src)[1]
        x = M + i * (sw + 64 + 32)
        s.img(src, x, 236, sw, sh, mode='contain', radius=12, border=LINE_L)
        s.wall_label(x, 236 + sh + 12, ctr, nm, pl + ' · Typography_Specimens', w=sw + 60, size=13)

    # 09 — graphic language -----------------------------------------------------------------------------------
    divider(9)
    s = content('dark', 9, 'Patterns, icons, illustrations, textures')
    s.title('The only decorative vocabulary.', size=72)
    pat = P('05_GRAPHIC_ASSETS/Patterns/sanzeed-patterns-contact-sheet.png')
    s.img(pat, M, 236, 760, 475, mode='contain', radius=20, border=LINE_D)
    s.wall_label(M, 726, '001', 'Patterns', 'seven seamless tiles × two inks, at ≤ 12 % behind content', w=760)
    ico = P('05_GRAPHIC_ASSETS/Icons/sanzeed-icons-sheet.png')
    s.img(ico, 888, 236, 740, 475, mode='contain', radius=20, border=LINE_D)
    s.wall_label(888, 726, '002', 'Icons', '54 icons on the 24 grid, dark and light ink, SVG + sprite', w=740)
    # textures column
    tex = [('sanzeed-texture-lamp-glow--2048.png', 'Lamp glow'), ('sanzeed-texture-grain--tile-1024.png', 'Grain 7 %'),
           ('sanzeed-texture-paper--plaster-2048.jpg', 'Paper'), ('sanzeed-texture-vignette--1920x1080.png', 'Vignette')]
    for j, (f, nm) in enumerate(tex):
        src = P(f'05_GRAPHIC_ASSETS/Textures/{f}')
        y = 236 + j * 118
        s.rect(1660, y, 164, 104, fill=C['black'] if 'paper' not in f else C['plaster'], line=LINE_D, radius=12)
        s.img(src, 1660, y, 164, 104, mode='cover', radius=12)
        s.text(1660, y + 80, 164, 20, nm, size=12, font='head', color=C['gwhite'] if 'paper' not in f else C['soot'], line=1.3, align='center')
    s.wall_label(1660, 726, '003', 'Textures', '', w=164, size=13)
    # illustrations row
    glyphs = ['01-experiential-design', '02-museum-planning', '03-storytelling', '04-spatial-branding', '05-event-production', '06-digital-physical', '07-leadership']
    s.eyebrow(M, 790, 'Seven service glyphs', size=13)
    for j, g in enumerate(glyphs):
        src = f'{ILL}/sanzeed-illustration-service-glyph-{g}--dark.png'; assert os.path.exists(src)
        s.img(src, M + j * 96, 820, 76, 76, mode='contain')
    orb = f'{ILL}/sanzeed-illustration-orbit-object--dark.png'
    s.img(orb, 900, 790, 220, 163, mode='contain')
    s.wall_label(1140, 800, '004', 'Orbit object', 'the site hero, drawn flat', w=300, size=13)
    lampill = f'{ILL}/sanzeed-illustration-lamp--dark.png'
    s.img(lampill, 1440, 780, 136, 170, mode='contain')
    s.wall_label(1600, 800, '005', 'The lamp', 'arch, point, pool', w=224, size=13)
    s.text(1140, 840, 280, 110, 'Monoline drawings at the wordmark\'s stroke weight; labels outlined from the brand fonts; dark and light inks.',
           size=13, color=s.T['fg3'], line=1.5)

    # 10 — photography ----------------------------------------------------------------------------------------
    divider(10)
    s = content('dark', 10, 'Moodboard')
    s.title('The lit room.', size=72)
    s.text(M + 420, 136, 1404, 60, 'One dominant light source. Blacks that hold detail, never crushed. Highlights that lean toward Lamp Gold. A person for scale, walking into the light. Dark is the gallery; the wall label captions every picture.',
           size=16, color=s.T['fg2'], line=1.5)
    for i, (f, ctr, nm, pl) in enumerate([('p01-overview', '001', 'Moodboard 001', 'Overview — the lit room'),
                                          ('p02-museums-experience-centres', '002', 'Moodboard 002', 'Museums and experience centres')]):
        src = P(f'06_PHOTOGRAPHY_ART_DIRECTION/Moodboard_Pages/sanzeed-moodboard--{f}.png')
        x = M + i * 880
        s.img(src, x, 236, 848, 600, mode='contain', radius=20, border=LINE_D)
        s.wall_label(x, 852, ctr, nm, pl + ' · A3 · 06_PHOTOGRAPHY_ART_DIRECTION/Moodboard.pdf', w=848)
    s.text(M, 892, 1728, 60, 'Thirty approved project images carry a repeatable grade (grade.py): S-curve contrast, a toe landing on Night, highlights warmed toward Lamp Gold. Rights: employee work for Tagbin, Sociopixel, DWS and B2W; portfolio and credential use.',
           size=14, color=s.T['fg3'], line=1.5)

    s = content('dark', 10, 'The grade')
    s.title('The grade, and the wall label.', size=72)
    ba = P('06_PHOTOGRAPHY_ART_DIRECTION/Image_Templates/examples/sanzeed-template--before-after-grade.png')
    s.img(ba, M, 236, 1000, 562, mode='contain', radius=20, border=LINE_D)
    s.wall_label(M, 814, '001', 'Before / after', 'the brand grade on an approved image · Image_Templates/before-after-grade.html', w=1000)
    s.text(M, 856, 1000, 100, 'Reference curve 0 → 13, 64 → 57, 128 → 128, 192 → 199, 255 → 255; warm shift of the 55–100 % band toward Lamp Gold, max 10 %; saturation 1.00. Portrait, 4:5, 1:1, 16:9 and 9:16 templates crop from a named focal point.',
           size=14, color=s.T['fg3'], line=1.5)
    for j, (f, ctr, nm, pl, fo) in enumerate([('sanzeed-img-ram-katha-show-diyas--projection.jpg', '002', 'Ram Katha Show', 'Ayodhya', (0.5, 0.5)),
                                              ('sanzeed-img-yuge-yugeen-bharat-museum--museum.jpg', '003', 'Yuge Yugeen Bharat Museum', 'New Delhi', (0.5, 0.58))]):
        src = f'{IMG}/{f}'; assert os.path.exists(src)
        y = 236 + j * 372
        s.img(src, 1136, y, 688, 316, mode='cover', focal=fo, radius=20, border=LINE_D)
        s.wall_label(1136, y + 330, ctr, nm, pl + ' · graded · Approved_Images', w=688)

    # 11 — website --------------------------------------------------------------------------------------------
    divider(11)
    s = content('dark', 11, 'Before and after')
    s.title('Before, and after.', size=72)
    s.text(M + 560, 136, 1264, 60, 'A drop-in replacement for the live Netlify site: same structure, copy, layout and scripts; new wordmark, served favicons and fonts, token-aligned colours, vector signature, footer lockup, new share images.',
           size=16, color=s.T['fg2'], line=1.5)
    bef = P('16_WEBSITE_IMPLEMENTATION/screenshots/before-index-desktop-dark.jpg')
    aft = P('16_WEBSITE_IMPLEMENTATION/screenshots/after-index-desktop-dark.jpg')
    s.img(bef, M, 236, 848, 530, mode='contain', radius=20, border=LINE_D)
    s.wall_label(M, 782, '001', 'Before', 'sanzeed.com as found, 5 November 2026 · 00_ORIGINAL_ASSETS_BACKUP', w=848)
    s.img(aft, 976, 236, 848, 530, mode='contain', radius=20, border=LINE_D)
    s.wall_label(976, 782, '002', 'After', '16_WEBSITE_IMPLEMENTATION · index.html', w=848)
    hb = P('16_WEBSITE_IMPLEMENTATION/screenshots/before-index-desktop-header-2x.png')
    ha = P('16_WEBSITE_IMPLEMENTATION/screenshots/after-index-desktop-header-2x.png')
    s.img(hb, M, 836, 848, 848 * imsize(hb)[1] / imsize(hb)[0], mode='contain', radius=8, border=LINE_D)
    s.img(ha, 976, 836, 848, 848 * imsize(ha)[1] / imsize(ha)[0], mode='contain', radius=8, border=LINE_D)
    s.wall_label(M, 900, '003', 'Header, before', 'hand-traced wordmark', w=848, size=13)
    s.wall_label(976, 900, '004', 'Header, after', 'refined original wordmark, same height', w=848, size=13)

    s = content('dark', 11, 'UI kit and responsive')
    s.title('The design system behind it.', size=72)
    kit = P('07_WEBSITE_DIGITAL_ASSETS/UI_Components/renders/ui-kit--1440.png')
    kw, kh = imsize(kit)
    s.img(kit, M, 236, 760, 686, mode='contain', radius=20, border=LINE_D, crop=(0, 0, 1, 1300 / kh))
    s.wall_label(M, 938, '001', 'UI component library', 'top of the 26-component kit · UI_Components/ui-kit.html', w=760)
    resp = P('07_WEBSITE_DIGITAL_ASSETS/UI_Components/renders/responsive-sheet.png')
    s.img(resp, 904, 236, 920, 389, mode='contain', radius=20, border=LINE_D)
    s.wall_label(904, 640, '002', 'Responsive', '1440 · 1280 · 834 · 390 px', w=920)
    s.text(904, 690, 920, 260,
           'What changed on the site, and nothing else: the inline wordmark SVG in loader and header; the horizontal-descriptor lockup in the footer; favicon.ico, SVG favicon, apple-touch, android-chrome, maskable icon and web manifest, served as files; the four variable woff2 fonts served instead of base64; colour tokens aligned to the system; the vector signature in place of the PNGs; an OG image per page.\n\nThe six hover-loop videos were not in the backup and must be copied from the current deploy before publishing.',
           size=15, color=s.T['fg2'], line=1.55)

    # 12 — digital assets -------------------------------------------------------------------------------------
    divider(12)
    s = content('dark', 12, 'Share images, email, icons')
    s.title('Everything a platform asks for.', size=72)
    og1 = P('07_WEBSITE_DIGITAL_ASSETS/Open_Graph/sanzeed-og--home-1200x630.png')
    og2 = P('07_WEBSITE_DIGITAL_ASSETS/Open_Graph/sanzeed-og--work--prime-minister-museum-1200x630.png')
    s.img(og1, M, 236, 544, 286, mode='contain', radius=16, border=LINE_D)
    s.wall_label(M, 534, '001', 'Open Graph — home', '1200 × 630', w=544, size=13)
    s.img(og2, M, 586, 544, 286, mode='contain', radius=16, border=LINE_D)
    s.wall_label(M, 884, '002', 'Open Graph — case study', 'Prime Minister Museum · New Delhi · 1200 × 630', w=544, size=13)
    x2 = M + 592
    eh = P('07_WEBSITE_DIGITAL_ASSETS/Email/sanzeed-email-header--dark-1200x400.png')
    el = P('07_WEBSITE_DIGITAL_ASSETS/Email/sanzeed-email-header--light-1200x400.png')
    s.img(eh, x2, 236, 544, 181, mode='contain', radius=16, border=LINE_D)
    s.wall_label(x2, 429, '003', 'Email header — dark', '1200 × 400 (600 × 200 @ 2×)', w=544, size=13)
    s.img(el, x2, 476, 544, 181, mode='contain', radius=16, border=LINE_D)
    s.wall_label(x2, 669, '004', 'Email header — light', '1200 × 400', w=544, size=13)
    ap = P('07_WEBSITE_DIGITAL_ASSETS/App_Icons/app-icons-preview.png')
    s.img(ap, x2, 716, 544, 208, mode='contain', radius=16, border=LINE_D)
    s.wall_label(x2, 936, '005', 'App icons', 'iOS · Android · Windows · macOS · PWA', w=544, size=13)
    x3 = M + 1184
    es = P('07_WEBSITE_DIGITAL_ASSETS/Email/sanzeed-email-signature--preview.png')
    s.img(es, x3, 236, 544, 440, mode='cover', focal=(0.5, 0.0), radius=16, border=LINE_D)
    s.wall_label(x3, 690, '006', 'Email signature', 'HTML + plain text · 320 × 100 @ 2× logo', w=544, size=13)
    s.eyebrow(x3, 740, 'Favicons', size=13)
    for j, (f, sz) in enumerate([('favicon-16.png', 16), ('favicon-32.png', 32), ('favicon-48.png', 48), ('favicon-64.png', 64), ('favicon-96.png', 96), ('favicon-180.png', 150)]):
        src = P(f'07_WEBSITE_DIGITAL_ASSETS/Favicon/{f}')
        xx = x3 + [0, 36, 86, 152, 236, 352][j]
        s.img(src, xx, 770 + (150 - sz), sz, sz, mode='contain')
    s.text(x3, 936, 544, 24, [('007  ', {'font': 'head', 'color': s.T['accent_text'], 'tracking': 0.08}), ('Favicon set', {'font': 'head'}), ('  16 – 1024 px, .ico, SVG, maskable, manifest', {'color': s.T['fg3']})], size=13, line=1.3)

    # 13 — social media ---------------------------------------------------------------------------------------
    divider(13)
    s = content('dark', 13, 'Grid, covers, banners')
    s.title('Six platforms, one gallery.', size=72)
    grid = P('08_SOCIAL_MEDIA/Instagram/sanzeed-ig-grid-preview--3x3-1632x1632.png')
    s.img(grid, M, 236, 700, 700, mode='contain', radius=20, border=LINE_D)
    s.wall_label(M, 950, '001', 'Instagram grid', '3 × 3 preview · posts 1080 × 1080 and 1080 × 1350', w=700)
    li = P('08_SOCIAL_MEDIA/LinkedIn/sanzeed-li-banner--personal-1584x396.png')
    s.img(li, 828, 236, 996, 249, mode='contain', radius=16, border=LINE_D)
    s.wall_label(828, 498, '002', 'LinkedIn personal banner', '1584 × 396 · avatar overlap kept clear', w=996)
    xh = P('08_SOCIAL_MEDIA/X/sanzeed-x-header-1500x500.png')
    s.img(xh, 828, 548, 996, 332, mode='contain', radius=16, border=LINE_D)
    s.wall_label(828, 894, '003', 'X header', '1500 × 500', w=996)
    for j, (f, nm) in enumerate([('Instagram/sanzeed-ig-profile--dark-320x320.png', 'Instagram'), ('LinkedIn/sanzeed-li-profile--dark-400x400.png', 'LinkedIn'), ('YouTube/sanzeed-yt-profile--dark-800x800.png', 'YouTube')]):
        src = P(f'08_SOCIAL_MEDIA/{f}')
        s.img(src, 1300 + j * 120, 920, 72, 72, mode='contain', radius=36)
    s.text(1300, 930, 500, 20, '', size=12)
    s.text(1660, 940, 164, 40, 'Profile tiles', size=13, font='head', color=s.T['fg3'], line=1.3)

    s = content('dark', 13, 'Stories and highlights')
    s.title('Stories, inside the safe area.', size=72)
    stories = [('Stories/sanzeed-ig-story--project-1080x1920.png', '001', 'Story — project', 'wall label, veil'),
               ('Stories/sanzeed-ig-story--quote-1080x1920.png', '002', 'Story — quote', 'the lit last word'),
               ('Stories/sanzeed-ig-story--method-1080x1920.png', '003', 'Story — method', 'four steps on one beam'),
               ('Stories/sanzeed-ig-story--cta-1080x1920.png', '004', 'Story — call', 'Tell me about the room.')]
    for j, (f, ctr, nm, pl) in enumerate(stories):
        src = P(f'08_SOCIAL_MEDIA/Instagram/{f}')
        x = M + j * 347
        s.img(src, x, 236, 315, 560, mode='contain', radius=20, border=LINE_D)
        s.wall_label(x, 812, ctr, nm, pl, w=315, size=13)
    s.eyebrow(1500, 236, 'Highlight covers', size=13)
    hl = ['work', 'museums', 'shows', 'method', 'about', 'contact']
    for j, h in enumerate(hl):
        src = P(f'08_SOCIAL_MEDIA/Instagram/Highlight_Covers/sanzeed-ig-highlight--{h}-1080x1920.png')
        x = 1500 + (j % 2) * 170; y = 272 + (j // 2) * 170
        s.img(src, x, y, 140, 140, mode='cover', focal=(0.5, 0.5), radius=70, border=LINE_D)
        s.text(x, y + 146, 140, 20, h, size=12, color=s.T['fg3'], line=1.3, align='center')
    s.text(M, 866, 1360, 90, 'Every story keeps its copy inside the 1080 × 1420 centre-safe band; highlight covers show the symbol or an approved image inside the centre circle. Editable HTML templates with a DATA block, and PPTX versions, live in 08_SOCIAL_MEDIA/Editable_Templates.',
           size=14, color=s.T['fg3'], line=1.5)

    # 14 — stationery -----------------------------------------------------------------------------------------
    divider(14)
    s = content('dark', 14, 'Stationery, in the hand')
    s.title('Stationery, in the hand.', size=72)
    m1 = P('13_BRAND_MOCKUPS/Stationery_Mockups/sanzeed-mockup--stationery-letterhead-envelope-card-1600w.jpg')
    s.img(m1, M, 236, 1000, 667, mode='cover', focal=(0.5, 0.5), radius=20, border=LINE_D, crop=(0, 0, 1, 0.94))
    s.wall_label(M, 918, '001', 'Letterhead, DL envelope, business card', 'A4 · 220 × 110 mm · 89 × 51 mm · 13_BRAND_MOCKUPS / 09_PRINT_STATIONERY', w=1000)
    m2 = P('13_BRAND_MOCKUPS/Stationery_Mockups/sanzeed-mockup--stationery-cards-flat-lay-plaster-1600w.jpg')
    s.img(m2, 1136, 236, 688, 310, mode='cover', focal=(0.5, 0.5), radius=20, border=LINE_D, crop=(0, 0, 1, 0.94))
    s.wall_label(1136, 560, '002', 'Business cards, front and back', 'concepts A and B · 350 gsm uncoated, optional foil dots', w=688)
    m3 = P('13_BRAND_MOCKUPS/Stationery_Mockups/sanzeed-mockup--stationery-thank-you-card-open-1600w.jpg')
    s.img(m3, 1136, 608, 688, 310, mode='cover', focal=(0.5, 0.5), radius=20, border=LINE_D, crop=(0, 0, 1, 0.94))
    s.wall_label(1136, 932, '003', 'Thank-you card, open', 'A6 folded · the signature mark', w=688)

    s = content('dark', 14, 'Stationery, flat')
    s.title('The set, flat.', size=72)
    lh = P('09_PRINT_STATIONERY/Letterheads/sanzeed-letterhead--a4-first.png')
    s.img(lh, M, 236, 495, 700, mode='contain', radius=12, border=LINE_D)
    s.wall_label(M, 950, '001', 'Letterhead', 'A4 first page · also US Letter, continuation, DOCX', w=495, size=13)
    cf = P('09_PRINT_STATIONERY/Business_Cards/sanzeed-business-card--a-front-2x.png')
    cb = P('09_PRINT_STATIONERY/Business_Cards/sanzeed-business-card--a-back-2x.png')
    s.img(cf, 640, 236, 480, 275, mode='contain', radius=12, border=LINE_D)
    s.img(cb, 640, 546, 480, 275, mode='contain', radius=12, border=LINE_D)
    s.wall_label(640, 836, '002', 'Business card, concept A', '89 × 51 mm · front and back', w=480, size=13)
    env = P('09_PRINT_STATIONERY/Envelopes/sanzeed-envelope--dl-front.png')
    s.img(env, 1168, 236, 656, 328, mode='contain', radius=12, border=LINE_D)
    s.wall_label(1168, 578, '003', 'Envelope', 'DL 220 × 110 mm · also C5', w=656, size=13)
    idc = P('09_PRINT_STATIONERY/ID_Card/sanzeed-id-card--front.png')
    s.img(idc, 1168, 630, 202, 320, mode='contain', radius=12, border=LINE_D)
    ty = P('09_PRINT_STATIONERY/Thank_You_Cards/sanzeed-thank-you-card--folded-outside.png')
    s.img(ty, 1404, 630, 420, 296, mode='contain', radius=12, border=LINE_D)
    s.wall_label(1168, 964, '004', 'ID card · thank-you card', 'CR80 · A5 flat, folded to A6', w=656, size=13)
    s.text(640, 880, 480, 80, 'Also in 09_PRINT_STATIONERY: invoice, quotation, proposal and official-document DOCX templates, notepad, folder, stamp, lanyard and the 14-slide PPTX template; seventeen print-ready CMYK PDFs with marks.',
           size=13, color=s.T['fg3'], line=1.5)

    # 15 — marketing and signage ------------------------------------------------------------------------------
    divider(15)
    s = content('dark', 15, 'Posters and brochure')
    s.title('Posters, and the brochure.', size=72)
    for j, (f, ctr, nm) in enumerate([('campaign', '001', 'Campaign poster'), ('method', '002', 'Method poster')]):
        src = P(f'10_MARKETING_COLLATERAL/Posters/sanzeed-poster--{f}-a2-preview.png')
        x = M + j * 487
        s.img(src, x, 236, 455, 640, mode='contain', radius=12, border=LINE_D)
        s.wall_label(x, 892, ctr, nm, 'A2 420 × 594 mm · also A3 · print-ready CMYK', w=455, size=13)
    tri = P('10_MARKETING_COLLATERAL/Brochures/sanzeed-brochure--a4-trifold-outside.png')
    s.img(tri, 1070, 236, 754, 538, mode='contain', radius=12, border=LINE_D)
    s.wall_label(1070, 790, '003', 'Trifold brochure, outside', 'A4 297 × 210 mm · panels 99 / 98 / 100', w=754, size=13)
    s.text(1070, 830, 754, 130, 'The campaign carries one idea through every piece: a single lit object or room on black, a Fraunces headline ending in the gold point, a wall label, the wordmark, sanzeed.com. Also in 10_MARKETING_COLLATERAL: key visuals in three ratios, seven digital ads, web banners, event set, flyers, a 12-page profile, media kit, sales deck, press kit.',
           size=14, color=s.T['fg3'], line=1.5)

    s = content('dark', 15, 'Signage')
    s.title('Signage you can read from the door.', size=72)
    tot = P('10_MARKETING_COLLATERAL/Signage/sanzeed-totem--600x1800mm-1-10.png')
    s.img(tot, M, 236, 233, 700, mode='contain', radius=12, border=LINE_D)
    s.wall_label(M, 950, '001', 'Totem', '600 × 1800 mm, 1:10', w=300, size=13)
    for j, (f, ctr, nm) in enumerate([('sanzeed-door-plate--300x100mm.png', '002', 'Door plate'),
                                      ('sanzeed-wayfinding--arrow-right-300x100mm.png', '003', 'Wayfinding arrow'),
                                      ('sanzeed-wayfinding--room-001-300x100mm.png', '004', 'Room number')]):
        src = P(f'10_MARKETING_COLLATERAL/Signage/{f}')
        y = 236 + j * 250
        s.img(src, 380, y, 560, 194, mode='contain', radius=12, border=LINE_D)
        s.wall_label(380, y + 206, ctr, nm, '300 × 100 mm · cap height ≥ 25 mm per 3 m', w=560, size=13)
    mw = P('13_BRAND_MOCKUPS/Marketing_Mockups/sanzeed-mockup--marketing-door-plate-wayfinding-museum-wall-1600w.jpg')
    s.img(mw, 992, 236, 832, 555, mode='cover', focal=(0.5, 0.5), radius=20, border=LINE_D, crop=(0, 0, 1, 0.94))
    s.wall_label(992, 806, '005', 'Door plate and wayfinding, in place', 'composite on an approved museum wall · 13_BRAND_MOCKUPS', w=832)
    s.text(992, 850, 832, 110, 'Plates in brushed black with the white wordmark or symbol, type in Inter Tight; a 1:10 spec sheet with materials, fixings and cap heights, plus the window-vinyl cut file, are in 10_MARKETING_COLLATERAL/Signage.',
           size=14, color=s.T['fg3'], line=1.5)

    # 16 — motion ---------------------------------------------------------------------------------------------
    divider(16)
    s = content('dark', 16, 'Key frames')
    s.title('Light, not bounce.', size=72)
    s.text(M + 600, 136, 1224, 60, 'The logo reveal, 4 s, 1920 × 1080: the point travels the beam S → D at the height of the Z and D points and the letters bloom as it passes. The A\'s point settles, the Z\'s point settles into its open ring, and the travelling point becomes the D\'s point — three points, A, Z, D. Ease-out cubic-bezier(.22,.8,.2,1); never spun, bounced or stretched.',
           size=16, color=s.T['fg2'], line=1.5)
    kf = f'{B}/11_MOTION_GRAPHICS/Exports/Key_Frames/Logo_Animations/sanzeed-logo-reveal--dark-1920x1080'
    for j, t in enumerate(['0.00', '0.77', '1.57', '2.37', '3.17', '3.97']):
        src = f'{kf}/sanzeed-logo-reveal--dark-1920x1080--t{t}s.jpg'; assert os.path.exists(src)
        x = M + (j % 3) * 592; y = 236 + (j // 3) * 366
        s.img(src, x, y, 544, 306, mode='contain', radius=16, border=LINE_D)
        s.wall_label(x, y + 320, f'{j + 1:03d}', f't = {t} s', 'logo reveal · dark' if j == 0 else '', w=544, size=13)

    s = Slide('black', '16 · Play')
    s._chrome = (16, SEC[16][0], False)
    S.append(s)
    poster = P('11_MOTION_GRAPHICS/Logo_Animations/sanzeed-logo-reveal--dark-1920x1080--poster.jpg')
    s.img(poster, 0, 0, W, Hh, mode='cover')
    # play affordance: the point on its ring
    s.ellipse(960, 760, 44, fill=None, line=C['gwhite'], lw=1)
    s.point(960, 760, r=7)
    s.text(760, 822, 400, 24, 'Play the reveal', size=14, font='head', color=s.T['fg2'], align='center', tracking=0.12, caps=True, line=1.4)
    s.wall_label(M, 940, '001', 'Logo reveal', '4 s · 1920 × 1080 · three points settle, A, Z, D; the Z ring stays open · MP4 H.264, WebM VP9, GIF · 11_MOTION_GRAPHICS/Logo_Animations', w=1200)
    s.text(W - M - 600, 136, 600, 330,
           'Also delivered\n\n'
           'Logo reveal on Plaster, 1:1 and 9:16\n'
           'Logo outro, 3 s\n'
           'Symbol loop, seamless, alpha\n'
           'Presentation logo, alpha\n'
           'Branded intro and end card, 6 s, two formats\n'
           'Beam transition, 1.5 s, alpha\n'
           'Three stories, two posts, a stat counter\n'
           'Three lower thirds with alpha (ProRes 4444, WebM)\n'
           'Website loader: CSS, SVG + SMIL, Lottie, GIF, MP4\n\n'
           'Lottie JSON and HTML/CSS sources import into After Effects.',
           size=15, color=s.T['fg2'], line=1.65, align='right')

    # 17 — applications gallery -------------------------------------------------------------------------------
    divider(17)
    gallery = [
        ('Logo_Mockups/sanzeed-mockup--logo-gold-foil-black-1600w.jpg', '001', 'Gold foil', 'primary wordmark hot-stamped on black stock', (0.5, 0.5)),
        ('Logo_Mockups/sanzeed-mockup--logo-backlit-signage-night-1600w.jpg', '002', 'Halo-lit signage', 'fabricated letters on a dark wall, night', (0.5, 0.5)),
        ('Digital_Mockups/sanzeed-mockup--digital-website-laptop-dark-1600w.jpg', '003', 'sanzeed.com', 'the rebuilt site on a laptop, dark theme', (0.5, 0.5)),
        ('Marketing_Mockups/sanzeed-mockup--marketing-backdrop-g20-show-1600w.jpg', '004', 'Event backdrop', 'LED wall, composite into the G20 LED Show · Gujarat', (0.5, 0.5)),
    ]
    for f, ctr, nm, pl, fo in gallery:
        s = Slide('black', f'17 · {nm}')
        s._chrome = None
        S.append(s)
        src = P(f'13_BRAND_MOCKUPS/{f}')
        s.img(src, 0, 0, W, Hh, mode='cover', focal=fo, crop=(0, 0, 1, 0.94))
        # label plate bottom-right (the room, small)
        pw = 640
        s.rect(W - M - pw, 1080 - 64 - 68, pw, 68, fill=C['night'], line=LINE_D, radius=16)
        s.text(W - M - pw + 24, 1080 - 64 - 68 + 16, pw - 48, 24,
               [(f'17 · Applications · {ctr}  ', {'font': 'head', 'color': C['lamp'], 'tracking': 0.08}), (nm, {'font': 'head', 'color': C['gwhite']})], size=15, line=1.3)
        s.text(W - M - pw + 24, 1080 - 64 - 68 + 38, pw - 48, 22, pl + '  ·  13_BRAND_MOCKUPS', size=12, color=C['mist'], line=1.3)

    # 18 — what you receive -----------------------------------------------------------------------------------
    divider(18)
    s = content('light', 18, 'The package')
    s.title('Seventeen folders, every source.', size=72)
    s.text(M + 1060, 136, 764, 60, 'Nothing here is a mockup of a deliverable; every item is the deliverable, with its editable source beside it and a README in every folder.',
           size=16, color=s.T['fg2'], line=1.5)
    folders = [
        ('00', 'Original assets backup', 'the live site untouched: HTML, images, fonts, icons, screenshots'),
        ('01', 'Brand strategy', 'audit, strategy, positioning, voice, messaging · MD + 32-page PDF'),
        ('02', 'Logo system', '11 variants × 7 colours · SVG PDF EPS PNG WebP · master refined_master.svg + build_logo_refined.py'),
        ('03', 'Colour system', 'tokens JSON CSS SCSS Tailwind · swatches · 12-page palette PDF'),
        ('04', 'Typography', 'OFL fonts TTF + woff2 · scale tokens · 10 specimens · Font Reference PDF'),
        ('05', 'Graphic assets', 'patterns, textures, illustrations, 54 icons, backgrounds, decorative elements'),
        ('06', 'Photography', '30 graded images, portrait crops, moodboard, 16-page guideline, treatments'),
        ('07', 'Website digital assets', 'UI kit, OG images, favicons, app icons, email, website graphics'),
        ('08', 'Social media', 'six platforms at exact pixels · HTML + PPTX templates'),
        ('09', 'Print stationery', 'cards, letterheads, envelopes, DOCX templates, ID, stamp, folder · CMYK PDFs'),
        ('10', 'Marketing collateral', 'ads, key visuals, events, signage, posters, flyers, brochures, media kit, decks'),
        ('11', 'Motion graphics', 'reveal, intro/outro, transition, social, lower thirds, loader · MP4 WebM MOV GIF Lottie'),
        ('12', 'Brand guidelines', 'the standards manual PDF with its editable source'),
        ('13', 'Brand mockups', '35 scenes built from the real deliverables · HTML sources, JPG 3000 / 1600'),
        ('14', 'Presentation', 'this deck · PDF, slide PNGs, editable PPTX and HTML source'),
        ('15', 'Source files', 'brand kit, logo master (refined_master.svg, build_logo_refined.py), colour masters, render tools'),
        ('16', 'Website implementation', 'deployable static site with change log and verification screenshots'),
    ]
    for i, (n, nm, d) in enumerate(folders):
        col = i // 9; row = i % 9
        x = M + col * 880; y = 244 + row * 74
        s.hline(x, y, 816)
        s.text(x, y + 16, 50, 24, n, size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
        s.text(x + 56, y + 12, 300, 30, nm, size=17, font='head', line=1.3)
        s.text(x + 56, y + 38, 760, 30, d, size=13, color=s.T['fg2'], line=1.4)
    s.hline(M, 244 + 9 * 74, 816)
    s.hline(M + 880, 244 + 8 * 74, 816)
    s.text(M + 880 + 56, 244 + 8 * 74 + 12, 760, 60, [('Formats  ', {'font': 'head', 'color': s.T['accent_text']}),
                                                       ('SVG · PDF · EPS · PNG · JPG · WebP · ICO · DOCX · PPTX · HTML/CSS/JS · Lottie JSON · MP4 · WebM · MOV ProRes 4444 · GIF · TTF / woff2 · JSON / CSS / SCSS. Not supplied: .ai, .psd, .indd, .aep, .fig — every SVG and PDF opens as editable vector in Illustrator and Figma.', {'color': s.T['fg2']})],
           size=13, line=1.5)

    # 19 — next steps -----------------------------------------------------------------------------------------
    divider(19)
    s = content('light', 19, 'Next steps')
    s.title('Next steps.', size=72)
    left = [
        ('Deploy the site', 'Publish 16_WEBSITE_IMPLEMENTATION to Netlify (drag-and-drop or the folder as publish directory, no build). Copy the six loop-*.mp4 hover videos from the current deploy into img/ first; run the post-deploy checklist in CHANGES.md.'),
        ('Print proofs', 'Business cards (350 gsm uncoated natural white, foil option for the dots), letterhead, envelopes, folder and thank-you cards from Print_Ready_Files; proof Old Gold on the chosen stock before a run; verify Pantone 7510 C against a swatch book.'),
        ('Register the handles', '@sanzeed on Instagram, Facebook, YouTube, X and Pinterest to match LinkedIn; upload the profile tiles and covers from 08_SOCIAL_MEDIA at the exact pixels.'),
        ('Install the fonts', 'Fraunces, Inter and Inter Tight from 04_TYPOGRAPHY/Font_Files (SIL OFL, free to install and share). Office templates reference Fraunces Light, Inter Tight SemiBold and Inter.'),
        ('Adopt the templates', 'Letterhead, invoice, quotation, proposal and official-document DOCX; the 14-slide deck; social templates. Replace bracketed fields once, then find-and-replace.'),
    ]
    right = [
        ('Registered business details', 'Registered name, GSTIN / PAN, postal address and bank details for invoices and quotations — currently bracketed fields.'),
        ('Priority audiences', 'Confirm the four segments and any sectors to decline.'),
        ('Image rights', 'Which project images may be used outside the portfolio context (employee work for Tagbin, Sociopixel, DWS and B2W).'),
        ('Original photography', 'Camera files or renders ≥ 2000 px for the A2 poster, backdrops and report covers; the same grade.py applies.'),
        ('Social handles and a date', 'Confirm the handles, and the event date for the invitation and the Facebook event cover.'),
    ]
    s.eyebrow(M, 236, 'To do — agency and production')
    yy = 276
    for i, (a, b) in enumerate(left):
        s.hline(M, yy, 900)
        s.text(M, yy + 18, 50, 24, f'{i + 1:03d}', size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
        s.text(M + 56, yy + 14, 844, 30, a, size=19, font='head', line=1.3)
        s.text(M + 56, yy + 44, 844, 80, b, size=14, color=s.T['fg2'], line=1.5)
        yy += 136
    s.hline(M, yy, 900)
    s.eyebrow(1100, 236, 'Information Sanzeed must supply')
    yy = 276
    for i, (a, b) in enumerate(right):
        s.hline(1100, yy, 724)
        s.text(1100, yy + 18, 50, 24, f'{i + 1:03d}', size=14, font='head', color=s.T['accent_text'], tracking=0.08, line=1.3)
        s.text(1156, yy + 14, 668, 30, a, size=19, font='head', line=1.3)
        s.text(1156, yy + 44, 668, 80, b, size=14, color=s.T['fg2'], line=1.5)
        yy += 136
    s.hline(1100, yy, 724)

    # end card ------------------------------------------------------------------------------------------------
    s = Slide('black', 'End card')
    s.lamp(960, 520, 1700, 1.0)
    s.text(M, 300, 1500, 300, [('Tell me about the ', {}), ('room.', {'color': s.T['accent']})], size=128, font='display', line=1.0)
    s.text(M, 560, 1200, 40, 'The first conversation is always free. I reply within two working days. If it is urgent, WhatsApp is fastest.',
           size=20, color=s.T['fg2'], line=1.5)
    s.hline(M, 660, 1200)
    s.text(M, 690, 1400, 120, 'sanzeed@gmail.com  ·  +91 7827051270 (call / WhatsApp)  ·  linkedin.com/in/sanzeed  ·  sanzeed.com\nNew Delhi, India',
           size=18, color=s.T['fg'], line=1.7)
    svg, png = logo('primary-wordmark', 'full-colour-dark')
    s.img(svg, M, 880, 560, 560 * ar(svg), mode='contain', png=png)
    sv, pn = signature('white')
    s.img(sv, W - M - 260, 850, 260, 260 * ar(sv), mode='contain', png=pn)
    S.append(s)

    # chrome with final folios ------------------------------------------------------------------------------------
    total = len(S)
    for i, s in enumerate(S):
        ch = getattr(s, '_chrome', None)
        if ch:
            sec, nm, wm = ch
            s.chrome(sec, nm, i + 1, total, wordmark=wm)
    return S


# ----------------------------------------------------------------------------- geometry helpers
def cover_crop(src, w, h, focal, crop=None):
    """Return (l, t, r, b) fractions of the source that fill a w × h box, centred on the focal point, after an
    optional pre-crop (fractions)."""
    iw, ih = imsize(src)
    l0, t0, r0, b0 = crop or (0, 0, 1, 1)
    cw, chh = iw * (r0 - l0), ih * (b0 - t0)
    s = max(w / cw, h / chh)
    vw, vh = w / s, h / s                      # visible source px
    fx, fy = l0 * iw + focal[0] * cw, t0 * ih + focal[1] * chh
    x0 = min(max(fx - vw / 2, l0 * iw), r0 * iw - vw)
    y0 = min(max(fy - vh / 2, t0 * ih), b0 * ih - vh)
    return x0 / iw, y0 / ih, (x0 + vw) / iw, (y0 + vh) / ih


# ----------------------------------------------------------------------------- HTML renderer
def rel(path, frm):
    return os.path.relpath(path, frm)


def css_font(font, weight=None, italic=False):
    if font == 'display':
        return f"font-family:'{F_DISPLAY}';font-weight:{weight or 300};font-variation-settings:'opsz' 144,'SOFT' 30,'WONK' 0;letter-spacing:-0.015em;" + ('font-style:italic;' if italic else '')
    if font == 'head':
        return f"font-family:'{F_HEAD}';font-weight:{weight or 600};letter-spacing:-0.01em;"
    return f"font-family:'{F_TEXT}';font-weight:{weight or 400};"


def render_html(S, out_html):
    frm = os.path.dirname(out_html)
    parts = []
    for i, s in enumerate(S):
        cls = 'slide' + (' grain' if s.grain else '')
        parts.append(f'<section class="{cls}" id="s{i + 1:02d}" data-name="{H.escape(s.name)}" style="background:{s.T["bg"]}">')
        for e in s.els:
            x, y, w, h = e['x'], e['y'], e['w'], e['h']
            box = f'left:{x:.2f}px;top:{y:.2f}px;width:{w:.2f}px;height:{h:.2f}px;'
            if e['t'] == 'rect':
                st = box + f'border-radius:{e["radius"]}px;'
                if e.get('gradient'):
                    kind, ang, stops = e['gradient']
                    st += 'background:linear-gradient(%ddeg,%s);' % (ang, ','.join(f'{c} {p * 100:.0f}%' for p, c in stops))
                elif e['fill']:
                    st += f'background:{e["fill"]};'
                if e['line']:
                    st += f'border:{e["lw"]}px solid {e["line"]};'
                parts.append(f'<div class="el" style="{st}"></div>')
            elif e['t'] == 'ellipse':
                st = box + 'border-radius:50%;'
                if e['fill']:
                    st += f'background:{e["fill"]};'
                if e['line']:
                    st += f'border:{e["lw"]}px solid {e["line"]};'
                if e.get('glow'):
                    st += 'box-shadow:0 0 24px rgba(233,178,90,.55),0 0 64px rgba(233,178,90,.25);'
                parts.append(f'<div class="el" style="{st}"></div>')
            elif e['t'] == 'img':
                is_svg = e['src'].endswith('.svg')
                src = rel(e['src'] if is_svg else prep_image(e['src'], w, h, e['mode'], e['focal'], e['crop']), frm)
                st = box + f'border-radius:{e["radius"]}px;overflow:hidden;'
                if e['border']:
                    st += f'box-shadow:inset 0 0 0 1px {e["border"]};'
                if e.get('alpha') is not None:
                    st += f'opacity:{e["alpha"]};'
                if not is_svg:
                    ist = 'width:100%;height:100%;object-fit:' + ('cover' if e['mode'] == 'cover' else 'contain') + ';'
                elif e['mode'] == 'cover':
                    l, t, r, b = cover_crop(e['src'], w, h, e['focal'], e['crop'])
                    iw, ih = imsize(e['src'])
                    sc = w / ((r - l) * iw)
                    ist = f'position:absolute;left:{-l * iw * sc:.2f}px;top:{-t * ih * sc:.2f}px;width:{iw * sc:.2f}px;height:{ih * sc:.2f}px;max-width:none;'
                elif e.get('crop'):
                    l, t, r, b = e['crop']; iw, ih = imsize(e['src'])
                    sc = min(w / ((r - l) * iw), h / ((b - t) * ih))
                    ist = f'position:absolute;left:{-l * iw * sc:.2f}px;top:{-t * ih * sc:.2f}px;width:{iw * sc:.2f}px;height:{ih * sc:.2f}px;max-width:none;'
                else:
                    ist = 'width:100%;height:100%;object-fit:contain;'
                parts.append(f'<div class="el im" style="{st}"><img src="{H.escape(src)}" alt="" style="{ist}"></div>')
            elif e['t'] == 'text':
                st = box + css_font(e['font'], e['weight'], e['italic']) + f'font-size:{e["size"]}px;line-height:{e["line"]};color:{e["color"]};text-align:{e["align"]};'
                if e['tracking']:
                    st += f'letter-spacing:{e["tracking"]}em;'
                if e['caps']:
                    st += 'text-transform:uppercase;'
                st += {'top': 'justify-content:flex-start;', 'middle': 'justify-content:center;', 'bottom': 'justify-content:flex-end;'}[e['anchor']]
                spans = []
                for txt, o in e['runs']:
                    ss = ''
                    if o.get('color'): ss += f'color:{o["color"]};'
                    if o.get('font'): ss += css_font(o['font'], o.get('weight'), o.get('italic', False))
                    if o.get('tracking'): ss += f'letter-spacing:{o["tracking"]}em;'
                    if o.get('size'): ss += f'font-size:{o["size"]}px;'
                    spans.append(f'<span style="{ss}">{H.escape(txt).replace(chr(10), "<br>")}</span>')
                parts.append(f'<div class="el tx" style="{st}"><div>{"".join(spans)}</div></div>')
        parts.append('</section>')
    kit_css = rel(f'{KIT}/brand.css', frm)
    doc = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<title>Sanzeed — Brand Presentation</title>
<link rel="stylesheet" href="{kit_css}">
<style>
@page {{ size: 508mm 285.75mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; background: #000; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
@media print {{ html {{ color-scheme: dark; }} body {{ background: #000 !important; color: #F5F5F7; }} }}
.slide {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; break-after: page; page-break-after: always; }}
.slide:last-child {{ break-after: auto; page-break-after: auto; }}
.el {{ position: absolute; box-sizing: border-box; }}
.tx {{ display: flex; flex-direction: column; white-space: pre-wrap; text-wrap: pretty; }}
.im img {{ display: block; }}
.grain::after {{ z-index: 5; }}
</style>
</head>
<body>
{"".join(parts)}
</body>
</html>'''
    open(out_html, 'w').write(doc)


# ----------------------------------------------------------------------------- PPTX renderer
PREP_LOG = {}


def prep_image(src, w, h, mode, focal, crop):
    """Prepared copy for the PPTX: pre-cropped (cover) or pre-cut (crop), downsized to ≤ 2 × its placed size."""
    iw, ih = imsize(src)
    if mode == 'cover':
        l, t, r, b = cover_crop(src, w, h, focal, crop)
    elif crop:
        l, t, r, b = crop
    else:
        l, t, r, b = 0, 0, 1, 1
    key = hashlib.md5(f'{src}|{l:.4f}|{t:.4f}|{r:.4f}|{b:.4f}|{int(w)}|{int(h)}'.encode()).hexdigest()[:8]
    stem = os.path.splitext(os.path.basename(src))[0]
    im = Image.open(src)
    has_alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    ext = '.png' if has_alpha else '.jpg'
    out = f'{ASSETS}/{stem}--{key}{ext}'
    PREP_LOG[os.path.basename(out)] = (os.path.relpath(src, B), (l, t, r, b), int(w), int(h))
    if os.path.exists(out):
        return out
    box = (int(l * iw), int(t * ih), int(r * iw), int(b * ih))
    if box != (0, 0, iw, ih):
        im = im.crop(box)
    maxw = min(2400, max(400, int(w * 1.5)))
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    if has_alpha:
        im.convert('RGBA').save(out, optimize=True)
    else:
        im.convert('RGB').save(out, quality=84, subsampling=0, optimize=True)
    return out


def render_pptx(S, out_pptx):
    from pptx import Presentation
    from pptx.util import Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.oxml.ns import qn
    from lxml import etree
    import copy

    def rgb(hexs):
        return RGBColor.from_string(hexs.lstrip('#'))

    def E(px):
        return Emu(int(round(px * EMU)))

    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    prs.slide_master.background.fill.solid(); prs.slide_master.background.fill.fore_color.rgb = rgb(C['black'])

    def set_alpha(shape, amt):
        """Picture transparency through a:alphaModFix on the blip."""
        blip = shape._element.find('.//' + qn('a:blip'))
        am = etree.SubElement(blip, qn('a:alphaModFix')); am.set('amt', str(int(amt * 100000)))

    def round_pic(pic, radius_px, w, h):
        prst = pic._element.find('.//' + qn('a:prstGeom'))
        if prst is None or radius_px <= 0:
            return
        prst.set('prst', 'roundRect')
        av = prst.find(qn('a:avLst'))
        if av is None:
            av = etree.SubElement(prst, qn('a:avLst'))
        for c in list(av):
            av.remove(c)
        gd = etree.SubElement(av, qn('a:gd')); gd.set('name', 'adj'); gd.set('fmla', f'val {int(min(50000, radius_px / min(w, h) * 100000))}')

    def no_shadow(shape):
        shape.shadow.inherit = False

    for s in S:
        sl = prs.slides.add_slide(blank)
        sl.name = s.name
        sl.background.fill.solid(); sl.background.fill.fore_color.rgb = rgb(s.T['bg'])
        for e in s.els:
            x, y, w, h = e['x'], e['y'], e['w'], e['h']
            if e['t'] == 'rect' and h <= 1.5 and e['fill'] and not e.get('gradient'):
                from pptx.enum.shapes import MSO_CONNECTOR
                ln = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x), E(y + h / 2), E(x + w), E(y + h / 2))
                ln.line.color.rgb = rgb(e['fill']); ln.line.width = Pt(0.75)
                st = ln._element.find(qn('p:style'))          # drop the theme style: its effectRef adds a shadow
                if st is not None:
                    ln._element.remove(st)
                etree.SubElement(ln._element.spPr, qn('a:effectLst'))
                continue
            if e['t'] in ('rect', 'ellipse'):
                if e['t'] == 'ellipse':
                    shp = sl.shapes.add_shape(MSO_SHAPE.OVAL, E(x), E(y), E(w), E(h))
                elif e['radius'] > 0:
                    shp = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(x), E(y), E(w), E(h))
                    shp.adjustments[0] = min(0.5, e['radius'] / min(w, h))
                else:
                    shp = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, E(x), E(y), E(w), E(h))
                no_shadow(shp)
                if e.get('gradient'):
                    kind, ang, stops = e['gradient']
                    f = shp.fill; f.gradient(); f.gradient_angle = (90 - ang) % 360
                    gs = f.gradient_stops
                    # python-pptx creates two stops; add more by cloning
                    gsLst = f._fill._gradFill.find(qn('a:gsLst')) if hasattr(f._fill, '_gradFill') else shp._element.find('.//' + qn('a:gsLst'))
                    while len(gsLst) < len(stops):
                        gsLst.append(copy.deepcopy(gsLst[-1]))
                    for i_, (pos, col) in enumerate(stops):
                        g = gsLst[i_]; g.set('pos', str(int(pos * 100000)))
                        for c in list(g):
                            g.remove(c)
                        srgb = etree.SubElement(g, qn('a:srgbClr')); srgb.set('val', col.lstrip('#'))
                elif e['fill']:
                    shp.fill.solid(); shp.fill.fore_color.rgb = rgb(e['fill'])
                else:
                    shp.fill.background()
                if e['line']:
                    shp.line.color.rgb = rgb(e['line']); shp.line.width = Pt(max(0.5, e['lw'] * 0.5))
                else:
                    shp.line.fill.background()
                shp.text_frame.text = ''
            elif e['t'] == 'img':
                src = e['png'] if e['png'] else e['src']
                if src.endswith('.svg'):
                    raise RuntimeError('no PNG for ' + src)
                prepared = prep_image(src, w, h, e['mode'], e['focal'], e['crop'])
                pic = sl.shapes.add_picture(prepared, E(x), E(y), E(w), E(h))
                if e['radius']:
                    round_pic(pic, e['radius'], w, h)
                if e.get('alpha') is not None and e['alpha'] < 1:
                    set_alpha(pic, e['alpha'])
                if e['border']:
                    pic.line.color.rgb = rgb(e['border']); pic.line.width = Pt(0.5)
            elif e['t'] == 'text':
                tb = sl.shapes.add_textbox(E(x), E(y), E(w), E(h))
                tf = tb.text_frame; tf.word_wrap = True
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.vertical_anchor = {'top': MSO_ANCHOR.TOP, 'middle': MSO_ANCHOR.MIDDLE, 'bottom': MSO_ANCHOR.BOTTOM}[e['anchor']]
                # split runs into paragraphs on \n
                paras = [[]]
                for txt, o in e['runs']:
                    pieces = txt.split('\n')
                    for k, pc in enumerate(pieces):
                        if k > 0:
                            paras.append([])
                        if pc:
                            paras[-1].append((pc, o))
                for pi, runs in enumerate(paras):
                    p = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
                    p.alignment = {'left': PP_ALIGN.LEFT, 'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT}[e['align']]
                    p.line_spacing = e['line']
                    if not runs:
                        r = p.add_run(); r.text = ' '
                        r.font.size = Pt(e['size'] * 0.5); r.font.name = P_TEXT
                        continue
                    for txt, o in runs:
                        r = p.add_run()
                        r.text = txt.upper() if e['caps'] else txt
                        fnt = o.get('font', e['font'])
                        r.font.name = {'display': P_DISPLAY, 'head': P_HEAD, 'text': P_TEXT}[fnt]
                        r.font.size = Pt(o.get('size', e['size']) * 0.5)
                        r.font.bold = False
                        r.font.italic = bool(o.get('italic', e['italic']))
                        r.font.color.rgb = rgb(o.get('color', e['color']))
                        tr = o.get('tracking', e['tracking'])
                        if tr:
                            rPr = r._r.get_or_add_rPr(); rPr.set('spc', str(int(tr * o.get('size', e['size']) * 0.5 * 100)))
    prs.save(out_pptx)


# ----------------------------------------------------------------------------- main
def run(cmd, **kw):
    print('$', ' '.join(cmd)); subprocess.run(cmd, check=True, **kw)


def write_manifest():
    """Every prepared copy → its source in the package; anything not used by this build is removed."""
    used = set(PREP_LOG)
    for f in os.listdir(ASSETS):
        if f not in used and f != 'MANIFEST.md':
            os.remove(f'{ASSETS}/{f}')
    with open(f'{ASSETS}/MANIFEST.md', 'w') as mf:
        mf.write('# Prepared image copies\n\nEvery file here is a copy of a package asset, pre-cropped and downsized by '
                 '`src/build_presentation.py` (`prep_image`) to at most 1.5 × its placed size, so the PPTX and the HTML stay small. '
                 'Nothing is redrawn or restyled; edit the source named below and rebuild. The folder is emptied at the start of '
                 'every build, so every copy comes from the current file in the package.\n\n'
                 '| Prepared file | Source (relative to BRAND_PACKAGE) | Crop (l, t, r, b fractions) | Placed at (px) |\n|---|---|---|---|\n')
        for f in sorted(PREP_LOG):
            src, (l, tt, r, b), w, h = PREP_LOG[f]
            mf.write(f'| `{f}` | `{src}` | {l:.3f}, {tt:.3f}, {r:.3f}, {b:.3f} | {w} × {h} |\n')


if __name__ == '__main__':
    # clear every prepared copy first so nothing stale survives from an earlier logo or mockup
    for f in os.listdir(ASSETS):
        os.remove(f'{ASSETS}/{f}')
    S = build_deck()
    print(len(S), 'slides')
    html_path = f'{HERE}/Brand_Presentation.html'
    render_html(S, html_path)
    json.dump([{'n': i + 1, 'name': s.name} for i, s in enumerate(S)], open(f'{HERE}/slide-index.json', 'w'), indent=1)
    if '--html-only' in sys.argv:
        write_manifest()
        sys.exit(0)
    pdf = f'{OUT}/Brand_Presentation.pdf'
    run(['node', f'{KIT}/render.js', '--in', html_path, '--out', pdf, '--pdf', '--size', '508x285.75', '--wait', '1200'])
    if '--no-png' not in sys.argv:
        for f in os.listdir(SLIDES_DIR):
            os.remove(f'{SLIDES_DIR}/{f}')
        run(['pdftoppm', '-r', '96', '-png', pdf, f'{SLIDES_DIR}/tmp'])
        n = 0
        for f in sorted(os.listdir(SLIDES_DIR)):
            n += 1
            os.rename(f'{SLIDES_DIR}/{f}', f'{SLIDES_DIR}/sanzeed-brand-presentation--slide-{n:02d}.png')
    if '--no-pptx' not in sys.argv:
        pptx_path = f'{EP}/Brand_Presentation.pptx'
        render_pptx(S, pptx_path)
        tmp = f'{EP}/_soffice'; os.makedirs(tmp, exist_ok=True)
        run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, pptx_path])
        shutil.move(f'{tmp}/Brand_Presentation.pdf', f'{OUT}/Brand_Presentation--pptx-export.pdf')
        shutil.rmtree(tmp)
    write_manifest()
    print('done')
