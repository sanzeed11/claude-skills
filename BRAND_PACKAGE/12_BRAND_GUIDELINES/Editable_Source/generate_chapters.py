#!/usr/bin/env python3
"""Write the chapter HTML files (00-cover.html … 27-appendix.html) from the chapter modules in lib/.

The chapter files are the editable layer: edit them directly for copy or layout changes and run
build.py; re-run this script when tokens (colour-tokens.json, typography-tokens.json) or an asset
path changes. Large rasters are copied, downsampled, into assets/ by lib/guide.A().
"""
import sys, os, importlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
import guide
from guide import chapter_file

mods = {}
for m in ['ch_a', 'ch_b', 'ch_c', 'ch_d']:
    try: mods[m] = importlib.import_module(m)
    except ModuleNotFoundError as e:
        if e.name == m: continue
        raise

def get(fn):
    for m in mods.values():
        if hasattr(m, fn): return getattr(m, fn)
    return None

CHAPTERS = [  # (num, slug, title, builder)
    ('01', 'introduction', 'Brand introduction', 'ch01'), ('02', 'strategy', 'Brand strategy', 'ch02'), ('03', 'positioning', 'Positioning', 'ch03'),
    ('04', 'personality-voice', 'Personality & voice summary', 'ch04'), ('05', 'logo-system', 'Logo system', 'ch05'), ('06', 'logo-construction', 'Logo construction', 'ch06'),
    ('07', 'logo-colour-versions', 'Logo variations & colour versions', 'ch07'), ('08', 'clear-space-placement', 'Clear space & placement', 'ch08'),
    ('09', 'minimum-sizes', 'Minimum sizes', 'ch09'), ('10', 'incorrect-usage', 'Incorrect usage', 'ch10'), ('11', 'signature-monogram', 'Signature mark and monogram', 'ch11'),
    ('12', 'colour-system', 'Colour system', 'ch12'), ('13', 'typography', 'Typography', 'ch13'), ('14', 'graphic-elements', 'Graphic elements', 'ch14'),
    ('15', 'iconography', 'Iconography', 'ch15'), ('16', 'photography', 'Photography standards & art direction', 'ch16'), ('17', 'website', 'Website application', 'ch17'),
    ('18', 'digital-assets', 'Digital assets', 'ch18'), ('19', 'social-media', 'Social media application', 'ch19'), ('20', 'print-stationery', 'Print & corporate stationery', 'ch20'),
    ('21', 'marketing', 'Marketing materials', 'ch21'), ('22', 'signage', 'Signage & environmental', 'ch22'), ('23', 'motion', 'Motion design', 'ch23'),
    ('24', 'voice-communication', 'Brand voice & communication', 'ch24'), ('25', 'applications-gallery', 'Applications gallery', 'ch25'),
    ('26', 'formats-production', 'File formats, naming & production specifications', 'ch26'), ('27', 'appendix', 'Appendix · Delivery index', 'appendix'),
]

def main():
    only = sys.argv[1:]  # optional chapter numbers to regenerate
    built = []
    pageno = 1  # cover
    toc = []
    cover = get('cover')()  # page 1; contents is page 2
    pageno = 3
    manifest = []
    for num, slug, title, fn in CHAPTERS:
        b = get(fn)
        if b is None:
            print('  (missing builder', fn, '— skipped)'); continue
        pages = b()
        if not only or num in only:
            f, n = chapter_file(num, slug, title, pages)
            print(f'  {f}: {n} pages')
        toc.append((num if num != '27' else 'A', title, pageno))
        manifest.append((num, slug, title, pageno, len(pages)))
        pageno += len(pages)
    back = get('back')()
    chapter_file('00', 'cover', 'Cover and contents', [cover, get('contents')(toc)])
    chapter_file('99', 'back-cover', 'Back cover', [back])
    print(f'  total pages: {pageno}')
    with open('page-manifest.txt', 'w') as f:
        f.write('chapter\tslug\ttitle\tfirst_page\tpages\n')
        for m in manifest: f.write('\t'.join(str(x) for x in m) + '\n')

if __name__ == '__main__': main()
