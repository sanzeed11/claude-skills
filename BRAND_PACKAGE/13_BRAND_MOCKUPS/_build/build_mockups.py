#!/usr/bin/env python3
"""
build_mockups.py — the master for 13_BRAND_MOCKUPS.

Writes the shared scene stylesheet (`_build/mockup.css`), one editable HTML scene per mockup into
`<Folder>/src/sanzeed-mockup--<scene>.html`, renders every scene with the brand kit's `render.js`
(Chromium, 1500×1000 CSS px at 2× = 3000×2000), exports `<name>-3000w.jpg` (q90) and `<name>-1600w.jpg`,
then builds the contact sheet and the README index.

    python3 build_mockups.py                 # everything
    python3 build_mockups.py cards-fanned    # scenes whose name contains the filter (no sheet/README)
    python3 build_mockups.py --html-only     # write sources only
    python3 build_mockups.py --sheet         # only the contact sheet (+ README)
    python3 build_mockups.py --readme        # only the README index

Every scene is composed from the real deliverables: logos from 02_LOGO_SYSTEM (SVG, used as images or CSS masks),
textures from 05_GRAPHIC_ASSETS/Textures, print pieces from 09/10 (re-rasterised PDFs in `_build/plates/`, see
make_plates.py), social from 08, OG / email / app icons from 07, site captures from 16, motion frames from 11.
Nothing is redrawn; the scenes only light, bend and place them.
"""
import os, re, subprocess, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))                       # 13_BRAND_MOCKUPS
B = os.path.abspath(os.path.join(ROOT, '..'))                          # BRAND_PACKAGE
RENDER = os.path.join(B, '15_SOURCE_FILES', 'Project_Files', 'brand-kit', 'render.js')
import tempfile
TMP = tempfile.mkdtemp(prefix='sanzeed-mockups-')          # intermediate PNGs; the JPG exports live beside the sources

# relative paths as seen from <Folder>/src/
R = '../../..'
P = '../../_build/plates'
LOGO = f'{R}/02_LOGO_SYSTEM/SVG'
TEX = f'{R}/05_GRAPHIC_ASSETS/Textures'
BG = f'{R}/05_GRAPHIC_ASSETS/Backgrounds'
SOC = f'{R}/08_SOCIAL_MEDIA'
WEB = f'{R}/07_WEBSITE_DIGITAL_ASSETS'
MOT = f'{R}/11_MOTION_GRAPHICS'
MKT = f'{R}/10_MARKETING_COLLATERAL'

# ----------------------------------------------------------------------------------------------------------------
# shared stylesheet
# ----------------------------------------------------------------------------------------------------------------
CSS = r'''
/* mockup.css — shared scene components for 13_BRAND_MOCKUPS (imports the brand kit). Scenes are 1500 × 1000 CSS px,
   rendered at 2× → 3000 × 2000. Every colour is a brand token; the only textures are the ones in 05_GRAPHIC_ASSETS. */
@import url("../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css");

html, body { margin: 0; width: 1500px; height: 1000px; overflow: hidden; background: #000; }
.stage { position: relative; width: 1500px; height: 1000px; overflow: hidden; background: #000; font-family: var(--font-text); color: var(--fg); }
.stage > * { position: absolute; }
.abs { position: absolute; }

/* ---------- surfaces ---------- */
.surf-night { background: radial-gradient(110% 80% at 50% 22%, #1c1c1f 0%, #0d0d0f 48%, #000 100%); }
.surf-charcoal { background: radial-gradient(120% 90% at 50% 10%, #2a2a2d 0%, #1c1c1e 45%, #0d0d0f 100%); }
.surf-plaster { background: #F5F0E7 url("../../05_GRAPHIC_ASSETS/Textures/sanzeed-texture-paper--plaster-2048.jpg") center / 1500px 1500px; }
.surf-paper { background: #FBF8F2 url("../../05_GRAPHIC_ASSETS/Textures/sanzeed-texture-paper--paper-2048.jpg") center / 1500px 1500px; }
.tex-grain { inset: 0; background: url("../../05_GRAPHIC_ASSETS/Textures/sanzeed-texture-grain--tile-1024.png") 0 0 / 640px 640px; mix-blend-mode: soft-light; opacity: .55; pointer-events: none; }
.tex-grain.fine { background-image: url("../../05_GRAPHIC_ASSETS/Textures/sanzeed-texture-grain--fine-1024.png"); }
.lamp { width: 1600px; height: 1600px; background: url("../../05_GRAPHIC_ASSETS/Textures/sanzeed-texture-lamp-glow--2048.png") center / contain no-repeat; pointer-events: none; }
.lamp.light { background-image: url("../../05_GRAPHIC_ASSETS/Textures/sanzeed-texture-lamp-glow--light-2048.png"); }
.vig { inset: 0; background: radial-gradient(ellipse at 50% 50%, transparent 52%, rgba(0,0,0,.62) 100%); pointer-events: none; }
.vig.soft { background: radial-gradient(ellipse at 50% 45%, transparent 60%, rgba(0,0,0,.42) 100%); }
.sweep { inset: 0; pointer-events: none; background: linear-gradient(118deg, rgba(255,255,255,.55) 0%, rgba(255,255,255,0) 40%, rgba(60,40,15,0) 62%, rgba(60,40,15,.14) 100%); }
.sweep.dark { background: linear-gradient(118deg, rgba(255,255,255,.08) 0%, rgba(255,255,255,0) 42%, rgba(0,0,0,0) 60%, rgba(0,0,0,.45) 100%); }
.floor-line { left: 0; right: 0; height: 1px; background: rgba(255,255,255,.06); }

/* ---------- 3-D helpers ---------- */
.p3d { transform-style: preserve-3d; }
.persp { perspective: 2400px; perspective-origin: 50% 50%; }

/* ---------- paper and shadows (reset the brand.css component classes that share a name) ---------- */
.stage .card, .stage .label, .stage .input { border: 0; padding: 0; background: none; box-shadow: none; margin: 0; }
.paper { background-size: 100% 100%; background-repeat: no-repeat; }
.stage .card.paper { background-size: 100% 100%; background-repeat: no-repeat; }   /* the reset above would otherwise paint card plates at native size (top-left corner only) */
.sh-dark { box-shadow: 0 1px 1px rgba(0,0,0,.4), 0 10px 24px rgba(0,0,0,.45), 0 36px 70px rgba(0,0,0,.5); }
.sh-light { box-shadow: 0 1px 1px rgba(40,30,10,.10), 0 8px 18px rgba(40,30,10,.12), 0 30px 60px rgba(40,30,10,.14); }
.sh-contact { box-shadow: 0 2px 3px rgba(0,0,0,.35), 0 18px 40px rgba(0,0,0,.45); }
.edge { box-shadow: inset 0 0 0 1px rgba(0,0,0,.06); }
.img-cover { width: 100%; height: 100%; object-fit: cover; display: block; }

/* ---------- masks (the logo SVGs from 02_LOGO_SYSTEM used as alpha) ---------- */
.mask { -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat; -webkit-mask-size: 100% 100%; mask-size: 100% 100%; -webkit-mask-position: center; mask-position: center; }

/* ---------- devices ---------- */
.phone { position: absolute; width: 422px; height: 876px; border-radius: 66px; background: #0b0b0c;
  box-shadow: inset 0 0 0 2px #333336, inset 0 0 0 4px #0b0b0c, inset 0 0 0 6px #1a1a1c, 0 60px 110px rgba(0,0,0,.65), 0 20px 40px rgba(0,0,0,.5); }
.phone .screen { position: absolute; left: 16px; top: 16px; width: 390px; height: 844px; border-radius: 50px; overflow: hidden; background: #000; }
.phone .screen > img.full { width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; }
.phone .island { position: absolute; left: 50%; top: 27px; width: 118px; height: 34px; margin-left: -59px; border-radius: 18px; background: #000; }
.phone .pbtn { position: absolute; width: 4px; background: #2b2b2e; border-radius: 2px; }
.phone .l1 { left: -4px; top: 150px; height: 34px; } .phone .l2 { left: -4px; top: 210px; height: 62px; } .phone .l3 { left: -4px; top: 286px; height: 62px; } .phone .r1 { right: -4px; top: 236px; height: 96px; }
.phone .status { position: absolute; left: 0; right: 0; top: 0; height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 34px 0 36px; font: 600 16px/1 var(--font-heading); color: #F5F5F7; pointer-events: none; }
.phone .status .r { display: flex; gap: 6px; align-items: center; }
.phone .status .bars { display: flex; gap: 2px; align-items: flex-end; } .phone .status .bars i { display: block; width: 3px; background: #F5F5F7; border-radius: 1px; }
.phone .status .batt { width: 26px; height: 12px; border: 1.5px solid rgba(245,245,247,.6); border-radius: 4px; position: relative; } .phone .status .batt::after { content: ""; position: absolute; left: 2px; top: 2px; bottom: 2px; width: 70%; background: #F5F5F7; border-radius: 2px; }
.phone .homebar { position: absolute; left: 50%; bottom: 10px; width: 134px; height: 5px; margin-left: -67px; border-radius: 3px; background: rgba(245,245,247,.8); }

.laptop { position: absolute; width: 1180px; height: 820px; }
.laptop .lid { position: absolute; left: 0; top: 0; width: 1180px; height: 762px; border-radius: 24px 24px 8px 8px; background: #141416; box-shadow: inset 0 0 0 1px #2e2e31, 0 50px 90px rgba(0,0,0,.6), 0 10px 20px rgba(0,0,0,.4); }
.laptop .screen { position: absolute; left: 22px; top: 22px; width: 1136px; height: 710px; border-radius: 10px; overflow: hidden; background: #000; }
.laptop .screen > img { width: 100%; height: 100%; object-fit: cover; object-position: top; display: block; }
.laptop .cam { position: absolute; left: 50%; top: 9px; width: 6px; height: 6px; margin-left: -3px; border-radius: 50%; background: #1f1f22; box-shadow: inset 0 0 0 1px #3a3a3e; }
.laptop .base { position: absolute; left: -90px; top: 762px; width: 1360px; height: 22px; border-radius: 0 0 28px 28px / 0 0 18px 18px; background: linear-gradient(#4a4a4f, #2a2a2d 55%, #151517); box-shadow: 0 30px 60px rgba(0,0,0,.6); }
.laptop .base::before { content: ""; position: absolute; left: 50%; top: 0; width: 220px; height: 8px; margin-left: -110px; border-radius: 0 0 8px 8px; background: #0f0f11; }
.laptop.silver .lid { background: #d9d7d2; box-shadow: inset 0 0 0 1px #bdbab3, 0 50px 90px rgba(40,30,10,.25), 0 10px 20px rgba(40,30,10,.12); }
.laptop.silver .cam { background: #a9a7a1; box-shadow: inset 0 0 0 1px #8c8a84; }
.laptop.silver .base { background: linear-gradient(#efede8, #cfccc5 55%, #a9a69f); box-shadow: 0 30px 60px rgba(40,30,10,.25); }
.laptop.silver .base::before { background: #b9b6af; }

.tablet { position: absolute; width: 1120px; height: 820px; border-radius: 44px; background: #0d0d0f; box-shadow: inset 0 0 0 2px #2f2f32, inset 0 0 0 4px #0d0d0f, 0 50px 90px rgba(0,0,0,.6); }
.tablet .screen { position: absolute; left: 36px; top: 36px; width: 1048px; height: 748px; border-radius: 16px; overflow: hidden; background: #000; }
.tablet .cam { position: absolute; left: 50%; top: 14px; width: 8px; height: 8px; margin-left: -4px; border-radius: 50%; background: #1f1f22; box-shadow: inset 0 0 0 1px #3a3a3e; }

.monitor { position: absolute; }
.monitor .bezel { position: absolute; inset: 0; border-radius: 10px; background: #0f0f11; box-shadow: inset 0 0 0 1px #2b2b2e, 0 40px 90px rgba(0,0,0,.65); }
.monitor .screen { position: absolute; left: 16px; top: 16px; right: 16px; bottom: 16px; overflow: hidden; background: #000; }

/* ---------- windows (generic UI chrome, no third-party branding) ---------- */
.win { position: absolute; border-radius: 14px; overflow: hidden; background: #1C1C1E; box-shadow: 0 1px 0 rgba(255,255,255,.06) inset, 0 50px 100px rgba(0,0,0,.6), 0 12px 30px rgba(0,0,0,.45); }
.win .dots { display: flex; gap: 8px; } .win .dots i { width: 12px; height: 12px; border-radius: 50%; background: #3a3a3e; display: block; }
.browser .tabs { height: 46px; background: #141416; display: flex; align-items: flex-end; padding: 0 14px; gap: 2px; }
.browser .tabs .dots { margin: 0 14px 12px 4px; }
.browser .tab { height: 36px; padding: 0 16px 0 12px; border-radius: 10px 10px 0 0; display: flex; align-items: center; gap: 9px; font: 500 13px/1 var(--font-text); color: #A1A1A6; white-space: nowrap; }
.browser .tab img { width: 16px; height: 16px; display: block; }
.browser .tab.active { background: #2A2A2D; color: #F5F5F7; }
.browser .tab .x { margin-left: 8px; width: 14px; height: 14px; position: relative; opacity: .6; } .browser .tab .x::before, .browser .tab .x::after { content: ""; position: absolute; left: 6px; top: 1px; width: 1.5px; height: 12px; background: currentColor; transform: rotate(45deg); } .browser .tab .x::after { transform: rotate(-45deg); }
.browser .bar { height: 48px; background: #2A2A2D; display: flex; align-items: center; gap: 12px; padding: 0 16px; }
.browser .nav { display: flex; gap: 14px; color: #808086; font-size: 16px; }
.browser .url { flex: 1; height: 32px; border-radius: 16px; background: #1C1C1E; display: flex; align-items: center; gap: 8px; padding: 0 14px; font: 400 13px/1 var(--font-text); color: #A1A1A6; }
.browser .url b { color: #F5F5F7; font-weight: 500; }
.browser .url .lock { width: 9px; height: 11px; border: 1.5px solid #808086; border-radius: 2px; position: relative; } .browser .url .lock::before { content: ""; position: absolute; left: 1px; top: -6px; width: 5px; height: 6px; border: 1.5px solid #808086; border-bottom: 0; border-radius: 4px 4px 0 0; }
.browser .page { position: relative; overflow: hidden; background: #000; }
.browser .page img { width: 100%; display: block; }

/* ---------- the scene caption (the brand's wall label) ---------- */
.cap { left: 40px; bottom: 28px; font: 400 12px/1.5 var(--font-text); color: #808086; letter-spacing: .01em; }
.cap b { font: 600 12px/1.5 var(--font-heading); color: #A1A1A6; margin-right: 10px; }
.cap .pt { display: inline-block; width: 5px; height: 5px; border-radius: 50%; background: #E9B25A; margin: 0 8px 1px 8px; }
.stage.light .cap { color: #8a8176; } .stage.light .cap b { color: #665F55; } .stage.light .cap .pt { background: #B8863B; }
'''

# ----------------------------------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------------------------------
SCENES = []
import base64
def durl(rel):
    """Inline a mask source as a data URI (Chromium will not load mask-image from file://). `rel` is relative to BRAND_PACKAGE."""
    path = os.path.join(B, rel); mime = 'image/svg+xml' if rel.endswith('.svg') else 'image/png'
    return f'url("data:{mime};base64,{base64.b64encode(open(path, "rb").read()).decode()}")'
MK_PLAIN = durl('02_LOGO_SYSTEM/SVG/sanzeed-wordmark-plain--black.svg')
MK_PRIMARY = durl('02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--black.svg')
MK_SYMBOL = durl('02_LOGO_SYSTEM/SVG/sanzeed-symbol--black.svg')
MK_STAMP = durl('09_PRINT_STATIONERY/Stamp/sanzeed-stamp--round-40mm.svg')


def scene(name, folder, title, uses, body, css='', theme='dark', light=False, caption=None):
    SCENES.append(dict(name=name, folder=folder, title=title, uses=uses, body=body, css=css, theme=theme, light=light, caption=caption))

def cap(title, spec):
    return f'<div class="cap"><b>{title}</b>{spec}</div>'

def status():
    return ('<div class="status"><span>10:08</span><span class="r"><span class="bars"><i style="height:4px"></i><i style="height:6px"></i>'
            '<i style="height:8px"></i><i style="height:10px"></i></span><span class="batt"></span></span></div>')

def phone(screen, style='', cls='', home=True):
    return (f'<div class="phone {cls}" style="{style}"><div class="pbtn l1"></div><div class="pbtn l2"></div><div class="pbtn l3"></div><div class="pbtn r1"></div>'
            f'<div class="screen">{screen}{"<div class=homebar></div>" if home else ""}</div><div class="island"></div></div>')

def laptop(screen, style='', cls=''):
    return f'<div class="laptop {cls}" style="{style}"><div class="lid"><div class="cam"></div><div class="screen">{screen}</div></div><div class="base"></div></div>'

def tablet(screen, style=''):
    return f'<div class="tablet" style="{style}"><div class="cam"></div><div class="screen">{screen}</div></div>'

def browser_tabs(active=0):
    tabs = [('Sanzeed Mirza — Experiential Design Consultant', True), ('Prime Minister Museum — Sanzeed Mirza', False), ('Ram Katha Show — Sanzeed Mirza', False)]
    fav = f'{R}/02_LOGO_SYSTEM/Favicon/favicon-32.png'
    out = '<div class="tabs"><div class="dots"><i></i><i></i><i></i></div>'
    for i, (t, a) in enumerate(tabs):
        out += f'<div class="tab{" active" if i == active else ""}"><img src="{fav}" alt="Sanzeed favicon"><span>{t}</span><span class="x"></span></div>'
    out += '<div class="tab" style="padding:0 10px;font-size:18px;color:#808086">+</div></div>'
    return out

# ================================================================================================================
# LOGO MOCKUPS
# ================================================================================================================
L = 'Logo_Mockups'

# 01 — blind deboss on Plaster card stock (macro)
scene('logo-blind-deboss-plaster', L, 'Blind deboss · wordmark on Plaster card stock', ['02 wordmark-plain--black.svg (as the deboss mask)', '05 paper texture'], f'''
<div class="abs surf-plaster" style="inset:0;background-size:2400px 2400px"></div>
<div class="abs sweep" style="background:linear-gradient(122deg,rgba(255,255,255,.62) 0%,rgba(255,255,255,0) 44%,rgba(60,40,15,0) 60%,rgba(60,40,15,.20) 100%)"></div>
<div class="abs" style="left:150px;top:399px;width:1200px;height:169px">
  <div class="abs mask hi"></div><div class="abs mask lo"></div><div class="abs mask face"></div>
</div>
<div class="abs vig soft" style="background:radial-gradient(ellipse at 45% 45%,transparent 55%,rgba(60,40,15,.22) 100%)"></div>
{cap('Blind deboss', 'wordmark · 350 gsm uncoated Plaster stock · no ink · <span class="pt"></span>02_LOGO_SYSTEM / wordmark-plain')}
''', css=f'''
.mask {{ inset: 0; -webkit-mask-image: {MK_PLAIN}; mask-image: {MK_PLAIN}; }}
.hi {{ background: rgba(255,255,255,.95); transform: translate(2.5px, 2.5px); filter: blur(.5px); }}
.lo {{ background: rgba(70,50,25,.62); transform: translate(-1.5px, -1.5px); filter: blur(.7px); }}
.face {{ background: linear-gradient(120deg, #ECE6DA, #F0EADF 50%, #E9E2D6); }}
''', light=True)

# 02 — gold foil on black (macro)
scene('logo-gold-foil-black', L, 'Gold foil · wordmark hot-stamped on black stock', ['02 primary-wordmark--black.svg (as the foil mask)', '03 foil gradient', '05 grain'], f'''
<div class="abs" style="inset:0;background:radial-gradient(90% 70% at 40% 30%,#1a1a1c 0%,#0d0d0f 55%,#000 100%)"></div>
<div class="abs tex-grain" style="opacity:.9;background-size:420px 420px"></div>
<div class="abs" style="inset:0;background:linear-gradient(118deg,rgba(255,255,255,.07) 0%,rgba(255,255,255,0) 40%)"></div>
<div class="abs" style="left:150px;top:399px;width:1200px;height:169px">
  <div class="abs mask foil-shadow"></div><div class="abs mask foil"></div><div class="abs mask sheen"></div><div class="abs mask brush"></div>
</div>
<div class="abs vig"></div>
{cap('Gold foil', 'primary wordmark · hot-foil, Old Gold / Lamp Gold foil · <span class="pt"></span>02_LOGO_SYSTEM / primary-wordmark')}
''', css=f'''
.mask {{ inset: 0; -webkit-mask-image: {MK_PRIMARY}; mask-image: {MK_PRIMARY}; }}
.foil-shadow {{ background: rgba(0,0,0,.9); transform: translate(2px, 3px); filter: blur(1.2px); }}
.foil {{ background: linear-gradient(135deg, #B8863B 0%, #F4C97A 48%, #B8863B 100%); }}
.sheen {{ background: linear-gradient(112deg, rgba(255,255,255,0) 30%, rgba(255,255,255,.55) 44%, rgba(255,255,255,0) 52%, rgba(255,255,255,0) 70%, rgba(120,80,20,.35) 100%); }}
.brush {{ background: repeating-linear-gradient(100deg, rgba(255,255,255,.07) 0 1px, rgba(0,0,0,0) 1px 3px); }}
''')

# 03 — backlit signage letters at night
scene('logo-backlit-signage-night', L, 'Halo-lit signage · fabricated letters on a dark wall', ['02 primary-wordmark--full-colour-dark.svg', '05 lamp glow + grain'], f'''
<div class="abs" style="inset:0;background:linear-gradient(180deg,#0a0a0b 0%,#151517 60%,#1a1a1c 82%,#0a0a0b 100%)"></div>
<div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.012) 0 2px,transparent 2px 9px)"></div>
<div class="abs tex-grain" style="opacity:.8"></div>
<div class="abs lamp" style="left:-50px;top:-320px;width:1600px;height:1600px;opacity:.55"></div>
<div class="abs halo-wrap" style="left:190px;top:402px;width:1120px;height:157.5px;filter:blur(26px)"><div class="abs halo" style="inset:0"></div></div>
<img class="abs sign" src="{LOGO}/sanzeed-primary-wordmark--full-colour-dark.svg" alt="Sanzeed wordmark, halo-lit signage" style="left:190px;top:402px;width:1120px">
<div class="abs" style="left:0;right:0;top:820px;height:180px;background:linear-gradient(180deg,rgba(233,178,90,.05),rgba(0,0,0,.6))"></div>
<div class="abs floor-line" style="top:820px;background:rgba(233,178,90,.10)"></div>
<div class="abs vig"></div>
{cap('Halo-lit signage', 'primary wordmark · 60 mm deep fabricated letters, warm-white halo · <span class="pt"></span>02_LOGO_SYSTEM / primary-wordmark')}
''', css=f'''
.halo {{ -webkit-mask-image: {MK_PRIMARY}; mask-image: {MK_PRIMARY}; -webkit-mask-size: 100% 100%; mask-size: 100% 100%; -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat; background: #fff3dc; opacity: .6; }}
.sign {{ filter: drop-shadow(0 0 10px rgba(255,243,220,.45)) drop-shadow(0 4px 2px rgba(0,0,0,.6)); }}
''')

# 04 — engraved brass plaque
scene('logo-brass-plaque-symbol', L, 'Engraved brass plaque · the symbol', ['02 symbol--black.svg (as the engraving mask)'], f'''
<div class="abs" style="inset:0;background:radial-gradient(90% 80% at 50% 30%,#2b2b2e 0%,#1a1a1c 50%,#0a0a0b 100%)"></div>
<div class="abs tex-grain" style="opacity:.9"></div>
<div class="abs lamp" style="left:-50px;top:-300px;opacity:.35"></div>
<div class="abs plaque" style="left:430px;top:180px;width:640px;height:640px">
  <div class="abs screw" style="left:26px;top:26px"></div><div class="abs screw" style="right:26px;top:26px"></div><div class="abs screw" style="left:26px;bottom:26px"></div><div class="abs screw" style="right:26px;bottom:26px"></div>
  <div class="abs" style="left:130px;top:157px;width:380px;height:327px"><div class="abs mask eng-hi"></div><div class="abs mask eng"></div></div>
  <div class="abs hairline"></div>
</div>
<div class="abs vig"></div>
{cap('Engraved brass plaque', 'symbol · 180 × 180 mm brushed brass, deep-etched and ink-filled · <span class="pt"></span>02_LOGO_SYSTEM / symbol')}
''', css=f'''
.plaque {{ border-radius: 14px; background: linear-gradient(155deg, #d5b06b 0%, #a4823f 30%, #8a6a2c 50%, #b8903f 70%, #6f531f 100%);
  box-shadow: inset 0 2px 0 rgba(255,245,210,.55), inset 0 -3px 0 rgba(0,0,0,.5), inset 2px 0 0 rgba(255,245,210,.25), inset -2px 0 0 rgba(0,0,0,.35), 0 30px 60px rgba(0,0,0,.6), 0 4px 8px rgba(0,0,0,.5); }}
.plaque::before {{ content: ""; position: absolute; inset: 0; border-radius: 14px; background: repeating-linear-gradient(0deg, rgba(255,255,255,.07) 0 1px, rgba(0,0,0,0) 1px 3px, rgba(0,0,0,.06) 3px 4px); mix-blend-mode: overlay; }}
.hairline {{ inset: 18px; border-radius: 8px; border: 1px solid rgba(60,40,10,.35); box-shadow: 0 1px 0 rgba(255,245,210,.25); }}
.screw {{ width: 20px; height: 20px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #e7cc8a, #8a6a2c 70%, #4d3812); box-shadow: 0 1px 2px rgba(0,0,0,.6), inset 0 0 0 1px rgba(0,0,0,.3); }}
.screw::after {{ content: ""; position: absolute; left: 3px; top: 9px; width: 14px; height: 2px; background: #3a2a10; transform: rotate(-30deg); box-shadow: 0 1px 0 rgba(255,245,210,.35); }}
.mask {{ inset: 0; -webkit-mask-image: {MK_SYMBOL}; mask-image: {MK_SYMBOL}; }}
.eng {{ background: #2a1d08; }}
.eng-hi {{ background: rgba(255,240,200,.75); transform: translate(0, 2.5px); filter: blur(.6px); }}
''')

# 05 — frosted glass door with the window vinyl
scene('logo-frosted-glass-door', L, 'Window vinyl · wordmark on a frosted glass door', ['02 primary-wordmark--white.svg (cut vinyl)', '10 Signage window-vinyl spec (600 mm band, 1200 mm wordmark)', '00/06 Prime Minister Museum lobby (behind the glass)'], f'''
<div class="abs" style="inset:0;background:#0a0a0b"></div>
<img class="abs" src="{P}/photo-prime-minister-museum-lobby.jpg" alt="" style="left:-140px;top:-40px;width:1780px;max-width:none;filter:blur(9px) brightness(.55) saturate(.8)">
<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.1) 40%,rgba(0,0,0,.55))"></div>
<div class="abs frame" style="left:170px;top:-20px;width:1160px;height:1040px"></div>
<div class="abs glass" style="left:200px;top:0;width:548px;height:1000px"></div>
<div class="abs glass" style="left:752px;top:0;width:548px;height:1000px"></div>
<div class="abs mullion" style="left:748px;top:0;width:4px;height:1000px"></div>
<div class="abs band" style="left:200px;top:290px;width:1100px;height:330px"></div>
<img class="abs vinyl" src="{LOGO}/sanzeed-primary-wordmark--white.svg" alt="Sanzeed wordmark in white cut vinyl" style="left:420px;top:409px;width:660px">
<div class="abs handle" style="left:706px;top:642px"></div><div class="abs handle" style="left:786px;top:642px"></div>
<div class="abs" style="left:0;right:0;top:930px;height:70px;background:linear-gradient(180deg,#15151780,#0a0a0b);"></div>
<div class="abs floor-line" style="top:930px;background:rgba(255,255,255,.1)"></div>
<div class="abs vig"></div>
{cap('Frosted glass door', 'primary wordmark, white cut vinyl 1200 mm on a 600 mm frosted band · <span class="pt"></span>10_MARKETING_COLLATERAL / Signage / window vinyl')}
''', css='''
.frame { background: #1c1c1e; box-shadow: inset 0 0 0 1px #3a3a3e, 0 40px 80px rgba(0,0,0,.6); border-radius: 4px; }
.glass { background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.02) 50%, rgba(255,255,255,.07)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.12), inset 0 0 60px rgba(255,255,255,.03); }
.glass::after { content: ""; position: absolute; inset: 0; background: linear-gradient(112deg, rgba(255,255,255,0) 35%, rgba(255,255,255,.08) 48%, rgba(255,255,255,0) 56%); }
.mullion { background: #2a2a2d; box-shadow: 0 0 0 1px #3a3a3e; }
.band { -webkit-backdrop-filter: blur(16px) saturate(.9); backdrop-filter: blur(16px) saturate(.9); background: rgba(235,235,238,.42); box-shadow: inset 0 1px 0 rgba(255,255,255,.35), inset 0 -1px 0 rgba(255,255,255,.2); }
.vinyl { filter: drop-shadow(0 1px 0 rgba(0,0,0,.25)); }
.handle { width: 14px; height: 270px; border-radius: 7px; background: linear-gradient(90deg, #6a6a6f, #c9c9ce 40%, #8a8a90 70%, #4a4a4f); box-shadow: 0 10px 20px rgba(0,0,0,.5); }
.handle::before, .handle::after { content: ""; position: absolute; left: 3px; width: 8px; height: 26px; background: #55555a; border-radius: 2px; }
.handle::before { top: 30px; } .handle::after { bottom: 30px; }
''')

# 06 — app icon on a phone home screen
icons = ''.join('<i></i>' for _ in range(19))
scene('logo-app-icon-phone', L, 'App icon · the symbol tile on a phone home screen', ['07 App_Icons/iOS/ios-icon-1024.png', '05 Backgrounds lamp 1080×1920 (wallpaper)'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-20px;top:-250px;opacity:.6"></div>
<div class="abs tex-grain"></div>
{phone(f'''<img class="full" src="{BG}/sanzeed-bg-lamp--dark-1080x1920.jpg" alt="">{status()}
  <div class="grid"><div class="app"><img src="{WEB}/App_Icons/iOS/ios-icon-1024.png" alt="Sanzeed app icon"><span>Sanzeed</span></div>{icons}</div>
  <div class="dock"><i></i><i></i><i></i><i></i></div>''', 'left:200px;top:70px;transform:scale(.98)')}
<div class="abs" style="left:800px;top:230px;width:520px;height:540px">
  <div class="abs lamp" style="left:-540px;top:-530px;opacity:.55"></div>
  <img class="abs big" src="{WEB}/App_Icons/iOS/ios-icon-1024.png" alt="Sanzeed app icon, 1024 px" style="left:60px;top:0;width:400px;height:400px">
  <div class="abs" style="left:60px;top:440px;width:400px;text-align:center;font:400 15px/1.5 var(--font-text);color:#A1A1A6">iOS · Android · PWA · 1024 px master</div>
</div>
<div class="abs vig"></div>
{cap('App icon', 'symbol tile on Night · 07_WEBSITE_DIGITAL_ASSETS / App_Icons · <span class="pt"></span>02_LOGO_SYSTEM / symbol-tile')}
''', css='''
.grid { position: absolute; left: 24px; top: 92px; width: 342px; display: grid; grid-template-columns: repeat(4, 62px); column-gap: 31px; row-gap: 34px; }
.grid i, .grid .app img { width: 62px; height: 62px; border-radius: 15px; display: block; }
.grid i { background: linear-gradient(160deg, rgba(255,255,255,.13), rgba(255,255,255,.05)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.08); }
.grid .app { position: relative; } .grid .app span { position: absolute; left: -10px; right: -10px; top: 67px; text-align: center; font: 500 11px/1.2 var(--font-text); color: #F5F5F7; }
.grid .app img { box-shadow: 0 6px 16px rgba(0,0,0,.5); }
.dock { position: absolute; left: 16px; right: 16px; bottom: 26px; height: 92px; border-radius: 30px; background: rgba(255,255,255,.08); -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px); display: flex; justify-content: space-between; align-items: center; padding: 0 20px; box-shadow: inset 0 0 0 1px rgba(255,255,255,.06); }
.dock i { width: 62px; height: 62px; border-radius: 15px; background: linear-gradient(160deg, rgba(255,255,255,.14), rgba(255,255,255,.05)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.08); }
.big { border-radius: 90px; box-shadow: 0 40px 80px rgba(0,0,0,.6), 0 10px 20px rgba(0,0,0,.5); }
''')

# 07 — favicon in a browser tab strip (with a loupe)
scene('logo-favicon-browser-tab', L, 'Favicon · the symbol tile in a browser tab strip', ['02 Favicon/favicon-32.png', '16 site capture (dark)'], f'''
<div class="abs surf-charcoal" style="inset:0"></div>
<div class="abs tex-grain"></div>
<div class="abs win browser" style="left:100px;top:150px;width:1300px;height:900px">
  {browser_tabs()}
  <div class="bar"><div class="nav"><span>&#8249;</span><span>&#8250;</span><span>&#8635;</span></div><div class="url"><span class="lock"></span><b>sanzeed.com</b></div><div class="nav"><span>&#9734;</span><span>&#8942;</span></div></div>
  <div class="page" style="height:806px"><img src="{P}/site-desktop-dark-2880x1800.png" alt="sanzeed.com, dark theme"></div>
</div>
<div class="abs loupe" style="left:880px;top:60px;width:440px;height:440px">
  <div class="abs browser" style="left:0;top:0;width:1300px;transform:scale(3.4);transform-origin:0 0;translate:-35px 110px">{browser_tabs()}<div class="bar"><div class="nav"><span>&#8249;</span><span>&#8250;</span><span>&#8635;</span></div><div class="url"><span class="lock"></span><b>sanzeed.com</b></div></div></div>
</div>
{cap('Favicon', 'favicon-32 · 02_LOGO_SYSTEM / Favicon (ICO 16/32/48, SVG, PNG 16–1024) · <span class="pt"></span>16_WEBSITE_IMPLEMENTATION')}
''', css='''
.loupe { border-radius: 50%; overflow: hidden; background: #141416; box-shadow: 0 0 0 8px #0d0d0f, 0 0 0 9px #3a3a3e, 0 40px 90px rgba(0,0,0,.7); }
.loupe::after { content: ""; position: absolute; inset: 0; border-radius: 50%; box-shadow: inset 0 0 60px rgba(0,0,0,.6); background: linear-gradient(135deg, rgba(255,255,255,.08), transparent 40%); }
''')

# ================================================================================================================
# STATIONERY MOCKUPS
# ================================================================================================================
S = 'Stationery_Mockups'

# 08 — cards fanned on a dark surface with a point of light
cards = [('card-a-back', -18, -60), ('card-b-front', -9, -24), ('card-a-back', 0, 0), ('card-b-front', 9, 24), ('card-a-front', 18, 60)]   # last = top of the fan: a front, so the wordmark shows
fan = ''.join(f'<div class="abs card sh-dark paper" style="background-image:url({P}/{c}.png);transform:rotate({a}deg) translateX({x}px)"></div>' for c, a, x in cards)
scene('stationery-cards-fanned-dark', S, 'Business cards · fanned on a dark surface', ['09 Business_Cards concept A + B (PDF, 600 dpi)', '05 lamp glow, grain'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-380px;top:-760px;width:1700px;height:1700px;opacity:.75"></div>
<div class="abs point"></div>
<div class="abs tex-grain"></div>
<div class="abs persp" style="left:0;top:0;width:1500px;height:1000px;perspective:2200px">
  <div class="abs p3d fanwrap" style="left:470px;top:300px;width:560px;height:321px;transform:scale(1.18) rotateX(52deg) rotateZ(-8deg)">{fan}</div>
</div>
<div class="abs vig"></div>
{cap('Business cards', 'concept A (Plaster) and concept B (Gallery Black) · 89 × 51 mm · <span class="pt"></span>09_PRINT_STATIONERY / Business_Cards')}
''', css='''
.card { width: 560px; height: 321px; border-radius: 3px; transform-origin: 50% 160%; }
.card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(115deg, rgba(255,255,255,.10), rgba(255,255,255,0) 45%, rgba(0,0,0,.18) 100%); }
.point { left: 300px; top: 150px; width: 10px; height: 10px; border-radius: 50%; background: #F4C97A; box-shadow: 0 0 24px rgba(233,178,90,.9), 0 0 90px rgba(233,178,90,.45); }
''')

# 09 — flat lay on Plaster
scene('stationery-cards-flat-lay-plaster', S, 'Business cards · front and back, flat lay on Plaster', ['09 Business_Cards concept A + B (PDF, 600 dpi)', '05 paper texture'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
<div class="abs persp" style="inset:0;perspective:3000px">
  <div class="abs p3d" style="left:0;top:0;width:1500px;height:1000px;transform:rotateX(6deg)">
    <div class="abs card sh-light paper" style="left:150px;top:150px;background-image:url({P}/card-a-front.png)"></div>
    <div class="abs card sh-light paper" style="left:790px;top:150px;background-image:url({P}/card-a-back.png)"></div>
    <div class="abs card sh-light paper" style="left:150px;top:530px;background-image:url({P}/card-b-front.png)"></div>
    <div class="abs card sh-light paper" style="left:790px;top:530px;background-image:url({P}/card-b-back.png)"></div>
  </div>
</div>
{cap('Business cards, flat lay', 'concept A front / back · concept B front / back · 89 × 51 mm, 350 gsm · <span class="pt"></span>09_PRINT_STATIONERY / Business_Cards')}
''', css='''
.card { width: 560px; height: 321px; border-radius: 3px; box-shadow: 0 1px 0 rgba(40,30,10,.18), 0 2px 2px rgba(40,30,10,.10), 0 14px 28px rgba(40,30,10,.14), 0 40px 70px rgba(40,30,10,.12); }
.card::after { content: ""; position: absolute; inset: 0; border-radius: 3px; background: linear-gradient(118deg, rgba(255,255,255,.18), rgba(255,255,255,0) 40%, rgba(40,30,10,0) 70%, rgba(40,30,10,.07) 100%); }
''', light=True)

# 10 — letterhead + envelope + card set from above
scene('stationery-letterhead-envelope-card', S, 'Stationery set · letterhead, DL envelope, business card', ['09 Letterheads sample letter (PDF, 220 dpi)', '09 Envelopes DL front + back (PDF, 300 dpi)', '09 Business_Cards concept A'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
<div class="abs persp" style="inset:0;perspective:3000px">
  <div class="abs p3d" style="inset:0;transform:rotateX(8deg)">
    <div class="abs paper sh-light sheet" style="left:140px;top:-40px;width:600px;height:849px;background-image:url({P}/letterhead-a4-sample-01.png);transform:rotate(-5deg)"></div>
    <div class="abs paper sh-light env" style="left:640px;top:140px;width:720px;height:360px;background-image:url({P}/envelope-dl-back.png);transform:rotate(7deg)"></div>
    <div class="abs paper sh-light env" style="left:700px;top:430px;width:720px;height:360px;background-image:url({P}/envelope-dl-front.png);transform:rotate(-4deg)"></div>
    <div class="abs paper sh-light card" style="left:1010px;top:690px;width:300px;height:172px;background-image:url({P}/card-a-front.png);transform:rotate(9deg)"></div>
  </div>
</div>
{cap('Stationery set', 'A4 letterhead (sample letter) · DL envelope, front and flap · business card A · <span class="pt"></span>09_PRINT_STATIONERY')}
''', css='''
.sheet, .env, .card { border-radius: 2px; }
.sheet::after, .env::after, .card::after { content: ""; position: absolute; inset: 0; background: linear-gradient(118deg, rgba(255,255,255,.16), rgba(255,255,255,0) 40%, rgba(40,30,10,0) 70%, rgba(40,30,10,.06) 100%); }
''', light=True)

# 11 — proposal cover on a desk
scene('stationery-proposal-cover-desk', S, 'Proposal · cover on a desk', ['09 Proposals template cover (PDF, 250 dpi)', '05 lamp glow'], f'''
<div class="abs" style="inset:0;background:radial-gradient(120% 80% at 70% 10%,#2a2a2d 0%,#161618 45%,#050505 100%)"></div>
<div class="abs" style="inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.012) 0 1px,transparent 1px 7px)"></div>
<div class="abs lamp" style="left:300px;top:-900px;width:1800px;height:1800px;opacity:.5"></div>
<div class="abs tex-grain"></div>
<div class="abs persp" style="inset:0;perspective:2600px">
  <div class="abs p3d" style="inset:0;transform:rotateX(46deg) rotateZ(-14deg);transform-origin:50% 60%">
    <div class="abs stack" style="left:440px;top:120px;width:620px;height:877px"></div>
    <div class="abs paper doc" style="left:440px;top:120px;width:620px;height:877px;background-image:url({P}/proposal-cover.png)"></div>
    <div class="abs pen" style="left:1130px;top:300px"></div>
  </div>
</div>
<div class="abs vig"></div>
{cap('Proposal cover', 'A4 proposal template, dark cover with the lamp · <span class="pt"></span>09_PRINT_STATIONERY / Proposals')}
''', css='''
.stack { background: #e8e2d6; box-shadow: 0 2px 0 #d8d2c6, 0 4px 0 #e2dcd0, 0 6px 0 #d5cfc3, 0 8px 0 #e0dace, 0 10px 0 #d2ccc0, 0 40px 80px rgba(0,0,0,.7), 0 10px 20px rgba(0,0,0,.6); border-radius: 2px; }
.doc { border-radius: 2px; box-shadow: 0 1px 0 rgba(255,255,255,.06) inset; }
.doc::after { content: ""; position: absolute; inset: 0; background: linear-gradient(160deg, rgba(255,255,255,.07), rgba(255,255,255,0) 35%, rgba(0,0,0,0) 65%, rgba(0,0,0,.25) 100%); }
.pen { width: 18px; height: 460px; border-radius: 9px 9px 4px 4px; background: linear-gradient(90deg, #0a0a0b, #3a3a3e 35%, #151517 65%, #050506); box-shadow: 0 20px 40px rgba(0,0,0,.7), 0 4px 8px rgba(0,0,0,.6); }
.pen::before { content: ""; position: absolute; left: 11px; top: 30px; width: 5px; height: 150px; border-radius: 3px; background: linear-gradient(90deg, #9a9aa0, #e2e2e6, #7a7a80); }
.pen::after { content: ""; position: absolute; left: 4px; bottom: -20px; width: 10px; height: 24px; background: linear-gradient(90deg, #6a6a70, #d0d0d5, #55555a); clip-path: polygon(0 0, 100% 0, 60% 100%, 40% 100%); }
''')

# 12 — ID card on a lanyard
scene('stationery-id-card-lanyard', S, 'ID card · on the lanyard, front and back', ['09 ID_Card front + back (PDF, 600 dpi)', '09 ID_Card lanyard strip'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-500px;opacity:.5"></div>
<div class="abs tex-grain"></div>
<div class="abs badge" style="left:470px;top:-20px;transform:rotate(-4deg)">
  <div class="abs strap" style="left:-849px;top:113px;transform:rotate(78deg)"></div>
  <div class="abs strap" style="left:-849px;top:113px;transform:rotate(102deg)"></div>
  <div class="abs clip" style="left:198px;top:120px"></div>
  <div class="abs paper card sh-dark" style="left:0;top:180px;width:420px;height:666px;background-image:url({P}/id-card-front.png)"><i class="slot"></i></div>
</div>
<div class="abs badge" style="left:920px;top:40px;transform:rotate(6deg)">
  <div class="abs strap" style="left:-849px;top:113px;transform:rotate(78deg)"></div>
  <div class="abs strap" style="left:-849px;top:113px;transform:rotate(102deg)"></div>
  <div class="abs clip" style="left:198px;top:120px"></div>
  <div class="abs paper card sh-dark" style="left:0;top:180px;width:420px;height:666px;background-image:url({P}/id-card-back.png)"><i class="slot"></i></div>
</div>
<div class="abs vig"></div>
{cap('ID card and lanyard', 'CR80 portrait 54 × 85.6 mm, front (portrait) and back (monogram, QR) · 20 mm lanyard · <span class="pt"></span>09_PRINT_STATIONERY / ID_Card')}
''', css=f'''
.badge {{ width: 420px; height: 900px; }}
.strap {{ width: 1060px; height: 34px; background: #000 url("{R}/09_PRINT_STATIONERY/ID_Card/sanzeed-lanyard--strip.png") 0 0 / auto 34px repeat-x; transform-origin: 100% 50%; box-shadow: 0 10px 30px rgba(0,0,0,.6); }}
.strap::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,0) 40%, rgba(0,0,0,.35)); }}
.clip {{ width: 26px; height: 70px; border-radius: 13px 13px 6px 6px; background: linear-gradient(90deg, #6a6a70, #d9d9de 45%, #8a8a90 70%, #4a4a50); box-shadow: 0 6px 14px rgba(0,0,0,.6); }}
.clip::after {{ content: ""; position: absolute; left: 7px; top: 8px; width: 12px; height: 26px; border-radius: 6px; background: #1a1a1c; box-shadow: inset 0 1px 0 rgba(255,255,255,.25); }}
.card {{ border-radius: 18px; }}
.card::after {{ content: ""; position: absolute; inset: 0; border-radius: 18px; background: linear-gradient(160deg, rgba(255,255,255,.10), rgba(255,255,255,0) 40%, rgba(0,0,0,0) 70%, rgba(0,0,0,.2) 100%); }}
.slot {{ position: absolute; left: 50%; top: 18px; width: 56px; height: 9px; margin-left: -28px; border-radius: 5px; background: #0d0d0f; box-shadow: inset 0 1px 2px rgba(0,0,0,.8), 0 1px 0 rgba(255,255,255,.3); }}
''')

# 13 — thank-you card open
scene('stationery-thank-you-card-open', S, 'Thank-you card · open, with the signature', ['09 Thank_You_Cards folded outside + inside (PDF, 300 dpi)', '05 paper texture'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
<div class="abs persp" style="inset:0;perspective:2400px">
  <div class="abs p3d" style="inset:0;transform:rotateX(14deg);transform-origin:50% 70%">
    <div class="abs paper flat sh-light" style="left:120px;top:560px;width:400px;height:282px;background-image:url({P}/thank-you-outside.png);background-position:right;background-size:200% 100%;transform:rotate(-9deg) translateZ(1px)"></div>
    <div class="abs p3d open" style="left:560px;top:150px;width:900px;height:450px;transform:scale(1.22) rotateY(-18deg) rotateX(-6deg)">
      <div class="abs paper half l" style="background-image:url({P}/thank-you-inside.png)"></div>
      <div class="abs paper half r" style="background-image:url({P}/thank-you-inside.png)"></div>
      <div class="abs ground"></div>
    </div>
  </div>
</div>
{cap('Thank-you card', 'A6 folded (A5 flat): front "Thank you." with the point, inside the signature mark · <span class="pt"></span>09_PRINT_STATIONERY / Thank_You_Cards')}
''', css='''
.flat { border-radius: 2px; }
.open { transform-origin: 50% 50%; }
.half { top: 0; width: 420px; height: 297px; transform-origin: 100% 50%; background-size: 200% 100%; border-radius: 2px; }
.half.l { left: 30px; background-position: left; transform: rotateY(44deg); box-shadow: 0 30px 50px rgba(40,30,10,.25); }
.half.r { left: 450px; transform-origin: 0 50%; background-position: right; transform: rotateY(-44deg); box-shadow: 0 30px 50px rgba(40,30,10,.18); }
.half::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(40,30,10,.18), rgba(40,30,10,0) 35%); }
.half.r::after { background: linear-gradient(270deg, rgba(40,30,10,.06), rgba(255,255,255,.12) 60%, rgba(40,30,10,.10)); }
.ground { left: 60px; top: 250px; width: 780px; height: 140px; background: radial-gradient(50% 50% at 50% 50%, rgba(40,30,10,.28), transparent 70%); transform: rotateX(80deg); filter: blur(10px); }
''', light=True)

# 14 — stamp impression on paper (macro)
scene('stationery-stamp-impression', S, 'Rubber stamp · impression in Gold Ink on the letterhead', ['09 Stamp round 40 mm (outlined SVG, as the ink mask)', '09 Letterheads sample letter (PDF, 220 dpi)'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs paper sheet" style="left:-180px;top:-1500px;width:1720px;height:2433px;background-image:url({P}/letterhead-a4-first.png)"></div>
<div class="abs sweep"></div>
<div class="abs imp" style="left:520px;top:300px;width:400px;height:400px;transform:rotate(-9deg)">
  <div class="abs mask ink"></div><div class="abs mask ink2"></div>
</div>
<div class="abs stamp" style="left:1040px;top:240px"><div class="abs s-base"></div><div class="abs s-cap"></div><div class="abs s-handle"></div></div>
<div class="abs vig soft" style="background:radial-gradient(ellipse at 50% 45%,transparent 55%,rgba(60,40,15,.2) 100%)"></div>
{cap('Stamp impression', 'round 40 mm stamp, Gold Ink pad on the letterhead · <span class="pt"></span>09_PRINT_STATIONERY / Stamp')}
''', css=f'''
.sheet {{ box-shadow: none; }}
.mask {{ inset: 0; -webkit-mask-image: {MK_STAMP}; mask-image: {MK_STAMP}; }}
.ink {{ background: #8A6124; opacity: .9; }}
.ink2 {{ background: url("{TEX}/sanzeed-texture-grain--tile-1024.png") 0 0 / 300px 300px; mix-blend-mode: screen; opacity: .9; }}
.imp {{ filter: blur(.35px); }}
.stamp {{ width: 300px; height: 300px; }}
.stamp .s-base {{ inset: 0; border-radius: 50%; background: radial-gradient(circle at 50% 50%, #2a2a2d, #141416 60%, #0b0b0c); box-shadow: 0 40px 70px rgba(40,30,10,.45), 0 10px 20px rgba(40,30,10,.3), inset 0 0 0 2px #2a2a2d; }}
.stamp .s-cap {{ inset: 44px; border-radius: 50%; background: radial-gradient(circle at 40% 35%, #4a4a4f, #1c1c1e 55%, #0b0b0c); box-shadow: 0 12px 24px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.12); }}
.stamp .s-handle {{ inset: 96px; border-radius: 50%; background: radial-gradient(circle at 40% 30%, #6a6a70, #2a2a2d 50%, #0b0b0c); box-shadow: 0 10px 20px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.2); }}
''', light=True)

# 15 — notepad with pen
scene('stationery-notepad-pen', S, 'Notepad · A5 pad with a pen', ['09 Notepad A5 (PDF, 300 dpi)', '05 paper texture'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
<div class="abs persp" style="inset:0;perspective:2600px">
  <div class="abs p3d" style="inset:0;transform:rotateX(22deg) rotateZ(-7deg);transform-origin:50% 55%">
    <div class="abs stack" style="left:470px;top:40px;width:560px;height:795px"></div>
    <div class="abs paper pad" style="left:470px;top:40px;width:560px;height:795px;background-image:url({P}/notepad-a5.png)"></div>
    <div class="abs bind" style="left:466px;top:30px;width:568px;height:42px"></div>
    <div class="abs pen" style="left:840px;top:430px;transform:rotate(-58deg)"></div>
  </div>
</div>
{cap('Notepad', 'A5 pad, Paper stock, 8 mm beams with the gold point · <span class="pt"></span>09_PRINT_STATIONERY / Notepad')}
''', css='''
.stack { background: #f1ece2; border-radius: 2px; box-shadow: 0 2px 0 #e3ddd1, 0 4px 0 #eee8dd, 0 6px 0 #ded8cc, 0 8px 0 #ebe5da, 0 10px 0 #d9d3c7, 0 12px 0 #e8e2d7, 0 30px 60px rgba(40,30,10,.25), 0 8px 16px rgba(40,30,10,.2); }
.pad { border-radius: 2px; }
.pad::after { content: ""; position: absolute; inset: 0; background: linear-gradient(160deg, rgba(255,255,255,.14), rgba(255,255,255,0) 35%, rgba(40,30,10,0) 70%, rgba(40,30,10,.08) 100%); }
.bind { border-radius: 4px 4px 2px 2px; background: linear-gradient(180deg, #2a2a2d, #0d0d0f 60%, #1c1c1e); box-shadow: 0 3px 6px rgba(40,30,10,.4), inset 0 1px 0 rgba(255,255,255,.12); }
.pen { width: 18px; height: 440px; border-radius: 9px 9px 4px 4px; background: linear-gradient(90deg, #0a0a0b, #3a3a3e 35%, #151517 65%, #050506); box-shadow: 0 24px 40px rgba(40,30,10,.4), 0 4px 8px rgba(40,30,10,.35); transform-origin: 50% 50%; }
.pen::before { content: ""; position: absolute; left: 11px; top: 26px; width: 5px; height: 140px; border-radius: 3px; background: linear-gradient(90deg, #9a9aa0, #e2e2e6, #7a7a80); }
.pen::after { content: ""; position: absolute; left: 4px; bottom: -20px; width: 10px; height: 24px; background: linear-gradient(90deg, #6a6a70, #d0d0d5, #55555a); clip-path: polygon(0 0, 100% 0, 60% 100%, 40% 100%); }
''', light=True)

# 16 — presentation folder open with insert
scene('stationery-folder-open-insert', S, 'Presentation folder · open, with the letterhead and card inserted', ['09 Folder A4 outside (PDF, 160 dpi): front panel, pocket', '09 Letterheads sample letter', '09 Business_Cards concept A'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-200px;top:-700px;opacity:.55"></div>
<div class="abs tex-grain"></div>
<div class="abs persp" style="inset:0;perspective:2800px">
  <div class="abs p3d" style="inset:0;transform:rotateX(36deg) rotateZ(-9deg);transform-origin:50% 55%">
    <div class="abs paper closed sh-dark" style="left:-60px;top:-260px;width:480px;height:665px;background-image:url({P}/folder-front.png);transform:rotate(-6deg)"></div>
    <div class="abs panel sh-dark" style="left:300px;top:150px;width:470px;height:652px"><div class="abs paper card sh-dark" style="left:140px;top:470px;width:190px;height:109px;background-image:url({P}/card-a-front.png);transform:rotate(-6deg)"></div><i class="abs slit" style="left:120px;top:462px"></i><i class="abs slit" style="left:330px;top:574px"></i></div>
    <div class="abs panel sh-dark" style="left:778px;top:150px;width:470px;height:652px">
      <div class="abs paper insert sh-dark" style="left:36px;top:30px;width:398px;height:563px;background-image:url({P}/letterhead-a4-sample-01.png)"></div>
      <div class="abs paper pocket" style="left:0;top:460px;width:470px;height:192px;background-image:url({P}/folder-pocket.png)"></div>
    </div>
    <div class="abs spine" style="left:770px;top:150px;width:8px;height:652px"></div>
  </div>
</div>
<div class="abs vig"></div>
{cap('Presentation folder', 'A4 pocket folder, 5 mm spine, Gallery Black · letterhead and card A inserted · <span class="pt"></span>09_PRINT_STATIONERY / Folder')}
''', css='''
.closed { border-radius: 3px; }
.closed::after { content: ""; position: absolute; inset: 0; background: linear-gradient(160deg, rgba(255,255,255,.08), rgba(255,255,255,0) 40%, rgba(0,0,0,.35) 100%); }
.panel { background: linear-gradient(160deg, #1c1c1e, #111113 60%, #0b0b0c); border-radius: 3px; }
.panel::before { content: ""; position: absolute; inset: 0; background: linear-gradient(118deg, rgba(255,255,255,.06), transparent 50%); }
.spine { background: #050506; }
.insert { border-radius: 2px; }
.insert::after { content: ""; position: absolute; inset: 0; background: linear-gradient(160deg, rgba(255,255,255,.1), rgba(255,255,255,0) 40%, rgba(0,0,0,0) 70%, rgba(0,0,0,.12) 100%); }
.pocket { border-radius: 0 0 3px 3px; box-shadow: 0 -8px 20px rgba(0,0,0,.6), inset 0 1px 0 rgba(255,255,255,.08); }
.pocket::before { content: ""; position: absolute; left: 24px; top: 24px; width: 120px; height: 2px; background: rgba(255,255,255,.08); transform: rotate(-30deg); transform-origin: 0 0; }
.card { border-radius: 2px; }
.slit { width: 30px; height: 3px; background: #000; transform: rotate(-45deg); box-shadow: 0 1px 0 rgba(255,255,255,.08); }
''')

# ================================================================================================================
# DIGITAL MOCKUPS
# ================================================================================================================
D = 'Digital_Mockups'

# 17 / 18 — website on a laptop, dark and light
scene('digital-website-laptop-dark', D, 'Website · hero on a laptop, dark theme', ['16 site capture, dark, 1440 × 900 @ 2×'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-500px;opacity:.7"></div>
<div class="abs tex-grain"></div>
{laptop(f'<img src="{P}/site-desktop-dark-2880x1800.png" alt="sanzeed.com hero, dark theme">', 'left:160px;top:110px')}
<div class="abs refl" style="left:70px;top:894px;width:1360px;height:106px;background:url({P}/site-desktop-dark-2880x1800.png) center bottom / 1136px auto no-repeat;transform:scaleY(-1);opacity:.14;filter:blur(3px);-webkit-mask-image:linear-gradient(180deg,transparent,#000 80%);mask-image:linear-gradient(180deg,transparent,#000 80%)"></div>
<div class="abs vig"></div>
{cap('Website, dark theme', 'sanzeed.com hero at 1440 × 900 · <span class="pt"></span>16_WEBSITE_IMPLEMENTATION')}
''')

scene('digital-website-laptop-light', D, 'Website · hero on a laptop, light theme', ['16 site capture, light, 1440 × 900 @ 2×'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
<div class="abs lamp light" style="left:-50px;top:-500px;opacity:.35"></div>
{laptop(f'<img src="{P}/site-desktop-light-2880x1800.png" alt="sanzeed.com hero, light theme">', 'left:160px;top:110px', 'silver')}
<div class="abs" style="left:0;top:884px;width:1500px;height:116px;background:linear-gradient(180deg,rgba(40,30,10,.18),rgba(40,30,10,0))"></div>
{cap('Website, light theme', 'sanzeed.com hero at 1440 × 900, Plaster · <span class="pt"></span>16_WEBSITE_IMPLEMENTATION')}
''', light=True)

# 19 — website on a phone
scene('digital-website-phone-dark', D, 'Website · on a phone, dark theme', ['16 site capture, mobile 390 × 844 @ 3×'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-420px;opacity:.75"></div>
<div class="abs tex-grain"></div>
<div class="abs persp" style="inset:0;perspective:2400px">
  {phone(f'<img class="full" src="{P}/site-mobile-dark-1170x2532.png" alt="sanzeed.com on a phone">', 'left:539px;top:60px;transform:rotateY(-14deg) rotateX(4deg)', home=False)}
</div>
<div class="abs vig"></div>
{cap('Website on a phone', 'sanzeed.com at 390 × 844, dark theme · <span class="pt"></span>16_WEBSITE_IMPLEMENTATION')}
''')

# 20 — Instagram feed grid on a phone
hl = [('work', 'Work'), ('museums', 'Museums'), ('shows', 'Shows'), ('method', 'Method'), ('contact', 'Contact')]
hls = ''.join(f'<div class="hl"><i style="background-image:url({SOC}/Instagram/Highlight_Covers/sanzeed-ig-highlight--{k}-1080x1920.png)"></i><span>{v}</span></div>' for k, v in hl)
scene('digital-instagram-feed-phone', D, 'Instagram · profile and feed grid on a phone', ['08 Instagram profile 1024 (dark)', '08 Instagram highlight covers ×5', '08 Instagram grid preview 3 × 3'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-420px;opacity:.6"></div>
<div class="abs tex-grain"></div>
{phone(f'''<div class="ig">{status()}
  <div class="top"><b>sanzeed</b><span class="ic"><i></i><i></i></span></div>
  <div class="head"><img src="{SOC}/Instagram/sanzeed-ig-profile--dark-1024x1024.png" alt="Sanzeed profile image"><div class="t"><b>Sanzeed Mirza</b><span>Experiential Design Consultant</span><span>Experiential design you can walk into.</span><span class="lnk">sanzeed.com</span></div></div>
  <div class="hls">{hls}</div>
  <div class="tabs"><i class="on"></i><i></i><i></i></div>
  <img class="grid" src="{SOC}/Instagram/sanzeed-ig-grid-preview--3x3-1632x1632.png" alt="Instagram feed, 3 × 3 grid">
</div>''', 'left:539px;top:60px')}
<div class="abs vig"></div>
{cap('Instagram profile', 'profile tile, five highlight covers, the 3 × 3 grid (posts, quotes, stat) · <span class="pt"></span>08_SOCIAL_MEDIA / Instagram')}
''', css='''
.ig { position: absolute; inset: 0; background: #000; color: #F5F5F7; }
.ig .top { position: absolute; left: 0; right: 0; top: 62px; height: 40px; display: flex; align-items: center; justify-content: space-between; padding: 0 18px; font: 600 20px/1 var(--font-heading); }
.ig .ic { display: flex; gap: 16px; } .ig .ic i { width: 22px; height: 22px; border: 2px solid #F5F5F7; border-radius: 6px; display: block; } .ig .ic i:first-child { border-radius: 50%; }
.ig .head { position: absolute; left: 18px; right: 18px; top: 116px; display: flex; gap: 20px; align-items: flex-start; }
.ig .head img { width: 86px; height: 86px; border-radius: 50%; box-shadow: 0 0 0 2px #000, 0 0 0 3.5px #3a3a3e; }
.ig .head .t { display: flex; flex-direction: column; gap: 3px; padding-top: 4px; font: 400 13px/1.35 var(--font-text); color: #F5F5F7; }
.ig .head .t b { font: 600 15px/1.3 var(--font-heading); } .ig .head .t .lnk { color: #E9B25A; }
.ig .hls { position: absolute; left: 0; right: 0; top: 232px; display: flex; gap: 14px; padding: 0 18px; }
.ig .hl { display: flex; flex-direction: column; align-items: center; gap: 6px; width: 60px; }
.ig .hl i { width: 60px; height: 60px; border-radius: 50%; background-size: 100% auto; background-position: center; box-shadow: 0 0 0 2px #000, 0 0 0 3px #3a3a3e; display: block; }
.ig .hl span { font: 400 11px/1 var(--font-text); color: #F5F5F7; }
.ig .tabs { position: absolute; left: 0; right: 0; top: 330px; height: 36px; display: flex; border-bottom: 1px solid #2A2A2D; }
.ig .tabs i { flex: 1; position: relative; } .ig .tabs i::after { content: ""; position: absolute; left: 50%; top: 9px; width: 18px; height: 18px; margin-left: -9px; border: 2px solid #808086; border-radius: 3px; }
.ig .tabs i.on { border-bottom: 1.5px solid #F5F5F7; } .ig .tabs i.on::after { border-color: #F5F5F7; }
.ig .grid { position: absolute; left: 0; top: 368px; width: 390px; display: block; }
''')

# 21 — LinkedIn profile on a laptop
scene('digital-linkedin-profile-laptop', D, 'LinkedIn · personal profile with banner and avatar, on a laptop', ['08 LinkedIn personal banner 1584 × 396', '08 LinkedIn profile 400 (dark)'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
{laptop(f'''<div class="li">
  <div class="nav"><div class="dots"><i></i><i></i><i></i></div><div class="search"></div><div class="nv"><i></i><i></i><i></i><i></i></div></div>
  <div class="wrap">
    <div class="card prof">
      <img class="banner" src="{SOC}/LinkedIn/sanzeed-li-banner--personal-1584x396.png" alt="LinkedIn banner">
      <img class="avatar" src="{SOC}/LinkedIn/sanzeed-li-profile--dark-400x400.png" alt="LinkedIn profile image">
      <div class="body"><h1>Sanzeed Mirza</h1><p class="hl">Experiential Design Consultant — museums, experience centres, pavilions, memorials, projection-mapping and light shows</p><p class="loc">New Delhi, India · <span>Contact info</span></p>
      <p class="btns"><b>Message</b><span>sanzeed.com</span></p></div>
    </div>
    <div class="card about"><h2>About</h2><p>Experiential design you can walk into. I direct museums, experience centres, pavilions, memorials, projection-mapping and light shows — one vision, from the brief to opening night. 15+ years, 90+ projects directed, 60+ museums and centres. Independent consultant since August 2026, based in New Delhi, working with institutions and brands wherever the project is.</p></div>
    <div class="side"><div class="card"><div class="ln" style="width:60%"></div><div class="ln"></div><div class="ln" style="width:80%"></div></div><div class="card"><div class="ln" style="width:50%"></div><div class="ln"></div></div></div>
  </div>
</div>''', 'left:160px;top:110px', 'silver')}
<div class="abs" style="left:0;top:884px;width:1500px;height:116px;background:linear-gradient(180deg,rgba(40,30,10,.18),rgba(40,30,10,0))"></div>
{cap('LinkedIn profile', 'personal banner 1584 × 396 (avatar overlap bottom-left) and profile tile · <span class="pt"></span>08_SOCIAL_MEDIA / LinkedIn')}
''', css='''
.li { position: absolute; inset: 0; background: #ECE7DC; font-family: var(--font-text); color: #1A1816; }
.li .nav { height: 52px; background: #FBF8F2; border-bottom: 1px solid rgba(40,30,10,.1); display: flex; align-items: center; gap: 18px; padding: 0 28px; }
.li .nav .dots i { background: #c9c4b9; } .li .search { width: 260px; height: 30px; border-radius: 6px; background: #ECE7DC; } .li .nv { margin-left: auto; display: flex; gap: 26px; } .li .nv i { width: 22px; height: 22px; border-radius: 5px; background: #d5cfc3; display: block; }
.li .wrap { position: absolute; left: 118px; top: 76px; width: 900px; display: grid; grid-template-columns: 1fr 280px; gap: 18px; }
.li .card { background: #FBF8F2; border: 1px solid rgba(40,30,10,.10); border-radius: 10px; overflow: hidden; }
.li .prof { grid-column: 1; }
.li .banner { width: 100%; display: block; aspect-ratio: 4 / 1; object-fit: cover; }
.li .avatar { position: absolute; left: 22px; top: 92px; width: 130px; height: 130px; border-radius: 50%; box-shadow: 0 0 0 4px #FBF8F2; }
.li .body { padding: 74px 24px 22px; }
.li h1 { font: 600 24px/1.2 var(--font-heading); margin: 0 0 4px; } .li .hl { font: 400 14px/1.45 var(--font-text); margin: 0 0 8px; max-width: 520px; } .li .loc { font: 400 13px/1.4 var(--font-text); color: #665F55; margin: 0 0 14px; } .li .loc span { color: #8A6124; font-weight: 500; }
.li .btns { margin: 0; display: flex; gap: 10px; align-items: center; } .li .btns b { display: inline-block; padding: 8px 18px; border-radius: 999px; background: #1A1816; color: #FBF8F2; font: 500 13px/1 var(--font-text); } .li .btns span { padding: 8px 16px; border-radius: 999px; border: 1px solid #1A1816; font: 500 13px/1 var(--font-text); }
.li .about { grid-column: 1; padding: 20px 24px; } .li .about h2 { font: 600 18px/1.3 var(--font-heading); margin: 0 0 8px; } .li .about p { font: 400 14px/1.55 var(--font-text); margin: 0; color: #1A1816; }
.li .side { grid-column: 2; grid-row: 1 / span 2; display: flex; flex-direction: column; gap: 18px; } .li .side .card { padding: 20px; } .li .ln { height: 10px; border-radius: 5px; background: #ECE7DC; margin: 0 0 12px; }
''', light=True)

# 22 — email signature in a mail window
scene('digital-email-signature-mail-window', D, 'Email signature · as received, in a mail window', ['07 Email/email-signature.html (live, in an iframe)', '07 Email signature preview copy'], f'''
<div class="abs surf-charcoal" style="inset:0"></div>
<div class="abs tex-grain"></div>
<div class="abs win mail" style="left:130px;top:90px;width:1240px;height:860px">
  <div class="tb"><div class="dots"><i></i><i></i><i></i></div><span>Re: The room — a first conversation</span></div>
  <div class="side"><div class="s-h">Inbox</div><div class="row on"><b>Sanzeed Mirza</b><span>Re: The room — a first conversation</span><em>Thank you for writing. I’ve read the brief twice. Could we speak on Thursday…</em></div><div class="row"><i style="width:40%"></i><i></i><i style="width:70%"></i></div><div class="row"><i style="width:55%"></i><i></i><i style="width:60%"></i></div><div class="row"><i style="width:45%"></i><i></i><i style="width:75%"></i></div><div class="row"><i style="width:35%"></i><i></i><i style="width:65%"></i></div></div>
  <div class="msg">
    <div class="hdr"><div class="av"><img src="{R}/02_LOGO_SYSTEM/Favicon/favicon-64.png" alt=""></div><div><b>Sanzeed Mirza</b> <span>&lt;sanzeed@gmail.com&gt;</span><div class="to">To: me</div></div></div>
    <div class="body"><p>Thank you for writing. I’ve read the brief twice. Could we speak on Thursday for twenty minutes?</p><p>The first conversation is always free.</p><p>— Sanzeed</p>
      <iframe src="{WEB}/Email/email-signature.html" title="Sanzeed email signature" scrolling="no"></iframe>
    </div>
  </div>
</div>
{cap('Email signature', 'HTML signature, 600 px, logo 320 × 100 @ 2× · <span class="pt"></span>07_WEBSITE_DIGITAL_ASSETS / Email')}
''', css='''
.mail { background: #FBF8F2; color: #1A1816; font-family: var(--font-text); }
.mail .tb { height: 46px; background: #ECE7DC; border-bottom: 1px solid rgba(40,30,10,.1); display: flex; align-items: center; gap: 16px; padding: 0 18px; font: 500 13px/1 var(--font-text); color: #665F55; }
.mail .tb .dots i { background: #c9c4b9; }
.mail .side { position: absolute; left: 0; top: 46px; bottom: 0; width: 330px; background: #F5F0E7; border-right: 1px solid rgba(40,30,10,.1); padding: 18px 0; }
.mail .s-h { font: 600 12px/1 var(--font-heading); letter-spacing: .12em; text-transform: uppercase; color: #8A6124; padding: 0 22px 14px; }
.mail .row { padding: 14px 22px; border-bottom: 1px solid rgba(40,30,10,.07); display: flex; flex-direction: column; gap: 5px; }
.mail .row.on { background: #FBF8F2; border-left: 3px solid #B8863B; }
.mail .row b { font: 600 14px/1.3 var(--font-heading); } .mail .row span { font: 500 13px/1.3 var(--font-text); } .mail .row em { font: 400 12px/1.4 var(--font-text); color: #665F55; font-style: normal; }
.mail .row i { display: block; height: 9px; border-radius: 5px; background: #e4ded2; margin: 3px 0; }
.mail .msg { position: absolute; left: 330px; top: 46px; right: 0; bottom: 0; }
.mail .hdr { display: flex; gap: 14px; align-items: center; padding: 24px 36px; border-bottom: 1px solid rgba(40,30,10,.08); font: 400 14px/1.4 var(--font-text); }
.mail .hdr .av { width: 44px; height: 44px; border-radius: 50%; overflow: hidden; } .mail .hdr .av img { width: 100%; display: block; }
.mail .hdr b { font: 600 15px/1.3 var(--font-heading); } .mail .hdr span { color: #665F55; } .mail .to { font-size: 12px; color: #665F55; }
.mail .body { padding: 26px 36px; } .mail .body p { font: 400 15px/1.55 var(--font-text); margin: 0 0 12px; }
.mail iframe { width: 620px; height: 420px; border: 0; margin-top: 10px; display: block; background: #fff; }
''')

# 23 — OG card in a chat bubble
scene('digital-og-card-chat-bubble', D, 'Share card · the Open Graph image in a chat link preview', ['07 Open_Graph og-home 1200 × 630', '16 og:title / og:description', '02 symbol tile (avatar)'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-420px;opacity:.6"></div>
<div class="abs tex-grain"></div>
{phone(f'''<div class="chat">{status()}
  <div class="top"><i class="bk"></i><img src="{SOC}/Instagram/sanzeed-ig-profile--dark-1024x1024.png" alt=""><div><b>Sanzeed Mirza</b><span>online</span></div></div>
  <div class="msgs">
    <div class="b in"><div class="prev"><img src="{WEB}/Open_Graph/sanzeed-og--home-1200x630.png" alt="Open Graph image"><div class="pt"><b>Sanzeed Mirza — Experiential Design Consultant</b><span>Sanzeed Mirza — Experiential design you can walk into.</span><em>sanzeed.com</em></div></div><a>https://sanzeed.com</a><time>10:06</time></div>
    <div class="b out"><span>Thank you — looks like exactly the room we have in mind.</span><time>10:08</time></div>
  </div>
  <div class="input"><span>Message</span></div>
</div>''', 'left:539px;top:60px')}
<div class="abs vig"></div>
{cap('Link preview in chat', 'og-home 1200 × 630, og:title and description from the site · <span class="pt"></span>07_WEBSITE_DIGITAL_ASSETS / Open_Graph')}
''', css='''
.chat { position: absolute; inset: 0; background: #0D0D0F; color: #F5F5F7; font-family: var(--font-text); }
.chat .top { position: absolute; left: 0; right: 0; top: 56px; height: 62px; background: #1C1C1E; display: flex; align-items: center; gap: 12px; padding: 0 16px; border-bottom: 1px solid rgba(255,255,255,.08); }
.chat .top .bk { width: 10px; height: 10px; border-left: 2px solid #F5F5F7; border-bottom: 2px solid #F5F5F7; transform: rotate(45deg); margin-right: 4px; }
.chat .top img { width: 40px; height: 40px; border-radius: 50%; } .chat .top b { display: block; font: 600 15px/1.2 var(--font-heading); } .chat .top span { font: 400 12px/1.2 var(--font-text); color: #A1A1A6; }
.chat .msgs { position: absolute; left: 14px; right: 14px; top: 150px; display: flex; flex-direction: column; gap: 12px; }
.chat .b { position: relative; max-width: 300px; padding: 8px 10px 20px; border-radius: 14px; font: 400 14px/1.4 var(--font-text); }
.chat .b.in { background: #1C1C1E; align-self: flex-start; border-top-left-radius: 4px; }
.chat .b.out { background: #2A2A2D; align-self: flex-end; border-top-right-radius: 4px; }
.chat .b time { position: absolute; right: 10px; bottom: 5px; font-size: 10px; color: #808086; }
.chat .b a { display: block; color: #E9B25A; padding: 6px 2px 0; word-break: break-all; }
.chat .prev { border-radius: 10px; overflow: hidden; background: #0D0D0F; }
.chat .prev img { width: 100%; display: block; }
.chat .pt { padding: 8px 10px 10px; display: flex; flex-direction: column; gap: 3px; } .chat .pt b { font: 600 13px/1.3 var(--font-heading); } .chat .pt span { font: 400 12px/1.35 var(--font-text); color: #A1A1A6; } .chat .pt em { font: 400 11px/1.3 var(--font-text); color: #808086; font-style: normal; }
.chat .input { position: absolute; left: 14px; right: 14px; bottom: 30px; height: 44px; border-radius: 22px; background: #1C1C1E; display: flex; align-items: center; padding: 0 18px; font: 400 14px/1 var(--font-text); color: #808086; }
''')

# 24 — YouTube channel page on a tablet
vids = [('project', 'The building is the screen.', 'Ram Katha Show · Ayodhya · project film'), ('process', 'The script comes first.', 'Process · every room, screen and surface carries a line of it'), ('talk', 'A method for the monumental.', 'Talk · Sanzeed Mirza')]
vid_html = ''.join(f'<div class="v"><img src="{SOC}/YouTube/sanzeed-yt-thumbnail--{k}-1280x720.png" alt=""><b>{t}</b><span>{s}</span></div>' for k, t, s in vids)
scene('digital-youtube-channel-tablet', D, 'YouTube · channel page on a tablet', ['08 YouTube banner 2560 × 1440 (safe band)', '08 YouTube profile 800 (dark)', '08 YouTube thumbnails ×3'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-500px;opacity:.55"></div>
<div class="abs tex-grain"></div>
{tablet(f'''<div class="yt">
  <div class="nav"><i class="m"></i><span class="logo"></span><div class="s"></div><i class="a"></i></div>
  <div class="banner"><img src="{SOC}/YouTube/sanzeed-yt-banner-2560x1440.png" alt="YouTube channel banner"></div>
  <div class="ch"><img src="{SOC}/YouTube/sanzeed-yt-profile--dark-800x800.png" alt=""><div><h1>Sanzeed Mirza</h1><p>sanzeed.com · Experiential Design Consultant</p><p class="d">Experiential design you can walk into. Museums, experience centres, pavilions and projection shows — directed by one person.</p></div><b class="sub">Subscribe</b></div>
  <div class="tabs"><span class="on">Home</span><span>Videos</span><span>Playlists</span><span>About</span></div>
  <div class="vids">{vid_html}</div>
</div>''', 'left:190px;top:90px')}
<div class="abs vig"></div>
{cap('YouTube channel', 'banner (centre safe area), profile tile, three thumbnails (project · process · talk) · <span class="pt"></span>08_SOCIAL_MEDIA / YouTube')}
''', css='''
.yt { position: absolute; inset: 0; background: #0D0D0F; color: #F5F5F7; font-family: var(--font-text); }
.yt .nav { height: 54px; display: flex; align-items: center; gap: 18px; padding: 0 22px; border-bottom: 1px solid rgba(255,255,255,.06); }
.yt .nav .m { width: 20px; height: 14px; border-top: 2px solid #F5F5F7; border-bottom: 2px solid #F5F5F7; position: relative; } .yt .nav .m::after { content: ""; position: absolute; left: 0; right: 0; top: 4px; height: 2px; background: #F5F5F7; }
.yt .nav .logo { width: 88px; height: 20px; border-radius: 4px; background: #2A2A2D; } .yt .nav .s { margin-left: auto; width: 420px; height: 34px; border-radius: 17px; background: #1C1C1E; border: 1px solid rgba(255,255,255,.08); } .yt .nav .a { width: 30px; height: 30px; border-radius: 50%; background: #2A2A2D; margin-left: auto; }
.yt .banner { height: 168px; overflow: hidden; } .yt .banner img { width: 100%; height: 100%; object-fit: cover; object-position: center; display: block; }
.yt .ch { display: flex; gap: 22px; align-items: flex-start; padding: 22px 40px 0; } .yt .ch img { width: 110px; height: 110px; border-radius: 50%; }
.yt h1 { font: 600 26px/1.2 var(--font-heading); margin: 6px 0 4px; } .yt .ch p { font: 400 13px/1.4 var(--font-text); color: #A1A1A6; margin: 0 0 4px; } .yt .ch .d { color: #F5F5F7; max-width: 560px; }
.yt .sub { margin-left: auto; margin-top: 10px; padding: 10px 18px; border-radius: 999px; background: #F5F5F7; color: #000; font: 500 13px/1 var(--font-text); }
.yt .tabs { display: flex; gap: 30px; padding: 18px 40px 0; border-bottom: 1px solid rgba(255,255,255,.08); font: 500 14px/1 var(--font-text); color: #A1A1A6; } .yt .tabs span { padding-bottom: 12px; } .yt .tabs .on { color: #F5F5F7; border-bottom: 2px solid #F5F5F7; }
.yt .vids { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 22px 40px; }
.yt .v img { width: 100%; border-radius: 10px; display: block; } .yt .v b { display: block; font: 600 14px/1.3 var(--font-heading); margin: 10px 0 3px; } .yt .v span { font: 400 12px/1.35 var(--font-text); color: #A1A1A6; }
''')

# 25 — presentation on a conference-room screen
scene('digital-presentation-conference-screen', D, 'Presentation template · on a conference-room screen', ['09 Presentation_Template slide 01 (PDF, 220 dpi)'], f'''
<div class="abs" style="inset:0;background:linear-gradient(180deg,#0a0a0b 0%,#19191b 45%,#232326 62%,#0d0d0f 63%,#050506 100%)"></div>
<div class="abs" style="left:0;right:0;top:0;height:620px;background:radial-gradient(40% 80% at 25% 0,rgba(255,255,255,.07),transparent 70%),radial-gradient(40% 80% at 75% 0,rgba(255,255,255,.07),transparent 70%)"></div>
<div class="abs tex-grain"></div>
<div class="abs monitor" style="left:210px;top:90px;width:1080px;height:640px"><div class="bezel"></div><div class="screen"><img class="img-cover" src="{P}/presentation-slide-01.png" alt="Presentation title slide"></div></div>
<div class="abs" style="left:0;right:0;top:630px;height:370px;background:linear-gradient(180deg,rgba(233,178,90,.05),rgba(0,0,0,0) 60%)"></div>
<div class="abs table" style="left:-100px;top:770px;width:1700px;height:230px"></div>
<div class="abs refl" style="left:226px;top:772px;width:1048px;height:220px;background:url({P}/presentation-slide-01.png) center bottom / 100% auto no-repeat;transform:scaleY(-1) translateY(-8px);opacity:.22;filter:blur(4px);-webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.8),transparent 85%);mask-image:linear-gradient(0deg,rgba(0,0,0,.8),transparent 85%)"></div>
<div class="abs vig"></div>
{cap('Presentation on screen', '16:9 template, title slide, wall-mounted 85-inch display · <span class="pt"></span>09_PRINT_STATIONERY / Presentation_Template')}
''', css='''
.table { background: linear-gradient(180deg, #2b2b2e, #151517 30%, #0a0a0b); transform: perspective(900px) rotateX(55deg); transform-origin: 50% 0; box-shadow: 0 -2px 0 rgba(255,255,255,.06); }
.refl { transform-origin: 50% 0; }
''')

# ================================================================================================================
# MARKETING MOCKUPS
# ================================================================================================================
M = 'Marketing_Mockups'

# 26 — A2 poster on a gallery wall
scene('marketing-poster-a2-gallery-wall', M, 'Poster · A2 campaign poster on a gallery wall', ['10 Posters campaign A2 (trim crop)'], f'''
<div class="abs" style="inset:0;background:linear-gradient(180deg,#ddd9d1 0%,#e9e5de 50%,#d9d5cd 84%,#8e8b85 84.2%,#6f6d68 100%)"></div>
<div class="abs" style="left:0;right:0;top:0;height:840px;background:radial-gradient(45% 70% at 50% -5%,rgba(255,250,235,.85),rgba(255,250,235,0) 70%)"></div>
<div class="abs" style="left:0;right:0;top:838px;height:4px;background:#cbc7bf;box-shadow:0 2px 4px rgba(0,0,0,.15)"></div>
<div class="abs frame sh-light" style="left:470px;top:110px;width:560px;height:790px"><div class="abs paper poster" style="inset:12px;background-image:url({P}/poster-campaign-a2.png)"></div><div class="abs reflex"></div></div>
<div class="abs label"><b>Carry the light across.</b><span>Campaign poster · A2 420 × 594 mm · 2026</span></div>
<div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 40%,transparent 60%,rgba(40,30,10,.22) 100%)"></div>
{cap('Poster on a gallery wall', 'campaign poster, A2, black frame, museum glass · <span class="pt"></span>10_MARKETING_COLLATERAL / Posters')}
''', css='''
.frame { background: #111113; box-shadow: inset 0 0 0 1px #2a2a2d, 0 2px 2px rgba(0,0,0,.2), 0 30px 60px rgba(40,30,10,.35), 0 80px 120px rgba(40,30,10,.25); }
.poster { }
.reflex { inset: 12px; background: linear-gradient(112deg, rgba(255,255,255,0) 38%, rgba(255,255,255,.10) 46%, rgba(255,255,255,0) 54%), linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,0) 30%); }
.label { left: 1090px; top: 470px; width: 220px; padding: 14px 16px; background: #FBF8F2; border: 1px solid rgba(40,30,10,.12); box-shadow: 0 4px 10px rgba(40,30,10,.12); font: 400 11px/1.5 var(--font-text); color: #665F55; }
.label b { display: block; font: 600 13px/1.3 var(--font-heading); color: #1A1816; margin-bottom: 4px; }
''', light=True)

# 27 — trifold brochure standing
scene('marketing-trifold-brochure-standing', M, 'Brochure · A4 trifold standing, inside spread behind', ['10 Brochures A4 trifold outside + inside (panels, trim crop)'], f'''
<div class="abs surf-plaster" style="inset:0"></div>
<div class="abs sweep"></div>
<div class="abs persp" style="inset:0;perspective:2600px">
  <div class="abs p3d" style="left:120px;top:40px;width:1000px;height:560px;transform:rotateX(50deg) rotateZ(-8deg);transform-origin:50% 100%">
    <div class="abs paper fl sh-light" style="left:0;top:0;width:330px;height:560px;background-image:url({P}/trifold-in-1.png)"></div>
    <div class="abs paper fl sh-light" style="left:330px;top:0;width:323px;height:560px;background-image:url({P}/trifold-in-2.png)"></div>
    <div class="abs paper fl sh-light" style="left:653px;top:0;width:330px;height:560px;background-image:url({P}/trifold-in-3.png)"></div>
  </div>
  <div class="abs p3d z" style="left:720px;top:250px;width:300px;height:636px">
    <div class="abs paper panel p3 sh-light" style="background-image:url({P}/trifold-out-3.png)">
      <div class="abs paper panel p2" style="background-image:url({P}/trifold-out-2.png)">
        <div class="abs paper panel p1" style="background-image:url({P}/trifold-out-1.png)"></div>
      </div>
    </div>
  </div>
</div>
<div class="abs shadow" style="left:520px;top:870px;width:620px;height:60px"></div>
{cap('Trifold brochure', 'A4 trifold 297 × 210 mm, panels 99 / 98 / 100 · front cover standing, inside spread open behind · <span class="pt"></span>10_MARKETING_COLLATERAL / Brochures')}
''', css='''
.fl { border-radius: 2px; } .fl::after { content: ""; position: absolute; inset: 0; background: linear-gradient(118deg, rgba(255,255,255,.14), rgba(255,255,255,0) 40%, rgba(40,30,10,.06) 100%); }
.z { transform: rotateY(-22deg) rotateX(-4deg); }
.panel { width: 300px; height: 636px; left: 0; top: 0; transform-origin: 0 50%; border-radius: 2px; }
.p3 { transform: rotateY(0deg); }
.p2 { left: -296px; width: 296px; transform-origin: 100% 50%; transform: rotateY(62deg); box-shadow: 0 30px 60px rgba(40,30,10,.3); }
.p2::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.08), rgba(0,0,0,.35)); }
.p1 { left: -299px; width: 299px; transform-origin: 100% 50%; transform: rotateY(-66deg); }
.p1::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.5), rgba(0,0,0,.18)); }
.shadow { background: radial-gradient(50% 50% at 50% 50%, rgba(40,30,10,.35), transparent 70%); filter: blur(8px); }
''', light=True)

# 28 — roll-up banner at an event entrance
scene('marketing-rollup-banner-entrance', M, 'Roll-up banner · at an event entrance', ['10 Events exhibition roll-up 850 × 2000 mm (1:5)'], f'''
<div class="abs" style="inset:0;background:linear-gradient(180deg,#0a0a0b,#161618 55%,#1c1c1e 78%,#0a0a0b 78.2%,#050506 100%)"></div>
<div class="abs tex-grain"></div>
<div class="abs door" style="left:170px;top:60px;width:520px;height:720px"></div>
<div class="abs" style="left:170px;top:60px;width:520px;height:720px;border-radius:260px 260px 0 0;background:radial-gradient(70% 60% at 50% 60%,rgba(233,178,90,.42),rgba(233,178,90,.08) 60%,rgba(0,0,0,0) 100%)"></div>
<div class="abs spill" style="left:60px;top:778px;width:760px;height:222px"></div>
<div class="abs pole" style="left:1039px;top:88px"></div>
<div class="abs paper banner sh-dark" style="left:875px;top:70px;width:330px;height:776px;background-image:url({P}/sanzeed-exhibition-rollup--850x2000mm-1-5.png)"></div>
<div class="abs cassette" style="left:830px;top:770px;width:420px;height:30px"></div>
<div class="abs refl" style="left:875px;top:782px;width:330px;height:220px;background:url({P}/sanzeed-exhibition-rollup--850x2000mm-1-5.png) center 90% / 100% auto;transform:scaleY(-1);opacity:.18;filter:blur(2px);-webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 90%);mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 90%)"></div>
<div class="abs vig"></div>
{cap('Roll-up banner', '850 × 2000 mm roll-up, bottom 200 mm in the cassette · at the doorway · <span class="pt"></span>10_MARKETING_COLLATERAL / Events')}
''', css='''
.door { border-radius: 260px 260px 0 0; background: linear-gradient(180deg, #fbf3e4, #e9b25a 60%, #6a4d1c); box-shadow: 0 0 0 16px #0d0d0f, 0 0 0 18px #2a2a2d, 0 0 120px rgba(233,178,90,.35); opacity: .9; }
.door::after { content: ""; position: absolute; inset: 0; border-radius: 260px 260px 0 0; background: linear-gradient(180deg, rgba(255,255,255,.4), rgba(0,0,0,0) 40%, rgba(0,0,0,.55) 100%); }
.spill { background: radial-gradient(50% 60% at 50% 0, rgba(233,178,90,.35), rgba(233,178,90,0) 70%); }
.banner { background-size: 100% auto; background-position: top; overflow: hidden; height: 700px; border-radius: 2px; }
.banner::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(0,0,0,.22), rgba(255,255,255,.06) 45%, rgba(0,0,0,.22)); }
.pole { width: 4px; height: 700px; background: linear-gradient(90deg, #55555a, #c0c0c6, #55555a); }
.cassette { border-radius: 15px; background: linear-gradient(180deg, #6a6a70, #c9c9ce 30%, #55555a 70%, #2a2a2d); box-shadow: 0 10px 30px rgba(0,0,0,.7); }
.cassette::before, .cassette::after { content: ""; position: absolute; top: 2px; width: 26px; height: 26px; border-radius: 50%; background: radial-gradient(circle at 40% 35%, #d9d9de, #4a4a50); }
.cassette::before { left: -6px; } .cassette::after { right: -6px; }
''')
SCENES[-1]['body'] = SCENES[-1]['body'].replace(f'{P}/sanzeed-exhibition-rollup--850x2000mm-1-5.png', f'{MKT}/Events/sanzeed-exhibition-rollup--850x2000mm-1-5.png')

# 29 — door plate + wayfinding on a museum wall (composite)
scene('marketing-door-plate-wayfinding-museum-wall', M, 'Signage · door plate and wayfinding on a museum wall', ['10 Signage door plate 300 × 100 + arrow plate (trim crop)', '06 Prime Minister Museum corridor (approved image)'], f'''
<div class="abs" style="inset:0;background:#000"></div>
<img class="abs" src="{P}/photo-prime-minister-museum-corridor.jpg" alt="Prime Minister Museum corridor" style="left:-258px;top:0;width:1780px;height:1000px;max-width:none;object-fit:cover">
<div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,.25) 45%,rgba(0,0,0,.05) 100%),linear-gradient(180deg,rgba(0,0,0,.25),rgba(0,0,0,0) 30%,rgba(0,0,0,.45) 100%)"></div>
<div class="abs persp" style="inset:0;perspective:1500px;perspective-origin:62% 50%">
  <div class="abs p3d wall" style="left:-80px;top:-300px;width:760px;height:1600px;transform:rotateY(46deg)">
    <div class="abs plate sh-dark" style="left:290px;top:690px;width:400px;height:133px;background-image:url({P}/door-plate.png)"></div>
    <div class="abs plate sh-dark" style="left:290px;top:850px;width:400px;height:133px;background-image:url({P}/wayfinding-ahead.png)"></div>
  </div>
</div>
<div class="abs" style="left:520px;top:0;width:260px;height:1000px;background:linear-gradient(90deg,rgba(0,0,0,.55),rgba(0,0,0,0))"></div>
<div class="abs label"><b>Prime Minister Museum</b><span>New Delhi</span></div>
<div class="abs vig soft"></div>
{cap('Door plate and wayfinding', '300 × 100 mm plates, Gallery Black, on the near wall · composite into the approved image · <span class="pt"></span>10_MARKETING_COLLATERAL / Signage')}
''', css='''
.wall { transform-origin: 0 50%; background: linear-gradient(90deg, #232326 0%, #1a1a1c 50%, #111113 100%); box-shadow: 40px 0 80px rgba(0,0,0,.6); }
.wall::before { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(255,255,255,.015) 0 1px, transparent 1px 6px); }
.wall::after { content: ""; position: absolute; right: 0; top: 0; bottom: 0; width: 10px; background: #2d2d31; }
.plate { background-size: 100% 100%; border-radius: 2px; box-shadow: 0 1px 0 rgba(255,255,255,.12), 0 10px 20px rgba(0,0,0,.7), 0 2px 4px rgba(0,0,0,.6); }
.label { right: 48px; top: 60px; text-align: right; font: 400 13px/1.5 var(--font-text); color: #A1A1A6; }
.label b { display: block; font: 600 14px/1.4 var(--font-heading); color: #F5F5F7; }
''')

# 30 — totem in a lobby (composite)
scene('marketing-totem-lobby', M, 'Signage · totem in a museum lobby', ['10 Signage totem 600 × 1800 mm (1:10)', '00/06 Prime Minister Museum lobby (case image)'], f'''
<div class="abs" style="inset:0;background:#000"></div>
<img class="abs" src="{P}/photo-prime-minister-museum-lobby.jpg" alt="Prime Minister Museum lobby" style="left:-278px;top:0;width:1780px;height:1000px;max-width:none;object-fit:cover">
<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.1) 40%,rgba(0,0,0,.5) 100%),radial-gradient(40% 60% at 68% 60%,rgba(0,0,0,.45),transparent 70%)"></div>
<div class="abs persp" style="inset:0;perspective:2000px;perspective-origin:50% 45%">
  <div class="abs p3d totemwrap" style="left:880px;top:200px;width:246px;height:738px;transform:rotateY(-16deg)">
    <div class="abs totem" style="inset:0;background-image:url({MKT}/Signage/sanzeed-totem--600x1800mm-1-10.png)"></div>
    <div class="abs side"></div>
  </div>
</div>
<div class="abs refl" style="left:880px;top:938px;width:246px;height:62px;background:url({MKT}/Signage/sanzeed-totem--600x1800mm-1-10.png) center bottom / 100% auto no-repeat;transform:scaleY(-1) skewX(16deg);opacity:.35;filter:blur(1.5px);-webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent);mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent)"></div>
<div class="abs ground" style="left:800px;top:905px;width:420px;height:90px"></div>
<div class="abs label"><b>Prime Minister Museum</b><span>New Delhi</span></div>
<div class="abs vig soft"></div>
{cap('Totem in a lobby', '600 × 1800 mm freestanding totem, vertical lockup and directory · composite into the case image · <span class="pt"></span>10_MARKETING_COLLATERAL / Signage')}
''', css='''
.totem { background-size: 100% 100%; box-shadow: 0 0 0 1px #2a2a2d, 0 40px 80px rgba(0,0,0,.7); }
.totem::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, rgba(255,255,255,.08), rgba(255,255,255,0) 40%, rgba(0,0,0,.25) 100%); }
.side { left: 246px; top: 0; width: 40px; height: 738px; background: linear-gradient(90deg, #202023, #0a0a0b); transform-origin: 0 50%; transform: rotateY(90deg); }
.ground { background: radial-gradient(50% 50% at 50% 50%, rgba(0,0,0,.65), transparent 70%); filter: blur(6px); }
.label { left: 48px; top: 60px; font: 400 13px/1.5 var(--font-text); color: #A1A1A6; }
.label b { display: block; font: 600 14px/1.4 var(--font-heading); color: #F5F5F7; }
''')

# 31 — backdrop at the G20-style show (composite)
scene('marketing-backdrop-g20-show', M, 'Event backdrop · LED wall at the G20-style show', ['10 Events backdrop 3000 × 2400 mm (1:10)', '06 G20 LED Show (approved image)'], f'''
<div class="abs" style="inset:0;background:#000"></div>
<img class="abs" src="{P}/photo-g20-led-show.jpg" alt="G20 LED Show hall" style="left:-280px;top:0;width:1780px;height:1000px;max-width:none;object-fit:cover">
<div class="abs" style="inset:0;background:linear-gradient(90deg,rgba(0,0,0,.1) 40%,rgba(0,0,0,.55) 100%),linear-gradient(180deg,rgba(0,0,0,.3),rgba(0,0,0,0) 35%,rgba(0,0,0,.5) 100%)"></div>
<div class="abs persp" style="inset:0;perspective:1800px;perspective-origin:45% 50%">
  <div class="abs p3d wallwrap" style="left:880px;top:290px;width:520px;height:416px;transform:rotateY(8deg)">
    <div class="abs led" style="inset:0;background-image:url({MKT}/Events/sanzeed-event-backdrop--3000x2400mm-1-10.png)"></div>
    <div class="abs ledframe"></div>
    <div class="abs plinth"></div>
  </div>
</div>
<div class="abs ground" style="left:850px;top:704px;width:560px;height:30px"></div>
<div class="abs refl" style="left:876px;top:724px;width:500px;height:190px;background:url({MKT}/Events/sanzeed-event-backdrop--3000x2400mm-1-10.png) center bottom / 100% auto no-repeat;transform:scaleY(-1) skewY(-1.2deg);opacity:.24;filter:blur(3px);-webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 80%);mask-image:linear-gradient(0deg,rgba(0,0,0,.9),transparent 80%)"></div>
<div class="abs glow" style="left:740px;top:640px;width:800px;height:260px"></div>
<div class="abs label"><b>G20 LED Show</b><span>Gujarat</span></div>
<div class="abs vig soft"></div>
{cap('Event backdrop', '3000 × 2400 mm LED backdrop, wordmark 1800 mm wide · composite into the approved image · <span class="pt"></span>10_MARKETING_COLLATERAL / Events')}
''', css='''
.wallwrap { transform-origin: 0 50%; }
.led { background-size: 100% 100%; box-shadow: 0 0 60px rgba(233,178,90,.18), 0 40px 90px rgba(0,0,0,.7); }
.led::after { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(0,0,0,.08) 0 1px, transparent 1px 3px), linear-gradient(90deg, rgba(255,255,255,.05), rgba(0,0,0,0) 50%, rgba(0,0,0,.2)); }
.ledframe { inset: -8px; border: 8px solid #0d0d0f; box-shadow: 0 0 0 1px #2a2a2d; }
.glow { background: radial-gradient(50% 50% at 50% 50%, rgba(233,178,90,.14), transparent 70%); }
.ground { background: radial-gradient(50% 50% at 50% 50%, rgba(0,0,0,.92), transparent 74%); filter: blur(4px); }
.plinth { left: -10px; right: -10px; bottom: -24px; height: 16px; background: linear-gradient(180deg, #2a2a2d, #0d0d0f 60%, #050506); box-shadow: 0 1px 0 rgba(255,255,255,.06) inset, 0 6px 10px rgba(0,0,0,.7); }
.label { left: 48px; top: 60px; font: 400 13px/1.5 var(--font-text); color: #A1A1A6; }
.label b { display: block; font: 600 14px/1.4 var(--font-heading); color: #F5F5F7; }
''')

# 32 — flyer in a stylised hand
scene('marketing-flyer-in-hand', M, 'Flyer · A5 flyer in a stylised hand', ['10 Flyers A5 two-sided front (trim crop)'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-420px;opacity:.75"></div>
<div class="abs tex-grain"></div>
<svg class="abs" viewBox="0 0 1500 1000" width="1500" height="1000" style="left:0;top:0">
  <defs><linearGradient id="hand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a2a2d"/><stop offset="1" stop-color="#121214"/></linearGradient></defs>
  <g fill="url(#hand)" stroke="#3a3a3e" stroke-width="2.5" stroke-linejoin="round">
    <!-- fingers, wrapped behind the flyer; only the knuckles show past its right edge -->
    <rect x="830" y="560" width="72" height="300" rx="36" transform="rotate(-58 866 710)"/>
    <rect x="860" y="610" width="72" height="300" rx="36" transform="rotate(-56 896 760)"/>
    <rect x="890" y="662" width="70" height="290" rx="35" transform="rotate(-54 925 807)"/>
    <rect x="915" y="716" width="64" height="260" rx="32" transform="rotate(-52 947 846)"/>
    <!-- palm and wrist -->
    <path d="M 900 1000 L 915 880 C 925 830 960 800 1010 790 C 1070 780 1140 800 1180 850 C 1215 895 1230 950 1235 1000 Z"/>
  </g>
</svg>
<div class="abs paper flyer sh-dark" style="left:560px;top:150px;width:420px;height:595px;background-image:url({P}/flyer-a5-front.png);transform:rotate(7deg)"></div>
<svg class="abs" viewBox="0 0 1500 1000" width="1500" height="1000" style="left:0;top:0">
  <g fill="url(#hand)" stroke="#3a3a3e" stroke-width="2.5" stroke-linejoin="round">
    <!-- thumb, over the flyer -->
    <path d="M 960 905 C 935 860 905 820 868 782 C 835 748 808 712 790 684 C 777 664 782 640 800 632 C 820 624 840 636 854 658 C 882 698 912 735 946 772 C 982 810 1005 855 1015 905 Z"/>
  </g>
  <path d="M 795 690 C 840 745 890 795 946 850" fill="none" stroke="rgba(0,0,0,.5)" stroke-width="30" stroke-linecap="round" style="filter:blur(12px)"/>
</svg>
<div class="abs vig"></div>
{cap('Flyer in hand', 'A5 two-sided flyer, front · <span class="pt"></span>10_MARKETING_COLLATERAL / Flyers')}
''', css='''
.flyer { border-radius: 2px; }
.flyer::after { content: ""; position: absolute; inset: 0; background: linear-gradient(160deg, rgba(255,255,255,.08), rgba(255,255,255,0) 40%, rgba(0,0,0,0) 70%, rgba(0,0,0,.2) 100%); }
''')

# 33 — social ad on a phone
scene('marketing-social-ad-phone', M, 'Social ad · 1080 × 1080 ad in a feed, on a phone', ['10 Campaign_Templates ad 1080 × 1080 @ 2×', '08 Instagram profile 1024 (dark)'], f'''
<div class="abs surf-night" style="inset:0"></div>
<div class="abs lamp" style="left:-50px;top:-420px;opacity:.6"></div>
<div class="abs tex-grain"></div>
{phone(f'''<div class="feed">{status()}
  <div class="top"><b>Home</b><span class="ic"><i></i><i></i></span></div>
  <div class="post">
    <div class="ph"><img src="{SOC}/Instagram/sanzeed-ig-profile--dark-1024x1024.png" alt=""><div><b>sanzeed</b><span>Sponsored</span></div><em>···</em></div>
    <img class="ad" src="{MKT}/Campaign_Templates/sanzeed-ad--1080x1080@2x.png" alt="Sanzeed social ad">
    <div class="cta"><span>See the work</span><i></i></div>
    <div class="acts"><i></i><i></i><i></i></div>
    <p><b>sanzeed</b> Experiential design you can walk into. Museums, experience centres, pavilions and projection shows — one vision, from the brief to opening night. sanzeed.com</p>
  </div>
</div>''', 'left:539px;top:60px')}
<div class="abs vig"></div>
{cap('Social ad in the feed', 'square ad 1080 × 1080 with the campaign line · <span class="pt"></span>10_MARKETING_COLLATERAL / Campaign_Templates')}
''', css='''
.feed { position: absolute; inset: 0; background: #000; color: #F5F5F7; font-family: var(--font-text); }
.feed .top { position: absolute; left: 0; right: 0; top: 62px; height: 40px; display: flex; align-items: center; justify-content: space-between; padding: 0 18px; font: 600 20px/1 var(--font-heading); }
.feed .ic { display: flex; gap: 16px; } .feed .ic i { width: 22px; height: 22px; border: 2px solid #F5F5F7; border-radius: 6px; display: block; } .feed .ic i:first-child { border-radius: 50%; }
.feed .post { position: absolute; left: 0; right: 0; top: 118px; }
.feed .ph { display: flex; align-items: center; gap: 10px; padding: 0 14px 10px; } .feed .ph img { width: 34px; height: 34px; border-radius: 50%; }
.feed .ph b { display: block; font: 600 13px/1.2 var(--font-heading); } .feed .ph span { font: 400 11px/1.2 var(--font-text); color: #A1A1A6; } .feed .ph em { margin-left: auto; font-style: normal; letter-spacing: 1px; }
.feed .ad { width: 390px; display: block; }
.feed .cta { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px; border-bottom: 1px solid rgba(255,255,255,.08); font: 500 14px/1 var(--font-text); color: #F5F5F7; }
.feed .cta i { width: 8px; height: 8px; border-right: 2px solid #F5F5F7; border-top: 2px solid #F5F5F7; transform: rotate(45deg); }
.feed .acts { display: flex; gap: 16px; padding: 12px 14px 8px; } .feed .acts i { width: 22px; height: 22px; border: 2px solid #F5F5F7; border-radius: 6px; display: block; } .feed .acts i:first-child { border-radius: 50% 50% 50% 50%; }
.feed p { margin: 0; padding: 0 14px; font: 400 13px/1.45 var(--font-text); color: #F5F5F7; } .feed p b { font-weight: 600; }
''')

# 34 — lower third over the Ram Katha Show image, on a broadcast monitor
scene('marketing-lower-third-ram-katha', M, 'Lower third · over the Ram Katha Show, on a broadcast monitor', ['11 Lower_Thirds name lower third (source, hold frame at 2.9 s, alpha)', '00/06 Ram Katha Show stage (case image)'], f'''
<div class="abs" style="inset:0;background:linear-gradient(180deg,#0a0a0b 0%,#151517 60%,#1c1c1e 76%,#0a0a0b 76.2%,#050506 100%)"></div>
<div class="abs tex-grain"></div>
<div class="abs spk" style="left:120px;top:330px"></div><div class="abs spk" style="left:1300px;top:330px"></div>
<div class="abs monitor" style="left:210px;top:120px;width:1080px;height:640px"><div class="bezel"></div><div class="screen">
  <img class="img-cover" src="{P}/photo-ram-katha-show-stage.jpg" alt="Ram Katha Show, Ayodhya">
  <img class="img-cover abs" src="{P}/lower-third-name-hold-3840x2160.png" alt="Lower third: Sanzeed Mirza, Experiential Design Consultant" style="left:0;top:0">
  <div class="abs osd"><span>REC</span><span>TC 00:00:02:27</span><span>1920 × 1080 · 25p</span></div>
</div></div>
<div class="abs stand" style="left:700px;top:760px"></div>
<div class="abs desk" style="left:-100px;top:800px;width:1700px;height:200px"></div>
<div class="abs refl" style="left:226px;top:802px;width:1048px;height:160px;background:url({P}/photo-ram-katha-show-stage.jpg) center bottom / 100% auto no-repeat;transform:scaleY(-1);opacity:.18;filter:blur(5px);-webkit-mask-image:linear-gradient(0deg,rgba(0,0,0,.8),transparent 85%);mask-image:linear-gradient(0deg,rgba(0,0,0,.8),transparent 85%)"></div>
<div class="abs vig"></div>
{cap('Lower third', 'name + descriptor lower third over the Ram Katha Show (Ayodhya) · <span class="pt"></span>11_MOTION_GRAPHICS / Lower_Thirds')}
''', css='''
.osd { left: 24px; top: 20px; display: flex; gap: 18px; font: 500 12px/1 var(--font-text); color: rgba(245,245,247,.8); letter-spacing: .04em; }
.osd span:first-child { color: #D64540; }
.spk { width: 80px; height: 300px; border-radius: 6px; background: linear-gradient(90deg, #1c1c1e, #0d0d0f); box-shadow: 0 30px 60px rgba(0,0,0,.6), inset 0 0 0 1px #26262a; }
.spk::before { content: ""; position: absolute; left: 10px; top: 110px; width: 60px; height: 60px; border-radius: 50%; background: radial-gradient(circle at 50% 50%, #0a0a0b, #1c1c1e 60%, #0d0d0f); box-shadow: inset 0 0 0 1px #2a2a2d; }
.stand { width: 100px; height: 40px; background: #0d0d0f; border-radius: 0 0 10px 10px; box-shadow: inset 0 0 0 1px #26262a; }
.desk { background: linear-gradient(180deg, #232326, #111113 40%, #050506); transform: perspective(900px) rotateX(55deg); transform-origin: 50% 0; }
''')

# 35 — logo reveal frame on a cinema screen
seats = ''.join(f'<div class="row" style="top:{620 + i * 70}px;left:{-40 - i * 30}px;right:{-40 - i * 30}px;transform:scale({1 + i * .12});opacity:{1 - i * .05}">' + ''.join('<i></i>' for _ in range(22)) + '</div>' for i in range(5))
scene('marketing-logo-reveal-cinema-screen', M, 'Logo reveal · final frame on a cinema screen', ['11 Logo_Animations logo reveal, dark 1920 × 1080 (poster frame)'], f'''
<div class="abs" style="inset:0;background:#000"></div>
<div class="abs" style="left:0;right:0;top:0;height:700px;background:radial-gradient(60% 70% at 50% 45%,rgba(233,178,90,.10),rgba(255,255,255,.03) 50%,transparent 75%)"></div>
<div class="abs beam"></div>
<div class="abs screen" style="left:150px;top:80px;width:1200px;height:675px"><img class="img-cover" src="{MOT}/Logo_Animations/sanzeed-logo-reveal--dark-1920x1080--poster.jpg" alt="Logo reveal, final frame"></div>
<div class="abs" style="left:0;right:0;top:560px;height:440px;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.7) 40%,#000 100%)"></div>
{seats}
<div class="abs tex-grain" style="opacity:.4"></div>
{cap('Logo reveal on a cinema screen', '4 s logo reveal, final hold frame, 1920 × 1080 · <span class="pt"></span>11_MOTION_GRAPHICS / Logo_Animations')}
''', css='''
.screen { box-shadow: 0 0 0 2px #1a1a1c, 0 0 120px rgba(245,245,247,.08), 0 0 300px rgba(233,178,90,.08); }
.beam { left: 50%; top: -40px; width: 1200px; height: 700px; margin-left: -600px; background: linear-gradient(180deg, rgba(245,245,247,.05), rgba(245,245,247,0)); clip-path: polygon(48% 0, 52% 0, 100% 100%, 0 100%); opacity: .8; }
.row { position: absolute; display: flex; justify-content: center; gap: 14px; }
.row i { display: block; width: 52px; height: 60px; border-radius: 26px 26px 6px 6px; background: linear-gradient(180deg, #1c1c1e, #0a0a0b 70%); box-shadow: inset 0 2px 0 rgba(245,245,247,.08), 0 -10px 30px rgba(0,0,0,.6); flex: none; }
''')

# ----------------------------------------------------------------------------------------------------------------
# writers / renderers
# ----------------------------------------------------------------------------------------------------------------
def html_for(s):
    uses = '\n'.join(f'       - {u}' for u in s['uses'])
    return f'''<!doctype html>
<html lang="en" data-theme="{'light' if s['light'] else 'dark'}">
<head>
<meta charset="utf-8">
<title>{s['title']} — Sanzeed mockup</title>
<!--
  13_BRAND_MOCKUPS · {s['folder']} · sanzeed-mockup--{s['name']}
  Scene: {s['title']}
  Deliverables used (linked by relative path; nothing is redrawn):
{uses}
  Shared components: ../../_build/mockup.css (devices, surfaces, textures, shadows) → brand.css (tokens, fonts).
  Render (3000 × 2000): node ../../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in sanzeed-mockup--{s['name']}.html --out ../sanzeed-mockup--{s['name']}-3000w.png --width 1500 --height 1000 --scale 2 --wait 800
  Or rebuild everything: python3 ../../_build/build_mockups.py {s['name']}
  Generated by _build/build_mockups.py — edit the scene there (or edit this file directly and re-render it by hand).
-->
<link rel="stylesheet" href="../../_build/mockup.css">
<style>
{s['css'].strip()}
</style>
</head>
<body>
<div class="stage{' light' if s['light'] else ''}">
{s['body'].strip()}
</div>
</body>
</html>
'''

def write_css():
    with open(os.path.join(HERE, 'mockup.css'), 'w') as f: f.write(CSS.strip() + '\n')

def write_html(s):
    d = os.path.join(ROOT, s['folder'], 'src'); os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"sanzeed-mockup--{s['name']}.html")
    with open(path, 'w') as f: f.write(html_for(s))
    return path

def render(s):
    os.makedirs(TMP, exist_ok=True)
    src = write_html(s)
    png = os.path.join(TMP, f"{s['name']}.png")
    subprocess.run(['node', RENDER, '--in', src, '--out', png, '--width', '1500', '--height', '1000', '--scale', '2', '--wait', '2500'], check=True, capture_output=True)
    im = Image.open(png).convert('RGB')
    out = os.path.join(ROOT, s['folder'])
    im.save(os.path.join(out, f"sanzeed-mockup--{s['name']}-3000w.jpg"), quality=90, subsampling=0, optimize=True, progressive=True)
    im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(os.path.join(out, f"sanzeed-mockup--{s['name']}-1600w.jpg"), quality=88, optimize=True, progressive=True)
    print(f"rendered {s['folder']}/sanzeed-mockup--{s['name']}  {im.size[0]}x{im.size[1]}")

def contact_sheet():
    cells = ''
    for i, s in enumerate(SCENES):
        cells += f'''<figure><img src="../{s['folder']}/sanzeed-mockup--{s['name']}-1600w.jpg" alt=""><figcaption><span class="counter">{i+1:03d}</span><b>{s['title'].split(' · ')[0]}</b><span>{s['title'].split(' · ', 1)[1] if ' · ' in s['title'] else ''}</span></figcaption></figure>'''
    html = f'''<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8"><title>Sanzeed — brand mockups, contact sheet</title>
<link rel="stylesheet" href="../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
html, body {{ width: 1500px; background: #000; }}
.sheet {{ width: 1500px; padding: 56px 60px 48px; background: #000; color: var(--fg); box-sizing: border-box; }}
.hd {{ display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 36px; }}
.hd h1 {{ font: 300 56px/1.02 var(--font-display); font-variation-settings: "opsz" 144; letter-spacing: -.015em; margin: 10px 0 0; }}
.hd p {{ font: 400 13px/1.6 var(--font-text); color: var(--fg-3); text-align: right; }}
.grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 22px 18px; }}
figure {{ margin: 0; }} figure img {{ width: 100%; border-radius: 10px; display: block; border: 1px solid rgba(255,255,255,.08); }}
figcaption {{ margin-top: 9px; font: 400 11px/1.4 var(--font-text); color: var(--fg-3); }}
figcaption b {{ display: block; font: 600 12px/1.35 var(--font-heading); color: var(--fg); margin: 2px 0 1px; }}
figcaption .counter {{ font-size: 10px; }}
.ft {{ margin-top: 40px; border-top: 1px solid var(--line); padding-top: 14px; display: flex; justify-content: space-between; font: 400 12px/1.5 var(--font-text); color: var(--fg-3); }}
</style></head><body><div class="sheet">
<div class="hd"><div><div class="eyebrow">Brand mockups · 001 – {len(SCENES):03d}</div><h1>The identity, applied.</h1></div><p>{len(SCENES)} scenes · logo, stationery, digital, marketing<br>HTML + CSS sources in each folder's src/ · 3000 px and 1600 px JPG exports</p></div>
<div class="grid">{cells}</div>
<div class="ft"><span>Sanzeed Mirza · Experiential Design Consultant · sanzeed.com</span><span>13_BRAND_MOCKUPS / sanzeed-mockups-contact-sheet.png</span></div>
</div></body></html>'''
    src = os.path.join(HERE, 'contact-sheet.html')
    with open(src, 'w') as f: f.write(html)
    out = os.path.join(ROOT, 'sanzeed-mockups-contact-sheet.png')
    subprocess.run(['node', RENDER, '--in', src, '--out', out, '--width', '1500', '--height', '1000', '--scale', '2', '--full', '--wait', '900'], check=True, capture_output=True)
    print('contact sheet', Image.open(out).size)


def write_readme():
    def kb(path):
        n = os.path.getsize(path); return f'{n/1024:.0f} KB' if n < 1024*1024 else f'{n/1024/1024:.1f} MB'
    rows = ''
    for i, s in enumerate(SCENES):
        f = s['folder']; n = s['name']; src = f'{f}/src/sanzeed-mockup--{n}.html'
        big = os.path.join(ROOT, f, f'sanzeed-mockup--{n}-3000w.jpg'); web = os.path.join(ROOT, f, f'sanzeed-mockup--{n}-1600w.jpg')
        rows += f"| {i+1:03d} | {s['title']} | {'; '.join(s['uses'])} | `{src}` | `{f}/sanzeed-mockup--{n}-3000w.jpg` ({kb(big)}) · `…-1600w.jpg` ({kb(web)}) |\n"
    total = sum(os.path.getsize(os.path.join(d, x)) for d, _, fs in os.walk(ROOT) for x in fs)
    txt = f"""# 13_BRAND_MOCKUPS — the identity, applied

{len(SCENES)} premium application mockups of the finished Sanzeed identity, the way the agency shows it at final delivery:
logo finishes, stationery, digital surfaces and marketing applications. Every scene is built from the **real deliverables of the
other folders** — logos from `02_LOGO_SYSTEM`, textures from `05_GRAPHIC_ASSETS/Textures`, print pieces from `09_PRINT_STATIONERY`
and `10_MARKETING_COLLATERAL`, social from `08_SOCIAL_MEDIA`, share images / email / app icons from `07_WEBSITE_DIGITAL_ASSETS`,
the live site from `16_WEBSITE_IMPLEMENTATION`, motion frames from `11_MOTION_GRAPHICS`, photography from `06_PHOTOGRAPHY_ART_DIRECTION`
and `00_ORIGINAL_ASSETS_BACKUP`. Nothing is redrawn or restyled; the scenes only light, bend, reflect and place them.

**Logo.** Every scene carries the approved master logo (20 Nov 2026): the **refined original wordmark, option B** — the client's own
hand-drawn SANZEED with the hooked S, the swooping N, and a Z whose diagonal swoops like the N's right leg; **three gold points**
(A, Z, D), the Z point inside a thin ring that shows the background through it. The symbol is the refined, hooked S with its full stop;
the monogram is "SM." (on the ID-card reverse). All 35 scenes and their plates were regenerated from the rebuilt upstream folders on
20 Nov 2026. The masked finishes size their boxes to the production SVGs' proportions: wordmark 3692.52 × 519.33 (≈ 7.11 : 1),
symbol 603.82 × 519.33 (≈ 1.16 : 1).

| Folder | Contents |
|---|---|
| `Logo_Mockups/` | 7 scenes: blind deboss, gold foil, halo-lit signage, engraved brass plaque, window vinyl on a frosted door, app icon, favicon |
| `Stationery_Mockups/` | 9 scenes: cards fanned, cards flat lay, letterhead + envelope + card, proposal cover, ID card and lanyard, thank-you card, stamp impression, notepad, presentation folder |
| `Digital_Mockups/` | 9 scenes: website on a laptop (dark, light), website on a phone, Instagram profile, LinkedIn profile, email signature, link preview in chat, YouTube channel, presentation on a conference screen |
| `Marketing_Mockups/` | 10 scenes: A2 poster on a gallery wall, trifold, roll-up at an entrance, door plate + wayfinding (composite), totem in a lobby (composite), event backdrop at the G20-style show (composite), flyer in hand, social ad, lower third over the Ram Katha Show, logo reveal on a cinema screen |
| `sanzeed-mockups-contact-sheet.png` | all {len(SCENES)} scenes on one 3000 px sheet, numbered 001–{len(SCENES):03d} |
| `_build/` | `build_mockups.py` (the master), `mockup.css` (shared devices, surfaces, textures, shadows), `make_plates.py` + `plates/` (the deliverables re-rasterised at mockup resolution), `capture_site.js`, `contact-sheet.html` |

Each scene: **editable HTML + CSS source** in the folder's `src/` (1500 × 1000 CSS px, all brand tokens via `brand.css`), a **3000 × 2000 JPG q90** (`-3000w.jpg`) and a **1600 × 1067 web JPG** (`-1600w.jpg`). Folder total: **{total/1024/1024:.0f} MB**.

## How the scenes are made

* **One master.** `_build/build_mockups.py` holds every scene (markup + scene CSS) and writes the `src/*.html` files, renders them with
  the brand kit's `render.js` (Chromium, 2×), exports both JPGs, the contact sheet and this README. `python3 _build/build_mockups.py`
  rebuilds everything; `python3 _build/build_mockups.py cards-fanned` rebuilds the scenes whose name contains the filter; `--html-only`
  writes sources only; `--sheet` rebuilds the contact sheet. A source can also be edited by hand and re-rendered with the command in its
  header comment.
* **Materials and light** are CSS: 3-D perspective transforms (`perspective` / `rotateX` / `rotateY`, `preserve-3d`) for cards, pages,
  panels and the composited signage; layered `box-shadow` for contact and ambient shadows; gradients for light fall-off and the
  `sweep` of a window; reflections are mirrored copies under a gradient mask; the brand **grain**, **paper** and **lamp glow**
  textures come from `05_GRAPHIC_ASSETS/Textures`. The emboss, foil and engraving use the production logo SVGs from `02_LOGO_SYSTEM`
  as CSS masks (inlined as data URIs — Chromium will not load a `mask-image` from `file://`), filled with the paper colour, the
  `--sz-gradient-foil` gradient, or the ink of the engraving.
* **Devices and windows** (phone, laptop, tablet, monitor, browser, mail and chat windows) are drawn in `mockup.css` — generic chrome,
  no third-party branding. Screens show the real site captured at device pixel density (`capture_site.js`, 1440 × 900 @ 2× and
  390 × 844 @ 3×), the real social assets, the OG image, the email signature loaded live in an iframe.
* **Plates** (`_build/plates/`, built by `make_plates.py`): the delivered PDFs of the business cards, letterhead, envelopes, thank-you
  card, notepad, ID card, proposal, presentation and folder re-rasterised with `pdftoppm` at 160–600 dpi; previews that carry bleed
  cropped back to trim; the trifold cut into its six panels; the four composite photographs upscaled to 3000 px (Lanczos + unsharp);
  the lower-third hold frame rendered from its motion source with alpha. (The stamp impression masks with the outlined stamp SVG
  from `09_PRINT_STATIONERY/Stamp` directly.) Delete the old plates and re-run `python3 _build/make_plates.py` whenever an upstream
  deliverable changes, then `python3 _build/build_mockups.py`.
* **Composites into approved imagery** (door plate / wayfinding, totem, event backdrop) place the real sign on a plane whose perspective
  matches the photograph, under a veil that keeps the plate on ≥ 80 % black, with a wall label (Title · Place) in the corner.
* **Captions.** Every scene carries a small wall-label caption (scene · spec · source folder) at the bottom-left in the brand's caption
  style; delete the `.cap` div in the source for an uncaptioned export.

## Rules applied and verified

Every render was opened and checked: the wordmark shows the three gold points with the ringed Z and the hooked S; the logo variant matches its background (`full-colour-dark` on black, `full-colour-light` on
Plaster, `white` for the vinyl and backlit letters, `black` masks for the finishes (`wordmark-plain` for the blind deboss, so no points), `symbol` on the plaque / avatars, `monogram`
only on the ID-card reverse as delivered); clear space is kept; one gold accent per composition (the deliverable's own point, or the
lamp); Fraunces 300 renders as the light serif in every caption and UI; nothing clipped, no missing fonts, no placeholder boxes;
the only copy is confirmed copy from `01_BRAND_STRATEGY`, the deliverables themselves and the site's own `<title>` / `og:` meta;
no invented statistics (the Instagram and YouTube mock profiles show no follower or view counts).

## Mockup index

| # | Scene | Deliverable used | Source (editable) | Export |
|---|---|---|---|---|
{rows}
## Known limits

* The approved photographs exist only at 960 × 540 / 1600 × 900, so the three photo composites and the frosted-door backdrop are
  upscaled 1.9–3.1× and are deliberately softened under the veil; for press use, re-run `make_plates.py` with higher-resolution originals.
* The scenes are rendered raster scenes, not layered PSD/Figma mockup files; the HTML sources are the layered, editable equivalent
  (every object is a positioned element with its own transform and shadow).
* `brand.css` sets `img {{ max-width: 100% }}`; the full-bleed photographs (door plate, totem, event backdrop, frosted-door lobby) carry
  `max-width:none` so they cover the stage edge to edge. Door plate and totem keep their earlier photo registration (offset by the
  138 px the old capped `object-fit: cover` cropped), so their signs sit exactly as tuned; the event backdrop was re-staged as a
  near-frontal (8°) freestanding LED wall on a plinth, standing on the hall floor, with a contact shadow and floor reflection.
* Chromium paints very large CSS background images from a low-resolution decode, so plates are kept ≤ 3400 px on the long edge
  (the A2 poster plate is 1600 px wide, 1.5× what the scene shows).
"""
    with open(os.path.join(ROOT, 'README.md'), 'w') as f: f.write(txt)
    print('README.md written')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:]]
    write_css()
    if '--sheet' in args:
        contact_sheet(); write_readme(); sys.exit()
    if '--readme' in args:
        write_readme(); sys.exit()
    if '--html-only' in args:
        for s in SCENES: write_html(s)
        sys.exit()
    flt = [a for a in args if not a.startswith('--')]
    todo = [s for s in SCENES if not flt or any(f in s['name'] for f in flt)]
    for s in todo: render(s)
    if not flt:
        contact_sheet()
    write_readme()
