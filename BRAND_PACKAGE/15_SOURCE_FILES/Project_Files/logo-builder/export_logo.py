#!/usr/bin/env python3
"""
Export pipeline for the Sanzeed logo system.

1. Takes the construction SVGs written by build_logo.py.
2. Unions each colour group's sub-paths into one clean outline (Inkscape 1.2, path-union).
3. Exports genuine PDF and EPS (Inkscape), transparent PNG (cairosvg), white-background JPG (Pillow),
   WebP (cwebp), favicon ICO/PNG sizes and social-profile sizes.

Nothing here renames a file to fake a format: every PDF/EPS is written by Inkscape's own exporters.

Usage: python3 export_logo.py <construction_dir> <02_LOGO_SYSTEM dir>
"""
import os, re, sys, json, subprocess, shutil, io
import cairosvg
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
PNG_WIDTHS = {'primary-wordmark': [3000, 1200, 600], 'wordmark-plain': [3000, 1200], 'secondary-symbol-wordmark': [3000, 1200],
              'horizontal-descriptor': [3000, 1200], 'vertical-stacked': [2000, 1000], 'symbol': [1200, 512, 256],
              'monogram': [1600, 800], 'simplified-small-size': [1200, 400, 200], 'symbol-small-size': [512, 128, 64],
              'symbol-tile': [1024, 512], 'symbol-tile-square': [1024, 512]}

def run(cmd, timeout=180):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        print("ERR", " ".join(cmd)[:200], r.stderr[-400:])
    return r.returncode == 0

def union_svg(src, dst):
    s = open(src).read()
    groups = re.findall(r'<g id="([^"]+)-ink"', s)
    actions = []
    for gname in groups:
        ids = re.findall(rf'<path id="({re.escape(gname)}-[^"]+)"', s)
        if len(ids) > 1:
            actions.append(f"select-by-id:{','.join(ids)};path-union;select-clear")
    if not actions:
        shutil.copy(src, dst); return
    act = ";".join(actions) + f";export-plain-svg;export-filename:{dst};export-do"
    ok = run(["inkscape", src, f"--actions={act}"])
    if not ok or not os.path.exists(dst):
        shutil.copy(src, dst); return
    # tidy Inkscape's plain SVG: drop generated ids on circles/defs, keep structure
    t = open(dst).read()
    t = re.sub(r'\s+id="(svg|defs|g|circle|title|desc)\d+"', '', t)
    t = re.sub(r'\s+xmlns:svg="[^"]+"', '', t)
    t = re.sub(r'<defs\s*/>', '', t)
    t = re.sub(r'\n\s*\n', '\n', t)
    open(dst, 'w').write(t)

def export_png(svg, png, width, bg=None):
    cairosvg.svg2png(url=svg, write_to=png, output_width=width, background_color=bg)

def main():
    for sub in ['Source_Files', 'SVG', 'PDF', 'EPS', 'PNG', 'JPG', 'WebP', 'Favicon', 'Social_Profile',
                'Full_Color', 'Black', 'White', 'Grayscale', 'Single_Color']:
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    manifest = json.load(open(os.path.join(SRC, 'manifest.json')))
    report = []
    for m in manifest:
        fn = m['file']; variant = m['variant']; colour = m['colour']; base = fn[:-4]
        src = os.path.join(SRC, fn)
        shutil.copy(src, os.path.join(OUT, 'Source_Files', fn))                 # construction source (separate sub-paths)
        svg = os.path.join(OUT, 'SVG', fn)
        union_svg(src, svg)                                                      # production SVG (unioned)
        pdf = os.path.join(OUT, 'PDF', base + '.pdf'); eps = os.path.join(OUT, 'EPS', base + '.eps')
        run(["inkscape", svg, "--export-type=pdf", f"--export-filename={pdf}", "--export-text-to-path"])
        run(["inkscape", svg, "--export-type=eps", f"--export-filename={eps}", "--export-text-to-path"])
        widths = PNG_WIDTHS.get(variant, [2000])
        for w in widths:
            png = os.path.join(OUT, 'PNG', f"{base}-{w}w.png")
            export_png(svg, png, w)
            if w == widths[0]:
                # JPG on white (for light-on-light that would vanish, use a dark plate and say so in the name)
                im = Image.open(png).convert('RGBA')
                plate = (255, 255, 255) if colour not in ('white', 'grayscale-inverted', 'full-colour-dark') else (13, 13, 15)
                bgname = 'white' if plate[0] == 255 else 'dark'
                out = Image.new('RGB', im.size, plate); out.paste(im, mask=im.split()[3])
                jpg = os.path.join(OUT, 'JPG', f"{base}-{w}w-on-{bgname}.jpg")
                out.save(jpg, quality=94, subsampling=0)
                webp = os.path.join(OUT, 'WebP', f"{base}-{w}w.webp")
                run(["cwebp", "-quiet", "-q", "92", "-exact", png, "-o", webp])
        report.append({'variant': variant, 'colour': colour, 'svg': svg, 'pdf': pdf, 'eps': eps})
        # convenience colour folders (SVG + largest PNG)
        folder = {'full-colour-dark': 'Full_Color', 'full-colour-light': 'Full_Color', 'black': 'Black', 'white': 'White',
                  'grayscale': 'Grayscale', 'grayscale-inverted': 'Grayscale', 'single-colour-gold': 'Single_Color'}.get(colour)
        if folder:
            shutil.copy(svg, os.path.join(OUT, folder, fn))
            shutil.copy(os.path.join(OUT, 'PNG', f"{base}-{widths[0]}w.png"), os.path.join(OUT, folder, f"{base}-{widths[0]}w.png"))

    # ---- favicons from the tile (dark) and the bare symbol
    tile = os.path.join(OUT, 'SVG', 'sanzeed-symbol-tile--dark.svg')
    fav = os.path.join(OUT, 'Favicon')
    sizes = [16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512, 1024]
    pngs = {}
    for s in sizes:
        p = os.path.join(fav, f"favicon-{s}.png"); export_png(tile, p, s); pngs[s] = p
    Image.open(pngs[256]).save(os.path.join(fav, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    shutil.copy(tile, os.path.join(fav, 'favicon.svg'))
    shutil.copy(pngs[180], os.path.join(fav, 'apple-touch-icon.png'))
    shutil.copy(pngs[192], os.path.join(fav, 'android-chrome-192x192.png'))
    shutil.copy(pngs[512], os.path.join(fav, 'android-chrome-512x512.png'))
    # maskable: tile without rounding (platform masks it) with extra safe padding
    sq = os.path.join(OUT, 'SVG', 'sanzeed-symbol-tile-square--dark.svg')
    export_png(sq, os.path.join(fav, 'maskable-icon-512x512.png'), 512)
    # light-mode favicon (cream tile)
    export_png(os.path.join(OUT, 'SVG', 'sanzeed-symbol-tile--light.svg'), os.path.join(fav, 'favicon-light-64.png'), 64)
    shutil.copy(os.path.join(OUT, 'SVG', 'sanzeed-symbol-tile--light.svg'), os.path.join(fav, 'favicon-light.svg'))
    # Safari pinned tab: monochrome symbol, black
    shutil.copy(os.path.join(OUT, 'SVG', 'sanzeed-symbol--black.svg'), os.path.join(fav, 'safari-pinned-tab.svg'))
    open(os.path.join(fav, 'site.webmanifest'), 'w').write(json.dumps({
        "name": "Sanzeed Mirza — Experiential Design Consultant", "short_name": "Sanzeed",
        "icons": [{"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/maskable-icon-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": "#0D0D0F", "background_color": "#0D0D0F", "display": "standalone", "start_url": "/"}, indent=2))
    open(os.path.join(fav, 'favicon-head-snippet.html'), 'w').write(
'''<!-- Sanzeed favicon set — paste into <head> and serve the files from the site root -->
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="mask-icon" href="/safari-pinned-tab.svg" color="#0D0D0F">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#F5F0E7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0D0D0F" media="(prefers-color-scheme: dark)">
''')

    # ---- social profile images (square + circle-safe), current platform specs
    soc = os.path.join(OUT, 'Social_Profile')
    specs = {'instagram-profile-320': 320, 'facebook-profile-320': 320, 'linkedin-profile-400': 400, 'x-profile-400': 400,
             'youtube-profile-800': 800, 'pinterest-profile-165': 165, 'whatsapp-profile-640': 640, 'universal-profile-1024': 1024}
    for name, s in specs.items():
        for bg in ['dark', 'light']:
            export_png(os.path.join(OUT, 'SVG', f'sanzeed-symbol-tile-square--{bg}.svg'), os.path.join(soc, f"{name}--{bg}.png"), s)
    # circle preview to check the circular crop that platforms apply
    im = Image.open(os.path.join(soc, 'universal-profile-1024--dark.png')).convert('RGBA')
    mask = Image.new('L', im.size, 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse((0, 0, im.size[0]-1, im.size[1]-1), fill=255)
    im.putalpha(mask); im.save(os.path.join(soc, 'universal-profile-1024--dark-circle-preview.png'))
    json.dump(report, open(os.path.join(OUT, 'export-report.json'), 'w'), indent=1)
    print("exported", len(report), "variants")

if __name__ == '__main__':
    main()
