# Business card — print specifications

**Sanzeed Mirza · Experiential Design Consultant** — two concepts, same back.

| | |
|---|---|
| Trim | 89 × 51 mm (3.5 × 2 in), landscape |
| Bleed | 3 mm all round (page 95 × 57 mm in the masters) |
| Safe area | 4 mm inside the trim — nothing essential outside it |
| Stock | 350 gsm uncoated natural white (e.g. GF Smith Colorplan Natural, Fedrigoni Arena Natural Rough or equivalent). 540 gsm duplex if a thicker card is wanted. |
| Finish | Uncoated, no lamination. Optional: soft-touch matt on concept B's black side only if the printer guarantees no scuffing. |
| Colour | CMYK process (print-ready PDFs are converted with `print_pdf.py --cmyk`). Soot text = C0 M8 Y15 K90; Old Gold = C0 M27 Y68 K28 — or spot **Pantone 7510 C** (verify with a swatch). Gallery Black side = rich black C60 M40 Y40 K100. Plaster background = C0 M2 Y6 K4 (omit the fill and print on natural-white stock if you prefer the paper colour). |
| Gold foil option | The three gold points in the wordmark (A, Z, D) and the full stop that ends the master line may be hot-foil stamped instead of printed: matt gold foil, nearest **Pantone 871 C** / Kurz Luxor 428. Supply the `wordmark-dots` group and the `.point` tspan as the foil plate (they are separate groups in the SVG). Points are 1.32 mm Ø on the lockup (concept A) and 1.12 mm Ø on the wordmark (concept B). The Z point sits inside a ring gap of only ≈ 0.20 mm (A) / 0.17 mm (B): foil must register within that, or the point should be printed rather than foiled. |
| Type | Fraunces Light (opsz 36) 12 pt name, 9.5 pt master line; Inter Tight SemiBold 5.6 pt descriptor (+0.12 em, caps); Inter 7 pt contacts. All text is outlined in the PDFs. |
| Logo | Concept A front: horizontal-descriptor lockup, full-colour-light, 54 mm wide (minimum 50 mm). Concept B front: primary wordmark, full-colour-dark, 46 mm wide (minimum 28 mm). Clear space ½ cap height. |
| Files | `sanzeed-business-card--concept-a--print-cmyk.pdf`, `sanzeed-business-card--concept-b--print-cmyk.pdf` — 2 pages (front, back) with crop marks, trim/bleed boxes, 10 mm slug. |
| Quantity / imposition | Printer's choice; back prints head-to-head with the front (work-and-turn). |

Proof the gold and the warm black against a physical swatch before the full run.
