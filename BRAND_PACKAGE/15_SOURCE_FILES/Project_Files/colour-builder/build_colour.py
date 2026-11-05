#!/usr/bin/env python3
"""
Sanzeed colour system — single source of truth.
Generates colour-tokens.json, colour-variables.css, swatch SVG/PNG files, a contrast matrix and a
Pantone proximity table. Edit the PALETTE below and re-run.
"""
import os, sys, json, math, colorsys
import cairosvg

OUT = sys.argv[1] if len(sys.argv) > 1 else '.'

# name, hex, group, role, usage
PALETTE = [
 # Core — dark gallery
 ("Gallery Black", "#000000", "core", "bg-dark",        "Primary dark background: website, social, presentations, video."),
 ("Night",         "#0D0D0F", "core", "surface-dark",   "Secondary dark surface, app-icon tile, footers, cards on black."),
 ("Charcoal",      "#1C1C1E", "core", "card-dark",      "Cards and panels on dark backgrounds."),
 ("Graphite",      "#2A2A2D", "core", "card-dark-2",    "Raised/hover state of dark cards, dividers on dark."),
 ("Mist",          "#808086", "core", "text-dark-3",    "Tertiary text on dark (captions, labels). Minimum size 12 px."),
 ("Silver",        "#A1A1A6", "core", "text-dark-2",    "Secondary text on dark."),
 ("Gallery White", "#F5F5F7", "core", "text-dark-1",    "Primary text and the logo on dark backgrounds."),
 # Core — light gallery
 ("Plaster",       "#F5F0E7", "core", "bg-light",       "Primary light background: documents, print, light mode."),
 ("Paper",         "#FBF8F2", "core", "surface-light",  "Cards, sheets and panels on Plaster; letterhead paper tone."),
 ("Stone",         "#ECE7DC", "core", "card-light-2",   "Raised state, table stripes, dividers on light."),
 ("Umber",         "#665F55", "core", "text-light-2",   "Secondary text on light."),
 ("Soot",          "#1A1816", "core", "text-light-1",   "Primary text and the logo on light backgrounds (warm black)."),
 # Accent — the point of light
 ("Lamp Gold",     "#E9B25A", "accent", "accent-dark",      "The point of light on dark: dots, eyebrows, links, highlights. One per composition."),
 ("Lamp Light",    "#F4C97A", "accent", "accent-dark-2",    "Glow and hover of Lamp Gold on dark; the beam highlight."),
 ("Old Gold",      "#B8863B", "accent", "accent-light",     "The point of light on light backgrounds; print spot colour; single-colour logo."),
 ("Amber",         "#D9A64A", "accent", "accent-light-2",   "Hover/secondary gold on light."),
 ("Gold Ink",      "#8A6124", "accent", "accent-text-light","Gold used as TEXT on light backgrounds (meets 4.5:1 on Plaster)."),
 # Functional
 ("Moss",          "#3D8B5E", "functional", "success-dark",  "Success on dark."),
 ("Moss Deep",     "#2E6E48", "functional", "success-light", "Success on light."),
 ("Ochre",         "#D4862B", "functional", "warning-dark",  "Warning on dark (distinct from Lamp Gold by hue and saturation)."),
 ("Ochre Deep",    "#A8651B", "functional", "warning-light", "Warning on light."),
 ("Signal Red",    "#D64540", "functional", "error-dark",    "Error on dark."),
 ("Brick",         "#C0392B", "functional", "error-light",   "Error on light (existing site value)."),
 ("Slate Blue",    "#4A86C8", "functional", "info-dark",     "Information on dark."),
 ("Slate Deep",    "#2F62A0", "functional", "info-light",    "Information on light."),
]

GRADIENTS = {
 "lamp":   {"type": "radial", "stops": [["#E9B25A", "0%", 0.55], ["#E9B25A", "28%", 0.12], ["#000000", "70%", 0.0]],
            "css": "radial-gradient(60% 60% at 50% 40%, rgba(233,178,90,.55) 0%, rgba(233,178,90,.12) 28%, rgba(0,0,0,0) 70%)",
            "use": "The glow behind a lit object on black. Hero backgrounds, cover pages, video."},
 "dusk":   {"type": "linear", "angle": 180, "stops": [["#000000", "0%"], ["#1C1C1E", "100%"]],
            "css": "linear-gradient(180deg, #000000 0%, #1C1C1E 100%)", "use": "Dark section backgrounds, slide backgrounds."},
 "plaster":{"type": "linear", "angle": 180, "stops": [["#FBF8F2", "0%"], ["#ECE7DC", "100%"]],
            "css": "linear-gradient(180deg, #FBF8F2 0%, #ECE7DC 100%)", "use": "Light document backgrounds, print covers."},
 "foil":   {"type": "linear", "angle": 135, "stops": [["#B8863B", "0%"], ["#F4C97A", "50%"], ["#B8863B", "100%"]],
            "css": "linear-gradient(135deg, #B8863B 0%, #F4C97A 50%, #B8863B 100%)", "use": "Gold-foil simulation for mockups and premium covers only. Never for text under 24 px."},
 "veil":   {"type": "linear", "angle": 180, "stops": [["rgba(0,0,0,0)", "0%"], ["rgba(0,0,0,.72)", "100%"]],
            "css": "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.72) 100%)", "use": "Over photography to carry captions and wall labels."},
}

# Approximate Pantone solid-coated sRGB values (public approximations, not the Pantone library).
PANTONE = {
 "Black C": "#2D2926", "Black 6 C": "#101820", "Black 7 C": "#3D3935", "Neutral Black C": "#222223",
 "Cool Gray 11 C": "#53565A", "Cool Gray 9 C": "#75787B", "Cool Gray 7 C": "#97999B", "Cool Gray 1 C": "#D9D9D6",
 "Warm Gray 11 C": "#6E6259", "Warm Gray 9 C": "#83786F", "Warm Gray 7 C": "#968C83", "Warm Gray 2 C": "#CBC4BC", "Warm Gray 1 C": "#D7D2CB",
 "141 C": "#F2C75C", "142 C": "#F1BE48", "143 C": "#F1B434", "7407 C": "#CBA052", "7408 C": "#F6BE00", "7409 C": "#F0AB00",
 "1235 C": "#FFB81C", "1245 C": "#C59217", "1255 C": "#AD841F", "7555 C": "#D29F13", "7556 C": "#B78B28", "7557 C": "#9F7A25",
 "7502 C": "#CEB888", "7503 C": "#A89968", "465 C": "#B89764", "466 C": "#C6AA76", "467 C": "#D2BC8E", "4505 C": "#B2975D",
 "1225 C": "#FFC87C", "1345 C": "#FDC882", "134 C": "#FDD07C", "157 C": "#EC9E3E", "158 C": "#E87722", "7413 C": "#DC8633",
 "1385 C": "#D57800", "7510 C": "#C6893F", "7511 C": "#B77729", "7527 C": "#D6D2C4", "7528 C": "#C5B9A5", "468 C": "#E3D2AC",
 "7401 C": "#F5E1A4", "7506 C": "#EFDBB2", "7499 C": "#F1E6B2", "9143 C": "#F1E8DA", "9224 C": "#F2EDE4",
 "7731 C": "#228848", "7732 C": "#007A33", "348 C": "#00843D", "356 C": "#007A33", "7741 C": "#44883E", "7725 C": "#00843D",
 "485 C": "#DA291C", "179 C": "#E03C31", "7621 C": "#AB2328", "180 C": "#BE3A34", "7597 C": "#D14124",
 "7461 C": "#007DBA", "7683 C": "#426DA9", "7684 C": "#385E9D", "660 C": "#407EC9", "2935 C": "#0057B8", "7455 C": "#3A5DAE",
}

def hex2rgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def rgb2cmyk(r,g,b):
    if (r,g,b)==(0,0,0): return (0,0,0,100)
    c,m,y = 1-r/255, 1-g/255, 1-b/255; k=min(c,m,y)
    return tuple(round(v*100) for v in ((c-k)/(1-k),(m-k)/(1-k),(y-k)/(1-k),k))
def srgb2lin(v): v/=255; return v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
def luminance(rgb): r,g,b=[srgb2lin(v) for v in rgb]; return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b): la,lb=luminance(hex2rgb(a)),luminance(hex2rgb(b)); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
def rgb2lab(rgb):
    r,g,b=[srgb2lin(v) for v in rgb]
    X=(0.4124*r+0.3576*g+0.1805*b)/0.95047; Y=(0.2126*r+0.7152*g+0.0722*b); Z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return (116*f(Y)-16, 500*(f(X)-f(Y)), 200*(f(Y)-f(Z)))
def deltaE(a,b): la,lb=rgb2lab(hex2rgb(a)),rgb2lab(hex2rgb(b)); return math.sqrt(sum((x-y)**2 for x,y in zip(la,lb)))

def nearest_pantone(h, n=2):
    ranked=sorted(((deltaE(h,v),k) for k,v in PANTONE.items()))[:n]
    return [{"pantone":k, "deltaE":round(d,1), "reliability": "close" if d<6 else ("approximate" if d<12 else "no reliable match")} for d,k in ranked]

tokens={"$schema":"sanzeed-colour-tokens/1.0","brand":"Sanzeed","generated_by":"build_colour.py","colours":{},"gradients":GRADIENTS,
        "themes":{"dark":{},"light":{}}}
for name,hx,group,role,use in PALETTE:
    rgb=hex2rgb(hx); c,m,y,k=rgb2cmyk(*rgb); hsl=colorsys.rgb_to_hls(*[v/255 for v in rgb])
    key=name.lower().replace(' ','-')
    tokens["colours"][key]={"name":name,"hex":hx,"rgb":list(rgb),"rgb_css":f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})",
        "cmyk":[c,m,y,k],"cmyk_note":"process conversion from sRGB (naive); proof with the printer",
        "hsl":[round(hsl[0]*360),round(hsl[2]*100),round(hsl[1]*100)],
        "group":group,"role":role,"usage":use,"pantone_nearest":nearest_pantone(hx),
        "contrast_on_black":round(contrast(hx,"#000000"),2),"contrast_on_plaster":round(contrast(hx,"#F5F0E7"),2)}

# semantic themes
tokens["themes"]["dark"]={"bg":"#000000","bg-2":"#0D0D0F","card":"#1C1C1E","card-2":"#2A2A2D","fg":"#F5F5F7","fg-2":"#A1A1A6","fg-3":"#808086",
  "line":"rgba(255,255,255,0.10)","line-2":"rgba(255,255,255,0.06)","accent":"#E9B25A","accent-2":"#F4C97A","accent-text":"#E9B25A","accent-ink":"#000000",
  "btn":"#F5F5F7","btn-fg":"#000000","glass":"rgba(10,10,12,0.62)","veil":"rgba(0,0,0,0.60)",
  "success":"#3D8B5E","warning":"#D4862B","error":"#D64540","info":"#4A86C8"}
tokens["themes"]["light"]={"bg":"#F5F0E7","bg-2":"#FBF8F2","card":"#FBF8F2","card-2":"#ECE7DC","fg":"#1A1816","fg-2":"#665F55","fg-3":"#6D665C",
  "line":"rgba(40,30,10,0.10)","line-2":"rgba(40,30,10,0.055)","accent":"#B8863B","accent-2":"#D9A64A","accent-text":"#8A6124","accent-ink":"#FFFFFF",
  "btn":"#1A1816","btn-fg":"#FBF8F2","glass":"rgba(245,240,231,0.74)","veil":"rgba(20,15,5,0.40)",
  "success":"#2E6E48","warning":"#A8651B","error":"#C0392B","info":"#2F62A0"}

# approved combinations (text on background) with measured contrast
pairs=[("Gallery White","Gallery Black"),("Silver","Gallery Black"),("Mist","Gallery Black"),("Lamp Gold","Gallery Black"),("Lamp Light","Gallery Black"),
       ("Gallery White","Charcoal"),("Lamp Gold","Charcoal"),("Soot","Plaster"),("Umber","Plaster"),("Gold Ink","Plaster"),("Old Gold","Plaster"),
       ("Soot","Paper"),("Gallery Black","Lamp Gold"),("Soot","Old Gold"),("Gallery White","Old Gold"),("Plaster","Gallery Black"),("Gallery White","Moss"),
       ("Gallery White","Brick"),("Gallery White","Slate Deep")]
hexof={n:h for n,h,*_ in PALETTE}
tokens["approved_combinations"]=[]
for fg,bg in pairs:
    r=contrast(hexof[fg],hexof[bg])
    grade="AAA" if r>=7 else "AA" if r>=4.5 else "AA-large" if r>=3 else "fail"
    tokens["approved_combinations"].append({"foreground":fg,"background":bg,"contrast":round(r,2),"wcag":grade,
        "allowed_for":"body text" if r>=4.5 else ("headlines ≥24 px / 19 px bold, UI graphics" if r>=3 else "decorative only — never text")})

os.makedirs(OUT, exist_ok=True)
json.dump(tokens, open(os.path.join(OUT,'colour-tokens.json'),'w'), indent=2)

# CSS variables
css=[":root {", "  /* Sanzeed colour system — generated by build_colour.py. Palette tokens: */"]
for key,c in tokens["colours"].items(): css.append(f"  --sz-{key}: {c['hex']};")
css.append("\n  /* Gradients */")
for g,v in GRADIENTS.items(): css.append(f"  --sz-gradient-{g}: {v['css']};")
css.append("\n  /* Semantic tokens — dark theme (default) */")
for k,v in tokens["themes"]["dark"].items(): css.append(f"  --{k}: {v};")
css.append("  color-scheme: dark;\n}\n")
css.append('html[data-theme="light"], .theme-light {')
for k,v in tokens["themes"]["light"].items(): css.append(f"  --{k}: {v};")
css.append("  color-scheme: light;\n}\n")
css.append("@media (prefers-color-scheme: light) {\n  html:not([data-theme=\"dark\"]) {")
for k,v in tokens["themes"]["light"].items(): css.append(f"    --{k}: {v};")
css.append("    color-scheme: light;\n  }\n}")
open(os.path.join(OUT,'colour-variables.css'),'w').write("\n".join(css))

# SCSS map + Tailwind snippet for convenience
open(os.path.join(OUT,'colour-tokens.scss'),'w').write("$sz-colours: (\n"+",\n".join(f'  "{k}": {c["hex"]}' for k,c in tokens["colours"].items())+"\n);\n")
open(os.path.join(OUT,'tailwind.colours.js'),'w').write("module.exports = {\n"+",\n".join(f'  "{k}": "{c["hex"]}"' for k,c in tokens["colours"].items())+"\n};\n")

# Swatches: one SVG+PNG per colour, plus a full palette sheet
sw=os.path.join(OUT,'Colour_Swatches'); os.makedirs(sw,exist_ok=True)
for key,c in tokens["colours"].items():
    txt = "#F5F5F7" if luminance(hex2rgb(c['hex']))<0.35 else "#1A1816"
    cmyk=c['cmyk']
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" width="600" height="400">
<rect width="600" height="400" rx="28" fill="{c['hex']}"/>
<g font-family="Inter, 'Inter Tight', Arial, sans-serif" fill="{txt}">
<text x="40" y="60" font-size="30" font-weight="600">{c['name']}</text>
<text x="40" y="300" font-size="22">{c['hex']}</text>
<text x="40" y="332" font-size="18" opacity="0.85">RGB {c['rgb'][0]} {c['rgb'][1]} {c['rgb'][2]}</text>
<text x="40" y="360" font-size="18" opacity="0.85">CMYK {cmyk[0]} {cmyk[1]} {cmyk[2]} {cmyk[3]}</text>
</g></svg>'''
    p=os.path.join(sw,f"{key}.svg"); open(p,'w').write(svg)
    cairosvg.svg2png(url=p, write_to=os.path.join(sw,f"{key}.png"), output_width=600)

# palette sheet
cols=5; cw,ch=360,300; pad=40
rows=math.ceil(len(PALETTE)/cols)
Wd=cols*cw+(cols+1)*pad; Hd=rows*ch+(rows+1)*pad+140
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Hd}" width="{Wd}" height="{Hd}"><rect width="100%" height="100%" fill="#0D0D0F"/>',
       f'<text x="{pad}" y="80" font-family="Fraunces, Georgia, serif" font-weight="300" font-size="56" fill="#F5F5F7">Sanzeed colour system</text>',
       f'<text x="{pad}" y="118" font-family="Inter, sans-serif" font-size="20" fill="#A1A1A6">Core · Accent · Functional — HEX / RGB / CMYK. Generated from colour-tokens.json.</text>']
for i,(name,hx,group,role,use) in enumerate(PALETTE):
    r,cI=divmod(i,cols); x=pad+cI*(cw+pad); y=140+pad+r*(ch+pad)
    txt="#F5F5F7" if luminance(hex2rgb(hx))<0.35 else "#1A1816"; cm=rgb2cmyk(*hex2rgb(hx)); rgb=hex2rgb(hx)
    parts.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="24" fill="{hx}" stroke="rgba(255,255,255,0.08)"/>')
    parts.append(f'<g font-family="Inter, sans-serif" fill="{txt}"><text x="{x+24}" y="{y+44}" font-size="24" font-weight="600">{name}</text>'
                 f'<text x="{x+24}" y="{y+ch-78}" font-size="18">{hx}</text><text x="{x+24}" y="{y+ch-52}" font-size="15" opacity=".85">RGB {rgb[0]} {rgb[1]} {rgb[2]}</text>'
                 f'<text x="{x+24}" y="{y+ch-28}" font-size="15" opacity=".85">CMYK {cm[0]} {cm[1]} {cm[2]} {cm[3]}</text>'
                 f'<text x="{x+cw-24}" y="{y+44}" font-size="13" text-anchor="end" opacity=".7" letter-spacing="1">{group.upper()}</text></g>')
parts.append('</svg>')
open(os.path.join(sw,'_palette-sheet.svg'),'w').write("\n".join(parts))
cairosvg.svg2png(url=os.path.join(sw,'_palette-sheet.svg'), write_to=os.path.join(sw,'_palette-sheet.png'), output_width=2000)

# Markdown reference
md=["# Colour reference — Sanzeed","","Generated by `15_SOURCE_FILES/Project_Files/colour-builder/build_colour.py`. Edit the palette there and re-run; `colour-tokens.json` and `colour-variables.css` are regenerated.","",
    "CMYK values are a process conversion from sRGB and must be proofed with the printer; Pantone references are nearest matches by colour distance against published sRGB approximations, not a Pantone library — verify against a physical swatch book before specifying a spot colour.","",
    "| Name | Role | HEX | RGB | CMYK | Nearest Pantone (ΔE) | On black | On Plaster | Usage |","|---|---|---|---|---|---|---|---|---|"]
for key,c in tokens["colours"].items():
    pn=", ".join(f"{p['pantone']} ({p['deltaE']}, {p['reliability']})" for p in c['pantone_nearest'])
    md.append(f"| **{c['name']}** | `{c['role']}` | `{c['hex']}` | {c['rgb'][0]} {c['rgb'][1]} {c['rgb'][2]} | {c['cmyk'][0]} {c['cmyk'][1]} {c['cmyk'][2]} {c['cmyk'][3]} | {pn} | {c['contrast_on_black']}:1 | {c['contrast_on_plaster']}:1 | {c['usage']} |")
md+=["","## Approved combinations (WCAG 2.2 contrast)","","| Foreground | Background | Ratio | Grade | Allowed for |","|---|---|---|---|---|"]
for p in tokens["approved_combinations"]:
    md.append(f"| {p['foreground']} | {p['background']} | {p['contrast']}:1 | {p['wcag']} | {p['allowed_for']} |")
md+=["","## Gradients","","| Token | CSS | Use |","|---|---|---|"]+[f"| `--sz-gradient-{g}` | `{v['css']}` | {v['use']} |" for g,v in GRADIENTS.items()]
md+=["","## Hierarchy and rules","",
"1. **One light source.** One gold accent per composition (Lamp Gold on dark, Old Gold on light). Never Lamp Gold and Ochre together.",
"2. **Dark is the gallery, cream is the label.** Screens, social, video and covers are dark-first. Documents, print and reading surfaces are Plaster/Paper.",
"3. **Gold is never body text on dark below 16 px**, and on light only as Gold Ink (#8A6124).",
"4. **Black is Gallery Black (#000000) on screen and 100 K (or rich black C60 M40 Y40 K100 for large solids) in print.**",
"5. **Functional colours are for states only** (success, warning, error, info); they never decorate.",
"6. **Tints:** the palette does not use tints of gold. Use opacity on Gallery White (10 %, 6 %) for hairlines on dark and on Soot (10 %, 5.5 %) on light.",
"7. **Metallic print:** Old Gold may be specified as a metallic spot (nearest metallic Pantone 871 C or 872 C — verify with a swatch) or as foil; on screen use the `foil` gradient for mockups only."]
open(os.path.join(OUT,'Colour_Reference.md'),'w').write("\n".join(md))
print("colour system written to", OUT)
