#!/usr/bin/env python3
"""build_specimens.py — writes the ten A4 typography specimen sheets (HTML) and type-scale.css
from 04_TYPOGRAPHY/typography-tokens.json and the brand kit (brand.css + doc.css).

    python3 build_specimens.py          # writes src/*.html and ../type-scale.css
    ../render.sh                        # renders every sheet to PDF + PNG (see README.md)

Edit copy or layout here (or directly in the generated HTML), then re-run and re-render.
All copy is confirmed brand copy from 01_BRAND_STRATEGY and sanzeed.com.
"""
import json, re, os, pathlib

HERE = pathlib.Path(__file__).resolve().parent
B = HERE.parents[2]                        # BRAND_PACKAGE/
KIT = "../../../15_SOURCE_FILES/Project_Files/brand-kit"
IMG = "../../../00_ORIGINAL_ASSETS_BACKUP/images/img"
TOK = json.load(open(B / "04_TYPOGRAPHY/typography-tokens.json"))

def logo(variant="primary-wordmark", colour="full-colour-dark", width="60mm", cls="logo"):
    svg = open(B / f"02_LOGO_SYSTEM/SVG/sanzeed-{variant}--{colour}.svg", encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return f'<span class="{cls}" style="display:block;width:{width}">{svg}</span>'

SPEC_CSS = """
.logo svg{display:block;width:100%;height:auto}
.spec-row{display:grid;grid-template-columns:32mm 1fr;gap:5mm;align-items:baseline;padding:3.2mm 0;border-top:1px solid var(--line)}
.spec-row.top{align-items:start}
.lbl{font-family:var(--font-heading);font-weight:500;font-size:6.8pt;letter-spacing:.04em;color:var(--fg-3);font-variant-numeric:tabular-nums;line-height:1.45}
.lbl b{display:block;font-weight:600;color:var(--fg-2);letter-spacing:.1em;text-transform:uppercase;font-size:6.5pt;margin-bottom:.6mm}
.lbl i{font-style:normal;color:var(--accent-text)}
.fr{font-family:var(--font-display);font-weight:300;font-variation-settings:"opsz" 72,"SOFT" 30,"WONK" 0}
.it{font-family:var(--font-heading)}
.in{font-family:var(--font-text)}
.big{font-size:46pt;line-height:1.02;letter-spacing:-0.015em;font-variation-settings:"opsz" 144,"SOFT" 30,"WONK" 0;text-wrap:balance}
.glyph-row{display:flex;gap:0;align-items:baseline;justify-content:space-between}
.glyph{text-align:center;flex:1}
.glyph .g{font-size:30pt;line-height:1;letter-spacing:0}
.glyph .c{font-size:6.3pt;color:var(--fg-3);margin-top:2mm;font-family:var(--font-heading);font-weight:500;letter-spacing:.06em;font-variant-numeric:tabular-nums}
.glyph.on .c{color:var(--accent-text);font-weight:600}
.glyph.on .g{position:relative}
.glyph.on .g::after{content:"";position:absolute;left:50%;bottom:-2.2mm;width:1.4mm;height:1.4mm;border-radius:50%;background:var(--accent);transform:translateX(-50%)}
.charset{font-size:10.5pt;line-height:1.45;word-break:break-all;letter-spacing:.02em;margin-top:.8mm}
.charset.sm{font-size:8.5pt}
.pill{white-space:nowrap}
.rule-list{padding-left:1.1em;font-size:8.5pt;line-height:1.45}
.rule-list li+li{margin-top:1.2mm}
.sample-h{font-size:28pt;line-height:1.05;letter-spacing:-0.01em}
.cmp{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm}
.cmp>div{border-top:1px solid var(--line);padding-top:2.5mm}
.cmp .c{font-family:var(--font-heading);font-weight:500;font-size:6.5pt;letter-spacing:.06em;color:var(--fg-3);margin-top:2mm;font-variant-numeric:tabular-nums}
.cmp .c i{font-style:normal;color:var(--accent-text);font-weight:600}
.stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm}
.stat-row .n{font-family:var(--font-display);font-weight:300;font-size:40pt;line-height:1;font-variant-numeric:tabular-nums;font-variation-settings:"opsz" 144}
.stat-row .n .plus{color:var(--accent-text)}
.theme-dark .stat-row .n .plus{color:var(--accent)}
.stat-row .l{font-size:7.5pt;color:var(--fg-3);margin-top:2mm}
.hier{display:grid;grid-template-columns:36mm 1fr;gap:4mm;align-items:baseline;padding:2mm 0;border-top:1px solid var(--line)}
.hier:first-child{border-top:0}
.ruler{position:relative;height:3mm;border-left:1px solid var(--fg-3);border-right:1px solid var(--fg-3)}
.ruler::before{content:"";position:absolute;left:0;right:0;top:50%;border-top:1px solid var(--fg-3)}
.ruler span{position:absolute;left:50%;top:-3.2mm;transform:translateX(-50%);background:var(--bg);padding:0 1.5mm;font-family:var(--font-heading);font-weight:500;font-size:6.3pt;letter-spacing:.06em;color:var(--fg-3)}
.pill{display:inline-flex;align-items:center;gap:2mm;padding:3.2mm 5mm;border-radius:999px;font:500 11.25pt/1 var(--font-text)}
.pill.solid{background:var(--btn);color:var(--btn-fg)}
.pill.ghost{border:1px solid var(--line);color:var(--fg)}
.pill.gold{background:var(--accent);color:var(--accent-ink)}
.field{border:1px solid var(--line);border-radius:12px;padding:3.2mm 4mm;font:400 11.25pt/1.3 var(--font-text);background:var(--card);color:var(--fg-3)}
.field.focus{border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent)}
.flabel{display:block;font:500 9.75pt/1.3 var(--font-text);color:var(--fg-2);margin-bottom:2mm}
.callout{font-family:var(--font-heading);font-weight:500;font-size:6.3pt;letter-spacing:.06em;color:var(--accent-text);font-variant-numeric:tabular-nums;line-height:1.4}
.ui-panel{border-radius:20px;border:1px solid var(--line);padding:5mm 6mm;background:var(--bg)}
.ui-nav{display:flex;align-items:center;justify-content:space-between;gap:3mm;padding-bottom:3mm;border-bottom:1px solid var(--line)}
.ui-nav ul{display:flex;gap:3.5mm;list-style:none;margin:0;padding:0;font:500 8pt/1 var(--font-text);color:var(--fg-2);white-space:nowrap}
.ui-card{border:1px solid var(--line);border-radius:20px;overflow:hidden;background:var(--card)}
.ui-card img{display:block;width:100%;aspect-ratio:2.2/1;object-fit:cover}
.ui-card .body{padding:3.2mm 4mm 4mm}
.ui-card .cat{font:500 6.5pt/1.3 var(--font-text);color:var(--fg-3)}
.ui-card .cat b{color:var(--accent-text);font-weight:500}
.ui-card .t{font:600 10.5pt/1.25 var(--font-heading);margin-top:1.2mm}
.ui-card .p{font:400 8pt/1.4 var(--font-text);color:var(--fg-3);margin-top:.6mm}
.ui-tags{display:flex;flex-wrap:wrap;gap:1.6mm}
.ui-tags span{border:1px solid var(--line);border-radius:999px;padding:1.5mm 2.8mm;font:500 7.5pt/1 var(--font-text);color:var(--fg-2);white-space:nowrap}
"""

def head(title, doc, extra_css=""):
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{KIT}/doc.css">
<style>{SPEC_CSS}{extra_css}</style>
</head>
<body>
<main class="doc" style="--doc:'{doc}'">
"""

FOOT = "</main>\n</body>\n</html>\n"

def page(body, section, cls="", attrs=""):
    return f'<section class="page {cls}" data-section="{section}" {attrs}>\n{body}\n</section>\n'

def page_head(eyebrow, title, lead="", lit=None):
    t = title
    if lit:
        t = title.replace(lit, f'<span class="lit">{lit}</span>')
    l = f'<p class="doc-lead">{lead}</p>' if lead else ""
    return f'<div class="page-head"><span class="eyebrow">{eyebrow}</span><h1 class="doc-title">{t}</h1>{l}</div>'

def row(label, content, top=False):
    return f'<div class="spec-row{" top" if top else ""}"><div class="lbl">{label}</div><div>{content}</div></div>'

def write(name, html):
    (HERE / name).write_text(html, encoding="utf-8")
    print("wrote", name)

SC = TOK["scale_px"]
PR = TOK["print_scale_pt"]
ABOUT = "I'm an experiential design consultant based in New Delhi, working with institutions and brands wherever the project is. Fifteen years in: first as a concept artist and VFX lead on films and animation, then eight years directing museums, experience centres, pavilions and shows. I lead the whole room — story, space, graphics, media and the team that builds it. The work I want to make is calm to run and impossible to forget once you have walked through it."
QUOTE = "The most powerful stories aren't just told — they're felt, lived, and remembered through the spaces we design and the moments we shape."

# ---------------------------------------------------------------- 01 Fraunces
def fraunces():
    weights = [100, 200, 300, 400, 500, 600, 700, 800, 900]
    glyphs = "".join(
        f'<div class="glyph{" on" if w == 300 else ""}"><div class="g fr" style="font-weight:{w};font-variation-settings:\'opsz\' 144,\'SOFT\' 30,\'WONK\' 0">Aa</div><div class="c">{w}</div></div>'
        for w in weights)
    p1 = page_head("Type specimen · 01 of 03 · Display serif", "Fraunces.",
                   "The display and editorial serif of the identity. Always weight 300 (Light): headlines, statements, large numerals and pull quotes. Variable axes: optical size 9–144, weight 100–900, SOFT 0–100, WONK 0–1; roman and italic. Undercase Type (Phaedra Charles, Flavia Zimbardi) · SIL Open Font License 1.1.")
    p1 += row("<b>Display</b>300 Light · opsz 144<br>46 pt · lh 1.02 · −0.015 em", '<p class="fr big">Experiential design you can walk <span class="lit">into.</span></p>', top=True)
    p1 += row("<b>Weight range</b>100 – 900 (variable)<br><i>300 is the only weight in use</i>", f'<div class="glyph-row">{glyphs}</div><p class="doc-small muted mt-3" style="max-width:120mm">The brand uses Light alone. The rest of the range is shown so it can be recognised — and declined. Fraunces is never set bold, never letter-spaced, and never below 16 px / 9 pt.</p>', top=True)
    cmp = ""
    for o, note in [(36, "below 24 px · text and captions-sized serif"), (72, "24–48 px · titles, h1, h2, quotes"), (144, "above 48 px · display, stats, covers")]:
        cmp += f'<div><p class="fr" style="font-size:26pt;line-height:1.08;font-variation-settings:\'opsz\' {o},\'SOFT\' 30,\'WONK\' 0">Eight rooms, lit.</p><div class="c"><i>opsz {o}</i> · {note}</div></div>'
    p1 += row("<b>Optical size</b>the same 26 pt, three opsz values<br>contrast and spacing change, the size does not", f'<div class="cmp">{cmp}</div>', top=True)
    p1 += row("<b>Headline mechanics</b>sentence case · full stop<br>last word .lit or .dim, never both",
              '<p class="fr" style="font-size:22pt;line-height:1.12;font-variation-settings:\'opsz\' 72,\'SOFT\' 30">A method for the <span class="lit">monumental.</span></p>'
              '<p class="fr" style="font-size:22pt;line-height:1.12;font-variation-settings:\'opsz\' 72,\'SOFT\' 30;margin-top:2mm">Between two points of <span class="dim">light.</span></p>', top=True)

    soft = "".join(f'<div><p class="fr" style="font-size:30pt;line-height:1;font-variation-settings:\'opsz\' 144,\'SOFT\' {s},\'WONK\' 0">Sanzeed</p><div class="c">{"<i>SOFT " + str(s) + "</i> · brand setting" if s == 30 else "SOFT " + str(s)}</div></div>' for s in (0, 30, 100))
    wonk = "".join(f'<div><p class="fr" style="font-size:30pt;line-height:1;font-variation-settings:\'opsz\' 144,\'SOFT\' 30,\'WONK\' {w}">Galleries</p><div class="c">{"<i>WONK 0</i> · brand setting" if w == 0 else "WONK 1 · wonky alternates, never used"}</div></div>' for w in (0, 1))
    p2 = page_head("Type specimen · 01 of 03 · Display serif", "Fraunces, italic and <span class='dim'>axes.</span>")
    p2 += row("<b>Italic</b>300 Light Italic · opsz 72 · SOFT 50<br>22 pt · lh 1.3 — pull quotes only",
              f'<p class="doc-quote" style="font-size:22pt">{QUOTE}</p><p class="doc-caption mt-2">— Sanzeed Mirza</p>', top=True)
    p2 += row("<b>SOFT axis</b>softens the serifs and terminals<br>the brand sits at 30 (50 in italic quotes)", f'<div class="cmp">{soft}</div>', top=True)
    p2 += row("<b>WONK axis</b>switches to quirkier lowercase alternates<br>fixed at 0 everywhere", f'<div class="cmp" style="grid-template-columns:1fr 1fr">{wonk}</div>', top=True)
    stats = "".join(f'<div><div class="n">{n}<span class="plus">+</span></div><div class="l">{l}</div></div>' for n, l in [("15", "years of experience"), ("8", "years experiential &amp; museum"), ("90", "projects directed"), ("60", "museums &amp; centres")])
    p2 += row("<b>Numerals</b>300 · opsz 144 · tnum<br>the plus sign is gold", f'<div class="stat-row">{stats}</div>', top=True)
    p2 += row("<b>Rules</b>from typography-tokens.json", '<ul class="rule-list"><li>Fraunces is always weight 300 (Light); use opsz 144 above 48 px, 72 for 24–48 px, 36 below.</li><li>Headlines are sentence case and end with a full stop. The last word may be set in gold (.lit) or Mist (.dim) — never both in one composition.</li><li>Never letter-space Fraunces; never set it below 16 px / 9 pt.</li><li>Italic is reserved for pull quotes and the personal line.</li></ul>', top=True)
    p2 += row("<b>Character set</b>Latin, Latin Extended-A, punctuation, ₹ (woff2 subset); arrows are set in Inter", '<p class="fr charset sm" style="font-variation-settings:\'opsz\' 36,\'SOFT\' 30">ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789 ₹ &amp; @ § ¶ . , ; : ! ? ‘ ’ “ ” — – ( ) [ ] / ÀÉÎÕÜ àéîõü ß ç ñ</p>', top=True)
    html = head("Sanzeed — Fraunces specimen", "Type specimen") + page(p1, "Fraunces · display serif") + page(p2, "Fraunces · display serif") + FOOT
    write("sanzeed-type-specimen--fraunces.html", html)

# ---------------------------------------------------------------- 02 Inter Tight
def inter_tight():
    body = page_head("Type specimen · 02 of 03 · Heading sans", "Inter Tight.",
                     "The working sans for headings, labels, eyebrows, counters and data. Weight 600 for H3/H4, eyebrows and labels; 500 for tables, counters and figures. Variable weight axis 100–900; roman and italic. Rasmus Andersson · SIL Open Font License 1.1.")
    rows = ""
    names = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}
    use = {400: "not used (Inter covers text)", 500: "data, tables, counters, wall-label meta", 600: "H3, H4, eyebrows, labels, table heads — the default", 700: "optional emphasis in UI only", 800: "shown for recognition; not in the system"}
    for w in (400, 500, 600, 700, 800):
        rows += f'<div class="spec-row" style="padding:2.4mm 0"><div class="lbl"><b>{w} {names[w]}</b>{use[w]}</div><p class="it" style="font-weight:{w};font-size:16pt;line-height:1.2;letter-spacing:-0.01em">Museum &amp; Cultural Exhibition Planning</p></div>'
    body += rows
    trk = ""
    for ls, note in [("0", "0 — too tight for caps"), ("0.08em", "+0.08 em — counters"), ("0.12em", "<i>+0.12 em — eyebrows</i>")]:
        trk += f'<div><p class="it" style="font-weight:600;font-size:9pt;letter-spacing:{ls};text-transform:uppercase;color:var(--accent-text)">Now showing</p><div class="c">{note}</div></div>'
    trk2 = ""
    for ls, note in [("0.04em", "+0.04 em — never on headings"), ("0", "0"), ("-0.01em", "<i>−0.01 em — brand headings</i>")]:
        trk2 += f'<div><p class="it" style="font-weight:600;font-size:16pt;line-height:1.15;letter-spacing:{ls}">Calm leadership</p><div class="c">{note}</div></div>'
    body += row("<b>Tracking · caps</b>letter-spaced caps only for eyebrows and counters", f'<div class="cmp">{trk}</div>', top=True)
    body += row("<b>Tracking · headings</b>slightly negative at size", f'<div class="cmp">{trk2}</div>', top=True)
    eyebrows = " &nbsp;·&nbsp; ".join(f'<span class="eyebrow" style="font-size:7pt">{e}</span>' for e in ["Now showing", "Services", "Method", "Galleries", "About", "Journey", "Get in touch"])
    counters = " ".join(f'<span class="counter" style="font-size:7.5pt;margin-right:5mm">{c}</span>' for c in ["001", "002", "003", "Step 01", "Step 02"])
    body += row("<b>In use</b>eyebrows 7 pt / 12 px caps<br>counters 001 · Step 01 · tnum<br>wall-label title 600", f'<p>{eyebrows}</p><p class="mt-2">{counters}</p>'
                '<div class="wall-label mt-2"><span class="title">Prime Minister Museum</span><span class="place">New Delhi</span></div>', top=True)
    body += row("<b>Rules</b>", '<ul class="rule-list" style="columns:2;column-gap:8mm"><li>Inter Tight is for headings and labels (600) and data (500); Inter for everything read.</li><li>Never use Inter Tight below 11 px.</li><li>Tabular numerals in every table, invoice, quotation and stat.</li><li>Letter-spaced caps only for eyebrows and counters.</li></ul>', top=True)
    html = head("Sanzeed — Inter Tight specimen", "Type specimen") + page(body, "Inter Tight · heading sans") + FOOT
    write("sanzeed-type-specimen--inter-tight.html", html)

# ---------------------------------------------------------------- 03 Inter
def inter():
    body = page_head("Type specimen · 03 of 03 · Text sans", "Inter.",
                     "Everything that is read: body copy, lead paragraphs, captions, forms, buttons and navigation. Weight 400 for text, 500 for UI, 600 for emphasis. Variable axes: optical size 14–32 and weight 100–900. Rasmus Andersson · SIL Open Font License 1.1.")
    for w, name, u, txt in [(400, "Regular", "body, lead, captions, wall labels", ABOUT), (500, "Medium", "buttons, inputs, navigation, UI", "Tell me about the room. A few lines are enough. I reply within two working days. If it is urgent, WhatsApp is fastest."), (600, "SemiBold", "emphasis inside text; never for headings", "Available for new projects and collaborations. <strong>The first conversation is always free.</strong>")]:
        body += f'<div class="spec-row top"><div class="lbl"><b>{w} {name}</b>{u}</div><p class="in" style="font-weight:{w};font-size:10pt;line-height:1.45;max-width:66ch">{txt}</p></div>'
    ops = ""
    for o, note in [(14, "<i>opsz 14</i> — text: wider spacing, open apertures"), (32, "opsz 32 — display: tighter, taller x-height")]:
        ops += f'<div><p class="in" style="font-size:20pt;line-height:1.15;font-variation-settings:\'opsz\' {o}">Tell me about the room.</p><div class="c">{note}</div></div>'
    body += row("<b>Optical size</b>auto by size (font-optical-sizing)<br>shown fixed at the same 20 pt", f'<div class="cmp" style="grid-template-columns:1fr 1fr">{ops}</div>', top=True)
    nums = [("Museums &amp; Experience Centres", "60"), ("Projection Mapping &amp; Shows", "15"), ("Explainer Videos &amp; Others", "15"), ("All galleries", "90")]
    def tbl(feat, label):
        r = "".join(f'<tr><td>{a}</td><td class="num">{b}</td><td class="num">{d}</td></tr>' for (a, b), d in zip(nums, ["2018 – 2026", "2011 – 2016", "2017 – 2018", "2011 – 2026"]))
        return f'<div><table class="doc compact" style="font-variant-numeric:{feat}"><thead><tr><th>Gallery</th><th class="num">Count</th><th class="num">Years</th></tr></thead><tbody>{r}</tbody></table><div class="c">{label}</div></div>'
    body += row("<b>Tabular numerals</b>font-variant-numeric: tabular-nums<br>columns of figures align; proportional ones drift", f'<div class="cmp" style="grid-template-columns:1fr 1fr">{tbl("proportional-nums", "proportional-nums — never in tables")}{tbl("tabular-nums", "<i>tabular-nums</i> — every table, invoice and stat")}</div>', top=True)
    body += row("<b>Measure</b>60–72 characters per line<br>10 pt / 1.45 in documents, 17 px / 1.6 on screen",
                '<div style="max-width:66ch"><div class="ruler mb-2"><span>66 ch</span></div><p>Off the spine, each gallery changes its mood to its subject: wood and light for one era, screens and sound for another. Guides stand at the thresholds; planting softens the floor so the passage reads as a walk rather than a hall.</p><p class="doc-caption mt-2">Prime Minister Museum · New Delhi · The walk</p></div>', top=True)
    html = head("Sanzeed — Inter specimen", "Type specimen") + page(body, "Inter · text sans") + FOOT
    write("sanzeed-type-specimen--inter.html", html)

# ---------------------------------------------------------------- 04 Hierarchy
SAMPLES = {
    "display-1": "Vision you can walk <span class='lit'>into.</span>",
    "display-2": "Eight rooms, <span class='lit'>lit.</span>",
    "h1": "A method for the monumental.",
    "h2": "Galleries planned as a route, not a floor plan.",
    "h3": "Immersive Storytelling &amp; Narrative Architecture",
    "h4": "Creative Director · Tagbin · Jun 2018 – Jul 2026",
    "lead": "Every environment begins as a question and ends as a memory. The path between is deliberate — equal parts strategy and craft, ambition and discipline.",
    "body": "The spine of the museum is a single long passage under a tricolour canopy. Visitors meet one Prime Minister at a time, in sequence, so the building itself tells the story of the office before any gallery does.",
    "small": "Available for new projects and collaborations. The first conversation is always free.",
    "caption": "Ram Katha Show · Ayodhya · The building is the screen.",
    "eyebrow": "Now showing",
    "ui": "Write in the visitor's book →",
    "stat": "90<span class='plus'>+</span>",
    "quote": "The script comes first. Every room, screen and surface carries a line of it.",
    "data": "01 Discover · research deck · 4 weeks · ₹25 lakh – ₹1 crore",
    "editorial": "Scenes move from the central shrine outwards along the galleries; the gilded ceiling becomes sky, then forest, then fire.",
    "counter": "001 · 002 · 003 · Step 04",
}

def style_for(tok, size_idx="desktop"):
    t = SC[tok]
    size, lh = t[size_idx]
    fam = {"Fraunces": "var(--font-display)", "Inter Tight": "var(--font-heading)", "Inter": "var(--font-text)"}[t["family"]]
    s = f"font-family:{fam};font-weight:{t['weight']};font-size:{size}px;line-height:{lh};letter-spacing:{t['tracking'].replace('+','')};"
    if t.get("opsz"): s += f"font-variation-settings:'opsz' {t['opsz']},'SOFT' {50 if t.get('style')=='italic' else 30},'WONK' 0;"
    if t.get("style") == "italic": s += "font-style:italic;"
    if t.get("features") == "tnum": s += "font-variant-numeric:tabular-nums;"
    if t.get("case") == "uppercase": s += "text-transform:uppercase;"
    if tok in ("eyebrow", "counter"): s += "color:var(--accent-text);"
    if tok in ("lead",): s += "color:var(--fg-2);"
    if tok in ("caption",): s += "color:var(--fg-3);"
    if tok == "ui": s += "display:inline-block;padding:14px 22px;border-radius:999px;background:var(--btn);color:var(--btn-fg);"
    return s

def hierarchy():
    def rows(toks):
        out = ""
        for tok in toks:
            t = SC[tok]
            d = t["desktop"]
            extra = f" · opsz {t['opsz']}" if t.get("opsz") else ""
            extra += " · italic" if t.get("style") == "italic" else ""
            extra += " · tnum" if t.get("features") == "tnum" else ""
            lbl = f"<b>{tok}</b>{t['family']} {t['weight']}{extra}<br>{d[0]} px / {d[1]} · {t['tracking']}<br><span style='color:var(--fg-3)'>{t['use']}</span>"
            out += f'<div class="hier"><div class="lbl">{lbl}</div><div style="{style_for(tok)}">{SAMPLES[tok]}</div></div>'
        return out
    p1 = page_head("Hierarchy · 01 of 03", "The scale, in <span class='dim'>order.</span>", "Every level of the type system at its desktop pixel size (1 px = 0.75 pt on this sheet), each set in a line from the headline bank or the site. Screen sizes from typography-tokens.json; print sizes on the responsive-scale sheet.")
    p1 += rows(["display-1", "display-2", "h1", "h2", "h3", "h4"])
    p2 = page_head("Hierarchy · 02 of 03", "Text and <span class='dim'>labels.</span>")
    p2 += rows(["lead", "body", "small", "caption", "eyebrow", "counter", "ui", "data"])
    p3 = page_head("Hierarchy · 03 of 03", "Voice and <span class='dim'>numbers.</span>")
    p3 += rows(["editorial", "quote", "stat"])
    p3 += '<div class="cols-3 mt-5" style="gap:5mm"><div class="note"><strong>One serif voice per page.</strong> display-1 or display-2 once; h1/h2 for the sections beneath; never two display sizes competing.</div><div class="note"><strong>Hierarchy by size and face, not by colour.</strong> Gold is reserved for the eyebrow, the counter, the plus sign and the lit last word.</div><div class="note"><strong>Scale on screen = scale in print.</strong> 1 px here equals 0.75 pt; the print column (responsive-scale sheet) is a separate, smaller scale for A4 documents.</div></div>'
    html = head("Sanzeed — type hierarchy", "Type hierarchy") + page(p1, "Hierarchy · display and headings") + page(p2, "Hierarchy · text and labels") + page(p3, "Hierarchy · voice and numbers") + FOOT
    write("sanzeed-type-hierarchy.html", html)

# ---------------------------------------------------------------- 05 Responsive scale
def responsive():
    body = page_head("Responsive scale", "Desktop, tablet, <span class='dim'>mobile.</span>", "Pixel sizes and line heights per breakpoint, from typography-tokens.json. The print sizes are on the next page.")
    rows = ""
    for tok, t in SC.items():
        extra = f" · opsz {t['opsz']}" if t.get("opsz") else ""
        extra += " · italic" if t.get("style") == "italic" else ""
        extra += " · tnum" if t.get("features") == "tnum" else ""
        rows += f"<tr><td><strong>{tok}</strong></td><td>{t['family']} {t['weight']}{extra}</td><td class='num'>{t['desktop'][0]} / {t['desktop'][1]}</td><td class='num'>{t['tablet'][0]} / {t['tablet'][1]}</td><td class='num'>{t['mobile'][0]} / {t['mobile'][1]}</td><td class='num'>{t['tracking']}</td></tr>"
    body += f'<table class="doc data compact" style="font-size:8pt"><thead><tr><th>Token</th><th>Family · weight</th><th class="num">Desktop px / lh</th><th class="num">Tablet</th><th class="num">Mobile</th><th class="num">Tracking</th></tr></thead><tbody>{rows}</tbody></table>'
    devs = ""
    for name, idx, w in [("Desktop ≥ 1024 px", "desktop", "1fr"), ("Tablet 640–1023 px", "tablet", "1fr"), ("Mobile < 640 px", "mobile", "1fr")]:
        d2 = SC["display-2"][idx]; bo = SC["body"][idx]; ey = SC["eyebrow"][idx]
        devs += f'<div class="room" style="padding:4mm 5mm;background:var(--card);align-self:stretch"><div class="c" style="font-family:var(--font-heading);font-weight:600;font-size:6.5pt;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-3);margin-bottom:2.5mm">{name}</div><div style="{style_for("eyebrow", idx)}">Now showing</div><div style="{style_for("display-2", idx)};margin-top:1.5mm">Eight rooms, <span class="lit">lit.</span></div><p style="{style_for("body", idx)};margin-top:2mm;color:var(--fg-2)">Open any card for the film.</p></div>'
    body += f'<div class="cols-3 mt-3" style="gap:4mm;grid-template-columns:82mm 48mm 36mm">{devs}</div>'
    p2 = page_head("Responsive scale · print", "On paper, in <span class='dim'>points.</span>", "The print column of typography-tokens.json, used by every A4 / US Letter document, the office templates and this sheet itself. Below, each print token at its true size.")
    samples = [("doc-title", "A method for the monumental."), ("doc-h2", "Galleries planned as a route, not a floor plan."), ("doc-h3", "02 Direct — a concept book and a walkthrough film"), ("doc-body", "Immersion in the subject — its history, intent and audience — until the central story reveals itself. You receive a research deck and the one central story."), ("doc-small", "Available for new projects and collaborations. The first conversation is always free."), ("doc-caption", "Buddha Park · Uttarakhand · A garden of gestures."), ("doc-eyebrow", "Now showing"), ("doc-table", "01 Discover · research deck · 4 weeks · ₹25,00,000"), ("business-card-name", "Sanzeed Mirza"), ("business-card-detail", "+91 7827051270 · sanzeed@gmail.com · sanzeed.com")]
    cls = {"doc-title": "doc-title", "doc-h2": "doc-h2", "doc-h3": "doc-h3", "doc-body": "doc-body", "doc-small": "doc-small", "doc-caption": "doc-caption", "doc-eyebrow": "eyebrow", "doc-table": "it tnum", "business-card-name": "it", "business-card-detail": "in"}
    srows = ""
    for k, s in samples:
        v = PR[k]
        st = ""
        if k == "doc-table": st = "font-weight:500;font-size:9pt;line-height:1.35"
        if k == "business-card-name": st = "font-weight:600;font-size:9pt;line-height:1.2"
        if k == "business-card-detail": st = "font-size:7pt;line-height:1.4"
        srows += f'<div class="hier" style="grid-template-columns:30mm 1fr;padding:1.5mm 0"><div class="lbl"><b>{k}</b>{v[0]}<br>{v[1]} pt / {v[2]}</div><div class="{cls[k]}" style="{st}">{s}</div></div>'
    prow = ""
    for k, v in PR.items():
        if k in ("note", "signage-min-cap-height-mm"): continue
        prow += f"<tr><td><strong>{k}</strong></td><td>{v[0]}</td><td class='num'>{v[1]} pt</td><td class='num'>{v[2]}</td></tr>"
    sg = PR["signage-min-cap-height-mm"]
    prow += "<tr><td><strong>signage cap height</strong></td><td>minimum, by viewing distance</td><td class='num' colspan='2'>" + " · ".join(f"{k}: {v} mm" for k, v in sg.items()) + "</td></tr>"
    p2 += f'<div class="cols-12" style="grid-template-columns:1fr 62mm;gap:8mm"><div>{srows}</div><div><span class="eyebrow">Print scale (A4 / US Letter)</span><table class="doc data compact mt-2" style="font-size:7.5pt"><thead><tr><th>Token</th><th>Face</th><th class="num">pt</th><th class="num">lh</th></tr></thead><tbody>{prow}</tbody></table></div></div>'
    p2 += '<div class="cols-3 mt-3" style="gap:5mm;font-size:8pt"><div class="note"><strong>brand.css</strong> — <span class="mono">.t-*</span> classes use <span class="mono">clamp()</span>; one class works at every screen width.</div><div class="note"><strong>type-scale.css</strong> — <span class="mono">.ts-*</span> set the exact screen tokens with media queries at 1024 and 640 px; <span class="mono">.tp-*</span> carry the print sizes.</div><div class="note"><strong>doc.css</strong> — implements the print column as <span class="mono">.doc-title, .doc-h2, .doc-h3, .doc-caption, .eyebrow, table.doc</span> for every A4 document.</div></div>'
    html = head("Sanzeed — responsive type scale", "Type scale") + page(body, "Responsive scale · screen") + page(p2, "Responsive scale · print") + FOOT
    write("sanzeed-type-responsive-scale.html", html)

# ---------------------------------------------------------------- 06 Pairing
def pairing():
    css = """
.comp{position:relative;border:1px solid var(--line);border-radius:20px;padding:9mm 9mm 8mm;background:var(--bg-2)}
.ann{position:absolute;right:-1mm;transform:translateX(100%);width:30mm;padding-left:3mm;border-left:1px solid var(--accent)}
"""
    body = page_head("Pairing", "Fraunces speaks, <span class='dim'>Inter works.</span>", "One page composition in the editorial system: a serif for what is said, a sans for what is read and used. Callouts on the right name the token for each line.")
    body += f"""
<div class="cols-12 gap-sm" style="grid-template-columns:1fr 34mm;gap:5mm">
 <div class="comp">
  <div class="eyebrow">Case study · Museums &amp; Experience Centres</div>
  <h2 class="doc-title mt-1" style="font-size:26pt">Prime Minister Museum.</h2>
  <p class="doc-lead mt-2" style="font-size:11pt;max-width:120mm">One museum for every Prime Minister of India since 1947, in New Delhi — a building that has to hold schoolchildren and heads of state on the same afternoon.</p>
  <div class="cols-2 mt-3" style="gap:6mm">
   <div>
    <h3 class="doc-h3">The idea</h3>
    <p class="mt-1" style="font-size:9.5pt">A corridor you walk in order. The spine of the museum is a single long passage under a tricolour canopy. Visitors meet one Prime Minister at a time, in sequence, so the building itself tells the story of the office before any gallery does.</p>
    <h3 class="doc-h3 mt-3">What visitors do</h3>
    <p class="doc-editorial mt-1" style="font-size:10.5pt">Visitors walk the whole line of leaders without a map, and come out knowing the order by heart.</p>
   </div>
   <figure class="figure"><div class="plate"><img src="{IMG}/case/prime-minister-museum-03.webp" alt="The tricolour corridor of the Prime Minister Museum"></div><div class="wall-label"><span class="title">Prime Minister Museum</span><span class="place">New Delhi</span><span class="line">003 · The tricolour corridor: one Prime Minister at a time</span></div></figure>
  </div>
  <div class="cols-3 mt-3" style="gap:5mm">
   <div><div class="counter">Type</div><p style="font-size:9pt" class="mt-1">Museums &amp; Experience Centres</p></div>
   <div><div class="counter">Location</div><p style="font-size:9pt" class="mt-1">New Delhi</p></div>
   <div><div class="counter">Role</div><p style="font-size:9pt" class="mt-1">Concept &amp; creative direction</p></div>
  </div>
  <div class="beam mt-3"></div>
  <div class="mt-3" style="display:flex;gap:3mm;align-items:center"><span class="pill solid" style="font-size:10pt;padding:3mm 4.5mm">Tell me about the room →</span><span class="pill ghost" style="font-size:10pt;padding:3mm 4.5mm">See the work</span><span class="doc-caption" style="margin-left:auto">I reply within two working days.</span></div>
 </div>
 <div class="callout" style="display:flex;flex-direction:column;gap:0;padding-top:10mm">
  <div style="margin-top:0">eyebrow · Inter Tight 600 · 7 pt · +0.12 em · Gold Ink</div>
  <div style="margin-top:7mm">doc-title · Fraunces 300 · opsz 72 · 26 pt</div>
  <div style="margin-top:12mm">lead · Inter 400 · 11 pt · Umber</div>
  <div style="margin-top:12mm">h3 · Inter Tight 600 · 11 pt<br>body · Inter 400 · 9.5 pt / 1.45</div>
  <div style="margin-top:14mm">wall label · Inter Tight 600 + Inter 400 · 8 / 7.5 pt</div>
  <div style="margin-top:12mm">editorial · Fraunces 300 · opsz 36 · 10.5 pt / 1.6</div>
  <div style="margin-top:12mm">counter · Inter Tight 500 · +0.08 em · tnum</div>
  <div style="margin-top:10mm">beam · 1 px hairline + the point</div>
  <div style="margin-top:6mm">ui · Inter 500 · pill buttons</div>
 </div>
</div>
<div class="cols-3 mt-3" style="gap:5mm">
 <div class="note"><strong>Serif speaks.</strong> Fraunces carries statements: titles, headlines, stats, quotes, long editorial reading. One serif voice per page.</div>
 <div class="note"><strong>Sans works.</strong> Inter Tight labels and structures; Inter is read and tapped. Neither is ever used for a headline that Fraunces could carry.</div>
 <div class="note"><strong>Never pair with a third face.</strong> No script, no slab, no condensed. The hand-lettered signature is a mark, not a typeface.</div>
</div>"""
    html = head("Sanzeed — type pairing", "Type pairing", css) + page(body, "Pairing · page composition") + FOOT
    write("sanzeed-type-pairing.html", html)

# ---------------------------------------------------------------- 07 Numbers and data
def numbers():
    css = """
.tl{position:relative;height:1px;background:var(--line);margin:16mm 0 22mm}
.tl .pt{position:absolute;top:-2.2px;width:6px;height:6px;border-radius:50%;background:var(--accent);transform:translateX(-50%)}
.tl .lab{position:absolute;top:4mm;transform:translateX(-50%);text-align:center;width:34mm}
.tl .lab .y{font-family:var(--font-heading);font-weight:500;font-size:8pt;font-variant-numeric:tabular-nums;color:var(--fg)}
.tl .lab .r{font-size:7pt;color:var(--fg-3);margin-top:.6mm;line-height:1.3}
.tl .lab.up{top:auto;bottom:4mm}
"""
    body = page_head("Numbers and data", "Figures that <span class='dim'>line up.</span>", "Big numbers in Fraunces 300, tables in Inter Tight 500, both with tabular numerals. Amounts the client must supply are bracketed; nothing here is an invented price.")
    stats = "".join(f'<div><div class="n">{n}<span class="plus">+</span></div><div class="l">{l}</div></div>' for n, l in [("15", "years of experience"), ("8", "years experiential &amp; museum"), ("90", "projects directed"), ("60", "museums &amp; centres")])
    body += f'<div class="stat-row">{stats}</div>'
    body += """
<div class="cols-2 mt-3" style="gap:8mm">
 <div>
  <span class="eyebrow">Quotation · table style</span>
  <table class="doc data mt-2"><thead><tr><th>No.</th><th>Item · you receive</th><th class="num">Qty</th><th class="num">Amount ₹</th></tr></thead>
  <tbody>
   <tr><td>01</td><td>Discover — research deck and the one central story</td><td class="num">1</td><td class="num">[Fee]</td></tr>
   <tr><td>02</td><td>Direct — concept book and walkthrough film</td><td class="num">1</td><td class="num">[Fee]</td></tr>
   <tr><td>03</td><td>Craft — detail drawings, media scripts, prototype room</td><td class="num">1</td><td class="num">[Fee]</td></tr>
   <tr><td>04</td><td>Deliver — built, tested and opened experience</td><td class="num">1</td><td class="num">[Fee]</td></tr>
  </tbody>
  <tfoot><tr><td></td><td>Subtotal · GST [rate] % · Total</td><td></td><td class="num">[Total]</td></tr></tfoot></table>
  <p class="doc-caption mt-2">Quotation no. [Quotation no.] · 5 November 2026 · GSTIN [GSTIN] · Bank [Bank name]</p>
 </div>
 <div>
  <span class="eyebrow">Budget bands · enquiry form</span>
  <table class="doc data mt-2"><thead><tr><th>Band</th><th class="num">From</th><th class="num">To</th></tr></thead>
  <tbody>
   <tr><td>Under ₹25 lakh</td><td class="num">—</td><td class="num">₹25,00,000</td></tr>
   <tr><td>₹25 lakh – ₹1 crore</td><td class="num">₹25,00,000</td><td class="num">₹1,00,00,000</td></tr>
   <tr><td>₹1 – 5 crore</td><td class="num">₹1,00,00,000</td><td class="num">₹5,00,00,000</td></tr>
   <tr><td>Over ₹5 crore</td><td class="num">₹5,00,00,000</td><td class="num">—</td></tr>
  </tbody></table>
  <span class="eyebrow mt-4" style="display:block">The galleries · counts</span>
  <table class="doc data compact mt-2"><thead><tr><th>Gallery</th><th class="num">Projects</th><th class="num">Share</th></tr></thead>
  <tbody>
   <tr><td>Museums &amp; Experience Centres</td><td class="num">60</td><td class="num">66.7 %</td></tr>
   <tr><td>Projection Mapping &amp; Shows</td><td class="num">15</td><td class="num">16.7 %</td></tr>
   <tr><td>Explainer Videos &amp; Others</td><td class="num">15</td><td class="num">16.7 %</td></tr>
  </tbody><tfoot><tr><td>All</td><td class="num">90</td><td class="num">100 %</td></tr></tfoot></table>
 </div>
</div>
<span class="eyebrow mt-4" style="display:block">Timeline · points on a beam</span>
<div class="tl">
 <div class="pt" style="left:2%"></div><div class="lab" style="left:2%;transform:none;text-align:left;width:40mm"><div class="y">Sep 2011 – Dec 2016</div><div class="r">Lead Concept Artist · Broadcast2world<br>VFX Artist · Prime Focus (in parallel)</div></div>
 <div class="pt" style="left:40%"></div><div class="lab up" style="left:40%"><div class="y">Feb 2017 – Mar 2018</div><div class="r">Creative Director · SocioPixels</div></div>
 <div class="pt" style="left:52%"></div><div class="lab" style="left:52%"><div class="y">Apr – May 2018</div><div class="r">Creative Head · Digital Web Solutions</div></div>
 <div class="pt" style="left:66%"></div><div class="lab up" style="left:66%"><div class="y">Jun 2018 – Jul 2026</div><div class="r">Creative Director · Tagbin</div></div>
 <div class="pt" style="left:97%;background:var(--accent);box-shadow:0 0 0 2px var(--bg),0 0 0 3px var(--accent)"></div><div class="lab" style="left:97%;transform:translateX(-100%);text-align:right;width:40mm"><div class="y">Aug 2026 – present</div><div class="r">Experiential Design Consultant · Independent</div></div>
</div>
<div class="cols-3 mt-3" style="gap:5mm">
 <div class="note"><strong>Dashes.</strong> En dash with spaces for ranges (2018 – 2026); spaced em dash in running text. Dates read "5 November 2026" in documents, "Aug 2026 — Present" in the timeline.</div>
 <div class="note"><strong>Currency.</strong> ₹ with Indian grouping: ₹25 lakh, ₹1 crore; in tables ₹25,00,000 with tabular numerals, right-aligned.</div>
 <div class="note"><strong>Counters.</strong> Three digits (001), steps as "Step 01". Set in Inter Tight 500, +0.08 em, Gold Ink on light and Lamp Gold on dark.</div>
</div>"""
    html = head("Sanzeed — numbers and data", "Numbers and data", css) + page(body, "Numbers and data") + FOOT
    write("sanzeed-type-numbers-data.html", html)

# ---------------------------------------------------------------- 08 Editorial
def editorial():
    body = page_head("Editorial", "The building is the <span class='lit'>screen.</span>", "Case-study text set in the editorial style: Fraunces 300 at optical size 36, 11 pt on 1.6, measure 60–72 characters, a serif pull quote in italic. Copy from the Ram Katha Show case study on sanzeed.com.")
    body += f"""
<div class="cols-12" style="grid-template-columns:1fr 60mm;gap:9mm">
 <div>
  <div class="eyebrow">Case study · Projection Mapping &amp; Shows · Ayodhya</div>
  <h3 class="doc-h3 mt-3">The brief</h3>
  <p class="doc-editorial mt-1">A night show for Ayodhya that tells the Ram Katha without a stage or actors — the audience is seated in front of a great hall, and the story has to come out of the architecture itself.</p>
  <h3 class="doc-h3 mt-3">The idea</h3>
  <p class="doc-editorial mt-1">Every dome, arch and column of the hall was mapped and painted with light, so the story seems to rise from the stone. Scenes move from the central shrine outwards along the galleries; the gilded ceiling becomes sky, then forest, then fire.</p>
  <div class="pull-quote mt-4"><p class="doc-quote" style="font-size:19pt">Visitors sit in the dark and watch a building they know by day become the story by night.</p><cite>What visitors do · Ram Katha Show</cite></div>
  <h3 class="doc-h3 mt-4">The walk</h3>
  <p class="doc-editorial mt-1">Projection, sound and timing were composed as one score: the beats of the narration cue the light, and the architecture's own rhythm (arch after arch) sets the pace of the scenes.</p>
 </div>
 <div>
  <figure class="figure"><div class="plate"><img src="{IMG}/case/ram-katha-show-06.webp" alt="The ceiling of the hall becomes the sky"></div><div class="wall-label"><span class="title">Ram Katha Show</span><span class="place">Ayodhya</span><span class="line">006 · The ceiling becomes the sky</span></div></figure>
  <figure class="figure mt-4"><div class="plate"><img src="{IMG}/case/ram-katha-show-04.webp" alt="The hall in darkness: the floor mandala wakes first"></div><div class="wall-label"><span class="title">Ram Katha Show</span><span class="place">Ayodhya</span><span class="line">004 · The hall in darkness: the floor mandala wakes first</span></div></figure>
  <div class="kv mt-4" style="grid-template-columns:18mm 1fr"><dt>Type</dt><dd>Projection Mapping &amp; Shows</dd><dt>Location</dt><dd>Ayodhya</dd><dt>Role</dt><dd>Show concept &amp; direction</dd></div>
  <div class="note mt-4"><strong>When to use the editorial style.</strong> Long-form reading where a serif voice is wanted: case-study narrative, brochure body, the brand story. Not for UI, tables or anything under 9 pt — those stay in Inter.</div>
 </div>
</div>"""
    html = head("Sanzeed — editorial style", "Editorial style") + page(body, "Editorial") + FOOT
    write("sanzeed-type-editorial.html", html)

# ---------------------------------------------------------------- 09 Character set
def charset():
    U = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; L = "abcdefghijklmnopqrstuvwxyz"; N = "0123456789"
    P = "₹ $ € £ % ‰ &amp; @ # § ¶ † * . , ; : … ! ? ¿ ¡ ‘ ’ “ ” ‚ „ ‹ › « » ' \" - – — _ ( ) [ ] { } / \\ | ¦ + − × ÷ = ≠ ≈ &lt; &gt; ≤ ≥ ± ° ′ ″ ← ↑ → ↓ ↗ ↘ © ® ™ · • ¬"
    D = "ÀÁÂÃÄÅÆ Ç ÈÉÊË ÌÍÎÏ Ð Ñ ÒÓÔÕÖØ Œ Š ÙÚÛÜ Ý Ÿ Ž Þ ß àáâãäåæ ç èéêë ìíîï ð ñ òóôõöø œ š ùúûü ý ÿ ž þ ā ē ī ō ū ă ğ ı ł ń ś ź ż ć č ď ě ň ř ť ů"
    def block(name, fam, w, extra="", note="", punct=P):
        s = f"font-family:{fam};font-weight:{w};{extra}"
        return f"""<div class="spec-row top"><div class="lbl"><b>{name}</b>{note}</div><div>
<p class="charset" style="{s}">{U}</p><p class="charset" style="{s}">{L}</p>
<p class="charset" style="{s}">{N} <span class="tnum">{N}</span> <span style="font-variant-numeric:oldstyle-nums">{N}</span></p>
<p class="charset sm" style="{s}">{punct}</p><p class="charset sm" style="{s}">{D}</p></div></div>"""
    PF = P.replace("← ↑ → ↓ ↗ ↘ ", "")   # Fraunces carries no arrows; the system sets arrows in Inter
    body = page_head("Character set", "Every glyph the subsets <span class='dim'>carry.</span>", "The woff2 web subsets cover Latin, Latin Extended-A, general punctuation and the rupee sign; Inter and Inter Tight also carry the arrows (Fraunces does not — arrows in a serif line are set in Inter). The TTFs installed for desktop work carry the full character sets. Numerals are shown proportional, tabular and old-style.")
    body += block("Fraunces", "var(--font-display)", 300, "font-variation-settings:'opsz' 36,'SOFT' 30,'WONK' 0;", "300 · opsz 36 · roman<br>no arrows — set them in Inter", PF)
    body += block("Fraunces Italic", "var(--font-display)", 300, "font-style:italic;font-variation-settings:'opsz' 36,'SOFT' 50,'WONK' 0;", "300 · opsz 36 · italic", PF)
    body += block("Inter Tight", "var(--font-heading)", 600, "", "600 SemiBold")
    body += block("Inter", "var(--font-text)", 400, "", "400 Regular")
    html = head("Sanzeed — character set", "Character set") + page(body, "Character set") + FOOT
    write("sanzeed-type-character-set.html", html)

# ---------------------------------------------------------------- 10 Type in the UI
def ui():
    def panel(theme, wm_colour, label):
        return f"""
<div class="ui-panel {theme}" style="background:var(--bg);color:var(--fg)">
 <div class="ui-nav">{logo("primary-wordmark", wm_colour, "24mm")}<ul><li>Now showing</li><li>Services</li><li>Method</li><li>Galleries</li><li>About</li><li>Contact</li></ul><span class="pill solid" style="font-size:8pt;padding:2.4mm 3.5mm">Get in touch</span></div>
 <div class="cols-12 mt-3" style="grid-template-columns:1fr 52mm 46mm;gap:6mm">
  <div>
   <div class="eyebrow">Now showing</div><h2 class="fr mt-1" style="font-size:22pt;line-height:1.08;font-variation-settings:'opsz' 72,'SOFT' 30">Eight rooms, <span class="lit">lit.</span></h2><p class="mt-1" style="font-size:8.5pt;color:var(--fg-2);max-width:60mm">Selected museums, pavilions, memorials and shows. Open any card for the film and the wall label.</p>
   <div class="mt-3" style="display:flex;gap:2.5mm;align-items:center;flex-wrap:wrap"><span class="pill solid" style="font-size:8pt;padding:2.4mm 3.5mm">Write in the visitor's book →</span><span class="pill ghost" style="font-size:8pt;padding:2.4mm 3.5mm">See the work</span></div>
  </div>
  <div class="ui-card"><img src="{IMG}/buddha-park.webp" alt="Buddha Park, Uttarakhand"><div class="body"><div class="cat">Museums &amp; Experience Centres · <b>Case study</b></div><div class="t">Buddha Park</div><div class="p">Uttarakhand</div></div></div>
  <div>
   <span class="flabel" style="font-size:8pt">Type of project</span><div class="field focus" style="font-size:9pt;padding:2.6mm 3.2mm;color:var(--fg)">Museum or experience centre</div>
   <div class="ui-tags mt-3"><span>Experiential Design</span><span>Museum Planning</span><span>Immersive Storytelling</span><span>Event Production</span></div>
  </div>
 </div>
 <div class="beam mt-3"></div>
 <div class="mt-2" style="display:flex;justify-content:space-between;align-items:baseline"><span class="fr" style="font-size:10pt;font-variation-settings:'opsz' 36,'SOFT' 30">Vision you can walk into.</span><span class="doc-caption">{label}</span></div>
</div>"""
    body = page_head("Type in the UI", "Read it, then <span class='dim'>tap it.</span>", "The same components in the dark gallery and on the light label: nav and buttons Inter 500 · 15 px, card title Inter Tight 600 · 18 px, label 13 px, input 15 px, tags 13 px, eyebrow 12 px caps.")
    body += f'<div class="stack" style="--gap:5mm">{panel("theme-dark", "full-colour-dark", "Dark theme · Gallery Black · Lamp Gold")}{panel("theme-light", "full-colour-light", "Light theme · Plaster · Gold Ink / Old Gold")}</div>'
    body += '<p class="doc-caption mt-2">Pills radius 999, padding 14 × 22 px, ≥ 44 px tall · focus ring = accent at 25 % · tags are hairline pills in fg-2 · dark uses Lamp Gold, light uses Gold Ink for text and Old Gold for the point.</p>'
    html = head("Sanzeed — type in the UI", "Type in the UI") + page(body, "Type in the UI") + FOOT
    write("sanzeed-type-ui.html", html)

# ---------------------------------------------------------------- type-scale.css
def type_scale_css():
    fam = {"Fraunces": "var(--font-display, \"Fraunces\", Georgia, serif)", "Inter Tight": "var(--font-heading, \"Inter Tight\", Arial, sans-serif)", "Inter": "var(--font-text, \"Inter\", Arial, sans-serif)"}
    out = ["/* SANZEED — type-scale.css  (generated by Typography_Specimens/src/build_specimens.py from typography-tokens.json)",
           "   Stepped export of the type scale: .ts-<token> for screen (desktop → tablet ≤ 1023 px → mobile ≤ 639 px)",
           "   and .tp-<token> for print documents in points. brand.css already provides the fluid clamp() versions",
           "   as .t-<token>; use this file where clamp() is unavailable (email, office tools, design handoff) or when",
           "   exact breakpoint values are required. Colours and families come from brand.css / colour-variables.css. */", ""]
    def decl(tok, t, idx):
        size, lh = t[idx]
        return f"  font-size: {size}px; line-height: {lh};"
    for tok, t in SC.items():
        props = [f"  font-family: {fam[t['family']]};", f"  font-weight: {t['weight']};", f"  letter-spacing: {t['tracking'].replace('+','')};", decl(tok, t, "desktop")]
        if t.get("opsz"): props.append(f"  font-variation-settings: \"opsz\" {t['opsz']}, \"SOFT\" {50 if t.get('style')=='italic' else 30}, \"WONK\" 0;")
        if t.get("style") == "italic": props.append("  font-style: italic;")
        if t.get("features") == "tnum": props.append("  font-variant-numeric: tabular-nums;")
        if t.get("case") == "uppercase": props.append("  text-transform: uppercase;")
        if tok in ("eyebrow", "counter"): props.append("  color: var(--accent-text);")
        if tok == "lead": props.append("  color: var(--fg-2);")
        if tok == "caption": props.append("  color: var(--fg-3);")
        out.append(f"/* {tok}: {t['use']} */")
        out.append(f".ts-{tok} {{\n" + "\n".join(props) + "\n}")
    out.append("\n@media (max-width: 1023px) {")
    for tok, t in SC.items():
        if t["tablet"] != t["desktop"]: out.append(f"  .ts-{tok} {{ font-size: {t['tablet'][0]}px; line-height: {t['tablet'][1]}; }}")
    out.append("}\n@media (max-width: 639px) {")
    for tok, t in SC.items():
        if t["mobile"] != t["tablet"]: out.append(f"  .ts-{tok} {{ font-size: {t['mobile'][0]}px; line-height: {t['mobile'][1]}; }}")
    out.append("}\n\n/* Print scale (A4 / US Letter documents) — typography-tokens.json → print_scale_pt */")
    pf = {"Fraunces": fam["Fraunces"], "Inter Tight": fam["Inter Tight"], "Inter": fam["Inter"]}
    for k, v in PR.items():
        if k in ("note", "signage-min-cap-height-mm"): continue
        face, size, lh = v
        f = "Fraunces" if face.startswith("Fraunces") else ("Inter Tight" if face.startswith("Inter Tight") else "Inter")
        w = re.search(r"\b(\d{3})\b", face).group(1)
        extra = ""
        if "opsz 72" in face: extra += ' font-variation-settings: "opsz" 72, "SOFT" 30, "WONK" 0;'
        elif "opsz 144" in face: extra += ' font-variation-settings: "opsz" 144, "SOFT" 30, "WONK" 0;'
        elif f == "Fraunces": extra += ' font-variation-settings: "opsz" 36, "SOFT" 30, "WONK" 0;'
        if "caps" in face: extra += " text-transform: uppercase; letter-spacing: .12em;"
        if "tnum" in face: extra += " font-variant-numeric: tabular-nums;"
        out.append(f".tp-{k} {{ font-family: {pf[f]}; font-weight: {w}; font-size: {size}pt; line-height: {lh};{extra} }}")
    out.append("\n/* Shared helpers */\n.tnum { font-variant-numeric: tabular-nums; }\n.lit { color: var(--accent); }\n.dim { color: var(--fg-3); }\n")
    (HERE.parent / "type-scale.css").write_text("\n".join(out), encoding="utf-8")
    print("wrote ../type-scale.css")

if __name__ == "__main__":
    fraunces(); inter_tight(); inter(); hierarchy(); responsive(); pairing(); numbers(); editorial(); charset(); ui(); type_scale_css()
