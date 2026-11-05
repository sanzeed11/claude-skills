#!/usr/bin/env python3
"""build_font_reference.py — assembles Font_Reference.html (A4, ~18 pages) from the specimen sheets in
Typography_Specimens/src/, typography-tokens.json (rules) and Font_Licensing.md, then it can be rendered:

    python3 build_font_reference.py
    node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in Font_Reference.html --out ../Font_Reference.pdf --pdf --size 210x297

Edit the specimen sheets (Typography_Specimens/src/build_specimens.py) for the specimen pages; edit this file for the
cover, overview, rules and licensing pages. Re-run both builders, then render.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
B = HERE.parents[1]                                   # BRAND_PACKAGE/
SPEC = HERE.parent / "Typography_Specimens" / "src"
KIT = "../../15_SOURCE_FILES/Project_Files/brand-kit"
TOK = json.load(open(B / "04_TYPOGRAPHY/typography-tokens.json"))

def logo(variant="primary-wordmark", colour="full-colour-dark", width="64mm"):
    svg = open(B / f"02_LOGO_SYSTEM/SVG/sanzeed-{variant}--{colour}.svg", encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return f'<div class="wordmark" style="width:{width}">{svg}</div>'

def sheet(name):
    """Return (style, [page html...]) from a specimen sheet, with relative paths rebased to this folder."""
    html = (SPEC / f"{name}.html").read_text(encoding="utf-8")
    style = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    pages = re.findall(r"<section class=\"page[^\"]*\"[^>]*>.*?</section>", html, re.S)
    pages = [p.replace("../../../", "../../") for p in pages]
    return style, pages

ORDER = ["sanzeed-type-specimen--fraunces", "sanzeed-type-specimen--inter-tight", "sanzeed-type-specimen--inter",
         "sanzeed-type-hierarchy", "sanzeed-type-responsive-scale", "sanzeed-type-pairing", "sanzeed-type-numbers-data",
         "sanzeed-type-editorial", "sanzeed-type-character-set", "sanzeed-type-ui"]

styles, pages, toc = [], [], []
for n in ORDER:
    st, pg = sheet(n)
    if st not in styles: styles.append(st)
    pages.append((n, pg))

CSS = """
.fam{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6mm}
.fam>div{border-top:1px solid var(--fg);padding-top:4mm}
.fam .aa{font-size:64pt;line-height:1;margin-bottom:3mm}
.fam h3{margin-top:2mm}
.fam p{font-size:8.5pt;color:var(--fg-2);margin-top:2mm}
.fam .meta{font-family:var(--font-heading);font-weight:500;font-size:6.8pt;letter-spacing:.06em;color:var(--fg-3);margin-top:3mm;line-height:1.5}
.rule{display:grid;grid-template-columns:8mm 1fr;gap:3mm;padding:3mm 0;border-top:1px solid var(--line);font-size:9pt;align-items:baseline}
.rule .n{font-family:var(--font-heading);font-weight:500;font-size:7.5pt;letter-spacing:.08em;color:var(--accent-text);font-variant-numeric:tabular-nums}
.dd{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm}
.dd .tile{border:1px solid var(--line);border-radius:12px;padding:4mm 4.5mm 3.5mm;background:var(--card);min-height:24mm;display:flex;flex-direction:column;justify-content:space-between}
.dd .tile .s{font-size:18pt;line-height:1.1}
.dd .tile .l{font-family:var(--font-heading);font-weight:600;font-size:6.5pt;letter-spacing:.12em;text-transform:uppercase;margin-top:4mm}
.dd .do .l{color:var(--success)} .dd .dont .l{color:var(--error)}
.dd .tile .l span{color:var(--fg-3);font-weight:500;letter-spacing:.04em;text-transform:none;display:block;margin-top:1mm;font-size:7pt}
.lic td{font-size:8pt}
.toc li{padding:2.7mm 0}
.toc li .t{font-size:14pt}
"""

head = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sanzeed — Font Reference</title>
<link rel="stylesheet" href="{KIT}/doc.css">
<style>{''.join(styles)}{CSS}</style>
</head>
<body>
<main class="doc" style="--doc:'Font Reference'">
"""

cover = f"""
<section class="page cover theme-dark grain">
  <div class="cover-top"><span class="eyebrow">Sanzeed Mirza · Experiential Design Consultant</span><span class="eyebrow" style="color:var(--fg-3)">Brand package · 04 Typography</span></div>
  <div class="cover-title"><h1 class="doc-display">Font <span class="lit">reference.</span></h1>
  <p class="cover-sub">Fraunces, Inter Tight and Inter: the three families, the scale on screen and in print, specimens, pairing, numbers, rules and licensing.</p>
  <p class="cover-meta">Version 1.0 · 5 November 2026</p></div>
  <div class="cover-foot">{logo()}<span class="cover-meta">sanzeed.com</span></div>
</section>
"""

# ---------- overview + contents
toc_items = [("01", "The three families", "Roles, axes, weights in use", 3), ("02", "Fraunces", "Display serif · weights · optical size · italic · SOFT and WONK", 4),
             ("03", "Inter Tight", "Heading sans · weights 400–800 · tracking", 6), ("04", "Inter", "Text sans · weights · opsz · tabular numerals · measure", 7),
             ("05", "Hierarchy", "display-1 … caption at true size", 8), ("06", "Responsive and print scale", "Desktop / tablet / mobile pixels · points on paper", 11),
             ("07", "Pairing", "A page composition", 13), ("08", "Numbers and data", "Stats, quotation table, timeline", 14), ("09", "Editorial", "Case-study text and pull quote", 15),
             ("10", "Character set", "Every glyph in the subsets", 16), ("11", "Type in the UI", "Dark and light components", 17), ("12", "Rules", "From typography-tokens.json", 18), ("13", "Licensing", "SIL Open Font License summary", 19)]
toc_html = "".join(f'<li><span class="n">{n}</span><span class="t">{t}<small>{s}</small></span><span class="p">{p:02d}</span></li>' for n, t, s, p in toc_items)

overview = f"""
<section class="page" data-section="01 · The three families">
  <div class="page-head"><span class="eyebrow">01 · The three families</span><h1 class="doc-title">Serif speaks, <span class="dim">sans works.</span></h1>
  <p class="doc-lead">Three open-licence families carry the whole identity. Fraunces, at a single light weight, is the voice; Inter Tight structures and labels; Inter is read and tapped. Nothing else is ever added.</p></div>
  <div class="fam">
    <div><div class="aa" style="font-family:var(--font-display);font-weight:300;font-variation-settings:'opsz' 144,'SOFT' 30,'WONK' 0">Aa</div><h3 class="doc-h3">Fraunces</h3><p>Display and editorial serif. Headlines, statements, stats, pull quotes, long editorial reading. Always 300 Light; italic for quotes.</p><div class="meta">VARIABLE · opsz 9–144 · wght 100–900 · SOFT · WONK<br>UNDERCASE TYPE · SIL OFL 1.1</div></div>
    <div><div class="aa" style="font-family:var(--font-heading);font-weight:600;letter-spacing:-0.01em">Aa</div><h3 class="doc-h3">Inter Tight</h3><p>Headings, labels, eyebrows, counters and tables. 600 for H3/H4, eyebrows and labels; 500 for data with tabular numerals.</p><div class="meta">VARIABLE · wght 100–900 · roman + italic<br>RASMUS ANDERSSON · SIL OFL 1.1</div></div>
    <div><div class="aa" style="font-family:var(--font-text);font-weight:400">Aa</div><h3 class="doc-h3">Inter</h3><p>Everything that is read: body, lead, captions, wall labels, forms, buttons and navigation. 400 for text, 500 for UI, 600 for emphasis.</p><div class="meta">VARIABLE · opsz 14–32 · wght 100–900<br>RASMUS ANDERSSON · SIL OFL 1.1</div></div>
  </div>
  <div class="cols-12 mt-5" style="grid-template-columns:1fr 1fr;gap:10mm">
    <div><div class="pull-quote" style="padding:5mm 0"><p class="doc-quote" style="font-size:18pt">The script comes first. Every room, screen and surface carries a line of it.</p><cite>Service copy · sanzeed.com</cite></div></div>
    <div><span class="eyebrow">Where the system lives</span>
      <dl class="kv mt-2" style="grid-template-columns:40mm 1fr">
        <dt>Font files</dt><dd>04_TYPOGRAPHY/Font_Files/&lt;Family&gt;/ — variable TTFs for desktop, woff2 subsets for the web, OFL.txt beside each</dd>
        <dt>Scale tokens</dt><dd>typography-tokens.json — px per breakpoint, pt for print, rules</dd>
        <dt>CSS</dt><dd>brand.css (.t-* fluid classes) · type-scale.css (.ts-* stepped, .tp-* print) · doc.css (A4 documents)</dd>
        <dt>Specimens</dt><dd>Typography_Specimens/ — every sheet in this document as HTML, PDF and PNG</dd>
        <dt>Licence</dt><dd>Font_Licensing.md and page 19</dd>
      </dl>
    </div>
  </div>
</section>
"""
contents = f"""
<section class="page" data-section="Contents">
  <div class="page-head"><span class="eyebrow">Contents</span><h1 class="doc-title">Three families, one <span class="dim">voice.</span></h1></div>
  <ul class="toc" style="max-width:150mm;--toc-pad:2.6mm">{toc_html}</ul>
</section>
"""

# ---------- rules page
rules = TOK["rules"]
rule_html = "".join(f'<div class="rule"><span class="n">{i+1:02d}</span><span>{r}</span></div>' for i, r in enumerate(rules))
F = "font-family:var(--font-display);font-weight:300;font-variation-settings:'opsz' 72,'SOFT' 30,'WONK' 0"
dd = f"""
<div class="dd">
 <div class="tile do"><div class="s" style="{F}">Eight rooms, <span class="lit">lit.</span></div><div class="l">Do<span>Sentence case, full stop, one lit last word</span></div></div>
 <div class="tile do"><div class="s" style="{F}">A method for the monumental.</div><div class="l">Do<span>Fraunces 300, opsz matched to size</span></div></div>
 <div class="tile do"><div class="s"><span class="eyebrow">Now showing</span><br><span style="{F};font-size:19pt">Between two points of light.</span></div><div class="l">Do<span>Eyebrow in Inter Tight caps, headline in Fraunces</span></div></div>
 <div class="tile dont"><div class="s" style="{F};font-weight:700">Eight rooms, lit.</div><div class="l">Don't<span>Bold Fraunces — the voice is light</span></div></div>
 <div class="tile dont"><div class="s" style="{F};letter-spacing:.12em;text-transform:uppercase;font-size:14pt">Eight rooms, lit.</div><div class="l">Don't<span>Letter-spaced or capitalised Fraunces</span></div></div>
 <div class="tile dont"><div class="s" style="{F}">Eight <span class="dim">rooms,</span> <span class="lit">lit.</span></div><div class="l">Don't<span>.lit and .dim in the same headline; gradients or shadows on type</span></div></div>
</div>"""
rules_page = f"""
<section class="page" data-section="12 · Rules">
  <div class="page-head"><span class="eyebrow">12 · Rules</span><h1 class="doc-title">Eight rules, <span class="dim">kept.</span></h1><p class="doc-lead">Taken verbatim from typography-tokens.json. They are the whole typographic law of the identity; everything else is layout.</p></div>
  <div class="cols-12" style="grid-template-columns:1fr 1fr;gap:10mm"><div>{rule_html}</div>
  <div><div class="kv" style="grid-template-columns:34mm 1fr"><dt>Minimum sizes</dt><dd>Fraunces 16 px / 9 pt · Inter Tight 11 px · Inter 12 px for captions on dark (Mist) · body never below 15 px on screen</dd><dt>Optical size</dt><dd>Fraunces opsz 144 ≥ 48 px, 72 for 24–48 px, 36 below; Inter opsz follows the size automatically</dd><dt>Measure</dt><dd>60–72 characters; paragraph spacing one line; no indents</dd><dt>Numerals</dt><dd>Tabular in every table, invoice, quotation and stat; the plus sign in a stat is gold</dd><dt>Case</dt><dd>Headlines sentence case with a full stop; eyebrows and counters are the only letter-spaced caps</dd><dt>Colour</dt><dd>Gold as text only as Lamp Gold on dark (≥ 16 px) and Gold Ink on light; one gold accent per composition</dd></div></div></div>
  <div class="mt-1">{dd}</div>
</section>
"""

# ---------- licensing page
lic_page = """
<section class="page" data-section="13 · Licensing">
  <div class="page-head"><span class="eyebrow">13 · Licensing</span><h1 class="doc-title">Open fonts, <span class="dim">kept open.</span></h1><p class="doc-lead">All three typefaces are released under the SIL Open Font License 1.1. They may be used, embedded, modified and redistributed with this package and the website, provided the licence file travels with them and they are never sold on their own.</p></div>
  <table class="doc lic"><thead><tr><th>Family</th><th>Role in the system</th><th>Designer / copyright</th><th>Source of the files</th><th>Official page</th></tr></thead><tbody>
  <tr><td><strong>Fraunces</strong><br><span class="faint">variable: opsz, wght, SOFT, WONK · roman + italic</span></td><td>Display and editorial serif — headlines, large numerals, pull quotes</td><td>© 2020 The Fraunces Project Authors (Undercase Type: Phaedra Charles, Flavia Zimbardi)</td><td>google/fonts repository, ofl/fraunces/ (fetched 5 Nov 2026)</td><td>fonts.google.com/specimen/Fraunces<br>github.com/undercasetype/Fraunces</td></tr>
  <tr><td><strong>Inter</strong><br><span class="faint">variable: opsz, wght · roman + italic</span></td><td>Text and UI sans — body, captions, forms, tables</td><td>© 2020 The Inter Project Authors (Rasmus Andersson)</td><td>google/fonts repository, ofl/inter/</td><td>fonts.google.com/specimen/Inter<br>rsms.me/inter</td></tr>
  <tr><td><strong>Inter Tight</strong><br><span class="faint">variable: wght · roman + italic</span></td><td>Headings, labels, eyebrows, descriptor lockup</td><td>© 2020 The Inter Project Authors (Rasmus Andersson)</td><td>google/fonts repository, ofl/intertight/</td><td>fonts.google.com/specimen/Inter+Tight</td></tr>
  </tbody></table>
  <div class="cols-2 mt-4" style="gap:10mm">
    <div><span class="eyebrow">What is included</span><ul class="mt-2" style="font-size:8.5pt"><li><strong>Font_Files/&lt;Family&gt;/*.ttf</strong> — the original variable TrueType fonts exactly as distributed by Google Fonts. Install these on desktop for InDesign, Illustrator, Word, PowerPoint, Keynote and Figma.</li><li><strong>Font_Files/&lt;Family&gt;/*-variable.woff2</strong> — web subsets (Latin, Latin Extended-A, general punctuation, ₹, arrows) produced with fontTools for the website design system. Variation axes are preserved.</li><li><strong>Font_Files/&lt;Family&gt;/OFL.txt</strong> — the licence that must travel with the files.</li></ul>
    <span class="eyebrow mt-4" style="display:block">Office documents</span><p class="doc-small mt-2">Word and PowerPoint templates in this package reference Fraunces, Inter Tight and Inter. Install the TTFs on every machine that edits them; if the fonts are missing, the documents fall back to Georgia and Arial (acceptable for internal drafts, not for client-facing output).</p></div>
    <div><span class="eyebrow">Obligations under the OFL</span><ol class="mt-2" style="font-size:8.5pt"><li>Keep OFL.txt with the font files when you redistribute them (for example inside a website build or a template pack).</li><li>Do not sell the fonts by themselves.</li><li>If you modify a font and redistribute it, do not use the Reserved Font Names ("Fraunces", "Inter") for the modified version. The woff2 subsets here are not renamed because subsetting for web embedding is standard practice and they are distributed only as part of this website; if in doubt, serve the original TTFs or Google Fonts' hosted CSS.</li></ol>
    <span class="eyebrow mt-4" style="display:block">Fallback stacks (brand.css)</span>
    <pre class="mono mt-2" style="white-space:pre-wrap;font-size:7pt;line-height:1.45;margin:0;padding:3.5mm 4mm;border:1px solid var(--line);border-radius:12px;background:var(--card)">--font-display: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
--font-heading: "Inter Tight", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
--font-text:    "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;</pre></div>
  </div>
</section>
"""

back = f"""
<section class="page cover theme-dark grain">
  <div class="cover-top"><span class="eyebrow" style="color:var(--fg-3)">Brand package · 04 Typography · Font reference</span><span class="eyebrow" style="color:var(--fg-3)">Version 1.0</span></div>
  <div class="cover-title"><p class="doc-display" style="font-size:40pt">Vision you can walk <span class="lit">into.</span></p>
  <p class="cover-sub">Sanzeed Mirza · Experiential Design Consultant<br>+91 7827051270 · sanzeed@gmail.com · sanzeed.com · New Delhi, India</p></div>
  <div class="cover-foot">{logo("horizontal-descriptor", "full-colour-dark", "70mm")}<span class="cover-meta">Fonts under SIL OFL 1.1</span></div>
</section>
"""

# renumber the specimen page eyebrows is not needed; sections are named by data-section already.
body = cover + contents + overview
for n, pg in pages:
    body += "\n".join(pg) + "\n"
body += rules_page + lic_page + back
html = head + body + "</main>\n</body>\n</html>\n"
(HERE / "Font_Reference.html").write_text(html, encoding="utf-8")
print("wrote Font_Reference.html with", body.count('<section class="page'), "pages")
