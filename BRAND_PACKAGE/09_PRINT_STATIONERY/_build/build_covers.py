#!/usr/bin/env python3
"""Covers — company profile + report, dark + light. HTML master (Chromium) → 4-page bleed PDF →
one trim PDF, one print-ready CMYK PDF and one PNG per cover."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from pypdf import PdfReader, PdfWriter

D = f'{OUT}/Covers'
SRC = f'{D}/src'
NAMES = ['company-profile--dark', 'company-profile--light', 'report--dark', 'report--light']
tmpd = tempfile.mkdtemp()
all_pdf = f'{tmpd}/covers-bleed.pdf'
render_html(f'{SRC}/sanzeed-covers.html', all_pdf, pdf=True, size='216x303', wait=900)
r = PdfReader(all_pdf)
assert len(r.pages) == 4, len(r.pages)
for i, name in enumerate(NAMES):
    w = PdfWriter(); w.add_page(r.pages[i]); bleed = f'{tmpd}/{name}-bleed.pdf'; w.write(bleed)
    crop_pdf(bleed, f'{D}/sanzeed-cover--{name}.pdf', 3)
    print_ready(bleed, f'{D}/sanzeed-cover--{name}--print-cmyk.pdf', 210, 297, 3)
    pdf_to_png(f'{D}/sanzeed-cover--{name}.pdf', f'{D}/sanzeed-cover--{name}.png', dpi=120)
    print(name, pdfinfo(f'{D}/sanzeed-cover--{name}.pdf').split('Page size:')[1].split('\n')[0].strip(), f'{size_mb(f"{D}/sanzeed-cover--{name}--print-cmyk.pdf"):.1f} MB print')
print('covers done')
