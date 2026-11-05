#!/usr/bin/env python3
"""Proposal template — DOCX. Cover: dark A4 page (wordmark + lamp, rendered from HTML as a 300-dpi image placed
behind editable white text). Then: The room · The one central story · Method · Scope · Timeline · Investment ·
Team · Terms · Next step. Sample text is confirmed copy from sanzeed.com; client fields are bracketed."""
import copy, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from docxlib import *
from docx.oxml import parse_xml
from PIL import Image

D = f'{OUT}/Proposals'
SRC = f'{D}/src'
AS = f'{SRC}/assets'
os.makedirs(AS, exist_ok=True)
LH = f'{OUT}/Letterheads/src/assets'
LOCKUP_PNG = f'{LH}/sanzeed-horizontal-descriptor--full-colour-light-300dpi.png'
WORDMARK_PNG = f'{LH}/sanzeed-primary-wordmark--full-colour-light-300dpi.png'

# ------------------------------------------------------------------ cover background (HTML → 300 dpi JPG)
COVER_HTML = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sanzeed — proposal cover background</title>
<link rel="stylesheet" href="../../../15_SOURCE_FILES/Project_Files/brand-kit/brand.css">
<style>
 html,body{{margin:0;background:#000}}
 .page{{position:relative;width:210mm;height:297mm;background:#000;overflow:hidden}}
 .lamp{{position:absolute;inset:0;background:radial-gradient(58% 44% at 50% 42%,rgba(233,178,90,.46) 0%,rgba(233,178,90,.11) 32%,rgba(0,0,0,0) 72%)}}
 .logo{{position:absolute;left:20mm;top:20mm;width:62mm;display:block}}
 .rule{{position:absolute;left:20mm;right:20mm;top:166mm;height:1px;background:rgba(255,255,255,.10)}}
</style></head><body>
<section class="page grain"><div class="lamp"></div>
<img class="logo" src="../../../02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg" alt="SANZEED">
<div class="rule"></div></section></body></html>'''
write(f'{SRC}/sanzeed-proposal-cover-background.html', COVER_HTML)
png = f'{AS}/sanzeed-proposal-cover-background.png'
render_html(f'{SRC}/sanzeed-proposal-cover-background.html', png, width=794, height=1123, scale=3.125, wait=800)
im = Image.open(png).convert('RGB').resize((2480, 3508), Image.LANCZOS)
COVER_JPG = f'{AS}/sanzeed-proposal-cover-background-300dpi.jpg'
im.save(COVER_JPG, quality=88, subsampling=0, dpi=(300, 300)); os.remove(png)


def add_background(doc, img, w_emu, h_emu):
    """Full-page picture anchored behind the text (wp:anchor behindDoc) — editable text sits on top."""
    p = doc.add_paragraph()
    para_fmt(p, after=0, line=1)
    run = p.add_run()
    shape = run.add_picture(img, width=w_emu, height=h_emu)
    inline = shape._inline
    docPr = copy.deepcopy(inline.docPr); frame = copy.deepcopy(inline.find(qn('wp:cNvGraphicFramePr'))); graphic = copy.deepcopy(inline.graphic)
    anchor = parse_xml(
        '<wp:anchor xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="0" behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/><wp:positionH relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionH>'
        '<wp:positionV relativeFrom="page"><wp:posOffset>0</wp:posOffset></wp:positionV>'
        f'<wp:extent cx="{int(w_emu)}" cy="{int(h_emu)}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/></wp:anchor>')
    anchor.append(docPr); anchor.append(frame); anchor.append(graphic)
    inline.getparent().replace(inline, anchor)
    return p


SERVICES = [
    ('01', 'Experiential Design & Creative Direction', 'One vision from brief to opening night: narrative, space, media and the team that builds it.'),
    ('02', 'Museum & Cultural Exhibition Planning', 'Galleries planned as a route, not a floor plan. Objects, stories and dwell time, in order.'),
    ('03', 'Immersive Storytelling & Narrative Architecture', 'The script comes first. Every room, screen and surface carries a line of it.'),
    ('04', 'Spatial Experience & Environmental Branding', 'Brands you can stand inside: pavilions, experience centres, thresholds and wayfinding.'),
    ('05', 'Event Production & Brand Activation', 'Shows, launches and tableaux where light and timing do the talking.'),
    ('06', 'Digital ↔ Physical Experience Integration', 'Projection, AR and VR, sensors and data brought into real rooms and real crowds.'),
    ('07', 'Cross-Functional Leadership & Mentorship', 'Designers, writers, architects, producers and technologists moved toward one outcome, calmly.'),
]
STEPS = [
    ('01', 'Discover', 'Immersion in the subject — its history, intent and audience — until the central story reveals itself.', 'A research deck and the one central story'),
    ('02', 'Direct', 'A unifying creative vision that aligns designers, architects, writers, producers and technologists toward one outcome.', 'A concept book and a walkthrough film'),
    ('03', 'Craft', 'Space, light, motion and interaction composed into environments that engage intellectually, emotionally and physically.', 'Detail drawings, media scripts and a prototype room'),
    ('04', 'Deliver', 'Concept to launch — balancing creative ambition with operational discipline. On scale, on story, on time.', 'A built, tested and opened experience'),
]


def h1(doc, txt):
    p = doc.add_paragraph(style='Heading 1'); add_point(p, txt); return p


def wall(doc, txt):
    return doc.add_paragraph(txt, style='Wall Label')


doc = Document()
brand_styles(doc)
# ---- section 1: cover
sec = page_setup(doc.sections[0], 'A4', margin_mm=0, header_mm=0, footer_mm=0, top_extra=0)
sec.top_margin = Mm(0); sec.bottom_margin = Mm(0); sec.left_margin = Mm(20); sec.right_margin = Mm(20)
sec.different_first_page_header_footer = False
add_background(doc, COVER_JPG, sec.page_width, sec.page_height)
GW = RGBColor(0xF5, 0xF5, 0xF7); SILVER = RGBColor(0xA1, 0xA1, 0xA6); LAMP = RGBColor(0xE9, 0xB2, 0x5A)
# push the text block to the lower part of the page
sp = doc.add_paragraph(); para_fmt(sp, before=0, after=0, line=1); set_run_font(sp.add_run(' '), size=1)
sp.paragraph_format.space_before = Mm(170)
p = doc.add_paragraph(style='Eyebrow'); para_fmt(p, after=8, line=1.2)
r = p.add_run('Proposal  ·  [Date]'); set_run_font(r, color=LAMP)
p = doc.add_paragraph(); para_fmt(p, after=10, line=1.04)
r = p.add_run('One vision, from the brief to opening '); set_run_font(r, name=F_DISPLAY, size=34, color=GW)
r = p.add_run('night.'); set_run_font(r, name=F_DISPLAY, size=34, color=LAMP)
p = doc.add_paragraph(); para_fmt(p, after=2, line=1.4)
r = p.add_run('Prepared for [Client]  ·  [Project / the room]'); set_run_font(r, name=F_HEAD, size=10.5, color=GW)
p = doc.add_paragraph(); para_fmt(p, after=0, line=1.4)
r = p.add_run('Sanzeed Mirza  ·  Experiential Design Consultant  ·  New Delhi  ·  sanzeed.com'); set_run_font(r, name=F_TEXT, size=8.5, color=SILVER)

# ---- section 2: body with the brand header/footer
# NB python-docx: add_section() re-uses the sentinel sectPr for the NEW last section and clones the old one
# into the cover, so re-fetch both sections afterwards rather than keeping the earlier object.
doc.add_section(WD_SECTION.NEW_PAGE)
cover, body = doc.sections[0], doc.sections[1]
page_setup(body, 'A4')
# the cover keeps its own, empty header and footer (not linked to the body's)
for hf in (cover.header, cover.footer):
    hf.is_linked_to_previous = False
    for p_ in hf.paragraphs:
        p_.text = ''
for hf in (body.header, body.footer, body.first_page_header, body.first_page_footer):
    hf.is_linked_to_previous = False
brand_header_footer(doc, body, LOCKUP_PNG, WORDMARK_PNG)

doc.add_paragraph('Proposal  ·  [Client]  ·  [Project]', style='Eyebrow')
p = doc.add_paragraph(style='Title'); add_point(p, 'The room')
doc.add_paragraph('Every environment begins as a question and ends as a memory. The path between is deliberate — equal parts strategy and craft, ambition and discipline. This proposal sets out the question I heard, the one story I think answers it, and the four steps that carry it to opening night.', style='Lead')
doc.add_paragraph('Heading 3', style='Heading 3').text = 'The brief, as I heard it'
doc.add_paragraph('[Restate the brief in two or three sentences: the building, the audiences, what must be true on opening day.]', style='Normal')
doc.add_paragraph('One museum for every Prime Minister of India since 1947, in New Delhi — a building that has to hold schoolchildren and heads of state on the same afternoon, and give each leader a room without turning the whole into a corridor of portraits.', style='Quote')
wall(doc, 'Example · Prime Minister Museum, New Delhi — replace with the client\'s brief.')

h1(doc, 'The one central story')
doc.add_paragraph('[The single line the whole experience carries. One sentence.]', style='Normal')
doc.add_paragraph('A corridor you walk in order.', style='Quote')
doc.add_paragraph('The spine of the museum is a single long passage under a tricolour canopy. Visitors meet one Prime Minister at a time, in sequence, so the building itself tells the story of the office before any gallery does. Portraits face you at eye level; the leaders\' own words sit beside them on the walls.', style='Normal')
wall(doc, 'Example · Prime Minister Museum — the idea in one paragraph, then what visitors do: "Visitors walk the whole line of leaders without a map, and come out knowing the order by heart."')

h1(doc, 'Method')
doc.add_paragraph('A method for the monumental. Four steps, each ending in a named deliverable; the next step begins once that deliverable is agreed.', style='Normal')
rows = [[f'Step {n}', name, desc, deliv] for n, name, desc, deliv in STEPS]
t = brand_table(doc, ['Step', 'Name', 'What happens', 'You receive'], rows, [16, 24, 76, 54])
for r_ in range(1, 5):
    for ci, fam, col in ((2, F_TEXT, SOOT), (3, F_TEXT, UMBER)):
        set_run_font(t.rows[r_].cells[ci].paragraphs[0].runs[0], name=fam, size=9, color=col)
    set_run_font(t.rows[r_].cells[0].paragraphs[0].runs[0], color=GOLDINK)
    set_run_font(t.rows[r_].cells[1].paragraphs[0].runs[0], name=F_HEAD, size=9.5)

h1(doc, 'Scope')
doc.add_paragraph('Between two points of light. A brief on one side, a visitor on the other. Seven ways to carry the light across — this project uses the ones ticked.', style='Normal')
for n, name, line in SERVICES:
    p = doc.add_paragraph(style='Normal'); para_fmt(p, after=5, line=1.4)
    p.paragraph_format.left_indent = Mm(12); p.paragraph_format.first_line_indent = Mm(-12)
    r = p.add_run(f'{n}\t'); set_run_font(r, name=F_DATA, size=9, color=GOLDINK, tnum=True)
    p.paragraph_format.tab_stops.add_tab_stop(Mm(12))
    r = p.add_run(name + '. '); set_run_font(r, name=F_HEAD, size=10)
    r = p.add_run(line); set_run_font(r, color=UMBER)
doc.add_paragraph('All seven, every time. Every room needs the whole list, held in one hand.', style='Quote')
doc.add_paragraph('Out of scope: [construction, fabrication, AV supply and site works are delivered by the client\'s appointed contractors under my direction — adjust per project].', style='Small')

h1(doc, 'Timeline')
doc.add_paragraph('[Dates to be agreed at confirmation. Durations below are fields, not estimates.]', style='Normal')
rows = [['01', 'Discover', '[n] weeks', 'Research deck and the one central story, presented in the building'],
        ['02', 'Direct', '[n] weeks', 'Concept book and walkthrough film'],
        ['03', 'Craft', '[n] weeks', 'Detail drawings, media scripts and a prototype room'],
        ['04', 'Deliver', '[n] weeks', 'Built, tested and opened experience — opening night [date]']]
t = brand_table(doc, ['Step', 'Name', 'Duration', 'Milestone'], rows, [14, 26, 26, 104])
for r_ in range(1, 5):
    set_run_font(t.rows[r_].cells[0].paragraphs[0].runs[0], color=GOLDINK)
    set_run_font(t.rows[r_].cells[1].paragraphs[0].runs[0], name=F_HEAD, size=9.5)
    set_run_font(t.rows[r_].cells[3].paragraphs[0].runs[0], name=F_TEXT, size=9, color=UMBER)

h1(doc, 'Investment')
doc.add_paragraph('Fees are quoted per step and invoiced on delivery of each step\'s deliverable, so you only ever commit to the next room. Projects fall into one of four bands; the figure for this project is in the attached quotation.', style='Normal')
rows = [['Under ₹25 lakh', '[Typical scope for this band]', ''],
        ['₹25 lakh – ₹1 crore', '[Typical scope for this band]', ''],
        ['₹1 – 5 crore', '[Typical scope for this band]', ''],
        ['Over ₹5 crore', '[Typical scope for this band]', ''],
        ['This project', '[Steps covered]', '₹ [Fee] + GST 18 %']]
t = brand_table(doc, ['Band', 'Scope', 'Fee'], rows, [40, 90, 40], aligns=['left', 'left', 'right'], total_rows=1)
for r_ in range(1, 6):
    set_run_font(t.rows[r_].cells[1].paragraphs[0].runs[0], name=F_TEXT, size=9, color=UMBER)
wall(doc, 'Bands follow the enquiry form on sanzeed.com. Amounts in Indian rupees, GST at 18 % shown separately on every invoice.')

h1(doc, 'Team')
p = doc.add_paragraph(style='Normal')
r = p.add_run('Sanzeed Mirza, Experiential Design Consultant. '); set_run_font(r, name=F_HEAD, size=10)
p.add_run('I\'m an experiential design consultant based in New Delhi, working with institutions and brands wherever the project is. Fifteen years in: first as a concept artist and VFX lead on films and animation, then eight years directing museums, experience centres, pavilions and shows. I lead the whole room — story, space, graphics, media and the team that builds it.')
rows = [['15+', 'Years of experience'], ['8+', 'Years experiential & museum'], ['90+', 'Projects directed'], ['60+', 'Museums & centres']]
t = doc.add_table(rows=2, cols=4)
for i, (n, l) in enumerate(rows):
    a = t.rows[0].cells[i]; b = t.rows[1].cells[i]
    pa = a.paragraphs[0]; pa.text = ''; para_fmt(pa, after=0, line=1)
    r = pa.add_run(n[:-1]); set_run_font(r, name=F_DISPLAY, size=30, color=SOOT, tnum=True)
    r = pa.add_run('+'); set_run_font(r, name=F_DISPLAY, size=30, color=OLDGOLD)
    set_cell_text(b, l, style='Wall Label', tnum=False)
    for c in (a, b):
        cell_borders(c, top='none', bottom='none', left='none', right='none'); cell_margins(c, top=80, bottom=20, left=0, right=80)
set_col_widths(t, [42.5] * 4)
doc.add_paragraph('Selected rooms: Prime Minister Museum, New Delhi · Ram Katha Show, Ayodhya · Buddha Park, Uttarakhand · Yuge Yugeen Bharat Museum · India Pavilion Expo 2025 (concept) · G20 Tree Show · RBI Museum, Mumbai · Army Museum Abu Dhabi · Dubai Police Control Center.', style='Small')
doc.add_paragraph('Specialists by step: [architect / exhibition fabricator / AV and projection integrator / show-control team — named per project and led under one direction].', style='Normal')

h1(doc, 'Terms')
for t_ in ['This proposal is valid until [Valid until].',
           'Fees exclude GST, charged at 18 %. Each step is quoted and invoiced separately.',
           'Payment schedule: [e.g. 50 % on confirmation of a step, 50 % on delivery of its deliverable].',
           'Expenses: [travel, site visits and production costs — state the basis].',
           'Intellectual property: [state the basis — concept and media scripts, drawings, films].',
           'Credits: the project may be shown in my portfolio after opening, with the client\'s approval of the images.']:
    p = doc.add_paragraph('·  ' + t_, style='Normal'); para_fmt(p, after=4, line=1.4)
    p.paragraph_format.left_indent = Mm(6); p.paragraph_format.first_line_indent = Mm(-6)

h1(doc, 'Next step')
p = doc.add_paragraph(style='Quote'); para_fmt(p, before=4, after=8, line=1.3)
r = p.add_run('Tell me about the room'); r2 = p.add_run('.'); set_run_font(r2, color=OLDGOLD)
doc.add_paragraph('A few lines are enough. The first conversation is always free; I reply within two working days, and if it is urgent, WhatsApp is fastest.', style='Normal')
kv_table(doc, [('Email', 'sanzeed@gmail.com'), ('Call / WhatsApp', '+91 7827051270'), ('Web', 'sanzeed.com'), ('LinkedIn', 'linkedin.com/in/sanzeed')], widths_mm=(40, 130))
p = doc.add_paragraph(style='Small'); para_fmt(p, before=16, after=0, line=1.3)
r = p.add_run('Sanzeed Mirza'); set_run_font(r, name=F_HEAD, size=9.5, color=SOOT)
p.add_run('  ·  Experiential Design Consultant  ·  New Delhi, India')
core_props(doc, 'Sanzeed Mirza — proposal template', 'Proposal')
DOCX = f'{SRC}/sanzeed-proposal-template.docx'
doc.save(DOCX)

# ---- exports
tmpd = tempfile.mkdtemp()
pdf = soffice_pdf(DOCX, tmpd)
shutil.move(pdf, f'{D}/sanzeed-proposal-template.pdf')
pages = pdf_pages_to_png(f'{D}/sanzeed-proposal-template.pdf', f'{tmpd}/p', dpi=110)
shutil.copy(pages[0], f'{D}/sanzeed-proposal-template--cover.png')
# two spreads: pages 2–3 and 4–5
for i, (a, b) in enumerate(((1, 2), (3, 4)), 1):
    if b < len(pages):
        A = Image.open(pages[a]); Bm = Image.open(pages[b])
        s = Image.new('RGB', (A.width + Bm.width + 6, A.height), '#D9D4C8'); s.paste(A, (0, 0)); s.paste(Bm, (A.width + 6, 0))
        s.save(f'{D}/sanzeed-proposal-template--spread-{i:02d}.png')
print('proposal pages:', len(pages))
print('proposals done')
