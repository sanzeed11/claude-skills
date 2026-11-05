#!/usr/bin/env python3
"""Official document template — generic DOCX: cover block (eyebrow, title, reference fields), numbered
headings, body, and a two-party signature block using the signature mark PNG."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from docxlib import *

D = f'{OUT}/Official_Document'
os.makedirs(f'{D}/src', exist_ok=True)
LH = f'{OUT}/Letterheads/src/assets'  # header/footer logo PNGs are shared with the letterhead
LOCKUP_PNG = f'{LH}/sanzeed-horizontal-descriptor--full-colour-light-300dpi.png'
WORDMARK_PNG = f'{LH}/sanzeed-primary-wordmark--full-colour-light-300dpi.png'
SIG_PNG = f'{LH}/sanzeed-signature--ink-300dpi.png'

doc = Document()
brand_styles(doc)
sec = page_setup(doc.sections[0], 'A4')
brand_header_footer(doc, sec, LOCKUP_PNG, WORDMARK_PNG)
core_props(doc, 'Sanzeed Mirza — official document template', 'Official document')

# cover block
doc.add_paragraph('Official document  ·  [Document type]', style='Eyebrow')
p = doc.add_paragraph(style='Title'); add_point(p, 'Statement of work')
doc.add_paragraph('[One line on what this document records — the engagement, the step, the decision.]', style='Lead')
t = doc.add_table(rows=2, cols=4)
for i, (k, v) in enumerate([('Reference', '[Ref no.]'), ('Date', '[Date]'), ('Client', '[Client]'), ('Project', '[Project / the room]')]):
    a, b = t.rows[0].cells[i], t.rows[1].cells[i]
    set_cell_text(a, k, style='Table Head', tnum=False); set_cell_text(b, v, style='Field', font=F_DATA, size=10)
    for c in (a, b):
        cell_borders(c, top='none', left='none', right='none', bottom='none'); cell_margins(c, top=40, bottom=40, left=0, right=80)
    cell_borders(a, top=(4, '1A1816')); cell_borders(b, bottom=(2, 'E3DED3'))
set_col_widths(t, [42.5] * 4)
doc.add_paragraph().paragraph_format.space_after = Pt(6)

def h1(txt):
    p = doc.add_paragraph(style='Heading 1'); add_point(p, txt); return p

h1('1. Purpose')
doc.add_paragraph('This document records what Sanzeed Mirza (Experiential Design Consultant, New Delhi) will do for [Client] on [Project], what each party receives, and how the work is approved. It follows the proposal dated [Date] and the quotation [Quotation no.].', style='Normal')
h1('2. Scope of work')
doc.add_paragraph('The work runs in four steps. Each step ends in a named deliverable; the next step begins once that deliverable is agreed in writing.', style='Normal')
for n, name, deliv in [('01', 'Discover', 'a research deck and the one central story'), ('02', 'Direct', 'a concept book and a walkthrough film'),
                       ('03', 'Craft', 'detail drawings, media scripts and a prototype room'), ('04', 'Deliver', 'a built, tested and opened experience')]:
    p = doc.add_paragraph(style='Normal'); para_fmt(p, after=4, line=1.4)
    p.paragraph_format.left_indent = Mm(14); p.paragraph_format.first_line_indent = Mm(-14); p.paragraph_format.tab_stops.add_tab_stop(Mm(14))
    r = p.add_run(f'Step {n}\t'); set_run_font(r, name=F_DATA, size=9, color=GOLDINK, tnum=True)
    r = p.add_run(f'{name}. '); set_run_font(r, name=F_HEAD, size=10)
    p.add_run(f'You receive {deliv}.')
doc.add_paragraph('Steps covered by this document: [01 · 02 · 03 · 04 — strike out those not included].', style='Small')
h1('3. Deliverables and approvals')
doc.add_paragraph('Heading 3', style='Heading 3').text = 'What is delivered'
doc.add_paragraph('[List the files, drawings, films and rooms the client receives at each step, with the format of each.]', style='Normal')
doc.add_paragraph('Heading 3', style='Heading 3').text = 'How approval works'
doc.add_paragraph('Each deliverable is presented in person where possible and approved in writing by [Client approver]. Comments are gathered into one round per deliverable; a second round is included, further rounds are quoted.', style='Normal')
h1('4. Responsibilities')
rows = [['Sanzeed Mirza', 'Story, space, graphics, media and show direction; leading the specialists; presenting each deliverable.'],
        ['[Client]', 'Access to the site, archive and stakeholders; one named approver; decisions within [n] working days.'],
        ['[Contractors]', 'Fabrication, AV supply, construction and site works under Sanzeed Mirza\'s direction.']]
t = brand_table(doc, ['Party', 'Responsible for'], rows, [44, 126])
for r_ in range(1, 4):
    set_run_font(t.rows[r_].cells[0].paragraphs[0].runs[0], name=F_HEAD, size=9.5)
    set_run_font(t.rows[r_].cells[1].paragraphs[0].runs[0], name=F_TEXT, size=9)
h1('5. Fees and terms')
doc.add_paragraph('Fees are those of quotation [Quotation no.]: ₹ [Fee] + GST 18 %, invoiced per step on delivery. Payment schedule: [e.g. 50 % on confirmation of a step, 50 % on delivery]. Expenses: [basis]. Intellectual property: [basis]. Either party may end the engagement at the close of a step with [n] days\' written notice; work delivered to that point is paid for.', style='Normal')
h1('6. Signatures')
doc.add_paragraph('Signed in two copies, one for each party.', style='Normal')
t = doc.add_table(rows=1, cols=2)
L, R = t.rows[0].cells
for c in (L, R):
    cell_borders(c, top='none', bottom='none', left='none', right='none'); cell_margins(c, top=120, bottom=60, left=0, right=200)
p = L.paragraphs[0]; p.text = ''; para_fmt(p, after=0, line=1); p.add_run().add_picture(SIG_PNG, width=Mm(34))
for cell, lines_ in ((L, [('Sanzeed Mirza', True), ('Experiential Design Consultant', False), ('New Delhi, India', False), ('Date: [Date]', False)]),
                     (R, [(' ', False), (' ', False), ('[Name]', True), ('[Role], [Client]', False), ('Date: [Date]', False)])):
    first = cell is R
    for i, (txt, strong) in enumerate(lines_):
        q = cell.add_paragraph(style='Field') if not (first and i == 0) else cell.paragraphs[0]
        q.text = ''; para_fmt(q, after=0, line=1.35)
        if first and i == 1:
            # signing line
            ppr = q._p.get_or_add_pPr(); bdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
            b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '4'); b.set(qn('w:space'), '1'); b.set(qn('w:color'), '1A1816'); bdr.append(b); ppr.append(bdr)
            q.paragraph_format.space_before = Mm(10)
        r = q.add_run(txt); set_run_font(r, name=F_HEAD if strong else F_TEXT, size=10 if strong else 9.5, color=SOOT if strong else UMBER)
set_col_widths(t, [85, 85])
DOCX = f'{D}/src/sanzeed-official-document-template.docx'
doc.save(DOCX)
tmpd = tempfile.mkdtemp()
pdf = soffice_pdf(DOCX, tmpd); shutil.move(pdf, f'{D}/sanzeed-official-document-template.pdf')
pdf_pages_to_png(f'{D}/sanzeed-official-document-template.pdf', f'{D}/sanzeed-official-document-template', dpi=110)
print('official document pages:', pdfinfo(f'{D}/sanzeed-official-document-template.pdf').split('Pages:')[1].split('\n')[0].strip())
