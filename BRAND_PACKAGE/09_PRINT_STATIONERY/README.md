# 09_PRINT_STATIONERY — corporate stationery system

**Sanzeed Mirza · Experiential Design Consultant · New Delhi.** Everything in this folder is built from the brand kit (`02_LOGO_SYSTEM`, `03_COLOUR_SYSTEM`, `04_TYPOGRAPHY`, `15_SOURCE_FILES/Project_Files/brand-kit`) and regenerates from the scripts in `_build/`. Every export has an editable source beside it in `src/`.

## System rules applied throughout

| | |
|---|---|
| Palette | Paper = Plaster `#F5F0E7` (or Paper `#FBF8F2` on pads), type = Soot `#1A1816` / Umber `#665F55`, accent = Old Gold `#B8863B` (the single gold point), gold text = Gold Ink `#8A6124`. Dark pieces (card B front, folder, dark covers, ID card, deck) = Gallery Black / Night with Gallery White, Silver and Lamp Gold `#E9B25A`. |
| Logos | Stationery header and formal documents: `horizontal-descriptor` (≥ 50 mm). Continuation pages, dark covers, deck: `primary-wordmark` (≥ 28 mm). Flap, seals, card corners: `symbol` (≥ 6 mm). ID-card reverse: `monogram`. `full-colour-light` on Plaster/Paper, `full-colour-dark` on black, `black` for single-colour stamps. Clear space ½ cap height. |
| Type | Fraunces Light for display (optical size per the brand rule: 144 ≥ 36 pt, 72 for 18–36 pt, 36 below — the SVG masters use the static instances in `_build/fonts/` so Inkscape honours it; office files use *Fraunces Light*). Inter Tight SemiBold for eyebrows / H3 / table heads (Medium with tabular numerals for figures). Inter for body. Headlines end with a full stop; the last word or the point may be gold — never both. |
| Print | Trim + 3 mm bleed in every master; `Print_Ready_Files/` carries crop marks, TrimBox/BleedBox and CMYK conversion. Fonts outlined (Inkscape) or embedded (Chromium, LibreOffice). |
| Copy | Confirmed details only (name, descriptor, +91 7827051270, sanzeed@gmail.com, sanzeed.com, linkedin.com/in/sanzeed, New Delhi, India; the master and short lines; the method and services from sanzeed.com). Everything the client must supply is a visible bracketed field: `[GSTIN]`, `[Bank name]`, `[Account no.]`, `[IFSC]`, `[Postal address]`, `[Invoice no.]`, `[Date]`, `[Client]`, `[Fee]` … |

## How to regenerate

```bash
cd BRAND_PACKAGE/09_PRINT_STATIONERY/_build
python3 make_font_instances.py        # once: static Fraunces 36pt / 72pt instances → ~/.fonts and _build/fonts
python3 build_business_cards.py && python3 build_letterheads.py && python3 build_envelopes.py
python3 build_invoices.py && python3 build_covers.py && python3 build_proposals.py && python3 build_official.py
python3 build_folder.py && python3 build_notepad.py && python3 build_id_card.py && python3 build_stamp.py
python3 build_thank_you.py && python3 build_presentation.py && python3 gather_print_ready.py
```

`szlib.py` (SVG layers, logo embedding, text helpers, Inkscape/pypdf/pdftoppm/print_pdf exports) and `docxlib.py` (python-docx brand styles, header/footer, tables with tabular numerals) are shared. Requirements: Inkscape 1.2, LibreOffice, Ghostscript, poppler, Node + Playwright (for `render.js`), python-docx, python-pptx, pypdf, reportlab, Pillow, numpy, qrcode, fontTools; the three brand fonts installed system-wide.

**Editing an SVG master** (Inkscape, Illustrator, Affinity, Figma): 1 unit = 1 mm; layers `paper`, `artwork`, `guides` (non-printing; `dieline` on the folder). Text is live — keep the brand fonts installed. Logos are embedded paths from `02_LOGO_SYSTEM/SVG` — replace, never redraw. Re-export with the matching build script, or by hand: Inkscape → PDF with *text to path*, then `python3 ../../15_SOURCE_FILES/Project_Files/brand-kit/print_pdf.py in.pdf out.pdf --trim=WxH --bleed=3 --cmyk`.

**Editing a DOCX / PPTX** (Word, PowerPoint, LibreOffice): install the fonts from `04_TYPOGRAPHY/Font_Files` first. Styles are named (Title, Heading 1–3, Eyebrow, Lead, Quote, Wall Label, Small, Contact, Table Head, Table Body, Field) — use them rather than direct formatting. Bracketed fields are plain text: find-and-replace. Export to PDF from the application (or `soffice --headless --convert-to pdf`).

---

## 1 · Business_Cards/ — 89 × 51 mm, 3 mm bleed, safe 4 mm

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-business-card--a-front.svg` | Concept A front: horizontal-descriptor lockup 54 mm centred on Plaster. Page 95 × 57 (bleed), guides layer | the SVG (Inkscape) · `_build/build_business_cards.py` |
| `src/sanzeed-business-card--a-back.svg` | Back: name Fraunces 12 pt, descriptor eyebrow, contacts Inter 7 pt, master line 9.5 pt ending on the Old Gold point | same |
| `src/sanzeed-business-card--b-front.svg` | Concept B front: primary wordmark 46 mm (full-colour-dark) on Gallery Black with the lamp | same |
| `src/sanzeed-business-card--b-back.svg` | Back as concept A | same |
| `src/sanzeed-business-card.html` | The same four faces as an HTML master on brand.css (`@page 95mm 57mm`) | the HTML; render with `render.js --pdf --size 95x57` |
| `sanzeed-business-card--concept-a.pdf`, `--concept-b.pdf` | Screen PDF at trim, 2 pages (front, back), text outlined | the SVGs |
| `sanzeed-business-card--concept-a--print-cmyk.pdf`, `--concept-b--print-cmyk.pdf` | Print-ready: crop marks, trim/bleed boxes, CMYK, 115 × 77 mm sheet | the SVGs via `print_pdf.py` |
| `sanzeed-business-card--{a,b}-{front,back}-2x.png` | 300 dpi previews, 1052 × 603 px | the PDFs |
| `sanzeed-business-card--html-version.pdf` | 4-page trim PDF rendered from the HTML master | the HTML |
| `specifications.md` | Stock, finish, colour, foil option for the dots, imposition | — |

## 2 · Letterheads/ — A4 and US Letter, first + continuation page

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-letterhead--a4.docx`, `--us-letter.docx` | python-docx template: different first-page header (lockup PNG 56 mm at the 20 mm margin) and continuation header (wordmark 30 mm); footer contact lines + `Page X of Y` fields; styles Title = Fraunces 28, Heading 2 = Fraunces 18, Heading 3 = Inter Tight 11, Body = Inter 10/1.45; margins 20 mm. Filled with a two-page sample letter in brand voice and the signature mark | Word/LibreOffice · `_build/build_letterheads.py` |
| `src/sanzeed-letterhead--{a4,us-letter}-{first,continuation}.svg` | Print masters with bleed (216 × 303 / 221.9 × 285.4), lockup 56 mm, footer contact + short line with the point | the SVGs |
| `src/assets/*.png` | Header logos at 300 dpi (2× pixel density), signature mark at 600 dpi | regenerate with the script |
| `sanzeed-letterhead--{a4,us-letter}.pdf` | Trim PDF, 2 pages (first, continuation), outlined | the SVGs |
| `sanzeed-letterhead--{a4,us-letter}--print-cmyk.pdf` | Print-ready with marks, CMYK | the SVGs |
| `sanzeed-letterhead--{a4,us-letter}-{first,continuation}.png` | 150 dpi previews of the print masters | the PDFs |
| `sanzeed-letterhead--{a4,us-letter}-sample-letter.pdf`, `-sample-letter-0{1,2}.png` | The DOCX exported through LibreOffice (fonts embedded), page previews | the DOCX |

## 3 · Envelopes/ — DL 220 × 110 and C5 229 × 162, window-free

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-envelope--{dl,c5}-front.svg` | Lockup top-left (52 / 56 mm at 12 / 15 mm margins); address zone and stamp zone on the guides layer | the SVGs · `_build/build_envelopes.py` |
| `src/sanzeed-envelope--{dl,c5}-back.svg` | Flap (36 / 46 mm, chamfered, dieline on the guides layer) with the symbol 9 mm; return line with `[Postal address]` | the SVGs |
| `sanzeed-envelope--{dl,c5}.pdf` | Trim PDF, 2 pages | the SVGs |
| `sanzeed-envelope--{dl,c5}--print-cmyk.pdf` | Print-ready | the SVGs |
| `sanzeed-envelope--{dl,c5}-{front,back}.png` | 200 dpi previews; `-with-guides.png` versions show the zones and the flap dieline | the PDFs / SVGs |

Converter note: the flap is drawn as a straight chamfered flap — adapt to the envelope maker's standard die; keep the symbol centred on it.

## 4 · Invoices/ and Quotations/ — A4 DOCX templates

| File | Spec | Edit from |
|---|---|---|
| `Invoices/src/sanzeed-invoice-template.docx` | Letterhead header/footer; eyebrow + "Tax invoice."; fields `[Invoice no.] [Date] [Due date] [GSTIN]`; From / Bill to blocks (`[Postal address] [PAN] [Client] …`); line-item table (Inter Tight Medium, tabular numerals, Stone header, hairline rows) with the four method steps as example rows, Subtotal / GST 18 % / Total; payment block `[Bank name] [Account no.] [IFSC] [UPI ID]`; terms; the two-working-days line | Word · `_build/build_invoices.py` |
| `Quotations/src/sanzeed-quotation-template.docx` | Mirrors the invoice: `[Quotation no.] [Date] [Valid until]`, Scope, Fees by step, Terms (validity, GST, step-by-step, payment schedule, expenses, first conversation free), confirmation block | same |
| `*/sanzeed-{invoice,quotation}-template.pdf`, `-0{1,2}.png` | LibreOffice export, 2 pages; 110 dpi previews | the DOCX |

## 5 · Proposals/ — A4 DOCX proposal template

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-proposal-template.docx` | Section 1: dark cover — the lamp + wordmark background image (`src/assets/sanzeed-proposal-cover-background-300dpi.jpg`, 2480 × 3508, anchored behind text) with editable white text (eyebrow, "One vision, from the brief to opening night.", `[Client] [Project] [Date]`). Section 2 (letterhead header/footer): The room · The one central story · Method (table) · Scope (seven services) · Timeline (table, `[n] weeks`) · Investment (the four bands from the site's enquiry form, `[Fee]`) · Team (bio, 15+ 8+ 90+ 60+, selected rooms) · Terms · Next step "Tell me about the room." with contact. Sample text is the Prime Minister Museum case study, labelled as an example | Word · `_build/build_proposals.py` |
| `src/sanzeed-proposal-cover-background.html` | HTML source of the cover background (brand.css, lamp, grain, wordmark) | render with `render.js` |
| `sanzeed-proposal-template.pdf` | 6 pages via LibreOffice | the DOCX |
| `sanzeed-proposal-template--cover.png`, `--spread-01.png`, `--spread-02.png` | Cover and two spreads (pages 2–3, 4–5) at 110 dpi | the PDF |

## 6 · Covers/ — A4 company-profile and report covers, dark + light

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-covers.html` | Four pages on brand.css (`@page 216mm 303mm`): company profile dark (lamp, grain, wordmark 62 mm, master line with the lit word), company profile light (lockup, Plaster), report dark and light (image plate = the room, wall label, "90 projects, one continuous craft.", `Prepared for [Client] · [Project]`) | the HTML · `_build/build_covers.py` |
| `sanzeed-cover--{company-profile,report}--{dark,light}.pdf` | Trim A4 PDFs, Chromium render, fonts embedded | the HTML |
| `sanzeed-cover--…--print-cmyk.pdf` | Print-ready | the HTML via `print_pdf.py` |
| `sanzeed-cover--….png` | 120 dpi previews | the PDFs |

## 7 · Folder/ — A4 pocket folder, 5 mm spine

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-folder--a4-dieline.svg` | Flat cut size 457 × 395 mm (+3 bleed): glue tab 12 · back panel 220 × 305 · spine 5 · front panel 220; one pocket 90 mm under the back panel with 89 × 51 card slits. Layers: `artwork` (outside: Gallery Black, wordmark 120 mm with the lamp on the front, symbol + contact on the back, master line on the pocket rotated 180° so it reads once folded), `dieline` (magenta cut, blue crease, green glue — non-printing spot), `guides` | the SVG · `_build/build_folder.py` |
| `sanzeed-folder--a4-outside.pdf` | Artwork at cut size | the SVG |
| `sanzeed-folder--a4--print-cmyk.pdf` | Print-ready artwork (483 × 421 sheet) | the SVG |
| `sanzeed-folder--a4-dieline.pdf` | Dieline only, vector, for the die maker | the SVG |
| `sanzeed-folder--a4-flat-with-dieline.png`, `-outside.png` | Flat previews (with / without dieline) | the SVG / PDF |

## 8 · Notepad/ — A5 and A4 pad sheets

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-notepad--{a5,a4}.svg` | Paper `#FBF8F2`; lockup 50 / 56 mm; hairline beams every 8 / 9 mm, the first carrying the gold point; footer contact + sanzeed.com; margins 12 / 20 mm | the SVGs · `_build/build_notepad.py` |
| `sanzeed-notepad--{a5,a4}.pdf`, `--print-cmyk.pdf`, `.png` | Trim PDF, print-ready, 150 dpi preview | the SVGs |

## 9 · ID_Card/ — CR80 portrait 54 × 85.6 mm + lanyard

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-id-card--front.svg` | Night background; portrait plate 40 × 50 mm (4:5 crop of the client's portrait, embedded base64 JPG, also at `src/assets/sanzeed-portrait--4x5.jpg`); name Fraunces 12 pt, descriptor eyebrow, symbol 7 mm, "New Delhi · sanzeed.com" | the SVG · `_build/build_id_card.py` |
| `src/sanzeed-id-card--back.svg` | Monogram SM. 16 mm; contact lines; QR code (qrcode module, EC M) to https://sanzeed.com, Soot modules on a Paper tile 22 mm | the SVG |
| `src/sanzeed-lanyard--strip.svg` | 900 × 20 mm strip: white wordmark 60 mm + gold point, pitch 110 mm, on black | the SVG |
| `sanzeed-id-card.pdf`, `--print-cmyk.pdf`, `--{front,back}.png` | Trim PDF (2 pages), print-ready (corner radius 3.18 on the guides), 300 dpi previews | the SVGs |
| `sanzeed-lanyard--strip.pdf`, `--print-cmyk.pdf`, `.png` | Lanyard artwork (dye-sublimation) | the SVG |

## 10 · Stamp/ — single colour black, text as outlines

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-stamp--round-40mm--editable.svg` | Round 40 mm: outer ring 0.7 mm, inner ring 0.5 mm, symbol 14 mm (stroke 1.5 mm), ring text "SANZEED MIRZA · EXPERIENTIAL DESIGN CONSULTANT · NEW DELHI ·" Inter Tight Bold 7 pt on a textPath (live text) | the SVG · `_build/build_stamp.py` |
| `src/sanzeed-stamp--rectangular-58x22mm--editable.svg` | 58 × 22 mm: border 0.6 mm, horizontal-descriptor lockup 50 mm (black), contact in Inter Tight Bold 6.2 pt, two lines | the SVG |
| `sanzeed-stamp--round-40mm.svg`, `--rectangular-58x22mm.svg` | Deliverable artwork, all text converted to outlines (Inkscape) | regenerate from the editable SVGs |
| `sanzeed-stamp--….pdf`, `….png` | Vector PDF (100 K) and 600 dpi PNG | the outlined SVGs |
| `sanzeed-stamp--…--impression-gold-ink.png` | Impression preview in Gold Ink `#8A6124` on Plaster | the outlined SVGs |

Line weights: rings and symbol ≥ 0.5 mm as specified; ring-text letter stems are ≈ 0.45 mm (Bold at 7 pt) — confirm with the stamp maker (laser-engraved rubber or photopolymer both hold this).

## 11 · Thank_You_Cards/ — A6 folded (A5 flat) and A6 postcard

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-thank-you-card--folded-outside.svg` | 210 × 148 flat, fold at 105 (guides). Right panel (front): "Thank you." Fraunces 36 pt with the Old Gold point; left panel (back): symbol + sanzeed.com | the SVG · `_build/build_thank_you.py` |
| `src/sanzeed-thank-you-card--folded-inside.svg` | Left page: signature mark 40 mm + name line; right page: blank with one hairline | the SVG |
| `src/sanzeed-thank-you-postcard--{front,back}.svg` | 148 × 105: "Thank you." front; postal back (divider, address lines, stamp box, signature mark, contact, symbol) | the SVGs |
| `sanzeed-thank-you-card--{folded,postcard}.pdf`, `--print-cmyk.pdf`, `-{outside,inside,front,back}.png` | Trim PDFs (2 pages), print-ready, 200 dpi previews | the SVGs |

## 12 · Official_Document/ — generic official document template

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-official-document-template.docx` | Letterhead header/footer; cover block (eyebrow, "Statement of work.", lead line, `[Ref no.] [Date] [Client] [Project]`); numbered Fraunces headings (Purpose, Scope of work, Deliverables and approvals, Responsibilities table, Fees and terms, Signatures); two-party signature block with the signature mark PNG and a signing line for `[Name]` | Word · `_build/build_official.py` (uses the letterhead's `src/assets`) |
| `sanzeed-official-document-template.pdf`, `-0{1,2}.png` | LibreOffice export, 2 pages, previews | the DOCX |

## 13 · Presentation_Template/ — 16:9 PPTX

| File | Spec | Edit from |
|---|---|---|
| `src/sanzeed-presentation-template.pptx` | 13.333 × 7.5 in, slide-master background Gallery Black, fonts Fraunces Light / Inter Tight SemiBold / Inter. Fourteen built slides, one per layout, named in the slide sorter: 01 title (lamp, wordmark) · 02 section divider (counter + title) · 03 agenda · 04 statement (lit word) · 05 full-bleed image + wall label (Prime Minister Museum) · 06 image + text (Ram Katha Show) · 07 two-column (Buddha Park) · 08 three-column cards (services) · 09 stats 15+ 8+ 90+ 60+ · 10 timeline (the career) · 11 method (four steps) · 12 quote · 13 team / contact (portrait) · 14 end card "Tell me about the room." Duplicate a slide to reuse its layout | PowerPoint/Keynote/LibreOffice · `_build/build_presentation.py` |
| `src/assets/` | Lamp backgrounds (1920 × 1080 JPG, generated), veiled and cropped project images (JPG q88), portrait 4:5, wordmark/symbol PNGs | regenerate with the script |
| `sanzeed-presentation-template.pdf` | 14 pages via LibreOffice | the PPTX |
| `sanzeed-presentation-template--slide-01…14.png` | 1280 × 720 previews of every slide | the PDF |

Install note for the client: copy the three families from `04_TYPOGRAPHY/Font_Files` (Fraunces variable, Inter, Inter Tight) and pick *Fraunces Light*, *Inter Tight SemiBold*, *Inter* in the font menu; the deck and documents reference those names.

## Print_Ready_Files/

Seventeen print PDFs named `sanzeed-<item>--print-cmyk.pdf` plus `MANIFEST.md` (trim, bleed, pages, sheet size, colour — verified with `pdfinfo` and `pdfimages`). The stamp PDFs (100 K, no bleed) and the folder dieline stay in their own folders and are referenced in the manifest.

## _build/

Build scripts (above), `fonts/` (static Fraunces 36pt / 72pt Light + Light Italic instances, OFL), and nothing else. Scratch exports go to temporary directories.

## Known limitations

- Approved imagery is 960 × 540 px (the site's gallery assets). On the A4 report covers the image plate prints at ≈ 115 dpi; for the final run, replace `prime-minister-museum.webp` / `ram-katha-show.webp` with the originals at ≥ 2000 px wide (same crop) and re-run `build_covers.py`. The presentation and the proposal use the same assets at screen resolution, where they are fine.
- Office apps cannot set Fraunces' optical-size axis, so the DOCX/PPTX files use *Fraunces Light* at the font's default optical size; the SVG/PDF masters follow the 144/72/36 rule exactly.
- Business terms, fees, durations, bank details, GSTIN/PAN and the postal address are not known and are left as bracketed fields; the four investment bands are the ones on the site's enquiry form.
- `.ai` / `.indd` files are not produced (Illustrator and InDesign only write their own formats); every SVG and PDF here opens in them as editable vector artwork.
