#!/usr/bin/env python3
"""docxlib.py — python-docx helpers shared by the letterhead, invoice, quotation, proposal and
official-document templates. Fonts are named as Office apps list them ("Fraunces Light",
"Inter Tight SemiBold") so the styles resolve once the three kit fonts are installed."""
import os
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor, Emu

SOOT = RGBColor(0x1A, 0x18, 0x16)
UMBER = RGBColor(0x66, 0x5F, 0x55)
GOLDINK = RGBColor(0x8A, 0x61, 0x24)
OLDGOLD = RGBColor(0xB8, 0x86, 0x3B)
MIST = RGBColor(0x6D, 0x66, 0x5C)
PAPER = 'FBF8F2'
STONE = 'ECE7DC'
PLASTER = 'F5F0E7'

F_DISPLAY = 'Fraunces Light'
F_HEAD = 'Inter Tight SemiBold'
F_DATA = 'Inter Tight Medium'
F_TEXT = 'Inter'

CONTACT_LINE = 'Sanzeed Mirza  ·  Experiential Design Consultant  ·  New Delhi, India'
CONTACT_LINE_2 = '+91 7827051270  ·  sanzeed@gmail.com  ·  sanzeed.com  ·  linkedin.com/in/sanzeed'


def set_run_font(run, name=None, size=None, bold=None, italic=None, color=None, caps=None, spacing=None, tnum=False):
    f = run.font
    if name:
        f.name = name
        rpr = run._r.get_or_add_rPr()
        rf = rpr.find(qn('w:rFonts'))
        if rf is None:
            rf = OxmlElement('w:rFonts'); rpr.append(rf)
        for k in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
            rf.set(qn(k), name)
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color
    if caps is not None:
        f.all_caps = caps
    if spacing is not None:  # letter-spacing in twentieths of a point
        rpr = run._r.get_or_add_rPr()
        sp = OxmlElement('w:spacing'); sp.set(qn('w:val'), str(int(spacing * 20))); rpr.append(sp)
    if tnum:
        rpr = run._r.get_or_add_rPr()
        # OpenType feature: tabular numerals (Word 2010+ honours w14:numSpacing)
        ns = 'http://schemas.microsoft.com/office/word/2010/wordml'
        el = OxmlElement('w14:numSpacing'); el.set(qn('w14:val'), 'tabular')
        rpr.append(el)
    return run


def style_font(style, name, size, bold=False, italic=False, color=SOOT, caps=False, spacing=None):
    f = style.font
    f.name = name; f.size = Pt(size); f.bold = bold; f.italic = italic; f.color.rgb = color; f.all_caps = caps
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    for k in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(k), name)
    # remove theme fonts so Word does not override
    for k in ('w:asciiTheme', 'w:hAnsiTheme', 'w:cstheme', 'w:eastAsiaTheme'):
        if rf.get(qn(k)) is not None:
            del rf.attrib[qn(k)]
    if spacing is not None:
        sp = rpr.find(qn('w:spacing'))
        if sp is None:
            sp = OxmlElement('w:spacing'); rpr.append(sp)
        sp.set(qn('w:val'), str(int(spacing * 20)))
    # strip borders that the default template puts on Title
    ppr = style.element.find(qn('w:pPr'))
    if ppr is not None:
        for b in ppr.findall(qn('w:pBdr')):
            ppr.remove(b)
    return style


def para_fmt(style_or_para, before=0, after=0, line=None, keep_next=None, align=None):
    pf = style_or_para.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after)
    if line is not None:
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = line
    if keep_next is not None:
        pf.keep_with_next = keep_next
    if align is not None:
        pf.alignment = align


def brand_styles(doc, body_size=10, body_line=1.45):
    """Title = Fraunces 28 · Heading 1 = Fraunces 22 · Heading 2 = Fraunces 18 · Heading 3 = Inter Tight 11 · Body = Inter 10/1.45."""
    st = doc.styles
    style_font(st['Normal'], F_TEXT, body_size)
    para_fmt(st['Normal'], after=8, line=body_line)
    style_font(st['Title'], F_DISPLAY, 28, color=SOOT)
    para_fmt(st['Title'], before=0, after=14, line=1.05, keep_next=True)
    style_font(st['Heading 1'], F_DISPLAY, 22, color=SOOT)
    para_fmt(st['Heading 1'], before=22, after=8, line=1.1, keep_next=True)
    style_font(st['Heading 2'], F_DISPLAY, 18, color=SOOT)
    para_fmt(st['Heading 2'], before=18, after=6, line=1.15, keep_next=True)
    style_font(st['Heading 3'], F_HEAD, 11, color=SOOT)
    para_fmt(st['Heading 3'], before=12, after=3, line=1.25, keep_next=True)
    # custom paragraph styles
    from docx.enum.style import WD_STYLE_TYPE
    for name, fam, size, color, caps, sp, after in [
            ('Eyebrow', F_HEAD, 7.5, GOLDINK, True, 0.9, 6),
            ('Wall Label', F_TEXT, 8, MIST, False, None, 4),
            ('Small', F_TEXT, 8.5, UMBER, False, None, 4),
            ('Lead', F_TEXT, 12, UMBER, False, None, 10),
            ('Quote', F_DISPLAY, 16, SOOT, False, None, 10),
            ('Contact', F_TEXT, 7.5, UMBER, False, None, 0),
            ('Table Head', F_HEAD, 8, UMBER, True, 0.6, 0),
            ('Table Body', F_DATA, 9, SOOT, False, None, 0),
            ('Field', F_TEXT, 9.5, SOOT, False, None, 2)]:
        if name in [s.name for s in st]:
            s = st[name]
        else:
            s = st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        s.base_style = st['Normal']
        style_font(s, fam, size, color=color, caps=caps, spacing=sp)
        para_fmt(s, after=after, line=1.3 if name != 'Quote' else 1.3)
        if name == 'Quote':
            s.font.italic = True
    return doc


def add_point(par, text, point_color=OLDGOLD, font=None, size=None):
    """Headline text + a gold full stop as its own run."""
    r = par.add_run(text)
    if font or size:
        set_run_font(r, name=font, size=size)
    p = par.add_run('.')
    set_run_font(p, name=font, size=size, color=point_color)
    return par


def add_field(run, instr):
    for tag, attrs, txt in [('w:fldChar', {'w:fldCharType': 'begin'}, None),
                            ('w:instrText', {'xml:space': 'preserve'}, instr),
                            ('w:fldChar', {'w:fldCharType': 'separate'}, None),
                            ('w:t', {}, '1'),
                            ('w:fldChar', {'w:fldCharType': 'end'}, None)]:
        el = OxmlElement(tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        if txt is not None:
            el.text = txt
        run._r.append(el)
    return run


def page_setup(section, size='A4', margin_mm=20, header_mm=20, footer_mm=14, top_extra=22):
    if size == 'A4':
        section.page_width, section.page_height = Mm(210), Mm(297)
    else:  # US Letter
        section.page_width, section.page_height = Mm(215.9), Mm(279.4)
    section.left_margin = section.right_margin = Mm(margin_mm)
    section.top_margin = Mm(margin_mm + top_extra)   # header (logo) sits at the 20 mm margin; body starts below it
    section.bottom_margin = Mm(margin_mm + 10)
    section.header_distance = Mm(header_mm)
    section.footer_distance = Mm(footer_mm)
    return section


def text_width_mm(section):
    return (section.page_width - section.left_margin - section.right_margin) / 36000


def brand_header_footer(doc, section, logo_png, wordmark_png, logo_w_mm=56, wordmark_w_mm=30, page_numbers=True,
                        footer_right='Page {PAGE} of {NUMPAGES}'):
    section.different_first_page_header_footer = True
    # first-page header: lockup
    h = section.first_page_header
    p = h.paragraphs[0]; p.text = ''
    para_fmt(p, after=0, line=1)
    p.add_run().add_picture(logo_png, width=Mm(logo_w_mm))
    # continuation header: wordmark
    h2 = section.header
    p2 = h2.paragraphs[0]; p2.text = ''
    para_fmt(p2, after=0, line=1)
    p2.add_run().add_picture(wordmark_png, width=Mm(wordmark_w_mm))
    # footers (same on both)
    tw = text_width_mm(section)
    for ft in (section.first_page_footer, section.footer):
        p = ft.paragraphs[0]; p.text = ''
        p.style = doc.styles['Contact']
        para_fmt(p, before=0, after=0, line=1.3)
        # hairline above
        ppr = p._p.get_or_add_pPr()
        bdr = OxmlElement('w:pBdr'); top = OxmlElement('w:top')
        top.set(qn('w:val'), 'single'); top.set(qn('w:sz'), '2'); top.set(qn('w:space'), '8'); top.set(qn('w:color'), 'E3DED3')
        bdr.append(top); ppr.append(bdr)
        p.paragraph_format.tab_stops.add_tab_stop(Mm(tw), WD_TAB_ALIGNMENT.RIGHT)
        p.add_run(CONTACT_LINE)
        if page_numbers:
            p.add_run('\t')
            p.add_run('Page ')
            add_field(p.add_run(), 'PAGE')
            p.add_run(' of ')
            add_field(p.add_run(), 'NUMPAGES')
        p2 = ft.add_paragraph(CONTACT_LINE_2, style='Contact')
        para_fmt(p2, before=0, after=0, line=1.3)
    return section


def shade_cell(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hex_fill)
    tcPr.append(shd)


def cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Each side: None (leave), 'none', or (sz_eighths_pt, hex)."""
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn('w:tcBorders'))
    if b is None:
        b = OxmlElement('w:tcBorders'); tcPr.append(b)
    for side, val in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        if val is None:
            continue
        el = OxmlElement(f'w:{side}')
        if val == 'none':
            el.set(qn('w:val'), 'nil')
        else:
            el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), str(val[0])); el.set(qn('w:color'), val[1]); el.set(qn('w:space'), '0')
        b.append(el)


def cell_margins(cell, top=60, bottom=60, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement('w:tcMar')
    for side, v in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        el = OxmlElement(f'w:{side}'); el.set(qn('w:w'), str(v)); el.set(qn('w:type'), 'dxa'); m.append(el)
    tcPr.append(m)


def set_cell_text(cell, text, style='Table Body', align=None, color=None, font=None, size=None, bold=None, tnum=True):
    p = cell.paragraphs[0]
    p.text = ''
    p.style = style
    para_fmt(p, before=0, after=0, line=1.25)
    if align == 'right':
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    elif align == 'center':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    set_run_font(r, name=font, size=size, color=color, bold=bold, tnum=tnum)
    return p


def set_col_widths(table, widths_mm, indent_dxa=None):
    table.autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
    if indent_dxa is not None:  # pull the table so its text aligns with the margin (cell padding compensation)
        ind = OxmlElement('w:tblInd'); ind.set(qn('w:w'), str(-indent_dxa)); ind.set(qn('w:type'), 'dxa'); tblPr.append(ind)
    for row in table.rows:
        for i, w in enumerate(widths_mm):
            row.cells[i].width = Mm(w)
    for i, w in enumerate(widths_mm):
        table.columns[i].width = Mm(w)


def brand_table(doc, headers, rows, widths_mm, aligns=None, total_rows=0, head_fill=STONE, stripe=None):
    """A brand table: Inter Tight SemiBold caps header on Stone, Inter Tight Medium tnum body,
    hairline rows, totals in Soot with a heavier rule above."""
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    # kill default style borders
    t.style = doc.styles['Table Grid'] if 'Table Grid' in [s.name for s in doc.styles] else None
    aligns = aligns or ['left'] * len(headers)
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        set_cell_text(c, h, style='Table Head', align=aligns[i])
        shade_cell(c, head_fill)
        cell_borders(c, top='none', left='none', right='none', bottom=(4, 'C9C2B4'))
        cell_margins(c)
    n = len(rows)
    for r, row in enumerate(rows, 1):
        is_total = r > n - total_rows
        for i, v in enumerate(row):
            c = t.rows[r].cells[i]
            set_cell_text(c, v, style='Table Body', align=aligns[i], bold=None,
                          font=(F_HEAD if is_total and i >= len(row) - 2 and v else None))
            if stripe and r % 2 == 0 and not is_total:
                shade_cell(c, stripe)
            top = (8, '1A1816') if (is_total and r == n - total_rows + 1) else 'none'
            cell_borders(c, top=top, left='none', right='none', bottom=(2, 'E3DED3') if not is_total else 'none')
            cell_margins(c)
    set_col_widths(t, widths_mm, indent_dxa=80)
    return t


def field(doc, label, value, style='Field'):
    p = doc.add_paragraph(style=style)
    r = p.add_run(label.upper() + '  ')
    set_run_font(r, name=F_HEAD, size=7, color=UMBER, spacing=0.6)
    p.add_run(value)
    return p


def kv_table(doc, pairs, widths_mm=(42, 128), label_style='Table Head', value_style='Field'):
    t = doc.add_table(rows=len(pairs), cols=2)
    for i, (k, v) in enumerate(pairs):
        a, b = t.rows[i].cells
        set_cell_text(a, k, style=label_style, tnum=False)
        set_cell_text(b, v, style=value_style, tnum=True)
        for c in (a, b):
            cell_borders(c, top='none', left='none', right='none', bottom=(2, 'E3DED3'))
            cell_margins(c, top=50, bottom=50, left=0, right=80)
    set_col_widths(t, widths_mm)
    return t


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def hr(doc, color='E3DED3', before=6, after=10):
    p = doc.add_paragraph()
    para_fmt(p, before=before, after=after, line=1)
    ppr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '2'); b.set(qn('w:space'), '1'); b.set(qn('w:color'), color)
    bdr.append(b); ppr.append(bdr)
    r = p.add_run(' '); set_run_font(r, size=2)
    return p


def core_props(doc, title, subject):
    cp = doc.core_properties
    cp.author = 'Sanzeed Mirza'
    cp.title = title
    cp.subject = subject
    cp.keywords = 'Sanzeed; Experiential Design Consultant; stationery'
    cp.comments = 'Brand stationery template — Fraunces Light / Inter Tight SemiBold / Inter. Install the fonts from 04_TYPOGRAPHY/Font_Files.'
