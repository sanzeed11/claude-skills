#!/usr/bin/env python3
"""
make_plates.py — derived "plates" for the mockup scenes (13_BRAND_MOCKUPS/_build/plates/).

Nothing here is redrawn or restyled: every plate is the real deliverable from another folder, re-rasterised at the
resolution a 3000 px mockup needs (pdftoppm on the delivered PDFs), cropped to trim where the delivered preview carries
bleed, or (for the four photo composites) the approved image upscaled with Lanczos + a mild unsharp mask.

    python3 make_plates.py            # rebuild every plate
    python3 make_plates.py site       # only the site captures (capture_site.js) and the lower-third hold frame

Requires: poppler (pdftoppm), Pillow, cairosvg, Node + Playwright (for the two captures).
"""
import os, subprocess, sys
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.abspath(os.path.join(HERE, '..', '..'))          # BRAND_PACKAGE
OUT = os.path.join(HERE, 'plates')
os.makedirs(OUT, exist_ok=True)
KIT = os.path.join(B, '15_SOURCE_FILES', 'Project_Files', 'brand-kit')

def p(*a): return os.path.join(B, *a)

def pdf_page(pdf, page, dpi, out, crop_mm=0):
    """Rasterise one PDF page with pdftoppm; optionally crop a bleed margin (mm) on every side."""
    base = os.path.join(OUT, '_tmp')
    subprocess.run(['pdftoppm', '-r', str(dpi), '-f', str(page), '-l', str(page), '-png', '-singlefile', pdf, base], check=True)
    im = Image.open(base + '.png').convert('RGB')
    if crop_mm:
        c = round(crop_mm / 25.4 * dpi)
        im = im.crop((c, c, im.width - c, im.height - c))
    im.save(os.path.join(OUT, out), optimize=True)
    os.remove(base + '.png')
    print(f'{out:48s} {im.width}x{im.height}')

def crop_png(src, out, bleed_mm, page_mm_w, box=None):
    """Crop a delivered preview PNG that carries bleed back to trim (and optionally to a sub-box, in mm of the trim)."""
    im = Image.open(src).convert('RGB')
    ppm = im.width / page_mm_w
    c = round(bleed_mm * ppm)
    im = im.crop((c, c, im.width - c, im.height - c))
    if box:
        x0, y0, x1, y1 = [round(v * ppm) for v in box]
        im = im.crop((x0, y0, x1, y1))
    im.save(os.path.join(OUT, out), optimize=True)
    print(f'{out:48s} {im.width}x{im.height}')

def photo(src, out, width=3000):
    """Upscale an approved image for a full-frame composite: Lanczos + mild unsharp, JPG q90."""
    im = Image.open(src).convert('RGB')
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))
    im.save(os.path.join(OUT, out), quality=90, subsampling=0, optimize=True)
    print(f'{out:48s} {im.width}x{im.height}')

def site_captures():
    site = p('16_WEBSITE_IMPLEMENTATION', 'index.html')
    cap = os.path.join(HERE, 'capture_site.js')
    for theme in ('dark', 'light'):
        subprocess.run(['node', cap, '--in', site, '--out', os.path.join(OUT, f'site-desktop-{theme}-2880x1800.png'),
                        '--width', '1440', '--height', '900', '--scale', '2', '--theme', theme], check=True)
    subprocess.run(['node', cap, '--in', site, '--out', os.path.join(OUT, 'site-mobile-dark-1170x2532.png'),
                    '--width', '390', '--height', '844', '--scale', '3'], check=True)
    # the name lower third, paused on its hold (2.9 s), 2× with alpha
    subprocess.run(['node', os.path.join(KIT, 'render.js'), '--in', p('11_MOTION_GRAPHICS', 'Source_Files', 'lower-third-name', 'index.html'),
                    '--out', os.path.join(OUT, 'lower-third-name-hold-3840x2160.png'), '--width', '1920', '--height', '1080', '--scale', '2',
                    '--transparent', '--wait', '400', '--js', 'document.getAnimations().forEach(a=>{a.pause();a.currentTime=2900})'], check=True)

def plates():
    S = p('09_PRINT_STATIONERY')
    pdf_page(f'{S}/Business_Cards/sanzeed-business-card--concept-a.pdf', 1, 600, 'card-a-front.png')
    pdf_page(f'{S}/Business_Cards/sanzeed-business-card--concept-a.pdf', 2, 600, 'card-a-back.png')
    pdf_page(f'{S}/Business_Cards/sanzeed-business-card--concept-b.pdf', 1, 600, 'card-b-front.png')
    pdf_page(f'{S}/Business_Cards/sanzeed-business-card--concept-b.pdf', 2, 600, 'card-b-back.png')
    pdf_page(f'{S}/Letterheads/sanzeed-letterhead--a4-sample-letter.pdf', 1, 220, 'letterhead-a4-sample-01.png')
    pdf_page(f'{S}/Letterheads/sanzeed-letterhead--a4.pdf', 1, 220, 'letterhead-a4-first.png')
    pdf_page(f'{S}/Envelopes/sanzeed-envelope--dl.pdf', 1, 300, 'envelope-dl-front.png')
    pdf_page(f'{S}/Envelopes/sanzeed-envelope--dl.pdf', 2, 300, 'envelope-dl-back.png')
    pdf_page(f'{S}/Thank_You_Cards/sanzeed-thank-you-card--folded.pdf', 1, 300, 'thank-you-outside.png')
    pdf_page(f'{S}/Thank_You_Cards/sanzeed-thank-you-card--folded.pdf', 2, 300, 'thank-you-inside.png')
    pdf_page(f'{S}/Notepad/sanzeed-notepad--a5.pdf', 1, 300, 'notepad-a5.png')
    pdf_page(f'{S}/ID_Card/sanzeed-id-card.pdf', 1, 600, 'id-card-front.png')
    pdf_page(f'{S}/ID_Card/sanzeed-id-card.pdf', 2, 600, 'id-card-back.png')
    pdf_page(f'{S}/Proposals/sanzeed-proposal-template.pdf', 1, 250, 'proposal-cover.png')
    pdf_page(f'{S}/Presentation_Template/sanzeed-presentation-template.pdf', 1, 220, 'presentation-slide-01.png')
    pdf_page(f'{S}/Folder/sanzeed-folder--a4-outside.pdf', 1, 160, 'folder-flat.png')
    # folder panels from the flat (457 × 395 mm: glue 12 · back 220 · spine 5 · front 220; pocket 90 mm below the back panel)
    im = Image.open(os.path.join(OUT, 'folder-flat.png')); ppm = im.width / 457
    def mm(x0, y0, x1, y1): return tuple(round(v * ppm) for v in (x0, y0, x1, y1))
    im.crop(mm(237, 0, 457, 305)).save(os.path.join(OUT, 'folder-front.png'))
    im.crop(mm(12, 0, 232, 305)).save(os.path.join(OUT, 'folder-back.png'))
    im.crop(mm(12, 305, 232, 395)).rotate(180).save(os.path.join(OUT, 'folder-pocket.png'))
    print('folder-front / folder-back / folder-pocket cropped')

    M = p('10_MARKETING_COLLATERAL')
    crop_png(f'{M}/Posters/sanzeed-poster--campaign-a2-preview.png', 'poster-campaign-a2.png', 3, 426)
    im = Image.open(os.path.join(OUT, 'poster-campaign-a2.png')); im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS).save(os.path.join(OUT, 'poster-campaign-a2.png'), optimize=True)   # 1600 wide is 1.5× what the scene shows; larger PNGs may be painted from a low-res decode
    crop_png(f'{M}/Flyers/sanzeed-flyer--a5-two-sided-front.png', 'flyer-a5-front.png', 3, 154)
    crop_png(f'{M}/Signage/sanzeed-door-plate--300x100mm.png', 'door-plate.png', 3, 306)
    crop_png(f'{M}/Signage/sanzeed-wayfinding--arrow-ahead-300x100mm.png', 'wayfinding-ahead.png', 3, 306)
    # trifold outside panels (297 × 210 landscape + 3 mm bleed; panels 99 / 98 / 100 mm)
    crop_png(f'{M}/Brochures/sanzeed-brochure--a4-trifold-outside.png', 'trifold-out-1.png', 3, 303, (0, 0, 99, 210))
    crop_png(f'{M}/Brochures/sanzeed-brochure--a4-trifold-outside.png', 'trifold-out-2.png', 3, 303, (99, 0, 197, 210))
    crop_png(f'{M}/Brochures/sanzeed-brochure--a4-trifold-outside.png', 'trifold-out-3.png', 3, 303, (197, 0, 297, 210))
    crop_png(f'{M}/Brochures/sanzeed-brochure--a4-trifold-inside.png', 'trifold-in-1.png', 3, 303, (0, 0, 100, 210))
    crop_png(f'{M}/Brochures/sanzeed-brochure--a4-trifold-inside.png', 'trifold-in-2.png', 3, 303, (100, 0, 198, 210))
    crop_png(f'{M}/Brochures/sanzeed-brochure--a4-trifold-inside.png', 'trifold-in-3.png', 3, 303, (198, 0, 297, 210))

    # (the stamp impression masks with the outlined stamp SVG directly, inlined by build_mockups.py)

    # photographs for the four composites
    A = p('06_PHOTOGRAPHY_ART_DIRECTION', 'Approved_Images', 'JPG')
    C = p('00_ORIGINAL_ASSETS_BACKUP', 'images', 'img', 'case')
    photo(f'{A}/sanzeed-img-prime-minister-museum--museum.jpg', 'photo-prime-minister-museum-corridor.jpg')
    photo(f'{C}/prime-minister-museum-06.webp', 'photo-prime-minister-museum-lobby.jpg')
    photo(f'{A}/sanzeed-img-g20-led-show--projection.jpg', 'photo-g20-led-show.jpg')
    photo(f'{C}/ram-katha-show-08.webp', 'photo-ram-katha-show-stage.jpg')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'site':
        site_captures()
    else:
        plates(); site_captures()
