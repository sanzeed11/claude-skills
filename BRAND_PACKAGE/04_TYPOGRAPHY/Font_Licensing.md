# Font licensing — Sanzeed typography system

All three typefaces are released under the **SIL Open Font License 1.1 (OFL)**. The OFL permits free use, embedding, modification and **redistribution** (the font files may be bundled with this package and with the website), provided the licence file accompanies them and they are not sold on their own. A copy of each family's `OFL.txt` sits beside its files in `Font_Files/`.

| Family | Role in the system | Designer / copyright | Source of the files in this package | Official page |
|---|---|---|---|---|
| **Fraunces** (variable: opsz, wght, SOFT, WONK; roman + italic) | Display and editorial serif — headlines, large numerals, pull quotes | Copyright 2020 The Fraunces Project Authors (Undercase Type: Phaedra Charles, Flavia Zimbardi) | `google/fonts` repository, `ofl/fraunces/` (fetched 5 Nov 2026) | https://fonts.google.com/specimen/Fraunces · https://github.com/undercasetype/Fraunces |
| **Inter** (variable: opsz, wght; roman + italic) | Text and UI sans — body, captions, forms, tables | Copyright 2020 The Inter Project Authors (Rasmus Andersson) | `google/fonts` repository, `ofl/inter/` | https://fonts.google.com/specimen/Inter · https://rsms.me/inter/ |
| **Inter Tight** (variable: wght; roman + italic) | Headings, labels, eyebrows, descriptor lockup | Copyright 2020 The Inter Project Authors (Rasmus Andersson) | `google/fonts` repository, `ofl/intertight/` | https://fonts.google.com/specimen/Inter+Tight |

## What is included
- `Font_Files/<Family>/*.ttf` — the original variable TrueType fonts exactly as distributed by Google Fonts (install these on desktop for InDesign, Illustrator, Word, PowerPoint, Keynote, Figma).
- `Font_Files/<Family>/*-variable.woff2` — web subsets (Latin, Latin Extended-A, general punctuation, ₹, arrows) produced with fontTools for the website design system. Variation axes are preserved.
- `Font_Files/<Family>/OFL.txt` — the licence that must travel with the files.

## Obligations under the OFL
1. Keep `OFL.txt` with the font files when you redistribute them (e.g. inside a website build or a template pack).
2. Do not sell the fonts by themselves.
3. If you modify a font and redistribute it, do not use the Reserved Font Names ("Fraunces", "Inter") for the modified version. The woff2 subsets here are *not* renamed because subsetting for web embedding is standard practice and they are distributed only as part of this website; if in doubt, serve the original TTFs or Google Fonts' hosted CSS.

## Fallback stacks (as used in `brand.css`)
```
--font-display: "Fraunces", "Iowan Old Style", Palatino, Georgia, serif;
--font-heading: "Inter Tight", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
--font-text:    "Inter", "SF Pro Text", -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
```

## Office documents
Word and PowerPoint templates in this package reference Fraunces, Inter Tight and Inter. Install the TTFs on every machine that edits them; if the fonts are missing, the documents fall back to Georgia and Arial (acceptable for internal drafts, not for client-facing output).
