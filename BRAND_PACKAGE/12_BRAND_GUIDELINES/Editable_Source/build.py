#!/usr/bin/env python3
"""Concatenate the chapter files into Brand_Guidelines.html, render the PDF with the kit's render.js
(A4 landscape, 297 × 210 mm) and write a PNG preview of every page into pages/.

  python3 build.py            # html → pdf → pages/*.png → checks
  python3 build.py --html     # only write Brand_Guidelines.html
  python3 build.py --ui       # (re)render the UI-kit sections used in chapter 17 into assets/ui/
  python3 build.py --check    # only run the checks on the existing files

Checks: every <img src> resolves; pdffonts lists only the brand fonts (plus the documented mono face);
page count and page size from pdfinfo.
"""
import os, re, sys, glob, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
KIT = os.path.join(ROOT, '15_SOURCE_FILES/Project_Files/brand-kit')
OUT_HTML = os.path.join(HERE, 'Brand_Guidelines.html')
OUT_PDF = os.path.join(HERE, '..', 'Brand_Guidelines.pdf')
PAGES = os.path.join(HERE, 'pages')

UI_SECTIONS = ['nav', 'hero', 'buttons', 'links', 'cards', 'forms', 'modal', 'dropdown', 'section', 'quote', 'cta', 'gallery', 'video', 'editorial', 'loading', 'empty', '404', 'toast', 'tags', 'table', 'pagination', 'tabs', 'accordion', 'footer']

def chapter_files():
    return sorted(f for f in glob.glob(os.path.join(HERE, '[0-9][0-9]-*.html')))

def concat():
    parts = []
    for f in chapter_files():
        s = open(f).read()
        m = re.search(r'<!-- chapter:start -->(.*)<!-- chapter:end -->', s, re.S)
        parts.append(f'<!-- {os.path.basename(f)} -->\n' + (m.group(1) if m else ''))
    doc = ('<!doctype html>\n<html lang="en" data-theme="light">\n<head>\n<meta charset="utf-8">\n<title>Sanzeed — Brand Guidelines</title>\n'
           '<link rel="stylesheet" href="guide.css">\n</head>\n<body>\n<main class="doc" style="--doc:\'Brand Guidelines\'">\n' + ''.join(parts) + '</main>\n</body>\n</html>\n')
    open(OUT_HTML, 'w').write(doc)
    print('wrote', os.path.relpath(OUT_HTML, ROOT))

def check_images():
    s = open(OUT_HTML).read()
    srcs = sorted(set(re.findall(r'<img[^>]+src="([^"]+)"', s)))
    missing = [x for x in srcs if not x.startswith('data:') and not os.path.exists(os.path.join(HERE, x))]
    print(f'images referenced: {len(srcs)} · missing: {len(missing)}')
    for m in missing: print('  MISSING', m)
    return not missing

def render_pdf():
    subprocess.run(['node', os.path.join(KIT, 'render.js'), '--in', OUT_HTML, '--out', OUT_PDF, '--pdf', '--size', '297x210', '--landscape', '--wait', '1200'], check=True)
    info = subprocess.run(['pdfinfo', OUT_PDF], capture_output=True, text=True).stdout
    print(''.join(l + '\n' for l in info.splitlines() if l.startswith(('Pages', 'Page size', 'File size'))))

def render_pages(dpi=100):
    shutil.rmtree(PAGES, ignore_errors=True); os.makedirs(PAGES)
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', OUT_PDF, os.path.join(PAGES, 'sanzeed-brand-guidelines--p')], check=True)
    for f in glob.glob(os.path.join(PAGES, '*.png')):  # pdftoppm writes p-001.png; keep the brand naming p001.png
        os.rename(f, f.replace('--p-', '--p'))
    n = len(glob.glob(os.path.join(PAGES, '*.png')))
    print(f'pages/: {n} PNG previews at {dpi} dpi')

def check_fonts():
    out = subprocess.run(['pdffonts', OUT_PDF], capture_output=True, text=True).stdout
    names = sorted(set(re.sub(r'^[A-Z]{6}\+', '', l.split()[0]) for l in out.splitlines()[2:] if l.strip()))
    print('fonts embedded:', ', '.join(names))
    bad = [n for n in names if not re.match(r'(Fraunces|Inter|InterTight|DejaVuSansMono|SFMono|Menlo|Consolas)', n)]
    if bad: print('  UNEXPECTED FONTS:', bad)
    return not bad

def render_ui():
    """Render the UI-kit sections individually (the full page is 27 000 px tall) for chapter 17."""
    os.makedirs(os.path.join(HERE, 'assets', 'ui'), exist_ok=True)
    kit = os.path.join(ROOT, '07_WEBSITE_DIGITAL_ASSETS/UI_Components/ui-kit.html')
    for s in UI_SECTIONS:
        out = os.path.join(HERE, 'assets', 'ui', f'{s}.png')
        subprocess.run(['node', os.path.join(KIT, 'render.js'), '--in', kit, '--out', out, '--width', '1440', '--height', '900', '--scale', '1', '--selector', f'#s-{s}', '--wait', '800'], check=True)
    # light theme of two sections
    for s in ['cards', 'forms']:
        out = os.path.join(HERE, 'assets', 'ui', f'{s}-light.png')
        subprocess.run(['node', os.path.join(KIT, 'render.js'), '--in', kit, '--out', out, '--width', '1440', '--height', '900', '--scale', '1', '--selector', f'#s-{s}', '--wait', '800',
                        '--js', "document.documentElement.setAttribute('data-theme','light')"], check=True)

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--ui' in a: render_ui(); sys.exit()
    if '--check' in a: ok = check_images() and check_fonts(); sys.exit(0 if ok else 1)
    concat()
    if '--html' in a: check_images(); sys.exit()
    if not check_images(): sys.exit('missing images — fix before rendering')
    render_pdf(); render_pages(); check_fonts()
