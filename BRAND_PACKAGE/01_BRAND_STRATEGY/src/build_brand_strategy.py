#!/usr/bin/env python3
"""build_brand_strategy.py — lays out the five strategy documents (Brand_Audit.md, Brand_Strategy.md,
Brand_Positioning.md, Brand_Voice_and_Tone.md, Brand_Messaging.md) as one designed A4 document, Brand_Strategy.html,
using the brand kit (brand.css + doc.css). The markdown files are the source of truth: every table, list and paragraph
is converted from them at build time, so the PDF never drifts from the .md text.

    python3 build_brand_strategy.py
    node ../../15_SOURCE_FILES/Project_Files/brand-kit/render.js --in Brand_Strategy.html --out ../Brand_Strategy.pdf --pdf --size 210x297

To change copy: edit the .md files, re-run. To change the page plan (which section goes on which page): edit PAGES below.
Figures: figures/*.jpg are crops of 00_ORIGINAL_ASSETS_BACKUP/site_source/screenshot-*.png (see README.md).
Diagrams: positioning-map.svg (inlined) and the message architecture (HTML/CSS in arch()).
"""
import re, html as H, pathlib

HERE = pathlib.Path(__file__).resolve().parent
B = HERE.parents[1]
KIT = "../../15_SOURCE_FILES/Project_Files/brand-kit"
IMG = "../../00_ORIGINAL_ASSETS_BACKUP/images/img"
MD = {k: (HERE.parent / f).read_text(encoding="utf-8") for k, f in
      [("audit", "Brand_Audit.md"), ("strategy", "Brand_Strategy.md"), ("positioning", "Brand_Positioning.md"),
       ("voice", "Brand_Voice_and_Tone.md"), ("messaging", "Brand_Messaging.md")]}

# ------------------------------------------------------------------ markdown → html (the subset these files use)
def inline(s):
    s = H.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r'<span class="mono">\1</span>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    def tag(m):
        kind, rest = m.group(1), m.group(2).strip(" ,—–-")
        cls = "tag-confirmed" if kind == "Confirmed" else "tag-rec"
        note = f' <span class="tagnote">{rest}</span>' if rest else ""
        return f'<span class="tag {cls}">{kind}</span>{note}'
    s = re.sub(r"\[(Confirmed|Recommendation)([^\]]*)\]", tag, s)
    return s

def table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if not re.match(r"^\s*\|?\s*-{2,}", l)]
    head, body = rows[0], rows[1:]
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    tr = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<table class="doc md"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def md_to_html(text):
    out, i, lines = [], 0, text.split("\n")
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"): j += 1
            out.append(table(lines[i:j])); i = j; continue
        if l.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"): j += 1
            out.append('<pre class="mono code">' + H.escape("\n".join(lines[i+1:j])) + "</pre>"); i = j + 1; continue
        if re.match(r"^\s*[-*] ", l):
            j = i; items = []
            while j < len(lines) and re.match(r"^\s*[-*] ", lines[j]): items.append(re.sub(r"^\s*[-*] ", "", lines[j])); j += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"); i = j; continue
        if re.match(r"^\s*\d+\. ", l):
            j = i; items = []
            while j < len(lines) and re.match(r"^\s*\d+\. ", lines[j]): items.append(re.sub(r"^\s*\d+\. ", "", lines[j])); j += 1
            out.append('<ol class="num">' + "".join(f"<li><span>{inline(x)}</span></li>" for x in items) + "</ol>"); i = j; continue
        if l.startswith(">"):
            j = i; q = []
            while j < len(lines) and lines[j].startswith(">"): q.append(lines[j].lstrip("> ")); j += 1
            out.append(f'<blockquote class="md-quote">{inline(" ".join(q))}</blockquote>'); i = j; continue
        if l.strip() == "" or l.strip() == "---":
            i += 1; continue
        if l.startswith("#"):
            i += 1; continue
        j = i; para = []
        while j < len(lines) and lines[j].strip() and not re.match(r"^(\||```|#|>|\s*[-*] |\s*\d+\. |---)", lines[j]): para.append(lines[j].strip()); j += 1
        out.append(f"<p>{inline(' '.join(para))}</p>"); i = j
    return "\n".join(out)

def sections(text):
    """Split a markdown file into {heading: body} (any heading level); body runs to the next heading."""
    parts, cur, buf = {}, "_intro", []
    for l in text.split("\n"):
        m = re.match(r"^(#{1,4})\s+(.*)$", l)
        if m:
            parts[cur] = "\n".join(buf); cur = m.group(2).strip(); buf = []
        else:
            buf.append(l)
    parts[cur] = "\n".join(buf)
    return parts

SEC = {k: sections(v) for k, v in MD.items()}

def S(doc, prefix, title=None, level="h2"):
    """Render a section: heading (number + title from the md) and converted body."""
    key = next(k for k in SEC[doc] if k.startswith(prefix))
    body = md_to_html(SEC[doc][key])
    t = inline(key if title is None else title)
    hcls = {"h2": "doc-h2", "h3": "doc-h3", "none": ""}[level]
    h = "" if level == "none" else f'<h2 class="{hcls} sec-h">{t}</h2>'
    return f'<div class="sec">{h}{body}</div>'

def body_of(doc, prefix):
    key = next(k for k in SEC[doc] if k.startswith(prefix))
    return md_to_html(SEC[doc][key])

# ------------------------------------------------------------------ helpers
def logo(variant="primary-wordmark", colour="full-colour-dark", width="64mm"):
    svg = open(B / f"02_LOGO_SYSTEM/SVG/sanzeed-{variant}--{colour}.svg", encoding="utf-8").read()
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return f'<div class="wordmark" style="width:{width}">{svg}</div>'

def svgfile(name, width="100%"):
    svg = (HERE / name).read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return f'<div style="width:{width}">{svg}</div>'

def fig(src, title, place, note="", cls=""):
    return f'<figure class="figure {cls}"><div class="plate"><img src="{src}" alt="{H.escape(title)} — {H.escape(place)}"></div><div class="wall-label"><span class="title">{title}</span><span class="place">{place}</span>{f"<span class=line>{note}</span>" if note else ""}</div></figure>'

def page(body, section, cls=""):
    return f'<section class="page {cls}" data-section="{section}">\n{body}\n</section>\n'

def phead(eyebrow, title, lead=""):
    l = f'<p class="doc-lead">{lead}</p>' if lead else ""
    return f'<div class="page-head"><span class="eyebrow">{eyebrow}</span><h1 class="doc-title">{title}</h1>{l}</div>'

def opener(num, title, lead, items):
    li = "".join(f"<div><span>{n}</span>{t}</div>" for n, t in items)
    return f'<section class="page opener" data-section="{num} · {re.sub("<[^>]+>", "", title)}"><div class="counter-big">{num}</div><h1 class="opener-title">{title}</h1><p class="doc-lead">{lead}</p><div class="beam"></div><div class="opener-list">{li}</div></section>\n'

def pull(text, cite):
    return f'<div class="pull-quote"><p class="doc-quote">{text}</p><cite>{cite}</cite></div>'

CSS = """
.sec+.sec{margin-top:6mm}
.sec-h{margin-bottom:2.5mm}
.sec h2.doc-h2{font-size:15pt}
.sec p{font-size:9pt;line-height:1.5;max-width:160mm}
.sec p+p{margin-top:.8em}
.sec ul,.sec ol{font-size:9pt;line-height:1.5;padding-left:1.2em;margin-top:1mm}
.sec li+li{margin-top:.5mm}
.sec ol.num{list-style:none;padding-left:0;counter-reset:n}
.sec ol.num li{counter-increment:n;display:grid;grid-template-columns:7mm 1fr;gap:2mm}
.sec ol.num li::before{content:counter(n,decimal-leading-zero);font-family:var(--font-heading);font-weight:500;font-size:7pt;letter-spacing:.08em;color:var(--accent-text);padding-top:.8mm;font-variant-numeric:tabular-nums}
table.md{font-size:8pt;line-height:1.4;margin-top:1.5mm}
table.md th{font-size:6.5pt}
table.md td{padding:1.8mm 2.5mm 1.8mm 0}
table.md td:first-child{font-family:var(--font-heading);font-weight:500}
table.md.plain td:first-child{font-family:var(--font-text);font-weight:400}
table.md.tight td{padding:1.3mm 2mm 1.3mm 0;font-size:7.5pt}
.tagnote{font-size:7pt;color:var(--fg-3)}
.md-quote{margin:0;padding:3mm 4mm;border-left:2px solid var(--accent);background:var(--card);font-size:8.5pt;line-height:1.5;border-radius:0 10px 10px 0}
pre.code{white-space:pre-wrap;font-size:7.5pt;line-height:1.55;margin:0;padding:3.5mm 4mm;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:8mm;align-items:start}
.two>*{min-width:0}
.legend{display:flex;gap:6mm;align-items:center;font-size:8pt;color:var(--fg-2);padding:3mm 4mm;border:1px solid var(--line);border-radius:12px;background:var(--card)}
.figs{display:grid;grid-template-columns:1fr 1fr;gap:6mm 6mm}
.figs>*{min-width:0}
.plate img{display:block;width:100%}
.glyphs{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:4mm}
.glyphs .g{border:1px solid var(--line);border-radius:12px;background:#000;height:26mm;position:relative;overflow:hidden}
.glyphs .cap{font-size:7.5pt;color:var(--fg-3);margin-top:1.5mm}
.glyphs .cap b{font-family:var(--font-heading);font-weight:600;color:var(--fg);display:block;font-size:8pt}
.route{border:1px solid var(--line);border-radius:12px;overflow:hidden}
.route .art{height:34mm;position:relative;overflow:hidden}
.small .sec p,.small .sec ul,.small .sec li{font-size:8pt;line-height:1.45}
.route .cap{padding:3mm 3.5mm 3.5mm;background:var(--card)}
.route .cap b{display:block;font-family:var(--font-heading);font-weight:600;font-size:8.5pt}
.route .cap span{font-size:7.5pt;color:var(--fg-3)}
.route .cap .counter{display:block;margin-bottom:1mm}
.arch{position:relative;padding-left:12mm}
.arch::before{content:"";position:absolute;left:4mm;top:3mm;bottom:3mm;width:1px;background:var(--line)}
.arch .row{position:relative;display:grid;grid-template-columns:30mm 1fr auto;gap:4mm;align-items:baseline;padding:2.6mm 0;border-bottom:1px solid var(--line)}
.arch .row::before{content:"";position:absolute;left:-8.8mm;top:50%;width:2.4mm;height:2.4mm;border-radius:50%;background:var(--fg-3);transform:translateY(-50%)}
.arch .row.lit::before{background:var(--accent);box-shadow:0 0 0 2mm rgba(184,134,59,.15)}
.arch .k{font-family:var(--font-heading);font-weight:600;font-size:6.5pt;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-text)}
.arch .v{font-size:9.5pt}
.arch .row.master .v{font-family:var(--font-display);font-weight:300;font-size:16pt;line-height:1.15;font-variation-settings:'opsz' 72,'SOFT' 30}
.elev{display:grid;grid-template-columns:14mm 1fr;gap:3mm;padding:2.5mm 0;border-top:1px solid var(--line);font-size:9pt}
.elev b{font-family:var(--font-heading);font-weight:500;font-size:7pt;letter-spacing:.08em;color:var(--accent-text);font-variant-numeric:tabular-nums;padding-top:.8mm}
.sig{padding:4mm 5mm;border:1px solid var(--line);border-radius:12px;background:var(--card);font-size:8.5pt;line-height:1.55}
.cta-row{display:flex;gap:2.5mm;flex-wrap:wrap}
.cta-row .pill{display:inline-flex;align-items:center;padding:2.4mm 3.6mm;border-radius:999px;font:500 8pt/1 var(--font-text);white-space:nowrap}
.cta-row .solid{background:var(--btn);color:var(--btn-fg)} .cta-row .ghost{border:1px solid var(--line);color:var(--fg)} .cta-row .text{color:var(--accent-text);padding-left:0}
.wordmark svg{display:block;width:100%;height:auto}
.vals li strong{display:block}
"""

def head():
    return f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sanzeed — Brand Strategy</title>
<link rel="stylesheet" href="{KIT}/doc.css">
<style>{CSS}</style>
</head>
<body>
<main class="doc" style="--doc:'Brand Strategy'">
"""

# ------------------------------------------------------------------ pages
P = []

P.append(f"""
<section class="page cover theme-dark grain">
  <div class="cover-top"><span class="eyebrow">Sanzeed Mirza · Experiential Design Consultant</span><span class="eyebrow" style="color:var(--fg-3)">Brand package · 01 Brand strategy</span></div>
  <div class="cover-title"><h1 class="doc-display">Brand <span class="lit">strategy.</span></h1>
  <p class="cover-sub">Audit · Strategy · Positioning · Voice and tone · Messaging. Everything confirmed on sanzeed.com, and everything the agency recommends, kept apart.</p>
  <p class="cover-meta">Version 1.0 · 5 November 2026</p></div>
  <div class="cover-foot">{logo()}<span class="cover-meta">sanzeed.com</span></div>
</section>
""")

TOC = [("001", "Brand audit", "Confirmed facts · strengths · gaps · opportunities · assumptions", 3), ("002", "Brand strategy", "The one idea · vision · values · positioning · personality · audience · story · taglines · creative routes · principles", 12),
       ("003", "Brand positioning", "Statement · map · competitive frame · pillars · proof · naming", 20), ("004", "Voice and tone", "Principles · tone by situation · vocabulary · mechanics", 24), ("005", "Messaging", "Architecture · elevator messages · key messages · headline bank · calls to action", 28)]
toc = "".join(f'<li><span class="n">{n}</span><span class="t">{t}<small>{s}</small></span><span class="p">@@PAGE{n}@@</span></li>' for n, t, s, p in TOC)
P.append(page(phead("Contents", "Five documents, one <span class='dim'>through-line.</span>") + f'<ul class="toc" style="max-width:150mm">{toc}</ul>'
    + '<div class="legend mt-5"><span class="tag tag-confirmed" style="margin:0">Confirmed</span><span>taken verbatim or directly measured from sanzeed.com (fetched 5 November 2026)</span><span class="tag tag-rec" style="margin:0 0 0 4mm">Recommendation</span><span>the agency\'s proposal — a decision for Sanzeed to accept, adjust or reject</span></div>'
    + '<p class="doc-small muted mt-3" style="max-width:150mm">This document lays out the five markdown files in 01_BRAND_STRATEGY without changing their meaning. Tables, lists and labels are converted from the source files at build time; where a diagram replaces a text sketch (the positioning map, the message architecture) the words are the same.</p>', "Contents"))

# ---------------- 001 AUDIT
P.append(opener("001", "Brand <span class='dim'>audit.</span>", "Prepared 5 November 2026 · Subject: Sanzeed Mirza, Experiential Design Consultant · Source of truth: the live website at sanzeed.com (fetched 5 Nov 2026, last modified 21 Oct 2026 per sitemap), its three case-study pages, its vCard, JSON-LD, favicon and inline CSS/JS. This audit separates confirmed facts from assumptions and recommendations; nothing in the confirmed column was invented.",
    [("1", "Confirmed facts"), ("2", "Strengths"), ("3", "Weaknesses and gaps"), ("4", "Opportunities"), ("5", "Assumptions and open questions")]))

P.append(page(phead("001 · Brand audit · 1 Confirmed facts", "Identity and <span class='dim'>business.</span>") + S("audit", "1.1", level="none"), "001 · Brand audit"))
P.append(page(phead("001 · Brand audit · 1 Confirmed facts", "Services and <span class='dim'>method.</span>") + S("audit", "1.2", "1.2 Services (seven, as listed)") + S("audit", "1.3", "1.3 Method (four steps, with stated deliverables)"), "001 · Brand audit"))
P.append(page(phead("001 · Brand audit · 1 Confirmed facts", "Career and <span class='dim'>portfolio.</span>") + '<div class="two">' + S("audit", "1.4", "1.4 Career timeline") + S("audit", "1.5", "1.5 Portfolio") + "</div>"
    + '<div class="figs mt-4" style="grid-template-columns:46mm 46mm 1fr;gap:5mm">' + fig("figures/site-desktop-journey.jpg", "sanzeed.com · Journey", "desktop, 1440 px", "The career timeline as a beam of roles, 2011 to the present") + fig("figures/site-desktop-galleries.jpg", "sanzeed.com · The galleries", "desktop, 1440 px", "90 projects in three galleries, filterable; wall labels under every card") + fig("figures/site-desktop-now-showing.jpg", "sanzeed.com · Now showing", "desktop, 1440 px", "Eight featured rooms as 16:9 cards; the last word of the headline is lit") + "</div>", "001 · Brand audit"))
P.append(page(phead("001 · Brand audit · 1 Confirmed facts", "The site as <span class='dim'>found.</span>", "Screenshots taken 5 November 2026 at 1440 px (desktop) and 390 px (mobile). Each is shown with its wall label, as the site shows its own work.")
    + '<div class="figs" style="grid-template-columns:1fr 30mm;gap:6mm">' + fig("figures/site-desktop-hero.jpg", "sanzeed.com · Hero", "desktop", "The master line as H1 above the three.js sphere; glass header; dark theme by default") + fig("figures/site-mobile-hero.jpg", "sanzeed.com · Hero", "mobile, 390 px", "Same hierarchy, stacked") + "</div>"
    + '<div class="figs mt-3">' + fig("figures/site-desktop-services.jpg", "sanzeed.com · Services", "desktop", "“Between two points of light” — seven services, counters 01–07") + fig("figures/site-desktop-method.jpg", "sanzeed.com · Method", "desktop", "“A method for the monumental” — a scroll-pinned sequence of four steps") + "</div>"
    + '<div class="figs mt-3">' + fig("figures/site-desktop-quote.jpg", "sanzeed.com · Personal quote", "desktop", "Fraunces italic with three lit words — the quote the purpose statement keeps") + fig("figures/site-desktop-contact.jpg", "sanzeed.com · Get in touch", "desktop", "“Let's shape something that endures.” — the three confirmed promises and the visitor's book") + "</div>", "001 · Brand audit"))
P.append(page(phead("001 · Brand audit · 1 Confirmed facts", "Existing visual identity, <span class='dim'>measured.</span>") + S("audit", "1.6", level="none").replace('class="doc md"', 'class="doc md tight"'), "001 · Brand audit"))
P.append(page(phead("001 · Brand audit", "Strengths and <span class='dim'>opportunities.</span>") + S("audit", "2. Strengths", "2 Strengths (evidence-based)") + S("audit", "4. Opportunities", "4 Opportunities"), "001 · Brand audit"))
P.append(page(phead("001 · Brand audit", "Weaknesses and open <span class='dim'>questions.</span>") + S("audit", "3. Weaknesses", "3 Weaknesses and gaps (evidence-based)") + S("audit", "5. Assumptions", "5 Assumptions and open questions (not confirmed by the site)")
    , "001 · Brand audit"))

# ---------------- 002 STRATEGY
P.append(opener("002", "Brand <span class='dim'>strategy.</span>", "Sanzeed Mirza · Experiential Design Consultant · New Delhi · Version 1.0 · 5 November 2026. Everything marked Confirmed is taken from sanzeed.com. Everything marked Recommendation is the agency's proposal and should be read as a decision for Sanzeed to accept, adjust or reject.",
    [("1", "The one idea"), ("2", "Vision, mission, purpose"), ("3", "Values"), ("4", "Positioning"), ("5", "Brand promise"), ("6", "Personality and archetype"), ("7", "Audience"), ("8", "Differentiation and USP"), ("9", "Brand story"), ("10", "Tagline system"), ("11", "Creative direction — three routes"), ("12", "Design principles"), ("13", "What this package does not change")]))

glyphs = """
<div class="glyphs">
 <div><div class="g"><div style="position:absolute;left:50%;top:50%;width:3mm;height:3mm;border-radius:50%;background:#E9B25A;transform:translate(-50%,-50%);box-shadow:0 0 10px rgba(233,178,90,.6),0 0 28px rgba(233,178,90,.3)"></div></div><div class="cap"><b>The point of light</b>the gold dot — in the wordmark, the signature, the lit word, the symbol</div></div>
 <div><div class="g"><div style="position:absolute;left:5mm;right:5mm;top:50%;height:1px;background:rgba(255,255,255,.18)"></div><div style="position:absolute;left:62%;top:50%;width:2.4mm;height:2.4mm;border-radius:50%;background:#E9B25A;transform:translate(-50%,-50%);box-shadow:0 0 8px rgba(233,178,90,.6)"></div></div><div class="cap"><b>The beam</b>the line the dot travels — route, timeline, hairline rule</div></div>
 <div><div class="g"><div style="position:absolute;inset:4mm;border:1px solid rgba(255,255,255,.14);border-radius:8px;background:#1C1C1E"></div></div><div class="cap"><b>The room</b>the dark field — the gallery before the lights come up</div></div>
</div>"""
P.append(page(phead("002 · Brand strategy", "The one <span class='lit'>idea.</span>") + S("strategy", "1. The one idea", level="none") + glyphs
    + '<div class="mt-4">' + pull("Between two points of light. A brief on one side, a visitor on the other. Seven ways to carry the light across.", "sanzeed.com · Services · Confirmed") + "</div>", "002 · Brand strategy"))
P.append(page(phead("002 · Brand strategy", "Vision, mission, purpose and <span class='dim'>values.</span>") + S("strategy", "2. Vision", "2 Vision, mission, purpose") + S("strategy", "3. Values", "3 Values").replace('<ol class="num">', '<ol class="num vals">'), "002 · Brand strategy"))
P.append(page(phead("002 · Brand strategy", "Positioning and <span class='dim'>promise.</span>") + S("strategy", "4. Positioning", "4 Positioning") + S("strategy", "5. Brand promise", "5 Brand promise") + S("strategy", "6. Personality", "6 Personality and archetype"), "002 · Brand strategy"))
P.append(page(phead("002 · Brand strategy", "Audience and <span class='dim'>difference.</span>") + S("strategy", "7. Audience", "7 Audience") + S("strategy", "8. Differentiation", "8 Differentiation and USP"), "002 · Brand strategy"))
P.append(page(phead("002 · Brand strategy", "The brand <span class='dim'>story.</span>") + '<div class="two" style="grid-template-columns:1fr 62mm">' + S("strategy", "9. Brand story", "9 Brand story (long form)").replace("<p>", '<p class="doc-editorial" style="font-size:10pt;max-width:none">')
    + '<div>' + fig(f"{IMG}/case/prime-minister-museum-03.webp", "Prime Minister Museum", "New Delhi", "The tricolour corridor: one Prime Minister at a time") + '<div class="mt-3">' + fig(f"{IMG}/case/ram-katha-show-05.webp", "Ram Katha Show", "Ayodhya", "The story arrives on the walls, scene by scene") + '</div><div class="mt-3">' + fig(f"{IMG}/case/buddha-park-05.webp", "Buddha Park", "Uttarakhand", "The reclining Buddha against the green slope") + "</div></div></div>"
    + '<div class="mt-3">' + pull("The most powerful stories aren't just told — they're felt, lived, and remembered through the spaces we design and the moments we shape.", "Sanzeed Mirza · sanzeed.com · Confirmed").replace('class="doc-quote"', 'class="doc-quote" style="font-size:17pt"') + "</div>", "002 · Brand strategy"))
P.append(page(phead("002 · Brand strategy", "The tagline <span class='dim'>system.</span>") + S("strategy", "10. Tagline", "10 Tagline system") + S("strategy", "11. Creative direction", "11 Creative direction — three routes evaluated"), "002 · Brand strategy"))

routeA = f"""<div class="route"><div class="art" style="background:#000"><div style="position:absolute;inset:0;background:radial-gradient(60% 60% at 50% 40%, rgba(233,178,90,.35) 0%, rgba(233,178,90,.08) 30%, rgba(0,0,0,0) 70%)"></div><img src="{IMG}/prime-minister-museum.webp" alt="Prime Minister Museum" style="position:absolute;left:4mm;top:4mm;width:20mm;border-radius:6px;border:1px solid rgba(255,255,255,.12)"><div style="position:absolute;right:4mm;top:4.5mm;font-family:var(--font-display);font-weight:300;font-size:10.5pt;color:#F5F5F7;line-height:1.05;text-align:right">Eight rooms,<br><span style="color:#E9B25A">lit.</span></div><div style="position:absolute;left:4mm;right:4mm;bottom:12mm;height:1px;background:rgba(255,255,255,.14)"><i style="position:absolute;left:30%;top:-1.5px;width:4px;height:4px;border-radius:50%;background:#E9B25A;box-shadow:0 0 6px rgba(233,178,90,.7)"></i></div><div style="position:absolute;left:4mm;bottom:4mm;width:28mm">{logo("primary-wordmark", "full-colour-dark", "28mm")}</div></div><div class="cap"><span class="counter">Route A · chosen</span><b>The Point of Light</b><span>Black, cream, the gold point; the existing wordmark refined, with a swooping Z and a third point; Fraunces + Inter</span></div></div>"""
routeB = """<div class="route"><div class="art" style="background:#FBF8F2;background-image:linear-gradient(rgba(26,24,22,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(26,24,22,.09) 1px,transparent 1px);background-size:5mm 5mm"><div style="position:absolute;left:8mm;top:8mm;width:30mm;height:20mm;border:1.2px solid #1A1816"></div><div style="position:absolute;left:22mm;top:8mm;width:1.2px;height:20mm;background:#1A1816"></div><div style="position:absolute;left:8mm;top:18mm;width:14mm;height:1.2px;background:#1A1816"></div><div style="position:absolute;left:30mm;top:14mm;width:2.2mm;height:2.2mm;border-radius:50%;background:#C0392B"></div><div style="position:absolute;right:5mm;bottom:5mm;font-family:var(--font-heading);font-weight:700;font-size:9pt;letter-spacing:.08em;color:#1A1816">PLAN 01</div></div><div class="cap"><span class="counter">Route B · rejected</span><b>The Plan</b><span>Ink on paper, blueprint grids, floor-plan devices, a red accent, a grotesque</span></div></div>"""
routeC = """<div class="route"><div class="art" style="background:linear-gradient(120deg,#5B2A86 0%,#C02A7A 35%,#F39A2B 70%,#2BB1C8 100%)"><div style="position:absolute;inset:0;background:radial-gradient(50% 60% at 70% 40%, rgba(255,255,255,.35), transparent 70%)"></div><div style="position:absolute;left:4mm;bottom:4mm;font-family:var(--font-heading);font-weight:800;font-size:17pt;letter-spacing:-.02em;color:#fff;filter:blur(.3px);line-height:.95">SHOW<br>NIGHT</div></div><div class="cap"><span class="counter">Route C · rejected</span><b>Spectacle</b><span>Saturated light gradients, motion-blur type, full-bleed show photography</span></div></div>"""
rc = body_of("strategy", "Route C")
i = rc.find("<p><strong>Decision:")
decision = rc[i:] if i >= 0 else ""
route_c = '<div class="sec"><h2 class="doc-h3 sec-h">Route C — “Spectacle”</h2>' + (rc[:i] if i >= 0 else rc) + "</div>"
P.append(page(phead("002 · Brand strategy · 11 Creative direction", "Three routes, one <span class='lit'>decision.</span>", "Three visual routes were developed to the same depth before choosing. Route A is built here from the real assets of this package; B and C are abstract tiles that stand for the rejected directions.")
    + f'<div class="cols-3" style="gap:5mm">{routeA}{routeB}{routeC}</div>'
    + '<div class="cols-3 mt-3 small" style="gap:5mm">' + S("strategy", "Route A", "Route A — “The Point of Light” (recommended, and chosen)", "h3") + S("strategy", "Route B", "Route B — “The Plan”", "h3") + route_c + "</div>"
    + f'<div class="note mt-4" style="font-size:9pt">{decision}</div>', "002 · Brand strategy"))
P.append(page(phead("002 · Brand strategy", "Design principles for the <span class='dim'>system.</span>") + S("strategy", "12. Design principles", "12 Design principles for the system (Route A)") + S("strategy", "13. What this package", "13 What this package deliberately does not change"), "002 · Brand strategy"))

# ---------------- 003 POSITIONING
P.append(opener("003", "Brand <span class='dim'>positioning.</span>", "Where Sanzeed stands against studios, architects, fabricators and show producers — and the words that keep the name straight.",
    [("1", "Positioning statement"), ("2", "Positioning map"), ("3", "Competitive frame"), ("4", "Brand pillars"), ("5", "Proof points"), ("6", "Naming rules"), ("7", "Missing information")]))
P.append(page(phead("003 · Brand positioning", "Story-led and whole-<span class='dim'>room.</span>") + S("positioning", "Positioning statement", "Positioning statement")
    + '<div class="mt-4">' + svgfile("positioning-map.svg", "150mm") + '</div><div class="wall-label"><span class="title">Positioning map</span><span class="place">drawn from Brand_Positioning.md</span></div>'
    + '<div class="mt-3">' + body_of("positioning", "Positioning map").replace('<pre class="mono code">', '<pre class="mono code" style="display:none">') + "</div>", "003 · Brand positioning"))
P.append(page(phead("003 · Brand positioning", "Frame and <span class='dim'>pillars.</span>") + S("positioning", "Competitive frame", "Competitive frame") + S("positioning", "Brand pillars", "Brand pillars"), "003 · Brand positioning"))
P.append(page(phead("003 · Brand positioning", "Proof, naming, <span class='dim'>gaps.</span>") + S("positioning", "Proof points", "Proof points (all confirmed)") + S("positioning", "Naming rules", "Naming rules") + S("positioning", "Missing information", "Missing information (to be supplied by Sanzeed)")
    + '<div class="mt-4" style="max-width:90mm">' + fig("figures/site-desktop-about.jpg", "sanzeed.com · About", "desktop, 1440 px", "The proof as the site shows it: portrait, three pillars, four numbers, the trust line and the seven services") + "</div>", "003 · Brand positioning"))

# ---------------- 004 VOICE
P.append(opener("004", "Voice and <span class='dim'>tone.</span>", "A museum's wall label, written by the person who built the room. Precise, calm, first person, short.",
    [("1", "The voice in one line"), ("2", "Voice principles"), ("3", "Tone by situation"), ("4", "Vocabulary"), ("5", "Mechanics"), ("6", "Three test sentences")]))
P.append(page(phead("004 · Voice and tone", "The voice in one <span class='dim'>line.</span>") + '<div class="mt-2">' + pull("A museum's wall label, written by the person who built the room.", "Brand_Voice_and_Tone.md") + "</div>"
    + '<div class="mt-4">' + S("voice", "Voice principles", "Voice principles (with confirmed examples from sanzeed.com)") + "</div>", "004 · Voice and tone"))
P.append(page(phead("004 · Voice and tone", "Tone by <span class='dim'>situation.</span>") + S("voice", "Tone by situation", "Tone by situation") + S("voice", "Vocabulary", "Vocabulary"), "004 · Voice and tone"))
P.append(page(phead("004 · Voice and tone", "Mechanics and the three <span class='dim'>tests.</span>") + '<div class="two">' + S("voice", "Mechanics", "Mechanics") + S("voice", "Three test sentences", "Three test sentences for any new copy") + "</div>"
    + '<div class="mt-4">' + fig(f"{IMG}/case/buddha-park-02.webp", "Buddha Park", "Uttarakhand", "002 · The fountain court from above, the Buddha resting beyond — a caption in the wall-label voice: title, place, one line") + "</div>", "004 · Voice and tone"))

# ---------------- 005 MESSAGING
P.append(opener("005", "<span class='dim'>Messaging.</span>", "The architecture of what is said, from the master line to the call; elevator messages at three lengths; key messages by audience; the approved headline bank.",
    [("1", "Message architecture"), ("2", "Elevator messages"), ("3", "Key messages by audience"), ("4", "Headline bank"), ("5", "Calls to action"), ("6", "Response promises"), ("7", "Email signature")]))

def arch():
    rows = [("Master line", "Experiential design you can walk into.", "Confirmed", "master lit"), ("Brand idea", "Carry the light across.", "Recommendation", "lit"),
            ("Promise", "One vision, carried across — from the brief to opening night.", "Recommendation", ""), ("Pillars", "Strategic Vision · Immersive Craft · Calm Leadership", "Confirmed", ""),
            ("Proof", "15+ yrs · 8+ yrs museums · 90+ projects · 60+ museums", "Confirmed", ""), ("Method", "Discover → Direct → Craft → Deliver", "Confirmed", ""),
            ("Offer", "Seven services, “all seven, every time”", "Confirmed", ""), ("Call", "Tell me about the room.", "Confirmed", "lit")]
    out = ""
    for k, v, t, cls in rows:
        tag = f'<span class="tag {"tag-confirmed" if t == "Confirmed" else "tag-rec"}" style="margin:0">{t}</span>'
        out += f'<div class="row {cls}"><span class="k">{k}</span><span class="v">{v}</span>{tag}</div>'
    return f'<div class="arch">{out}</div>'

el = body_of("messaging", "Elevator messages")
el = el.replace("<p><strong>10 words:</strong>", '<div class="elev"><b>10 words</b><span>').replace("<p><strong>25 words:</strong>", '<div class="elev"><b>25 words</b><span>').replace("<p><strong>50 words:</strong>", '<div class="elev"><b>50 words</b><span>').replace("<p><strong>Boilerplate (press / media kit):</strong>", '<div class="elev"><b>Boiler­plate</b><span>').replace("</p>", "</span></div>")
P.append(page(phead("005 · Messaging", "Message <span class='dim'>architecture.</span>", "The eight lines everything else is built from, in order, each with its status.") + arch() + '<h2 class="doc-h2 sec-h mt-5" style="font-size:15pt">Elevator messages</h2>' + el, "005 · Messaging"))
P.append(page(phead("005 · Messaging", "Key messages and the headline <span class='dim'>bank.</span>") + S("messaging", "Key messages", "Key messages by audience") + S("messaging", "Headline bank", "Headline bank (approved style)").replace("<ul>", '<ul style="columns:2;column-gap:8mm">'), "005 · Messaging"))
sig = body_of("messaging", "Email signature").replace('<pre class="mono code">', '<pre class="mono code" style="font-family:var(--font-text);font-size:9pt;line-height:1.6">')
ctas = body_of("messaging", "Calls to action")
cta_demo = '<div class="cta-row mt-3"><span class="pill solid">Tell me about the room →</span><span class="pill ghost">See the work</span><span class="pill text">WhatsApp @sanzeed</span></div>'
P.append(page(phead("005 · Messaging", "Calls, promises and the <span class='dim'>signature.</span>") + '<div class="sec"><h2 class="doc-h2 sec-h">Calls to action</h2>' + ctas + cta_demo + "</div>"
    + '<div class="two mt-4">' + S("messaging", "Response promises", "Response promises (confirmed, repeat consistently)") + '<div class="sec"><h2 class="doc-h2 sec-h">Email signature text</h2>' + sig + "</div></div>"
    + '<div class="mt-3" style="max-width:110mm">' + fig(f"{IMG}/case/ram-katha-show-08.webp", "Ram Katha Show", "Ayodhya", "008 · The darbar: the end of the story, in full light") + "</div>", "005 · Messaging"))

P.append(f"""
<section class="page cover theme-dark grain">
  <div class="cover-top"><span class="eyebrow" style="color:var(--fg-3)">Brand package · 01 Brand strategy</span><span class="eyebrow" style="color:var(--fg-3)">Version 1.0 · 5 November 2026</span></div>
  <div class="cover-title"><p class="doc-display" style="font-size:40pt">Tell me about the <span class="lit">room.</span></p>
  <p class="cover-sub">The first conversation is always free. I reply within two working days. If it is urgent, WhatsApp is fastest.<br><br>Sanzeed Mirza · Experiential Design Consultant<br>+91 7827051270 · sanzeed@gmail.com · linkedin.com/in/sanzeed · sanzeed.com · New Delhi, India</p></div>
  <div class="cover-foot">{logo("horizontal-descriptor", "full-colour-dark", "70mm")}<span class="cover-meta">Source: 01_BRAND_STRATEGY/*.md</span></div>
</section>
""")

# resolve contents page numbers from the opener positions
for i, pg in enumerate(P):
    m = re.search(r'class="page opener" data-section="(\d{3})', pg)
    if m: P[1] = P[1].replace(f"@@PAGE{m.group(1)}@@", f"{i+1:02d}")
html = head() + "".join(P) + "</main>\n</body>\n</html>\n"
(HERE / "Brand_Strategy.html").write_text(html, encoding="utf-8")
print("wrote Brand_Strategy.html with", html.count('<section class="page'), "pages")
