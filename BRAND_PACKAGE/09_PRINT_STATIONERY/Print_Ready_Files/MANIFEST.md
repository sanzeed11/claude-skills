# Print-ready files — manifest

Every file: trim + 3 mm bleed + 10 mm slug with crop marks at the trim; TrimBox and BleedBox set; colours converted to CMYK by Ghostscript (`print_pdf.py --cmyk`); all text outlined or embedded. Verified with `pdfinfo` (sheet size = trim + 2 × bleed + 2 × slug) and `pdfimages -list` (raster colour space).

Rich black for large dark solids: C60 M40 Y40 K100. Old Gold = C0 M27 Y68 K28 (or spot Pantone 7510 C — verify with a swatch). Proof the gold and the warm black before the run.

| File | Trim (mm) | Bleed | Pages | Sheet incl. slug | Colour | Notes |
|---|---|---|---|---|---|---|
| sanzeed-business-card-concept-a--print-cmyk.pdf | 89 × 51 | 3 mm | 2 | 115.0 × 77.0 mm | CMYK (vector) | front + back; Plaster both sides; foil option on the dots |
| sanzeed-business-card-concept-b--print-cmyk.pdf | 89 × 51 | 3 mm | 2 | 115.0 × 77.0 mm | CMYK (images: cmyk) | front (rich black) + back (Plaster) |
| sanzeed-letterhead-a4--print-cmyk.pdf | 210 × 297 | 3 mm | 2 | 236.0 × 323.0 mm | CMYK (vector) | first page + continuation page |
| sanzeed-letterhead-us-letter--print-cmyk.pdf | 215.9 × 279.4 | 3 mm | 2 | 241.9 × 305.4 mm | CMYK (vector) | first page + continuation page |
| sanzeed-envelope-dl--print-cmyk.pdf | 220 × 110 | 3 mm | 2 | 246.0 × 136.0 mm | CMYK (vector) | front + back (flap); window-free |
| sanzeed-envelope-c5--print-cmyk.pdf | 229 × 162 | 3 mm | 2 | 255.0 × 188.0 mm | CMYK (vector) | front + back (flap); window-free |
| sanzeed-cover-company-profile-dark--print-cmyk.pdf | 210 × 297 | 3 mm | 1 | 236.0 × 323.0 mm | CMYK (vector) | rich black with the lamp |
| sanzeed-cover-company-profile-light--print-cmyk.pdf | 210 × 297 | 3 mm | 1 | 236.0 × 323.0 mm | CMYK (vector) | Plaster |
| sanzeed-cover-report-dark--print-cmyk.pdf | 210 × 297 | 3 mm | 1 | 236.0 × 323.0 mm | CMYK (images: cmyk) | rich black, image plate (image 960 px wide — see README) |
| sanzeed-cover-report-light--print-cmyk.pdf | 210 × 297 | 3 mm | 1 | 236.0 × 323.0 mm | CMYK (images: cmyk) | Plaster, image plate |
| sanzeed-folder-a4--print-cmyk.pdf | 457 × 395 (flat) | 3 mm | 1 | 483.0 × 421.0 mm | CMYK (images: cmyk) | outside 4/0; dieline supplied separately (Folder/sanzeed-folder--a4-dieline.pdf) |
| sanzeed-notepad-a5--print-cmyk.pdf | 148 × 210 | 3 mm | 1 | 174.0 × 236.0 mm | CMYK (vector) | single sheet, pad of 50 |
| sanzeed-notepad-a4--print-cmyk.pdf | 210 × 297 | 3 mm | 1 | 236.0 × 323.0 mm | CMYK (vector) | single sheet, pad of 50 |
| sanzeed-id-card-cr80--print-cmyk.pdf | 54 × 85.6 | 3 mm | 2 | 80.0 × 111.6 mm | CMYK (images: cmyk) | front + back; corner radius 3.18 |
| sanzeed-lanyard-strip--print-cmyk.pdf | 900 × 20 | 3 mm | 1 | 926.0 × 46.0 mm | CMYK (vector) | dye-sublimation strip, repeat |
| sanzeed-thank-you-card-folded--print-cmyk.pdf | 210 × 148 (A5 flat, folds to A6) | 3 mm | 2 | 236.0 × 174.0 mm | CMYK (vector) | outside + inside |
| sanzeed-thank-you-postcard-a6--print-cmyk.pdf | 148 × 105 | 3 mm | 2 | 174.0 × 131.0 mm | CMYK (vector) | front + back |

Not in this folder (single-colour, no bleed): the stamp artwork — `Stamp/sanzeed-stamp--round-40mm.pdf` and `Stamp/sanzeed-stamp--rectangular-58x22mm.pdf` (100 K, text outlined). The folder dieline is `Folder/sanzeed-folder--a4-dieline.pdf` (supply with the folder print file).
