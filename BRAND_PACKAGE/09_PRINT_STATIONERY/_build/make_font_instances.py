#!/usr/bin/env python3
"""Static optical-size instances of the Fraunces variable font (Light 300, SOFT 30, WONK 0) so that
Inkscape — which ignores CSS font-variation-settings — can honour the brand's opsz rule
(144 ≥ 36 pt, 72 for 18–36 pt, 36 below). Installed to ~/.fonts/brand-instances for rendering and
shipped in _build/fonts for anyone editing the SVG masters. SIL OFL 1.1 (same licence as the source)."""
import os, shutil, subprocess
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
SRC = '/home/user/claude-skills/BRAND_PACKAGE/04_TYPOGRAPHY/Font_Files/Fraunces'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
INST = os.path.expanduser('~/.fonts/brand-instances')
def rename(font, family, style):
    name = font['name']
    full = f'{family} {style}'
    ps = (family + '-' + style).replace(' ', '')
    for rec in list(name.names):
        nid = rec.nameID
        if nid in (1, 16): name.setName(family, nid, rec.platformID, rec.platEncID, rec.langID)
        elif nid in (2, 17): name.setName(style, nid, rec.platformID, rec.platEncID, rec.langID)
        elif nid == 4: name.setName(full, nid, rec.platformID, rec.platEncID, rec.langID)
        elif nid == 6: name.setName(ps, nid, rec.platformID, rec.platEncID, rec.langID)
        elif nid == 3: name.setName(f'{full};sanzeed-instance', nid, rec.platformID, rec.platEncID, rec.langID)
    font['OS/2'].usWeightClass = 300
    # fsSelection: clear bold/regular bits; keep italic bit as-is
    font['OS/2'].fsSelection &= ~(1 << 5 | 1 << 6)
for opsz in (36, 72):
    for src, style in (('Fraunces[SOFT,WONK,opsz,wght].ttf', 'Light'), ('Fraunces-Italic[SOFT,WONK,opsz,wght].ttf', 'Light Italic')):
        f = TTFont(f'{SRC}/{src}')
        inst = instantiateVariableFont(f, {'opsz': opsz, 'wght': 300, 'SOFT': 30, 'WONK': 0}, inplace=False, updateFontNames=False)
        fam = f'Fraunces {opsz}pt'
        rename(inst, fam, style)
        out = f'{OUT}/{fam.replace(" ", "")}-{style.replace(" ", "")}.ttf'
        inst.save(out)
        shutil.copy(out, INST)
        print('wrote', out)
shutil.copy(f'{SRC}/OFL.txt', f'{OUT}/OFL.txt')
subprocess.run(['fc-cache', '-f', INST], check=True)
print(subprocess.run(['fc-list', ':family=Fraunces 36pt'], capture_output=True, text=True).stdout)
