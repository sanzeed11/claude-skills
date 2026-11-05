#!/usr/bin/env python3
"""build_checklist.py — generates DELIVERY_CHECKLIST.md from the files actually on disk.
Each deliverable from the brief is mapped to glob patterns; an item is 'complete' only when at least one
matching file exists (and 'partial'/'limitation' notes come from the per-folder READMEs where recorded).
Usage: python3 build_checklist.py <BRAND_PACKAGE> [out.md]
"""
import os, sys, glob, json, re
from collections import OrderedDict
ROOT = sys.argv[1].rstrip('/'); OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, 'DELIVERY_CHECKLIST.md')
def g(*pats):
    out = []
    for p in pats:
        out += sorted(x for x in glob.glob(os.path.join(ROOT, p), recursive=True) if os.path.isfile(x) and os.path.getsize(x) > 0 and '_frames' not in x)
    return list(OrderedDict.fromkeys(out))
LOGO = '02_LOGO_SYSTEM'
ITEMS = [
 ('PHASE 1 — BRAND DISCOVERY & STRATEGY', [
  ('Brand audit (confirmed facts vs assumptions)', g('01_BRAND_STRATEGY/Brand_Audit.md')),
  ('Brand strategy: vision, mission, purpose, values, positioning, promise, personality, archetype, audience, differentiation, USP, voice, messaging, story, taglines', g('01_BRAND_STRATEGY/Brand_Strategy.md')),
  ('Brand_Strategy.pdf (designed document)', g('01_BRAND_STRATEGY/Brand_Strategy.pdf')),
  ('Brand_Positioning.md', g('01_BRAND_STRATEGY/Brand_Positioning.md')),
  ('Brand_Voice_and_Tone.md', g('01_BRAND_STRATEGY/Brand_Voice_and_Tone.md')),
  ('Brand_Messaging.md', g('01_BRAND_STRATEGY/Brand_Messaging.md')),
  ('Creative directions evaluated (3 routes) with recommendation', g('01_BRAND_STRATEGY/Brand_Strategy.md')),
 ]),
 ('PHASE 2.1 — LOGO SYSTEM', [
  ('Primary logo', g(f'{LOGO}/SVG/sanzeed-primary-wordmark--*.svg')),
  ('Secondary logo (symbol + wordmark)', g(f'{LOGO}/SVG/sanzeed-secondary-symbol-wordmark--*.svg')),
  ('Horizontal logo (wordmark + descriptor)', g(f'{LOGO}/SVG/sanzeed-horizontal-descriptor--*.svg')),
  ('Vertical / stacked logo', g(f'{LOGO}/SVG/sanzeed-vertical-stacked--*.svg')),
  ('Symbol / icon', g(f'{LOGO}/SVG/sanzeed-symbol--*.svg')),
  ('Monogram', g(f'{LOGO}/SVG/sanzeed-monogram--*.svg')),
  ('Wordmark (plain, no dots)', g(f'{LOGO}/SVG/sanzeed-wordmark-plain--*.svg')),
  ('Simplified logo', g(f'{LOGO}/SVG/sanzeed-simplified-small-size--*.svg')),
  ('Full-colour logo', g(f'{LOGO}/Full_Color/*.svg')),
  ('Black logo', g(f'{LOGO}/Black/*.svg')),
  ('White / inverted logo', g(f'{LOGO}/White/*.svg')),
  ('Grayscale logo', g(f'{LOGO}/Grayscale/*.svg')),
  ('Single-colour logo', g(f'{LOGO}/Single_Color/*.svg')),
  ('Small-size logo', g(f'{LOGO}/SVG/sanzeed-*small-size--*.svg')),
  ('Favicon version (ICO, PNG 16–1024, SVG, manifest)', g(f'{LOGO}/Favicon/favicon.ico', f'{LOGO}/Favicon/favicon-*.png', f'{LOGO}/Favicon/site.webmanifest')),
  ('Social media profile version', g(f'{LOGO}/Social_Profile/*.png')),
  ('Light and dark background variants', g(f'{LOGO}/SVG/*--full-colour-dark.svg', f'{LOGO}/SVG/*--full-colour-light.svg')),
  ('Signature mark (vectorised)', g(f'{LOGO}/Signature/*.svg')),
  ('Logo clear space diagram', g(f'{LOGO}/Guidelines/logo-clear-space.*')),
  ('Minimum sizes diagram', g(f'{LOGO}/Guidelines/logo-minimum-sizes*')),
  ('Construction / proportions diagram', g(f'{LOGO}/Guidelines/logo-construction.*')),
  ('Incorrect usage sheet', g(f'{LOGO}/Guidelines/logo-incorrect-usage.*')),
  ('Placement rules diagram', g(f'{LOGO}/Guidelines/logo-placement.*')),
  ('Format: SVG', g(f'{LOGO}/SVG/*.svg')), ('Format: PDF (vector)', g(f'{LOGO}/PDF/*.pdf')), ('Format: EPS (genuine, Inkscape/cairo)', g(f'{LOGO}/EPS/*.eps')),
  ('Format: PNG transparent', g(f'{LOGO}/PNG/*.png')), ('Format: JPG on white', g(f'{LOGO}/JPG/*.jpg')), ('Format: WebP', g(f'{LOGO}/WebP/*.webp')),
  ('Format: AI — NOT SUPPLIED (proprietary; cannot be written here — SVG/PDF open natively in Illustrator; see 02 README)', []),
  ('Editable construction source (parametric master + per-stroke SVGs)', g('15_SOURCE_FILES/Project_Files/logo-builder/build_logo.py', f'{LOGO}/Source_Files/*.svg')),
 ]),
 ('PHASE 2.2 — COLOUR SYSTEM', [
  ('Colour_Palette.pdf', g('03_COLOUR_SYSTEM/Colour_Palette.pdf')),
  ('Colour swatches (per colour + sheet)', g('03_COLOUR_SYSTEM/Colour_Swatches/*.png')),
  ('colour-tokens.json (HEX, RGB, CMYK, HSL, nearest Pantone, usage, contrast)', g('03_COLOUR_SYSTEM/colour-tokens.json')),
  ('colour-variables.css (dark + light themes, functional colours)', g('03_COLOUR_SYSTEM/colour-variables.css')),
  ('Colour reference (hierarchy, usage, accessibility, approved combinations, gradients)', g('03_COLOUR_SYSTEM/Colour_Reference.md')),
  ('SCSS / Tailwind exports', g('03_COLOUR_SYSTEM/colour-tokens.scss', '03_COLOUR_SYSTEM/tailwind.colours.js')),
 ]),
 ('PHASE 2.3 — TYPOGRAPHY', [
  ('Font_Reference.pdf', g('04_TYPOGRAPHY/Font_Reference.pdf')),
  ('Typography specimens (families, hierarchy, responsive scale, pairing, numbers, editorial, character set, UI)', g('04_TYPOGRAPHY/Typography_Specimens/*.pdf', '04_TYPOGRAPHY/Typography_Specimens/*.png')),
  ('Font files (OFL TTF originals + woff2 subsets + licences)', g('04_TYPOGRAPHY/Font_Files/*/*.ttf', '04_TYPOGRAPHY/Font_Files/*/*.woff2', '04_TYPOGRAPHY/Font_Files/*/OFL.txt')),
  ('Font_Licensing.md', g('04_TYPOGRAPHY/Font_Licensing.md')),
  ('Typography tokens (desktop/tablet/mobile scale, print scale)', g('04_TYPOGRAPHY/typography-tokens.json')),
 ]),
 ('PHASE 2.4 — GRAPHIC LANGUAGE', [
  ('Brand patterns (seamless SVG + PNG + CSS)', g('05_GRAPHIC_ASSETS/Patterns/**/*.svg', '05_GRAPHIC_ASSETS/Patterns/patterns.css')),
  ('Textures (grain, paper, lamp glow, vignette)', g('05_GRAPHIC_ASSETS/Textures/*.png', '05_GRAPHIC_ASSETS/Textures/*.jpg')),
  ('Illustrations (orbit object, method, two points, route, service glyphs, lamp)', g('05_GRAPHIC_ASSETS/Illustrations/**/*.svg')),
  ('Iconography (icon set SVG + sprite + PNG)', g('05_GRAPHIC_ASSETS/Icons/**/*.svg')),
  ('Backgrounds (lamp, dusk, plaster, presentation, document covers, photo plates)', g('05_GRAPHIC_ASSETS/Backgrounds/**/*.png', '05_GRAPHIC_ASSETS/Backgrounds/**/*.jpg')),
  ('Dividers, frames, borders, corner marks, counters, signature elements', g('05_GRAPHIC_ASSETS/Decorative_Elements/**/*.svg')),
 ]),
 ('PHASE 3 — PHOTOGRAPHY & ART DIRECTION', [
  ('Moodboard.pdf', g('06_PHOTOGRAPHY_ART_DIRECTION/Moodboard.pdf')),
  ('Photography_Guidelines.pdf', g('06_PHOTOGRAPHY_ART_DIRECTION/Photography_Guidelines.pdf')),
  ('Approved image library (graded, indexed)', g('06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/JPG/*.jpg', '06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/**/*.jpg')),
  ('Image treatment templates + treat_image.py', g('06_PHOTOGRAPHY_ART_DIRECTION/Image_Templates/**/*.html', '06_PHOTOGRAPHY_ART_DIRECTION/Image_Templates/**/*.py')),
 ]),
 ('PHASE 4 — WEBSITE & DIGITAL', [
  ('Website UI design system (component library HTML/CSS)', g('07_WEBSITE_DIGITAL_ASSETS/UI_Components/*.html', '07_WEBSITE_DIGITAL_ASSETS/UI_Components/*.css')),
  ('Responsive renders (desktop, laptop, tablet, mobile)', g('07_WEBSITE_DIGITAL_ASSETS/UI_Components/**/*.png')),
  ('Website favicon + browser icons + Apple touch + PWA icons', g('07_WEBSITE_DIGITAL_ASSETS/Favicon/*', '07_WEBSITE_DIGITAL_ASSETS/App_Icons/*.png')),
  ('Open Graph / social-sharing images', g('07_WEBSITE_DIGITAL_ASSETS/Open_Graph/*.png', '07_WEBSITE_DIGITAL_ASSETS/Social_Sharing/*.png')),
  ('Email header, newsletter header, email signature', g('07_WEBSITE_DIGITAL_ASSETS/Email/*')),
  ('Website background graphics, custom UI icons', g('07_WEBSITE_DIGITAL_ASSETS/Website_Graphics/*', '05_GRAPHIC_ASSETS/Icons/**/*.svg')),
  ('Branded presentation backgrounds, branded document covers', g('05_GRAPHIC_ASSETS/Backgrounds/**/*presentation*', '05_GRAPHIC_ASSETS/Backgrounds/**/*cover*', '09_PRINT_STATIONERY/Covers/*')),
  ('Website implementation (identity applied to the existing site, functionality preserved)', g('16_WEBSITE_IMPLEMENTATION/index.html', '16_WEBSITE_IMPLEMENTATION/work/*.html', '16_WEBSITE_IMPLEMENTATION/CHANGES.md')),
  ('Website verification screenshots (before/after, desktop/mobile, dark/light)', g('16_WEBSITE_IMPLEMENTATION/screenshots/*')),
 ]),
 ('PHASE 4 — SOCIAL MEDIA', [
  ('Instagram profile, post, portrait, story, highlight covers, reel covers', g('08_SOCIAL_MEDIA/Instagram/*.png')),
  ('Facebook profile, cover, post, event', g('08_SOCIAL_MEDIA/Facebook/*.png')),
  ('LinkedIn personal banner, company banner, profile, posts, carousel', g('08_SOCIAL_MEDIA/LinkedIn/*')),
  ('YouTube banner, profile, thumbnails, end screen', g('08_SOCIAL_MEDIA/YouTube/*.png')),
  ('X profile, header, post images', g('08_SOCIAL_MEDIA/X/*.png')),
  ('Pinterest profile and pins', g('08_SOCIAL_MEDIA/Pinterest/*.png')),
  ('Editable templates (HTML sources + PPTX)', g('08_SOCIAL_MEDIA/Editable_Templates/**/*.html', '08_SOCIAL_MEDIA/Editable_Templates/**/*.pptx')),
 ]),
 ('PHASE 5 — PRINT & CORPORATE STATIONERY', [
  ('Business card front and back', g('09_PRINT_STATIONERY/Business_Cards/*.pdf')),
  ('Letterhead (DOCX + print master)', g('09_PRINT_STATIONERY/Letterheads/**/*.docx', '09_PRINT_STATIONERY/Letterheads/*.pdf')),
  ('Official document template', g('09_PRINT_STATIONERY/**/*official*', '09_PRINT_STATIONERY/Official_Document/**/*')),
  ('Envelope design', g('09_PRINT_STATIONERY/Envelopes/*.pdf')),
  ('Invoice template', g('09_PRINT_STATIONERY/Invoices/**/*.docx', '09_PRINT_STATIONERY/Invoices/*.pdf')),
  ('Quotation template', g('09_PRINT_STATIONERY/Quotations/**/*.docx', '09_PRINT_STATIONERY/Quotations/*.pdf')),
  ('Proposal template', g('09_PRINT_STATIONERY/Proposals/**/*.docx', '09_PRINT_STATIONERY/Proposals/*.pdf')),
  ('Presentation template (PPTX)', g('09_PRINT_STATIONERY/**/*.pptx')),
  ('Thank-you card', g('09_PRINT_STATIONERY/Thank_You_Cards/*.pdf')),
  ('Company profile cover', g('09_PRINT_STATIONERY/Covers/*profile*')),
  ('Report cover', g('09_PRINT_STATIONERY/Covers/*report*')),
  ('Folder design (dieline)', g('09_PRINT_STATIONERY/Folder/*')),
  ('Notepad', g('09_PRINT_STATIONERY/Notepad/*')),
  ('ID card', g('09_PRINT_STATIONERY/ID_Card/*')),
  ('Official stamp design', g('09_PRINT_STATIONERY/Stamp/*')),
  ('Print-ready files (CMYK, bleed, crop marks)', g('09_PRINT_STATIONERY/Print_Ready_Files/*.pdf')),
 ]),
 ('PHASE 6 — MARKETING & BRAND COMMUNICATION', [
  ('Digital advertising templates (IAB sizes)', g('10_MARKETING_COLLATERAL/Campaign_Templates/*ad*')),
  ('Promotional banners', g('10_MARKETING_COLLATERAL/Campaign_Templates/*banner*')),
  ('Campaign graphics / key visuals', g('10_MARKETING_COLLATERAL/Campaign_Templates/*key-visual*')),
  ('Event invitations', g('10_MARKETING_COLLATERAL/Events/*invitation*')),
  ('Event branding (backdrop, welcome board, badge, lanyard)', g('10_MARKETING_COLLATERAL/Events/*')),
  ('Exhibition graphics (roll-up, booth wall)', g('10_MARKETING_COLLATERAL/Events/*roll*', '10_MARKETING_COLLATERAL/Events/*booth*', '10_MARKETING_COLLATERAL/**/*roll-up*')),
  ('Signage (door plate, wayfinding, totem, window vinyl, spec sheet)', g('10_MARKETING_COLLATERAL/Signage/*')),
  ('Posters', g('10_MARKETING_COLLATERAL/Posters/*.pdf')),
  ('Flyers', g('10_MARKETING_COLLATERAL/Flyers/*.pdf')),
  ('Brochures (trifold + company profile)', g('10_MARKETING_COLLATERAL/Brochures/*.pdf')),
  ('Media kit', g('10_MARKETING_COLLATERAL/Media_Kit/*.pdf')),
  ('Company profile', g('10_MARKETING_COLLATERAL/Brochures/*profile*.pdf')),
  ('Sales presentation template', g('10_MARKETING_COLLATERAL/Presentations/*sales*')),
  ('Marketing proposal template', g('10_MARKETING_COLLATERAL/Presentations/*proposal*')),
  ('Case study template', g('10_MARKETING_COLLATERAL/Presentations/*case-study*')),
  ('Portfolio template', g('10_MARKETING_COLLATERAL/Presentations/*portfolio*')),
  ('Press / media assets (release template, headshots, fact sheet)', g('10_MARKETING_COLLATERAL/Press/*')),
 ]),
 ('PHASE 7 — MOTION & ANIMATION IDENTITY', [
  ('Logo reveal animation', g('11_MOTION_GRAPHICS/Logo_Animations/*reveal*')),
  ('Logo outro animation', g('11_MOTION_GRAPHICS/Logo_Animations/*outro*')),
  ('Website loading animation (CSS, SVG, Lottie, GIF, MP4)', g('11_MOTION_GRAPHICS/Website_Loader/*', '11_MOTION_GRAPHICS/**/*loader*')),
  ('Brand transition', g('11_MOTION_GRAPHICS/Intros_Outros/*transition*')),
  ('Social media motion templates', g('11_MOTION_GRAPHICS/Social_Animations/*')),
  ('Animated logo for presentations (alpha)', g('11_MOTION_GRAPHICS/Logo_Animations/*presentation*')),
  ('Branded video intro', g('11_MOTION_GRAPHICS/Intros_Outros/*intro*')),
  ('Branded video outro', g('11_MOTION_GRAPHICS/Intros_Outros/*outro*')),
  ('Lower thirds', g('11_MOTION_GRAPHICS/Lower_Thirds/*')),
  ('Editable animation sources (HTML/CSS + Lottie JSON)', g('11_MOTION_GRAPHICS/Source_Files/**/*.html', '11_MOTION_GRAPHICS/Source_Files/**/*.json')),
  ('Motion principles (timing, easing, transitions, rules)', g('11_MOTION_GRAPHICS/Motion_Principles.md')),
 ]),
 ('PHASE 8 — BRAND GUIDELINES', [
  ('Brand_Guidelines.pdf (26 sections, visual)', g('12_BRAND_GUIDELINES/Brand_Guidelines.pdf')),
  ('Editable source (HTML/CSS chapters + build)', g('12_BRAND_GUIDELINES/Editable_Source/**/*.html')),
  ('Brand_Usage_Reference.md', g('12_BRAND_GUIDELINES/Brand_Usage_Reference.md')),
 ]),
 ('PHASE 9 — PRESENTATION & MOCKUPS', [
  ('Brand_Presentation.pdf', g('14_PRESENTATION/Brand_Presentation.pdf')),
  ('Editable presentation (PPTX + HTML source + slide PNGs)', g('14_PRESENTATION/Editable_Presentation/**/*.pptx', '14_PRESENTATION/Editable_Presentation/**/*.html')),
  ('Logo mockups', g('13_BRAND_MOCKUPS/Logo_Mockups/*.jpg')),
  ('Stationery mockups', g('13_BRAND_MOCKUPS/Stationery_Mockups/*.jpg')),
  ('Digital mockups', g('13_BRAND_MOCKUPS/Digital_Mockups/*.jpg')),
  ('Marketing mockups', g('13_BRAND_MOCKUPS/Marketing_Mockups/*.jpg')),
 ]),
 ('PHASE 10 — SOURCE FILES & DELIVERY', [
  ('Original assets backup (untouched)', g('00_ORIGINAL_ASSETS_BACKUP/**/*')),
  ('Brand kit (tokens CSS, render/capture/export/print helpers, production brief)', g('15_SOURCE_FILES/Project_Files/brand-kit/*')),
  ('Logo builder, colour builder, QA scripts', g('15_SOURCE_FILES/Project_Files/logo-builder/*.py', '15_SOURCE_FILES/Project_Files/colour-builder/*.py', '15_SOURCE_FILES/Project_Files/qa/*.py')),
  ('Original designs / editable assets index', g('15_SOURCE_FILES/Original_Designs/*', '15_SOURCE_FILES/Editable_Assets/*')),
  ('README.md (package guide)', g('README.md')),
  ('QA report', g('QA_REPORT.md')),
 ]),
]
FMT = lambda f: f.rsplit('.', 1)[-1].upper() if '.' in os.path.basename(f) else '—'
lines = ['# DELIVERY_CHECKLIST — Sanzeed Brand Package', '', 'Generated from the files on disk by `15_SOURCE_FILES/Project_Files/qa/build_checklist.py`. An item is marked **complete** only when at least one matching file exists and is non-empty; counts and paths are measured, not claimed. "Limitation" items are recorded honestly with the reason.', '']
tot = done = 0
for phase, items in ITEMS:
    lines += [f'## {phase}', '', '| Deliverable | Status | Files | Formats | Example path(s) |', '|---|---|---|---|---|']
    for name, files in items:
        tot += 1
        if files:
            done += 1; status = '✅ complete'
            fmts = ', '.join(sorted(set(FMT(f) for f in files)))
            ex = '<br>'.join(f'`{os.path.relpath(f, ROOT)}`' for f in files[:3]) + (f'<br>… +{len(files)-3} more' if len(files) > 3 else '')
        elif 'NOT SUPPLIED' in name:
            status = '⚠️ limitation'; fmts = '—'; ex = 'see `02_LOGO_SYSTEM/README.md`'
        else:
            status = '❌ missing'; fmts = '—'; ex = '—'
        lines.append(f'| {name} | {status} | {len(files)} | {fmts} | {ex} |')
    lines.append('')
# folder totals
lines += ['## Package totals', '', '| Folder | Files | Size |', '|---|---|---|']
grand = 0
for d in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, d)
    if os.path.isdir(p) and re.match(r'\d\d_', d):
        n = sz = 0
        for dp, dn, fn in os.walk(p):
            for f in fn: n += 1; sz += os.path.getsize(os.path.join(dp, f))
        grand += sz; lines.append(f'| `{d}` | {n} | {sz/1e6:.1f} MB |')
lines += ['', f'**Deliverables complete: {done} / {tot}** · package size {grand/1e6:.0f} MB', '']
open(OUT, 'w').write('\n'.join(lines)); print(f'{done}/{tot} complete →', OUT)
