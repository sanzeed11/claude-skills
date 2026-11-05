#!/usr/bin/env python3
"""print_pdf.py — turn a screen PDF (RGB, trimmed size) into a print-ready PDF: adds bleed by scaling the
   page onto a larger sheet, draws crop marks, and converts colours to CMYK with Ghostscript.
   python3 print_pdf.py in.pdf out.pdf --trim 90x54 --bleed 3 [--marks] [--cmyk]
   Trim size in mm. The input must already be laid out with artwork extending into the bleed area
   (i.e. the input page size = trim + 2*bleed). This script only adds marks, slug and CMYK conversion.
"""
import sys, subprocess, os, tempfile
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
src, dst = sys.argv[1], sys.argv[2]
opts = dict(a.split('=', 1) if '=' in a else (a, '1') for a in sys.argv[3:])
tw, th = [float(v) for v in opts.get('--trim', '210x297').split('x')]
bleed = float(opts.get('--bleed', '3')); slug = 10.0
reader = PdfReader(src); writer = PdfWriter()
sheet_w, sheet_h = tw + 2*bleed + 2*slug, th + 2*bleed + 2*slug
for pg in reader.pages:
    tmp = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False).name
    c = canvas.Canvas(tmp, pagesize=(sheet_w*mm, sheet_h*mm)); c.setLineWidth(0.25); c.setStrokeColorCMYK(0, 0, 0, 1)
    ox, oy = slug*mm, slug*mm; bw, bh = (tw + 2*bleed)*mm, (th + 2*bleed)*mm; b = bleed*mm; gap = 3*mm; ln = 6*mm
    for (x, y) in [(ox + b, oy + b), (ox + bw - b, oy + b), (ox + b, oy + bh - b), (ox + bw - b, oy + bh - b)]:
        sx = -1 if x < ox + bw/2 else 1; sy = -1 if y < oy + bh/2 else 1
        c.line(x + sx*gap, y, x + sx*(gap + ln), y); c.line(x, y + sy*gap, x, y + sy*(gap + ln))
    c.setFont('Helvetica', 6); c.drawString(ox, 3*mm, f"Sanzeed — trim {tw:g}×{th:g} mm, bleed {bleed:g} mm. Crop marks at trim. Colours CMYK (converted; proof before print).")
    c.save()
    marks = PdfReader(tmp).pages[0]
    marks.merge_transformed_page(pg, Transformation().translate(slug*mm, slug*mm))
    marks.mediabox = RectangleObject([0, 0, sheet_w*mm, sheet_h*mm])
    marks.trimbox = RectangleObject([(slug+bleed)*mm, (slug+bleed)*mm, (slug+bleed+tw)*mm, (slug+bleed+th)*mm])
    marks.bleedbox = RectangleObject([slug*mm, slug*mm, (slug+2*bleed+tw)*mm, (slug+2*bleed+th)*mm])
    writer.add_page(marks); os.remove(tmp)
mid = dst + '.rgb.pdf'; writer.write(mid)
if '--cmyk' in opts:
    subprocess.run(['gs', '-q', '-dNOPAUSE', '-dBATCH', '-sDEVICE=pdfwrite', '-dPDFSETTINGS=/prepress', '-sColorConversionStrategy=CMYK', '-dProcessColorModel=/DeviceCMYK', '-dOverrideICC', f'-sOutputFile={dst}', mid], check=True)
    os.remove(mid)
else:
    os.replace(mid, dst)
print('print-ready', dst)
