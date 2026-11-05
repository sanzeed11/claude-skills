#!/usr/bin/env python3
"""
build_icons.py — editable master for the Sanzeed icon set.

  python3 build_icons.py        # writes svg/ (one file per icon, stroke=currentColor), sanzeed-icons-sprite.svg,
                                # png/{dark,light}/{48,96}/, icons.html and sanzeed-icons-sheet.png

Grammar: 24 px grid, 1.5 px stroke, round caps and round joins, no fills except the brand "point"
(a filled dot, r 1.75 — the gold point when the context allows one accent; otherwise it takes the ink).
Icons are drawn as path data below; every icon is one <svg viewBox="0 0 24 24"> with stroke="currentColor",
so on the web they take the text colour. PNGs are exported in dark ink (Gallery White #F5F5F7, for black)
and light ink (Soot #1A1816, for Plaster) at 48 and 96 px. Add an icon: add a line to ICONS, re-run.
"""
import sys, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / '_build')); import szlib as sz

P = lambda d: f'<path d="{d}"/>'
C = lambda cx, cy, r: f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
PT = lambda cx, cy, r=1.75: f'<circle class="pt" cx="{cx}" cy="{cy}" r="{r}" fill="currentColor" stroke="none"/>'
R = lambda x, y, w, h, rx=2: f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'

ICONS = {
  # ---- contact
  'mail':      ('contact', R(3, 5, 18, 14) + P('M3 7l9 6 9-6')),
  'phone':     ('contact', P('M5 4h3l2 5-2.4 1.4a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z')),
  'whatsapp':  ('contact', P('M12 3a9 9 0 0 0-7.7 13.6L3 21l4.5-1.2A9 9 0 1 0 12 3z') + P('M9 8.5l1.3 1.4-.6 1.2a5.5 5.5 0 0 0 3.2 3.2l1.2-.6 1.4 1.3-.7 1.2c-3.7-.4-6.5-3.2-6.9-6.9z')),
  'linkedin':  ('contact', R(3, 3, 18, 18, 3) + P('M7.5 10.5V17M7.5 7.5v.01M11.5 17v-6.5M11.5 13.5a2.25 2.25 0 0 1 4.5 0V17')),
  'location':  ('contact', P('M12 21s-7-5.6-7-11a7 7 0 0 1 14 0c0 5.4-7 11-7 11z') + C(12, 10, 2.5)),
  'calendar':  ('contact', R(3, 5, 18, 16) + P('M3 10h18M8 3v4M16 3v4')),
  'clock':     ('contact', C(12, 12, 9) + P('M12 7v5l3 2')),
  'globe':     ('contact', C(12, 12, 9) + P('M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z')),
  # ---- ui
  'arrow-left':   ('ui', P('M20 12H4M11 5l-7 7 7 7')),
  'arrow-right':  ('ui', P('M4 12h16M13 5l7 7-7 7')),
  'arrow-up':     ('ui', P('M12 20V4M5 11l7-7 7 7')),
  'arrow-down':   ('ui', P('M12 4v16M5 13l7 7 7-7')),
  'chevron-left': ('ui', P('M15 5l-7 7 7 7')),
  'chevron-right':('ui', P('M9 5l7 7-7 7')),
  'chevron-up':   ('ui', P('M5 15l7-7 7 7')),
  'chevron-down': ('ui', P('M5 9l7 7 7-7')),
  'close':     ('ui', P('M6 6l12 12M18 6L6 18')),
  'menu':      ('ui', P('M4 7h16M4 12h16M4 17h16')),
  'search':    ('ui', C(11, 11, 7) + P('M20 20l-4-4')),
  'filter':    ('ui', P('M4 6h16M7 12h10M10 18h4')),
  'grid':      ('ui', R(4, 4, 6.5, 6.5, 1.5) + R(13.5, 4, 6.5, 6.5, 1.5) + R(4, 13.5, 6.5, 6.5, 1.5) + R(13.5, 13.5, 6.5, 6.5, 1.5)),
  'list':      ('ui', P('M9 6h12M9 12h12M9 18h12M4.5 6h.01M4.5 12h.01M4.5 18h.01')),
  'play':      ('ui', P('M8 5.5v13l10.5-6.5z')),
  'pause':     ('ui', P('M8 5v14M16 5v14')),
  'sun':       ('ui', C(12, 12, 4) + P('M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4')),
  'moon':      ('ui', P('M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z')),
  'external-link': ('ui', P('M14 4h6v6M20 4l-9 9M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5')),
  'download':  ('ui', P('M12 4v12M6 11l6 6 6-6M4 20h16')),
  'upload':    ('ui', P('M12 16V4M6 9l6-6 6 6M4 20h16')),
  'check':     ('ui', P('M5 12.5l5 5 9-11')),
  'info':      ('ui', C(12, 12, 9) + P('M12 11v5M12 8v.01')),
  'warning':   ('ui', P('M10.3 4.5L2.6 18a2 2 0 0 0 1.7 3h15.4a2 2 0 0 0 1.7-3L13.7 4.5a2 2 0 0 0-3.4 0zM12 10v4M12 17.5v.01')),
  'error':     ('ui', C(12, 12, 9) + P('M9 9l6 6M15 9l-6 6')),
  'plus':      ('ui', P('M12 5v14M5 12h14')),
  'minus':     ('ui', P('M5 12h14')),
  'copy':      ('ui', R(9, 9, 12, 12) + P('M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1')),
  'share':     ('ui', C(18, 5, 2.5) + C(6, 12, 2.5) + C(18, 19, 2.5) + P('M8.2 10.8l7.6-4.5M8.2 13.2l7.6 4.5')),
  'zoom-in':   ('ui', C(11, 11, 7) + P('M20 20l-4-4M11 8v6M8 11h6')),
  'zoom-out':  ('ui', C(11, 11, 7) + P('M20 20l-4-4M8 11h6')),
  # ---- domain
  'museum':    ('domain', P('M3 9l9-5 9 5M4 9h16M6.5 9v8M11 9v8M15.5 9v8M20 9v8M3 20h18M3 17h18')),
  'pavilion':  ('domain', P('M2 10c3-5.3 17-5.3 20 0M5 9.6V20M19 9.6V20M12 8v12M3 20h18')),
  'projection':('domain', R(2, 8, 13, 8) + C(8.5, 12, 2.2) + P('M15 10l6-2.5M15 14l6 2.5M21 7.5v9')),
  'light-beam':('domain', PT(5, 5, 2) + P('M7.2 6.6L16.5 15') + P('M12.5 17.5a4.5 2 0 1 0 9 0 4.5 2 0 1 0-9 0')),
  'route':     ('domain', f'<path d="M3 18c3-8 6-8 9 0s6 8 9 0" stroke-dasharray="0 3.2"/>' + PT(3, 18, 1.6) + PT(21, 18, 1.6) + PT(12, 18, 1.6)),
  'doorway':   ('domain', P('M6 21V10a6 6 0 0 1 12 0v11M3 21h18')),
  'stage':     ('domain', P('M4 15.5a8 3 0 0 1 16 0M4 15.5v3a8 3 0 0 0 16 0v-3') + PT(12, 7, 2) + P('M12 10v2')),
  'screen':    ('domain', R(3, 4, 18, 12) + P('M8 20h8M12 16v4')),
  'ar-vr':     ('domain', P('M3 9a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-3.5l-1.7-2h-3.6l-1.7 2H5a2 2 0 0 1-2-2z') + C(8.5, 12, 1.5) + C(15.5, 12, 1.5)),
  'team':      ('domain', C(9, 7, 3.5) + P('M3 20v-1.5a4.5 4.5 0 0 1 4.5-4.5h3a4.5 4.5 0 0 1 4.5 4.5V20M16 3.6a3.5 3.5 0 0 1 0 6.8M21 20v-1.5a4.5 4.5 0 0 0-3-4.2')),
  'script':    ('domain', P('M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8zM14 3v5h5M9 13h6M9 17h4')),
  'drawing':   ('domain', P('M17 3l4 4L8 20H4v-4zM14 6l4 4')),
  'film':      ('domain', P('M3 8h18v12H3zM3 8l2-4h14l2 4M8 4l-1.5 4M13 4l-1.5 4M18 4l-1.5 4')),
  'award':     ('domain', C(12, 9, 5.5) + P('M9 13.5L7 21l5-2 5 2-2-7.5')),
  'book':      ('domain', P('M4 19.5A2.5 2.5 0 0 1 6.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z')),
}
INKS = {'dark': '#F5F5F7', 'light': '#1A1816'}

def icon_svg(name, body, colour='currentColor'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{colour}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="{name}"><title>{name}</title>{body}</svg>\n')

def main():
    (HERE / 'svg').mkdir(exist_ok=True)
    for ink in INKS:
        for size in (48, 96): (HERE / 'png' / ink / str(size)).mkdir(parents=True, exist_ok=True)
    symbols = []
    for name, (group, body) in ICONS.items():
        sz.write(HERE / 'svg' / f'sanzeed-icon-{name}.svg', icon_svg(name, body))
        symbols.append(f'<symbol id="icon-{name}" viewBox="0 0 24 24">{body}</symbol>')
        for ink, col in INKS.items():
            b = body.replace('currentColor', col)
            tmp = HERE / '_tmp.svg'; tmp.write_text(icon_svg(name, b, col))
            for size in (48, 96):
                sz.svg_to_png(tmp, HERE / 'png' / ink / str(size) / f'sanzeed-icon-{name}--{ink}-{size}.png', size, size)
            tmp.unlink()
    sprite = ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">\n'
              '<!-- Sanzeed icon sprite. Inline this file once, then: <svg class="icon"><use href="#icon-mail"/></svg> -->\n' + '\n'.join(symbols) + '\n</svg>\n')
    sz.write(HERE / 'sanzeed-icons-sprite.svg', sprite)
    # ---- preview sheet
    def cells(ink):
        out = []
        for group in ('contact', 'ui', 'domain'):
            out.append(f'<h2 class="eyebrow">{group} · {sum(1 for n in ICONS if ICONS[n][0]==group)} icons</h2><div class="grid">')
            for name, (g, body) in ICONS.items():
                if g != group: continue
                out.append(f'<figure><svg class="icon" viewBox="0 0 24 24"><use href="#icon-{name}"/></svg><figcaption>{name}</figcaption></figure>')
            out.append('</div>')
        return ''.join(out)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sanzeed — icon set</title>
<link rel="stylesheet" href="../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
body{{margin:0;width:1920px;font-family:"Inter"}} .half{{padding:56px 64px 48px}} .dark{{background:#000;color:#F5F5F7}} .light{{background:#F5F0E7;color:#1A1816}}
.head{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px}}
h1{{font:300 40px/1.1 "Fraunces";font-variation-settings:"opsz" 72,"SOFT" 30;letter-spacing:-.01em}} .dark h1 .lit{{color:#E9B25A}} .light h1 .lit{{color:#B8863B}}
.eyebrow{{font:600 12px/1 "Inter Tight";letter-spacing:.12em;text-transform:uppercase;margin:32px 0 16px}} .dark .eyebrow{{color:#E9B25A}} .light .eyebrow{{color:#8A6124}}
.grid{{display:grid;grid-template-columns:repeat(16,1fr);gap:14px 10px}} figure{{margin:0;text-align:center}}
.icon{{width:48px;height:48px;stroke:currentColor;fill:none;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;margin:0 auto}}
figcaption{{font:400 11px/1.3 "Inter";color:#808086;margin-top:6px}} .light figcaption{{color:#6D665C}}
.spec{{font:400 13px/1.5 "Inter";color:#808086}} .light .spec{{color:#665F55}}
</style></head><body>
{sprite.replace('style="display:none"', 'style="position:absolute;width:0;height:0"')}
<section class="half dark"><div class="head"><h1>{len(ICONS)} icons, one <span class="lit">line.</span></h1><div class="spec">24 px grid · 1.5 px stroke · round caps and joins · dark ink Gallery White</div></div>{cells('dark')}</section>
<section class="half light"><div class="head"><h1>The same set, on <span class="lit">Plaster.</span></h1><div class="spec">light ink Soot · the point may take Old Gold when it is the only accent</div></div>{cells('light')}</section>
</body></html>'''
    sz.write(HERE / 'icons.html', html)
    sz.render_html(HERE / 'icons.html', HERE / 'sanzeed-icons-sheet.png', 1920, 1200, scale=1, full=True)
    print(len(ICONS), 'icons written')

if __name__ == '__main__': main()
