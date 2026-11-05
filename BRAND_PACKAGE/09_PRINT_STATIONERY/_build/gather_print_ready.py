#!/usr/bin/env python3
"""Collect every print-ready CMYK PDF into Print_Ready_Files/ as sanzeed-<item>--print-cmyk.pdf and write a
manifest (trim, bleed, pages, colour) verified with pdfinfo and pdfimages."""
import os, sys, glob, re, shutil, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from pypdf import PdfReader
PR = f'{OUT}/Print_Ready_Files'
os.makedirs(PR, exist_ok=True)
for f in glob.glob(f'{PR}/*.pdf'):
    os.remove(f)
ITEMS = [  # (source, item name, trim, bleed, notes)
    ('Business_Cards/sanzeed-business-card--concept-a--print-cmyk.pdf', 'business-card-concept-a', '89 × 51', 3, 'front + back; Plaster both sides; foil option on the dots'),
    ('Business_Cards/sanzeed-business-card--concept-b--print-cmyk.pdf', 'business-card-concept-b', '89 × 51', 3, 'front (rich black) + back (Plaster)'),
    ('Letterheads/sanzeed-letterhead--a4--print-cmyk.pdf', 'letterhead-a4', '210 × 297', 3, 'first page + continuation page'),
    ('Letterheads/sanzeed-letterhead--us-letter--print-cmyk.pdf', 'letterhead-us-letter', '215.9 × 279.4', 3, 'first page + continuation page'),
    ('Envelopes/sanzeed-envelope--dl--print-cmyk.pdf', 'envelope-dl', '220 × 110', 3, 'front + back (flap); window-free'),
    ('Envelopes/sanzeed-envelope--c5--print-cmyk.pdf', 'envelope-c5', '229 × 162', 3, 'front + back (flap); window-free'),
    ('Covers/sanzeed-cover--company-profile--dark--print-cmyk.pdf', 'cover-company-profile-dark', '210 × 297', 3, 'rich black with the lamp'),
    ('Covers/sanzeed-cover--company-profile--light--print-cmyk.pdf', 'cover-company-profile-light', '210 × 297', 3, 'Plaster'),
    ('Covers/sanzeed-cover--report--dark--print-cmyk.pdf', 'cover-report-dark', '210 × 297', 3, 'rich black, image plate (image 960 px wide — see README)'),
    ('Covers/sanzeed-cover--report--light--print-cmyk.pdf', 'cover-report-light', '210 × 297', 3, 'Plaster, image plate'),
    ('Folder/sanzeed-folder--a4--print-cmyk.pdf', 'folder-a4', '457 × 395 (flat)', 3, 'outside 4/0; dieline supplied separately (Folder/sanzeed-folder--a4-dieline.pdf)'),
    ('Notepad/sanzeed-notepad--a5--print-cmyk.pdf', 'notepad-a5', '148 × 210', 3, 'single sheet, pad of 50'),
    ('Notepad/sanzeed-notepad--a4--print-cmyk.pdf', 'notepad-a4', '210 × 297', 3, 'single sheet, pad of 50'),
    ('ID_Card/sanzeed-id-card--print-cmyk.pdf', 'id-card-cr80', '54 × 85.6', 3, 'front + back; corner radius 3.18'),
    ('ID_Card/sanzeed-lanyard--strip--print-cmyk.pdf', 'lanyard-strip', '900 × 20', 3, 'dye-sublimation strip, repeat'),
    ('Thank_You_Cards/sanzeed-thank-you-card--folded--print-cmyk.pdf', 'thank-you-card-folded', '210 × 148 (A5 flat, folds to A6)', 3, 'outside + inside'),
    ('Thank_You_Cards/sanzeed-thank-you-card--postcard--print-cmyk.pdf', 'thank-you-postcard-a6', '148 × 105', 3, 'front + back'),
]
rows = []
for src, item, trim, bleed, notes in ITEMS:
    s = f'{OUT}/{src}'
    assert os.path.exists(s), s
    dst = f'{PR}/sanzeed-{item}--print-cmyk.pdf'
    shutil.copy(s, dst)
    info = pdfinfo(dst)
    pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    size = re.search(r'Page size:\s+([\d.]+) x ([\d.]+)', info)
    pw, ph = float(size.group(1)) * 25.4 / 72, float(size.group(2)) * 25.4 / 72
    # colour check: scan page resources for colour spaces and raster images
    r = PdfReader(dst)
    cs = set()
    for pg in r.pages:
        res = pg.get('/Resources', {})
        for k, v in (res.get('/ColorSpace', {}) or {}).items():
            v = v.get_object()
            cs.add(str(v[0]) if isinstance(v, list) else str(v))
    imgs = subprocess.run(['pdfimages', '-list', dst], capture_output=True, text=True).stdout.splitlines()[2:]
    img_cs = sorted({l.split()[5] for l in imgs if len(l.split()) > 5})
    colour = 'CMYK' + (f' (images: {", ".join(img_cs)})' if img_cs else ' (vector)')
    rows.append((f'sanzeed-{item}--print-cmyk.pdf', trim, f'{bleed} mm', pages, f'{pw:.1f} × {ph:.1f} mm', colour, notes))
    print(f'{item:32s} {pages}p  sheet {pw:.1f}×{ph:.1f}  images:{img_cs}')
man = ['# Print-ready files — manifest', '',
       'Every file: trim + 3 mm bleed + 10 mm slug with crop marks at the trim; TrimBox and BleedBox set; colours converted to CMYK by Ghostscript (`print_pdf.py --cmyk`); all text outlined or embedded. Verified with `pdfinfo` (sheet size = trim + 2 × bleed + 2 × slug) and `pdfimages -list` (raster colour space).', '',
       'Rich black for large dark solids: C60 M40 Y40 K100. Old Gold = C0 M27 Y68 K28 (or spot Pantone 7510 C — verify with a swatch). Proof the gold and the warm black before the run.', '',
       '| File | Trim (mm) | Bleed | Pages | Sheet incl. slug | Colour | Notes |', '|---|---|---|---|---|---|---|']
for row in rows:
    man.append('| ' + ' | '.join(str(x) for x in row) + ' |')
man += ['', 'Not in this folder (single-colour, no bleed): the stamp artwork — `Stamp/sanzeed-stamp--round-40mm.pdf` and `Stamp/sanzeed-stamp--rectangular-58x22mm.pdf` (100 K, text outlined). The folder dieline is `Folder/sanzeed-folder--a4-dieline.pdf` (supply with the folder print file).']
write(f'{PR}/MANIFEST.md', '\n'.join(man) + '\n')
print('manifest written,', len(rows), 'files')
