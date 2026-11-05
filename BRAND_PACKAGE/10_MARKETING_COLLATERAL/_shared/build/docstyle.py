"""docstyle.py — shared A4 document CSS (light 'label' pages, dark cover pages) for the media kit,
case-study template, portfolio template and 'About Sanzeed' sheet."""
A4_CSS = """
@page { size: 210mm 297mm; margin: 0; }
body { background: #000; }
.sheet { width: 210mm; height: 297mm; font-family: var(--font-text); }
.sheet.light { background: #F5F0E7; }
.pad { position: absolute; left: 18mm; right: 18mm; top: 18mm; bottom: 18mm; }
.mark { position: absolute; display: block; }
.hl { color: var(--fg); line-height: 1.04; }
h2.hl { font-size: 24pt; margin: 1.5mm 0 5mm; }
h3 { font-family: var(--font-heading); font-weight: 600; font-size: 8pt; letter-spacing: .12em; text-transform: uppercase; color: var(--accent-text); margin: 6mm 0 1.5mm; }
.eyebrow, .eyebrow-quiet { font-size: 6.5pt; }
p.body { font-size: 8.5pt; line-height: 1.6; color: var(--fg-2); margin-bottom: 3mm; max-width: 130mm; }
p.lead { font-size: 10.5pt; line-height: 1.5; color: var(--fg-2); margin-bottom: 5mm; max-width: 130mm; }
.folio { position: absolute; left: 18mm; right: 18mm; bottom: 10mm; display: flex; justify-content: space-between; font-size: 6.5pt; color: var(--fg-3); }
table { width: 100%; }
th, td { font-size: 8pt; padding: 1.8mm 3mm 1.8mm 0; line-height: 1.45; }
th { font-size: 6.5pt; }
td.k { width: 42mm; font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.wl { font-size: 6.5pt; }
.contact { font-size: 8.5pt; line-height: 1.7; color: var(--fg-2); }
.contact b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.cols { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0 4mm; }
.cat { font-family: var(--font-heading); font-weight: 600; font-size: 5.8pt; letter-spacing: .1em; text-transform: uppercase; color: var(--accent-text); border-bottom: 1px solid var(--line); padding-bottom: 1mm; margin-bottom: 1.2mm; }
.item { font-size: 6pt; line-height: 1.45; color: var(--fg-3); display: grid; grid-template-columns: 6mm 1fr; }
.item .c { font-family: var(--font-heading); font-weight: 500; color: var(--accent-text); font-size: 5.2pt; letter-spacing: .05em; padding-top: .3mm; font-variant-numeric: tabular-nums; }
.item b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.stat .n { font-family: var(--font-display); font-weight: 300; font-size: 24pt; line-height: 1; color: var(--fg); font-variant-numeric: tabular-nums; font-variation-settings: "opsz" 144; }
.stat .n .plus { color: var(--accent); }
.stat .l { font-size: 7pt; color: var(--fg-2); margin-top: 1mm; }
"""

def page(id_, cls, inner, theme, folio_l, folio_r):
    th = "theme-light light" if theme == "light" else "grain"
    return f'<section class="sheet {th} {cls}" id="{id_}"><div class="pad">{inner}</div><div class="folio"><span>{folio_l}</span><span>{folio_r}</span></div></section>'

def gallery_cols(C, esc):
    cols = ""; k = 0
    mus = [g for g in C.GALLERY if g["cat"] == "Museums & Experience Centres"]
    groups = [("Museums & Experience Centres", mus[:30]), ("Museums & Experience Centres", mus[30:]),
              ("Projection Mapping & Shows", [g for g in C.GALLERY if g["cat"] == "Projection Mapping & Shows"]),
              ("Explainer Videos & Others", [g for g in C.GALLERY if g["cat"] == "Explainer Videos & Others"])]
    for cat, items in groups:
        rows = "".join(f'<div class="item"><span class="c">{(k:=k+1):03d}</span><span><b>{esc(g["title"])}</b> · {esc(g["place"])}</span></div>' for g in items)
        cols += f'<div><div class="cat">{esc(cat)}</div>{rows}</div>'
    return cols
