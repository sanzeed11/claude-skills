#!/usr/bin/env python3
"""Letterheads — A4 and US Letter; first page + continuation page.
SVG print masters (with bleed) + DOCX templates (python-docx) filled with a sample letter."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from docxlib import *
from PIL import Image

D = f'{OUT}/Letterheads'
SRC = f'{D}/src'
AS = f'{SRC}/assets'
os.makedirs(AS, exist_ok=True)
BL = 3
M = 20  # margin mm

# ---------------------------------------------------------------- header logo PNGs (300 dpi metadata)
def logo_png_300(variant, colour, width_mm, out, scale=2):
    """Transparent PNG whose DPI tag is 300 and whose pixel size covers width_mm at 300 dpi × scale."""
    px = int(round(width_mm / 25.4 * 300 * scale))
    tmp = out + '.tmp.png'
    inkscape([f'{LOGO_DIR}/sanzeed-{variant}--{colour}.svg', '--export-type=png', f'--export-width={px}', f'--export-filename={tmp}'])
    im = Image.open(tmp); im.save(out, dpi=(300 * scale, 300 * scale)); os.remove(tmp)
    return out

LOCKUP_PNG = logo_png_300('horizontal-descriptor', 'full-colour-light', 56, f'{AS}/sanzeed-horizontal-descriptor--full-colour-light-300dpi.png')
WORDMARK_PNG = logo_png_300('primary-wordmark', 'full-colour-light', 30, f'{AS}/sanzeed-primary-wordmark--full-colour-light-300dpi.png')
# signature (ink) for the letter, 300 dpi at 34 mm
sig_px = int(round(34 / 25.4 * 600))
inkscape([f'{SIG_DIR}/sanzeed-signature--ink.svg', '--export-type=png', f'--export-width={sig_px}', f'--export-filename={AS}/sanzeed-signature--ink-300dpi.png'])
im = Image.open(f'{AS}/sanzeed-signature--ink-300dpi.png'); im.save(f'{AS}/sanzeed-signature--ink-300dpi.png', dpi=(600, 600))
SIG_PNG = f'{AS}/sanzeed-signature--ink-300dpi.png'

# ---------------------------------------------------------------- SVG print masters
def master(tw, th, first=True, title=''):
    W, H = tw + 2 * BL, th + 2 * BL
    a = []
    if first:
        g, lh, cap = logo('horizontal-descriptor', 'full-colour-light', 56, BL + M, BL + M, 'lockup')
    else:
        g, lh, cap = logo('primary-wordmark', 'full-colour-light', 30, BL + M, BL + M, 'wordmark')
    a.append(g)
    # footer: hairline, contact line left, short line right ending on the point
    fy = BL + th - M
    a.append(hairline(BL + M, fy - 6.5, BL + tw - M, fy - 6.5))
    a.append(text(BL + M, fy - 2.2, 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  +91 7827051270  ·  sanzeed@gmail.com', 7, fill=C['umber']))
    a.append(text(BL + M, fy + 1.6, 'sanzeed.com  ·  linkedin.com/in/sanzeed  ·  New Delhi, India', 7, fill=C['umber']))
    a.append(text_point(BL + tw - M, fy + 0.2, SHORT, 9, C['oldgold'], fill=C['soot'], anchor='end', opsz=36))
    paper = rect(0, 0, W, H, fill=C['plaster'])
    return svg_doc(W, H, paper, '\n'.join(a), guides(tw, th, BL, M, label=True), title=title,
                   desc=('First page: horizontal-descriptor lockup 56 mm at the 20 mm margins.' if first else
                         'Continuation page: primary wordmark 30 mm at the 20 mm margins.') + ' Footer: contact line and the short line.')

SIZES = {'a4': (210, 297), 'us-letter': (215.9, 279.4)}
for key, (tw, th) in SIZES.items():
    write(f'{SRC}/sanzeed-letterhead--{key}-first.svg', master(tw, th, True, f'Sanzeed letterhead — {key.upper()} first page'))
    write(f'{SRC}/sanzeed-letterhead--{key}-continuation.svg', master(tw, th, False, f'Sanzeed letterhead — {key.upper()} continuation page'))

# ---------------------------------------------------------------- DOCX template + sample letter
LETTER = [
    ('Eyebrow', 'Letter'),
    ('Title', 'The room, after our first conversation'),
    ('Normal', 'Thank you for Thursday. Twenty minutes was enough to see the room.'),
    ('Normal', 'You have one building and three audiences: schoolchildren in the morning, families at the weekend and your trustees on the same afternoon. The brief asks for a museum. What I heard was a route — one spine that every visitor walks in order, with galleries off it that change their mood with the subject.'),
    ('Normal', 'Here is what I propose as a first step.'),
    ('Heading 3', 'Step 01 — Discover'),
    ('Normal', 'Immersion in the subject, the site and the audience, until the one central story shows itself. You receive a research deck and the one central story, presented in your building. Nothing is designed until that line is agreed.'),
    ('Heading 3', 'Step 02 — Direct'),
    ('Normal', 'If the story holds, direction follows: a unifying creative vision that aligns designers, architects, writers, producers and technologists toward one outcome. You receive a concept book and a walkthrough film that the whole team can build from.'),
    ('Normal', 'I have attached the quotation for Step 01. The first conversation was free; this is the first thing I would charge for, and it is the only decision I would ask you to make now.'),
    ('Heading 2', 'What happens next.'),
    ('Normal', 'Once you confirm, I spend the first week on site and in your archive. At the end of the step we meet in the building, walk the route together and agree the one central story on the wall before anything is drawn.'),
    ('Normal', 'I reply within two working days. If it is urgent, WhatsApp is fastest.'),
    ('Normal', 'With warm regards,'),
]


def build_docx(size, out):
    doc = Document()
    brand_styles(doc)
    sec = page_setup(doc.sections[0], size)
    brand_header_footer(doc, sec, LOCKUP_PNG, WORDMARK_PNG)
    core_props(doc, 'Sanzeed Mirza — letterhead', 'Letter template')
    # date and addressee
    p = doc.add_paragraph('5 November 2026', style='Small'); para_fmt(p, after=14, line=1.3)
    for line in ['[Recipient name]', '[Role, Organisation]', '[Postal address]']:
        p = doc.add_paragraph(line, style='Normal'); para_fmt(p, after=0, line=1.3)
    para_fmt(p, after=16, line=1.3)
    p = doc.add_paragraph('Dear [Recipient name],'); para_fmt(p, after=10, line=1.45)
    for style, txt in LETTER:
        if style == 'Title':
            p = doc.add_paragraph(style='Title'); add_point(p, txt)
        else:
            p = doc.add_paragraph(txt, style=style)
    # signature block
    p = doc.add_paragraph(); para_fmt(p, before=6, after=0, line=1)
    p.add_run().add_picture(SIG_PNG, width=Mm(34))
    p = doc.add_paragraph(); para_fmt(p, after=0, line=1.3)
    r = p.add_run('Sanzeed Mirza'); set_run_font(r, name=F_HEAD, size=10)
    p = doc.add_paragraph('Experiential Design Consultant', style='Small'); para_fmt(p, after=10, line=1.3)
    p = doc.add_paragraph('Enclosed: Quotation [Quotation no.] — Step 01, Discover.', style='Small')
    doc.save(out)
    return out


A4_DOCX = build_docx('A4', f'{SRC}/sanzeed-letterhead--a4.docx')
LT_DOCX = build_docx('Letter', f'{SRC}/sanzeed-letterhead--us-letter.docx')

# ---------------------------------------------------------------- exports
tmpd = tempfile.mkdtemp()
for key, (tw, th) in SIZES.items():
    pages = []
    for part in ('first', 'continuation'):
        pdf = f'{tmpd}/{key}-{part}.pdf'
        svg_to_pdf(f'{SRC}/sanzeed-letterhead--{key}-{part}.svg', pdf)
        pages.append(pdf)
    bleed_pdf = f'{tmpd}/{key}-bleed.pdf'
    merge_pdfs(pages, bleed_pdf)
    crop_pdf(bleed_pdf, f'{D}/sanzeed-letterhead--{key}.pdf', BL)
    print_ready(bleed_pdf, f'{D}/sanzeed-letterhead--{key}--print-cmyk.pdf', tw, th, BL)
    pdf_to_png(f'{D}/sanzeed-letterhead--{key}.pdf', f'{D}/sanzeed-letterhead--{key}-first.png', dpi=150, page=1)
    pdf_to_png(f'{D}/sanzeed-letterhead--{key}.pdf', f'{D}/sanzeed-letterhead--{key}-continuation.png', dpi=150, page=2)
for docx_path, key in ((A4_DOCX, 'a4'), (LT_DOCX, 'us-letter')):
    pdf = soffice_pdf(docx_path, tmpd)
    shutil.move(pdf, f'{D}/sanzeed-letterhead--{key}-sample-letter.pdf')
    for p in pdf_pages_to_png(f'{D}/sanzeed-letterhead--{key}-sample-letter.pdf', f'{D}/sanzeed-letterhead--{key}-sample-letter', dpi=110):
        pass
print('letterheads done')
