#!/usr/bin/env python3
"""export_svg.py — export any SVG to PDF / EPS (Inkscape) and PNG / JPG / WebP (cairosvg, Pillow, cwebp).
   python3 export_svg.py in.svg out_basename [--png 2000,1000] [--jpg-bg "#FFFFFF"] [--formats svg,pdf,eps,png,jpg,webp]
"""
import sys, subprocess, os, shutil, cairosvg
from PIL import Image
src, base = sys.argv[1], sys.argv[2]
opts = dict(a.split('=', 1) if '=' in a else (a, '1') for a in sys.argv[3:])
fmts = opts.get('--formats', 'pdf,eps,png,webp').split(',')
widths = [int(w) for w in opts.get('--png', '2000').split(',')]
if 'pdf' in fmts: subprocess.run(['inkscape', src, '--export-type=pdf', f'--export-filename={base}.pdf', '--export-text-to-path'], capture_output=True)
if 'eps' in fmts: subprocess.run(['inkscape', src, '--export-type=eps', f'--export-filename={base}.eps', '--export-text-to-path'], capture_output=True)
for w in widths:
    png = f'{base}-{w}w.png' if len(widths) > 1 else f'{base}.png'
    if 'png' in fmts or 'jpg' in fmts or 'webp' in fmts: cairosvg.svg2png(url=src, write_to=png, output_width=w)
    if 'jpg' in fmts:
        im = Image.open(png).convert('RGBA'); bg = Image.new('RGB', im.size, opts.get('--jpg-bg', '#FFFFFF')); bg.paste(im, mask=im.split()[3]); bg.save(png[:-4] + '.jpg', quality=92, subsampling=0)
    if 'webp' in fmts: subprocess.run(['cwebp', '-quiet', '-q', '92', '-exact', png, '-o', png[:-4] + '.webp'], capture_output=True)
    if 'png' not in fmts: os.remove(png)
print('exported', base)
