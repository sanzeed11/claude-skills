#!/usr/bin/env python3
"""Invoice and quotation templates — A4 DOCX (python-docx) with brand tables (Inter Tight, tabular numerals).
Example rows are the four method steps; every figure the client must supply is a bracketed field."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from szlib import *
from docxlib import *

LH = f'{OUT}/Letterheads/src/assets'
LOCKUP_PNG = f'{LH}/sanzeed-horizontal-descriptor--full-colour-light-300dpi.png'
WORDMARK_PNG = f'{LH}/sanzeed-primary-wordmark--full-colour-light-300dpi.png'

STEPS = [
    ('01', 'Discover', 'Immersion in the subject, the site and the audience, until the central story reveals itself.', 'Research deck + the one central story'),
    ('02', 'Direct', 'A unifying creative vision that aligns designers, architects, writers, producers and technologists.', 'Concept book + walkthrough film'),
    ('03', 'Craft', 'Space, light, motion and interaction composed into the environment.', 'Detail drawings, media scripts + prototype room'),
    ('04', 'Deliver', 'Concept to launch — on scale, on story, on time.', 'Built, tested and opened experience'),
]


def two_col_block(doc, left_title, left_lines, right_title, right_lines, widths=(85, 85)):
    t = doc.add_table(rows=1, cols=2)
    for cell, title, lines_ in ((t.rows[0].cells[0], left_title, left_lines), (t.rows[0].cells[1], right_title, right_lines)):
        p = cell.paragraphs[0]; p.style = doc.styles['Eyebrow']; p.text = ''
        para_fmt(p, after=4, line=1.2)
        p.add_run(title)
        for i, l in enumerate(lines_):
            q = cell.add_paragraph(style='Field'); para_fmt(q, after=0, line=1.35)
            r = q.add_run(l)
            if i == 0:
                set_run_font(r, name=F_HEAD, size=10)
        cell_borders(cell, top='none', bottom='none', left='none', right='none')
        cell_margins(cell, top=0, bottom=0, left=0, right=160)
    set_col_widths(t, widths)
    return t


def meta_row(doc, pairs):
    t = doc.add_table(rows=2, cols=len(pairs))
    w = 170 / len(pairs)
    for i, (k, v) in enumerate(pairs):
        a = t.rows[0].cells[i]; b = t.rows[1].cells[i]
        set_cell_text(a, k, style='Table Head', tnum=False)
        set_cell_text(b, v, style='Field', tnum=True, font=F_DATA, size=10)
        for c in (a, b):
            cell_borders(c, top='none', left='none', right='none', bottom='none')
            cell_margins(c, top=40, bottom=40, left=0, right=80)
        cell_borders(a, top=(4, '1A1816'))
        cell_borders(b, bottom=(2, 'E3DED3'))
    set_col_widths(t, [w] * len(pairs))
    return t


def line_items(doc, qty_label='Qty'):
    headers = ['#', 'Description', 'Deliverable', qty_label, 'Rate (₹)', 'Amount (₹)']
    rows = []
    for n, name, desc, deliv in STEPS:
        rows.append([n, f'Step {n} — {name}. {desc}', deliv, '1', '[Rate]', '[Amount]'])
    rows += [['', '', '', '', 'Subtotal', '[Subtotal]'],
             ['', '', '', '', 'GST 18 %', '[GST]'],
             ['', '', '', '', 'Total (₹)', '[Total]']]
    t = brand_table(doc, headers, rows, [8, 66, 44, 10, 20, 22], aligns=['left', 'left', 'left', 'right', 'right', 'right'], total_rows=3)
    # description column: body text in Inter (not tnum), deliverable in Umber
    for r in range(1, 1 + len(STEPS)):
        c = t.rows[r].cells[1]; run = c.paragraphs[0].runs[0]; set_run_font(run, name=F_TEXT, size=9)
        c = t.rows[r].cells[2]; run = c.paragraphs[0].runs[0]; set_run_font(run, name=F_TEXT, size=9, color=UMBER)
        c = t.rows[r].cells[0]; run = c.paragraphs[0].runs[0]; set_run_font(run, color=GOLDINK)
    return t


def build(kind, out):
    doc = Document()
    brand_styles(doc)
    sec = page_setup(doc.sections[0], 'A4')
    brand_header_footer(doc, sec, LOCKUP_PNG, WORDMARK_PNG)
    is_inv = kind == 'invoice'
    core_props(doc, f'Sanzeed Mirza — {kind} template', kind.capitalize())
    doc.add_paragraph('Invoice' if is_inv else 'Quotation', style='Eyebrow')
    p = doc.add_paragraph(style='Title'); add_point(p, 'Tax invoice' if is_inv else 'Quotation')
    para_fmt(p, after=12, line=1.05)
    if is_inv:
        meta_row(doc, [('Invoice no.', '[Invoice no.]'), ('Date', '[Date]'), ('Due date', '[Due date]'), ('GSTIN', '[GSTIN]')])
    else:
        meta_row(doc, [('Quotation no.', '[Quotation no.]'), ('Date', '[Date]'), ('Valid until', '[Valid until]'), ('GSTIN', '[GSTIN]')])
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    two_col_block(doc, 'From', ['Sanzeed Mirza', 'Experiential Design Consultant', '[Postal address]', 'New Delhi, India', 'GSTIN [GSTIN]  ·  PAN [PAN]'],
                  'Bill to' if is_inv else 'Prepared for',
                  ['[Client]', '[Contact name, role]', '[Client address]', '[Client GSTIN]'] + ([] if is_inv else ['Project: [Project / the room]']))
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    if not is_inv:
        h = doc.add_paragraph('Scope.', style='Heading 2'); para_fmt(h, before=10, after=6, line=1.15)
        doc.add_paragraph('[One paragraph on the room: the building, the audience and the brief as discussed. A few lines are enough.]', style='Normal')
        doc.add_paragraph('The method runs in four steps. Each step ends in a named deliverable; the next step begins once that deliverable is agreed. This quotation covers the steps ticked below.', style='Normal')
    h = doc.add_paragraph('Line items.' if is_inv else 'Fees by step.', style='Heading 2'); para_fmt(h, before=10, after=8, line=1.15)
    line_items(doc)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p = doc.add_paragraph('Amounts in Indian rupees. GST at 18 % is shown separately. Figures use tabular numerals — keep the Inter Tight Medium font when editing.', style='Wall Label')
    if is_inv:
        h = doc.add_paragraph('Payment.', style='Heading 2'); para_fmt(h, before=14, after=6, line=1.15)
        doc.add_paragraph('Please pay by bank transfer by the due date above and quote the invoice number with the transfer.', style='Normal')
        kv_table(doc, [('Account name', 'Sanzeed Mirza'), ('Bank name', '[Bank name]'), ('Account no.', '[Account no.]'), ('IFSC', '[IFSC]'), ('UPI', '[UPI ID]')], widths_mm=(40, 130))
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        doc.add_paragraph('Payment terms: [e.g. 15 days from the invoice date]. Each step is invoiced on delivery of its named deliverable.', style='Normal')
    else:
        h = doc.add_paragraph('Terms.', style='Heading 2'); para_fmt(h, before=14, after=6, line=1.15)
        for t_ in ['This quotation is valid until [Valid until].',
                   'Fees exclude GST, which is charged at 18 %.',
                   'Each step is quoted and invoiced separately; the next step begins once its deliverable is agreed in writing.',
                   'Payment schedule: [e.g. 50 % on confirmation of a step, 50 % on delivery of its deliverable].',
                   'Expenses: [travel, site visits and production costs outside New Delhi — state the basis].',
                   'The first conversation is always free.']:
            p = doc.add_paragraph(t_, style='Normal'); para_fmt(p, after=4, line=1.4)
            p.paragraph_format.left_indent = Mm(6); p.paragraph_format.first_line_indent = Mm(-6)
            r = p.runs[0]; r.text = '·  ' + r.text
        doc.add_paragraph().paragraph_format.space_after = Pt(4)
        p = doc.add_paragraph(style='Normal'); para_fmt(p, before=6, after=2, line=1.4)
        r = p.add_run('To confirm, reply to sanzeed@gmail.com with the quotation number, or sign below and return this page.');
        kv_table(doc, [('Confirmed by', '[Name, role]'), ('Organisation', '[Client]'), ('Date', '[Date]'), ('Signature', ' ')], widths_mm=(40, 130))
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    p = doc.add_paragraph(style='Normal'); para_fmt(p, before=8, after=0, line=1.45)
    p.add_run('Questions about this ' + ('invoice' if is_inv else 'quotation') + '? Write to sanzeed@gmail.com — I reply within two working days. If it is urgent, WhatsApp is fastest.')
    p = doc.add_paragraph(style='Small'); para_fmt(p, before=14, after=0, line=1.3)
    r = p.add_run('Sanzeed Mirza'); set_run_font(r, name=F_HEAD, size=9.5, color=SOOT)
    p.add_run('  ·  Experiential Design Consultant  ·  Experiential design you can walk into.')
    doc.save(out)
    return out


tmpd = tempfile.mkdtemp()
for kind, folder in (('invoice', 'Invoices'), ('quotation', 'Quotations')):
    D = f'{OUT}/{folder}'
    os.makedirs(f'{D}/src', exist_ok=True)
    docx = build(kind, f'{D}/src/sanzeed-{kind}-template.docx')
    pdf = soffice_pdf(docx, tmpd)
    shutil.move(pdf, f'{D}/sanzeed-{kind}-template.pdf')
    pdf_pages_to_png(f'{D}/sanzeed-{kind}-template.pdf', f'{D}/sanzeed-{kind}-template', dpi=110)
    print(kind, pdfinfo(f'{D}/sanzeed-{kind}-template.pdf').split('Pages:')[1].split('\n')[0].strip(), 'pages')
print('invoices + quotations done')
