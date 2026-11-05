#!/usr/bin/env python3
"""build_press.py — Press/: press-release DOCX template + sample release (python-docx), fact sheet DOCX,
PDF previews via LibreOffice, logo-pack note, one-page 'About Sanzeed' PDF (HTML source). Headshots are copied
by build_mediakit.py."""
import os, sys, shutil, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C
from docstyle import A4_CSS, page
from docx import Document
from docx.shared import Pt, Mm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = f"{MC}/Press"; SRC = f"{OUT}/src"; os.makedirs(SRC, exist_ok=True)
SOOT = RGBColor(0x1A, 0x18, 0x16); UMBER = RGBColor(0x66, 0x5F, 0x55); GOLD_INK = RGBColor(0x8A, 0x61, 0x24); MIST = RGBColor(0x6D, 0x66, 0x5C)
LOGO_PNG = f"{B}/02_LOGO_SYSTEM/PNG/sanzeed-horizontal-descriptor--full-colour-light-1200w.png"

def set_font(run, name, size, color=SOOT, bold=False, italic=False):
    run.font.name = name; run.font.size = Pt(size); run.font.color.rgb = color; run.font.bold = bold; run.font.italic = italic
    rpr = run._element.get_or_add_rPr(); rf = rpr.find(qn("w:rFonts"))
    if rf is None: rf = OxmlElement("w:rFonts"); rpr.append(rf)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"): rf.set(qn(k), name)

def para(doc, text="", font="Inter", size=10.5, color=SOOT, bold=False, italic=False, before=0, after=6, line=1.35, align=None):
    p = doc.add_paragraph(); pf = p.paragraph_format; pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = line
    if align: p.alignment = align
    if text:
        r = p.add_run(text); set_font(r, font, size, color, bold, italic)
    return p

def eyebrow(doc, text, before=0, after=4):
    p = para(doc, before=before, after=after); r = p.add_run(text.upper()); set_font(r, "Inter Tight SemiBold", 8, GOLD_INK)
    r.font.all_caps = True
    rpr = r._element.get_or_add_rPr(); sp = OxmlElement("w:spacing"); sp.set(qn("w:val"), "30"); rpr.append(sp)
    return p

def headline(doc, text, size=26, after=10):
    p = para(doc, after=after, line=1.05); r = p.add_run(text.rstrip(".")); set_font(r, "Fraunces Light", size, SOOT)
    r2 = p.add_run("."); set_font(r2, "Fraunces Light", size, RGBColor(0xB8, 0x86, 0x3B)); return p

def hairline(doc):
    p = para(doc, after=6, before=2); pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr"); b = OxmlElement("w:bottom")
    b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4"); b.set(qn("w:space"), "1"); b.set(qn("w:color"), "D9D2C5"); pbdr.append(b); pPr.append(pbdr)

def base_doc():
    doc = Document(); s = doc.sections[0]
    s.page_width = Mm(210); s.page_height = Mm(297); s.left_margin = s.right_margin = Mm(20); s.top_margin = Mm(18); s.bottom_margin = Mm(18)
    st = doc.styles["Normal"]; st.font.name = "Inter"; st.font.size = Pt(10.5); st.font.color.rgb = SOOT
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Inter")
    # header: logo; footer: contact
    hp = s.header.paragraphs[0]; hp.add_run().add_picture(LOGO_PNG, width=Mm(48)); hp.paragraph_format.space_after = Pt(6)
    fp = s.footer.paragraphs[0]; r = fp.add_run(f"Sanzeed Mirza · Experiential Design Consultant · {C.EMAIL} · {C.PHONE} · {C.SITE} · New Delhi"); set_font(r, "Inter", 7.5, MIST)
    return doc

def release(sample=True):
    doc = base_doc()
    eyebrow(doc, "Press release · For immediate release" if sample else "Press release · [For immediate release / Embargoed until date]")
    if sample:
        headline(doc, "Sanzeed Mirza begins independent practice.")
        para(doc, "The experiential design consultant, Creative Director at Tagbin from 2018 to 2026, now works directly with museums, cultural institutions and brands as creative lead from first concept to opening day.", size=12, color=UMBER, after=10, line=1.4)
        p = para(doc, after=8); r = p.add_run("NEW DELHI, 5 November 2026 — "); set_font(r, "Inter Tight SemiBold", 10.5, SOOT)
        r = p.add_run("Sanzeed Mirza, Experiential Design Consultant, has begun working independently from New Delhi. Since August 2026 he has partnered directly with museums, cultural institutions and brands, leading experience vision, narrative and design direction from first concept to opening day — wherever the project is."); set_font(r, "Inter", 10.5)
        para(doc, "Over fifteen years he has directed more than 90 projects, including 60+ museums and experience centres and 15 projection-mapping and light shows, among them the Prime Minister Museum in New Delhi, the Ram Katha Show in Ayodhya and Buddha Park in Uttarakhand. From June 2018 to July 2026 he was Creative Director at Tagbin, directing the creative vision for national-level projects commissioned by ministries and top institutions and leading interdisciplinary teams across physical and digital spatial storytelling. He began his career in 2011 as Lead Concept Artist at Broadcast2world and, in parallel, as a VFX Artist at Prime Focus.", after=8)
        para(doc, "“I lead the whole room — story, space, graphics, media and the team that builds it. The work I want to make is calm to run and impossible to forget once you have walked through it,” said Sanzeed Mirza.", font="Fraunces Light", size=13, color=SOOT, after=8, line=1.3)
        para(doc, "The practice offers seven services — Experiential Design & Creative Direction; Museum & Cultural Exhibition Planning; Immersive Storytelling & Narrative Architecture; Spatial Experience & Environmental Branding; Event Production & Brand Activation; Digital ↔ Physical Experience Integration; and Cross-Functional Leadership & Mentorship — through a four-step method: Discover, Direct, Craft and Deliver. Each step ends with a named deliverable, from a research deck and the one central story to a built, tested and opened experience.", after=8)
        para(doc, "Sanzeed Mirza is available for new projects and collaborations. The first conversation is always free.", after=8)
        para(doc, "“The most powerful stories aren’t just told — they’re felt, lived, and remembered through the spaces we design and the moments we shape.” — Sanzeed Mirza", font="Fraunces Light", size=11.5, color=UMBER, italic=True, after=10, line=1.3)
    else:
        headline(doc, "[Headline in sentence case, ending with a full stop].")
        para(doc, "[One-sentence sub-heading: what happened, for whom, and why it matters. No adjectives.]", size=12, color=UMBER, after=10, line=1.4)
        p = para(doc, after=8); r = p.add_run("[CITY], [Day Month Year] — "); set_font(r, "Inter Tight SemiBold", 10.5, SOOT)
        r = p.add_run("[Lead paragraph: who, what, where, when. One thought per sentence. Name the room, the route or the deliverable.]"); set_font(r, "Inter", 10.5)
        para(doc, "[Second paragraph: the brief and the idea. What the client asked for; what visitors do. Use confirmed numbers only: 15+ years · 8+ years museums · 90+ projects · 60+ museums and centres.]", after=8)
        para(doc, "“[Quote from Sanzeed Mirza — first person, short sentences, spatial vocabulary.]” said Sanzeed Mirza, Experiential Design Consultant.", font="Fraunces Light", size=13, color=SOOT, after=8, line=1.3)
        para(doc, "[Third paragraph: the method step and the named deliverable — research deck · concept book and walkthrough film · detail drawings, media scripts and prototype room · built, tested and opened experience.]", after=8)
        para(doc, "[Optional partner quote: “[Quote],” said [Name], [Title], [Organisation].]", font="Fraunces Light", size=11.5, color=UMBER, italic=True, after=8, line=1.3)
        para(doc, "[Closing paragraph: opening date, where to see it, and the call: Tell me about the room.]", after=10)
    hairline(doc)
    eyebrow(doc, "About Sanzeed Mirza", before=4)
    para(doc, C.BOILERPLATE, size=9.5, color=UMBER, after=8, line=1.4)
    eyebrow(doc, "Media contact", before=4)
    para(doc, f"Sanzeed Mirza · {C.EMAIL} · {C.PHONE} (call / WhatsApp) · {C.SITE} · {C.LINKEDIN}", size=9.5, after=6)
    eyebrow(doc, "Images", before=4)
    para(doc, "Headshots (1:1, 4:5, 3:4 at 2000 px) and project images with wall labels are in the media kit (10_MARKETING_COLLATERAL/Media_Kit and /Press). " + C.RIGHTS, size=9, color=MIST, after=10, line=1.4)
    p = para(doc, "— ENDS —", font="Inter Tight SemiBold", size=9, color=MIST, align=WD_ALIGN_PARAGRAPH.CENTER)
    return doc

def fact_sheet():
    doc = base_doc()
    eyebrow(doc, "Fact sheet · confirmed facts only")
    headline(doc, "Sanzeed Mirza, Experiential Design Consultant.")
    para(doc, "Everything below is taken from sanzeed.com. Nothing here is estimated.", size=10, color=UMBER, after=10)
    rows = [("Name", "Sanzeed Mirza"), ("Title", "Experiential Design Consultant"), ("Based in", "New Delhi, India — working with institutions and brands wherever the project is"),
            ("Practice", "Independent since August 2026"), ("Experience", "15+ years; 8+ years in experiential and museum design"), ("Projects directed", "90+"), ("Museums and experience centres", "60+"),
            ("Portfolio by category", "Museums & Experience Centres 60 · Projection Mapping & Shows 15 · Explainer Videos & Others 15"),
            ("Selected projects", "Prime Minister Museum (New Delhi) · Ram Katha Show (Ayodhya) · Buddha Park (Uttarakhand) · Yuge Yugeen Bharat Museum (New Delhi) · India Pavilion Expo 2025 (concept) · G20 Tree Show (New Delhi) · Tribal Museum (New Delhi) · RBI Museum (Mumbai) · Army Museum Abu Dhabi · Dubai Police Control Center"),
            ("Published case studies", "Prime Minister Museum · Ram Katha Show · Buddha Park"),
            ("Services (7)", "\n".join(f"{n}  {t}" for n, t, _, _, _ in C.SERVICES)),
            ("Method (4)", "\n".join(f"{n}  {t} — you receive {r}" for n, t, _, r in C.METHOD)),
            ("Career", "\n".join(f"{d}  ·  {r}, {o}" for d, r, o, _ in C.TIMELINE)),
            ("Trusted by", "PwC, Microsoft, Discovery and National Museums, from concept to public unveiling"),
            ("Master line", C.MASTER_LINE), ("Contact", f"{C.EMAIL} · {C.PHONE} (call / WhatsApp) · {C.SITE} · {C.LINKEDIN}"), ("Rights note", C.RIGHTS)]
    t = doc.add_table(rows=0, cols=2); t.alignment = WD_TABLE_ALIGNMENT.LEFT; t.autofit = False
    for k, v in rows:
        c = t.add_row().cells; c[0].width = Mm(45); c[1].width = Mm(125)
        p = c[0].paragraphs[0]; r = p.add_run(k); set_font(r, "Inter Tight SemiBold", 9, SOOT); p.paragraph_format.space_after = Pt(4)
        p = c[1].paragraphs[0]; r = p.add_run(v); set_font(r, "Inter", 9, UMBER); p.paragraph_format.space_after = Pt(4); p.paragraph_format.line_spacing = 1.3
        for cell in c:
            tcPr = cell._tc.get_or_add_tcPr(); borders = OxmlElement("w:tcBorders"); b = OxmlElement("w:bottom")
            b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "4"); b.set(qn("w:color"), "D9D2C5"); borders.append(b); tcPr.append(borders)
    para(doc, "", after=6)
    eyebrow(doc, "Boilerplate", before=6); para(doc, C.BOILERPLATE, size=9.5, color=UMBER, line=1.4)
    return doc

ABOUT_CSS = A4_CSS + """
.about .mark { left: 18mm; top: 18mm; width: 52mm; }
.about .flow { position: absolute; left: 18mm; right: 18mm; top: 38mm; }
.about .top { display: grid; grid-template-columns: 1fr 56mm; gap: 10mm; }
.about .plate { width: 56mm; height: 70mm; border-radius: 5mm; }
.about .wl { margin-top: 2mm; }
.about .stats { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm 4mm; margin-top: 7mm; }
.about .stat .n { font-size: 20pt; } .about .stat .l { font-size: 6.5pt; }
.about p.body { max-width: none; }
.about .career p { margin-bottom: 1mm; font-size: 7.6pt; }
.about .career b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.about .svcs { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 8mm; font-size: 7.6pt; line-height: 1.45; color: var(--fg-2); }
.about .svcs div { display: grid; grid-template-columns: 7mm 1fr; }
.about .svcs .c { font-family: var(--font-heading); font-weight: 500; font-size: 6.5pt; letter-spacing: .08em; color: var(--accent-text); padding-top: .3mm; }
.about .svcs b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.about .method { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; }
.about .method b { display: block; font-family: var(--font-display); font-weight: 300; font-size: 13pt; color: var(--fg); font-variation-settings: "opsz" 72; margin: .5mm 0 1mm; }
.about .method .ey { font-family: var(--font-heading); font-weight: 600; font-size: 5.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); }
.about .method span { font-size: 6.8pt; line-height: 1.4; color: var(--fg-2); }
.about .contact { position: absolute; left: 18mm; right: 18mm; bottom: 18mm; border-top: 1px solid var(--line); padding-top: 3mm; font-size: 7.5pt; display: flex; justify-content: space-between; }
"""
def about_page():
    svcs = "".join(f'<div><span class="c">{n}</span><span><b>{esc(t)}</b> — {esc(l)}</span></div>' for n, t, l, _, _ in C.SERVICES)
    meth = "".join(f'<div><div class="ey">Step {n}</div><b>{esc(t)}</b><span>You receive {esc(r)}.</span></div>' for n, t, _, r in C.METHOD)
    career = "".join(f'<p class="body"><b>{esc(r)}</b>, {esc(o)} · {esc(d)}</p>' for d, r, o, _ in C.TIMELINE)
    inner = f"""<img class="mark" src="{logo('horizontal-descriptor','full-colour-light')}" alt="Sanzeed — Experiential Design Consultant">
  <div class="flow">
  <div class="top"><div><div class="eyebrow">About Sanzeed</div><h2 class="hl">Strategy, craft and calm leadership, in one person<span class="pt">.</span></h2>
  <p class="body">{esc(C.ABOUT_1)}</p><p class="body">{esc(C.ABOUT_2)}</p>
  <p class="body" style="color:var(--fg-3)">{esc(C.TRUST)}</p>
  <h3>Career</h3><div class="career">{career}</div></div>
  <div><div class="plate"><img src="{shared_img('portrait--4x5-2000.jpg')}" alt="Sanzeed Mirza"></div><div class="wl"><b>Sanzeed Mirza</b><span class="sep">·</span>New Delhi</div>
  <div class="stats">{''.join(f'<div class="stat"><div class="n">{n}<span class="plus">+</span></div><div class="l">{esc(l)}</div></div>' for n, l in C.PROOF)}</div></div></div>
  <h3>Seven services</h3><div class="svcs">{svcs}</div>
  <h3>Method</h3><div class="method">{meth}</div>
  </div>
  <div class="contact"><span><b style="font-family:var(--font-heading);font-weight:600;color:var(--fg)">Tell me about the room.</b> {C.EMAIL} · {C.PHONE} (call / WhatsApp) · {C.LINKEDIN}</span><span>{C.SITE} · New Delhi</span></div>"""
    body = f'<section class="sheet theme-light light about" id="art">{inner}</section>'
    return head("Sanzeed — About Sanzeed, one page", "light", ABOUT_CSS) + "<body>\n" + body + "\n</body>\n</html>\n"

def to_pdf(docx_path):
    run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, docx_path])

if __name__ == "__main__":
    release(True).save(f"{OUT}/sanzeed-press-release--2026-independent-practice.docx")
    release(False).save(f"{OUT}/sanzeed-press-release--template.docx")
    fact_sheet().save(f"{OUT}/sanzeed-fact-sheet.docx")
    for f in ("sanzeed-press-release--2026-independent-practice", "sanzeed-press-release--template", "sanzeed-fact-sheet"):
        to_pdf(f"{OUT}/{f}.docx"); print(f, page_sizes(f"{OUT}/{f}.pdf"))
    hp = write(f"{SRC}/sanzeed-about--one-page.html", about_page())
    render_jobs([pdf(hp, f"{OUT}/sanzeed-about--one-page.pdf", 210, 297), png(hp, f"{OUT}/sanzeed-about--one-page.png", 796, 1126, 2, selector="#art")])
    note = f"""# Logo pack — where the files are

The logo is not duplicated in this folder. Every production file lives in **`BRAND_PACKAGE/02_LOGO_SYSTEM/`** and is generated from one editable master (`15_SOURCE_FILES/Project_Files/logo-builder/`).

| Need | Use |
|---|---|
| Web, apps, editors | `02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg` (on dark) · `--full-colour-light.svg` (on light) |
| Print, office documents | `02_LOGO_SYSTEM/PDF/` and `EPS/` — vector, fonts outlined |
| Transparent bitmaps | `02_LOGO_SYSTEM/PNG/` — width in the file name, e.g. `-3000w.png` |
| Formal lockup (press, stationery, signage) | `sanzeed-horizontal-descriptor--*` |
| Symbol, avatars, favicons | `sanzeed-symbol--*`, `sanzeed-symbol-tile--*`, `02_LOGO_SYSTEM/Favicon/`, `02_LOGO_SYSTEM/Social_Profile/` |
| Single-ink print, engraving | `--black`, `--single-colour-gold`, `sanzeed-wordmark-plain--*` |

Rules in one breath: full-colour-dark on dark, full-colour-light on light, never the reverse; clear space = half the cap height; minimum 120 px / 28 mm wide for the wordmark; nothing added to the letters; the dots stay gold. Full rules: `02_LOGO_SYSTEM/README.md` and `12_BRAND_GUIDELINES/`. A one-page summary for editors is page 05 of `Media_Kit/sanzeed-media-kit--a4.pdf`.

Headshots for press: `sanzeed-mirza-headshot--1x1-2000.jpg`, `--4x5-2000.jpg`, `--3x4-2000.jpg` in this folder.
"""
    write(f"{OUT}/logo-pack-note.md", note)
    print("press done", folder_size_mb(OUT), "MB")
