#!/usr/bin/env python3
"""build_mediakit.py — Media_Kit/: A4 media kit PDF (HTML source), headshot exports into Press/, media-kit-contents.md."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C
from docstyle import A4_CSS, page, gallery_cols

OUT = f"{MC}/Media_Kit"; SRC = f"{OUT}/src"; PRESS = f"{MC}/Press"
os.makedirs(SRC, exist_ok=True); os.makedirs(PRESS, exist_ok=True)

CSS = A4_CSS + """
.cover .mark { left: 18mm; top: 18mm; width: 44mm; }
.cover .plate { position: absolute; left: 18mm; top: 52mm; width: 174mm; height: 120mm; border-radius: 7mm; }
.cover .wl { position: absolute; left: 18mm; top: 176mm; }
.cover .eyebrow-quiet { position: absolute; left: 18mm; top: 196mm; }
.cover .hl { position: absolute; left: 18mm; top: 203mm; width: 170mm; font-size: 36pt; line-height: 1.0; }
.cover .toc { position: absolute; left: 18mm; bottom: 18mm; width: 174mm; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1mm 6mm; font-size: 7pt; color: var(--fg-3); }
.cover .toc b { font-family: var(--font-heading); font-weight: 500; color: var(--accent-text); margin-right: 2mm; font-variant-numeric: tabular-nums; }
.bio .block { border-top: 1px solid var(--line); padding-top: 3mm; margin-bottom: 6mm; }
.bio .block .count { font-size: 6.5pt; color: var(--fg-3); font-variant-numeric: tabular-nums; }
.shots .grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6mm; align-items: start; }
.shots .plate { border-radius: 4mm; }
.shots .spec { font-size: 6.8pt; line-height: 1.5; color: var(--fg-2); margin-top: 2mm; }
.shots .spec b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); display: block; }
.logos .tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; margin-top: 2mm; }
.logos .tile { border-radius: 4mm; border: 1px solid var(--line); height: 34mm; display: flex; align-items: center; justify-content: center; }
.logos .tile.dark { background: #000; } .logos .tile.plaster { background: #F5F0E7; } .logos .tile.gold { background: #B8863B; }
.logos .tile img { width: 60%; }
.logos .tile.sym img { width: 14mm; }
.logos .cap { font-size: 6.5pt; color: var(--fg-3); margin-top: 1.5mm; }
.logos ul { padding-left: 4mm; margin: 0; font-size: 8pt; line-height: 1.5; color: var(--fg-2); } .logos li { margin-bottom: 1mm; }
.logos .two { display: grid; grid-template-columns: 1fr 1fr; gap: 8mm; }
.contactp .hl { font-size: 36pt; }
.contactp .contact { font-size: 11pt; line-height: 1.8; margin-top: 8mm; }
.contactp .promises { margin-top: 10mm; border-top: 1px solid var(--line); padding-top: 5mm; font-size: 9pt; line-height: 1.8; color: var(--fg-2); }
.contactp .lock { position: absolute; left: 0; bottom: 0; width: 60mm; }
.featured { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin-bottom: 5mm; }
.featured .plate { height: 22mm; border-radius: 3mm; }
.featured .wl { margin-top: 1mm; font-size: 6pt; }
"""

def build():
    pages = []
    toc = [("01", "Biographies and boilerplate"), ("02", "Headshots"), ("03", "Fact sheet"), ("04", "Logo usage"), ("05", "Projects"), ("06", "Contact")]
    pages.append(f"""<section class="sheet grain cover" id="p1">
  <img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
  <div class="plate"><img src="{shared_img('portrait--4x5-2000.jpg')}" alt="Sanzeed Mirza" style="object-position:50% 25%"></div>
  <div class="wl"><b>Sanzeed Mirza</b><span class="sep">·</span>New Delhi</div>
  <div class="eyebrow-quiet">Media kit · Sanzeed Mirza · Experiential Design Consultant · 2026</div>
  <h1 class="hl">Experiential design you can walk into<span class="pt">.</span></h1>
  <div class="toc">{''.join(f'<div><b>{n}</b>{esc(t)}</div>' for n, t in toc)}</div>
</section>""")
    # 2 bios
    pages.append(page("p2", "bio", f"""<div class="eyebrow">01 · Biographies</div><h2 class="hl">Sanzeed Mirza, in 10, 25 and 50 words<span class="pt">.</span></h2>
    <div class="block"><h3>Ten words</h3><p class="body">{esc(C.BIO_10)}</p></div>
    <div class="block"><h3>Short biography · 25 words</h3><p class="body">{esc(C.BIO_25)}</p></div>
    <div class="block"><h3>Long biography · 50 words</h3><p class="body">{esc(C.BIO_50)}</p></div>
    <div class="block"><h3>In his words</h3><p class="body">{esc(C.ABOUT_1)}</p><p class="body">{esc(C.ABOUT_2)}</p></div>
    <div class="block"><h3>Boilerplate · for press releases and listings</h3><p class="body">{esc(C.BOILERPLATE)}</p></div>
    <div class="block"><h3>Naming</h3><p class="body">Brand mark and handles: <b>SANZEED</b> / @sanzeed. Formal, bylines, legal: <b>Sanzeed Mirza</b>. Descriptor, always with the full name on first use: <b>Experiential Design Consultant</b>. Never “Sanzeed Studio”, “Sanzeed Design” or “Mirza Design” — the brand is the person.</p></div>""",
    "light", "Media kit · Biographies", "02"))
    # 3 headshots
    shots = ""
    for ratio, fn, use in [("1:1", "sanzeed-mirza-headshot--1x1-2000.jpg", "Profiles, avatars, round crops"), ("4:5", "sanzeed-mirza-headshot--4x5-2000.jpg", "Portrait layouts, speaker cards"), ("3:4", "sanzeed-mirza-headshot--3x4-2000.jpg", "Print, programmes, press")]:
        w, h = {"1:1": (1, 1), "4:5": (4, 5), "3:4": (3, 4)}[ratio]
        shots += f'<div><div class="plate" style="width:50mm;height:{50*h/w:.1f}mm"><img src="../../Press/{fn}" alt="Sanzeed Mirza headshot {ratio}"></div><div class="spec"><b>{fn}</b>{ratio} · 2000 px · JPEG · sRGB<br>{use}</div></div>'
    pages.append(page("p3", "shots", f"""<div class="eyebrow">02 · Headshots</div><h2 class="hl">Portrait, three crops<span class="pt">.</span></h2>
    <p class="lead">One portrait, supplied in three crops at 2000 px on the long side. Files are in <b>10_MARKETING_COLLATERAL/Press</b>.</p>
    <div class="grid">{shots}</div>
    <h3>Use</h3><p class="body">Use as supplied. Do not flip, tint, add filters or crop tighter than the 1:1 version. Caption as “Sanzeed Mirza, Experiential Design Consultant”. The source portrait is 1100 × 1574 px; the 2000 px files are upsampled for layout convenience — for print larger than A5, request the original from {C.EMAIL}.</p>""",
    "light", "Media kit · Headshots", "03"))
    # 4 fact sheet
    facts = [("Name", "Sanzeed Mirza"), ("Title", "Experiential Design Consultant"), ("Based in", "New Delhi, India — working with institutions and brands wherever the project is"),
             ("Practice", "Independent since August 2026"), ("Experience", "15+ years; 8+ years in experiential and museum design"), ("Projects directed", "90+"), ("Museums and experience centres", "60+"),
             ("Portfolio by category", "Museums & Experience Centres 60 · Projection Mapping & Shows 15 · Explainer Videos & Others 15"),
             ("Selected projects", "Prime Minister Museum (New Delhi) · Ram Katha Show (Ayodhya) · Buddha Park (Uttarakhand) · Yuge Yugeen Bharat Museum (New Delhi) · India Pavilion Expo 2025 (concept) · G20 Tree Show (New Delhi) · Tribal Museum (New Delhi) · RBI Museum (Mumbai) · Army Museum Abu Dhabi · Dubai Police Control Center"),
             ("Published case studies", "Prime Minister Museum · Ram Katha Show · Buddha Park (sanzeed.com/work)"),
             ("Services", " · ".join(t for _, t, _, _, _ in C.SERVICES)),
             ("Method", "01 Discover → 02 Direct → 03 Craft → 04 Deliver"),
             ("Career", "Experiential Design Consultant, Independent (Aug 2026 – present) · Creative Director, Tagbin (Jun 2018 – Jul 2026) · Creative Head, Digital Web Solutions (Apr – May 2018) · Creative Director, SocioPixels (Feb 2017 – Mar 2018) · Lead Concept Artist, Broadcast2world and VFX Artist, Prime Focus (Sep 2011 – Dec 2016)"),
             ("Trusted by", "PwC, Microsoft, Discovery and National Museums, from concept to public unveiling"),
             ("Master line", C.MASTER_LINE), ("Contact", f"{C.EMAIL} · {C.PHONE} (call / WhatsApp) · {C.SITE} · {C.LINKEDIN}"),
             ("Rights note", C.RIGHTS)]
    rows = "".join(f'<tr><td class="k">{esc(k)}</td><td>{esc(v)}</td></tr>' for k, v in facts)
    pages.append(page("p4", "facts", f"""<div class="eyebrow">03 · Fact sheet</div><h2 class="hl">Confirmed facts only<span class="pt">.</span></h2>
    <p class="lead">Everything below is taken from sanzeed.com. Nothing here is estimated.</p><table>{rows}</table>""", "light", "Media kit · Fact sheet", "04"))
    # 5 logo usage
    pages.append(page("p5", "logos", f"""<div class="eyebrow">04 · Logo usage</div><h2 class="hl">The wordmark and the point<span class="pt">.</span></h2>
    <p class="lead">Full logo files, colour versions and formats are in <b>02_LOGO_SYSTEM</b>. This page is the summary for editors and partners.</p>
    <div class="two"><div>
    <div class="tiles">
      <div><div class="tile dark"><img src="{logo('primary-wordmark','full-colour-dark')}" alt=""></div><div class="cap">Primary wordmark · full-colour-dark · on Gallery Black and dark photography</div></div>
      <div><div class="tile plaster"><img src="{logo('primary-wordmark','full-colour-light')}" alt=""></div><div class="cap">Primary wordmark · full-colour-light · on Plaster, Paper, white</div></div>
      <div><div class="tile dark"><img src="{logo('horizontal-descriptor','full-colour-dark')}" alt=""></div><div class="cap">Horizontal descriptor lockup · stationery, covers, signage</div></div>
      <div><div class="tile plaster sym"><img src="{logo('symbol','full-colour-light')}" alt=""></div><div class="cap">Symbol “S.” · avatars, favicons, stamps</div></div>
    </div></div>
    <div><h3>Rules</h3><ul>
    <li><b>Pairing.</b> Dark backgrounds take the full-colour-dark (white + gold) logo; light backgrounds take full-colour-light (soot + old gold). Never the reverse. Single-ink print: black or single-colour-gold.</li>
    <li><b>Clear space</b> = half the wordmark’s cap height on all sides.</li>
    <li><b>Minimum sizes.</b> Wordmark 120 px / 28 mm; descriptor lockup 220 px / 50 mm; symbol 16 px / 6 mm.</li>
    <li><b>Backgrounds.</b> Flat brand colours or photography darkened to ≥ 80 % black under the logo. Never on busy imagery, never on gold.</li>
    <li><b>Never</b> stretch, rotate, outline, add shadows or glows, recolour the dots, change letter spacing, typeset the name instead of the wordmark, or crop the S.</li>
    <li><b>Files.</b> SVG, PDF, EPS, PNG (transparent), JPG, WebP in <b>02_LOGO_SYSTEM/</b>; favicons and social tiles in their own folders.</li>
    </ul></div></div>""", "light", "Media kit · Logo usage", "05"))
    # 6 projects
    feat = "".join(f'<div><div class="plate"><img src="{jimg(im)}" alt="{esc(t)}"></div><div class="wl"><b>{esc(t)}</b><span class="sep">·</span>{esc(p)}</div></div>' for im, t, p, _ in C.FEATURED)
    pages.append(page("p6", "projects", f"""<div class="eyebrow">05 · Projects</div><h2 class="hl">90 projects, one continuous craft<span class="pt">.</span></h2>
    <h3>Now showing · eight rooms, lit</h3><div class="featured">{feat}</div>
    <h3>All ninety, by gallery</h3><div class="cols">{gallery_cols(C, esc)}</div>
    <p class="body" style="margin-top:4mm;font-size:6.5pt;color:var(--fg-3)">{esc(C.RIGHTS)} Images may be used for editorial coverage of Sanzeed Mirza’s work with a wall label (title · place).</p>""", "light", "Media kit · Projects", "06"))
    # 7 contact
    pages.append(page("p7", "contactp", f"""<div class="eyebrow-quiet">06 · Contact</div><h2 class="hl">Tell me about the room<span class="pt">.</span></h2>
    <p class="lead">{esc(C.CALL_SUB)}</p>
    <div class="contact"><b>{C.EMAIL}</b><br>{C.WHATSAPP} · Call {C.PHONE}<br>{C.LINKEDIN}<br>{C.SITE}<br>{C.CITY}</div>
    <div class="promises">{'<br>'.join(esc(p) for p in C.PROMISES)}</div>
    <img class="mark lock" src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed — Experiential Design Consultant">""", "dark", "Media kit · Contact", "07"))
    return head("Sanzeed — media kit (A4)", "dark", CSS) + "<body>\n" + "\n".join(pages) + "\n</body>\n</html>\n"

if __name__ == "__main__":
    for r in ("1x1", "4x5", "3x4"):
        shutil.copy(f"{MC}/_shared/img/portrait--{r}-2000.jpg", f"{PRESS}/sanzeed-mirza-headshot--{r}-2000.jpg")
    hp = write(f"{SRC}/sanzeed-media-kit--a4.html", build())
    render_jobs([pdf(hp, f"{OUT}/sanzeed-media-kit--a4.pdf", 210, 297)])
    tmp = f"{OUT}/_p"; os.makedirs(tmp, exist_ok=True)
    pages = pdf_pages_png(f"{OUT}/sanzeed-media-kit--a4.pdf", f"{tmp}/p", 90)
    for i, p in enumerate(pages): os.replace(p, f"{OUT}/sanzeed-media-kit--a4-page-{i+1:02d}.png")
    os.rmdir(tmp)
    sizes = page_sizes(f"{OUT}/sanzeed-media-kit--a4.pdf")
    md = f"""# Media kit — contents

Sanzeed Mirza · Experiential Design Consultant · New Delhi · sanzeed.com

| File | What it is |
|---|---|
| `sanzeed-media-kit--a4.pdf` | {len(sizes)}-page A4 media kit: 01 biographies and boilerplate · 02 headshots · 03 fact sheet · 04 logo usage · 05 projects · 06 contact |
| `sanzeed-media-kit--a4-page-01.png … -{len(sizes):02d}.png` | page previews (90 dpi) |
| `src/sanzeed-media-kit--a4.html` | editable source (brand.css + collateral.css); re-export with `node 15_SOURCE_FILES/Project_Files/brand-kit/render.js --in src/sanzeed-media-kit--a4.html --out sanzeed-media-kit--a4.pdf --pdf --size 210x297` |
| `../Press/sanzeed-mirza-headshot--1x1-2000.jpg` | headshot, square, 2000 × 2000 px |
| `../Press/sanzeed-mirza-headshot--4x5-2000.jpg` | headshot, 4:5, 2000 × 2500 px |
| `../Press/sanzeed-mirza-headshot--3x4-2000.jpg` | headshot, 3:4, 2000 × 2667 px |
| `../Press/sanzeed-press-release--2026-independent-practice.docx` | sample press release (confirmed facts only) |
| `../Press/sanzeed-fact-sheet.docx` | fact sheet, editable |
| `../Press/sanzeed-about--one-page.pdf` | one-page “About Sanzeed” |
| `../../02_LOGO_SYSTEM/` | logo files (SVG, PDF, EPS, PNG, JPG, WebP), favicons, social tiles — see `../Press/logo-pack-note.md` |

## Copy blocks (plain text)

**Ten words.** {C.BIO_10}

**25 words.** {C.BIO_25}

**50 words.** {C.BIO_50}

**Boilerplate.** {C.BOILERPLATE}

**Contact.** {C.EMAIL} · {C.PHONE} (call / WhatsApp) · {C.LINKEDIN} · {C.SITE}

Rights note: {C.RIGHTS}
"""
    write(f"{OUT}/media-kit-contents.md", md)
    print(sizes); print("media kit done", folder_size_mb(OUT), "MB")
