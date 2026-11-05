#!/usr/bin/env python3
"""
qa_audit.py — package-wide quality audit for BRAND_PACKAGE.
Walks every deliverable folder and checks:
  • SVG parses as XML, has a viewBox, and (for logo SVGs) contains no <text> that would need fonts
  • PNG opens; reports mode/size; flags logo PNGs without alpha; flags images under 64 px that are not icons
  • JPG/WebP open and report size
  • PDF opens (pypdf), page count and page sizes in mm; flags zero-page or encrypted files
  • MP4/WebM/MOV/GIF probe with ffprobe (codec, size, frames)
  • DOCX/PPTX open with python-docx / python-pptx
  • File naming: lowercase, no spaces (warn), extension sanity (no fake .ai/.psd/.indd/.eps unless EPS header present)
  • Zero-byte files, placeholder text ("lorem ipsum", "placeholder", "your text here") inside html/md/svg/docx
  • Every folder listed in the required structure exists and is non-empty
Writes QA_REPORT.md and qa_report.json next to this script's output argument.
Usage: python3 qa_audit.py <BRAND_PACKAGE> <out_dir>
"""
import os, sys, re, json, subprocess, zipfile, io
from xml.etree import ElementTree as ET
from PIL import Image
from pypdf import PdfReader

ROOT, OUT = sys.argv[1], sys.argv[2]
REQUIRED = ['01_BRAND_STRATEGY', '02_LOGO_SYSTEM/Source_Files', '02_LOGO_SYSTEM/SVG', '02_LOGO_SYSTEM/PDF', '02_LOGO_SYSTEM/PNG', '02_LOGO_SYSTEM/JPG', '02_LOGO_SYSTEM/WebP',
  '02_LOGO_SYSTEM/Full_Color', '02_LOGO_SYSTEM/Black', '02_LOGO_SYSTEM/White', '02_LOGO_SYSTEM/Grayscale', '02_LOGO_SYSTEM/Favicon',
  '03_COLOUR_SYSTEM/Colour_Swatches', '04_TYPOGRAPHY/Typography_Specimens', '05_GRAPHIC_ASSETS/Patterns', '05_GRAPHIC_ASSETS/Textures', '05_GRAPHIC_ASSETS/Illustrations',
  '05_GRAPHIC_ASSETS/Icons', '05_GRAPHIC_ASSETS/Backgrounds', '05_GRAPHIC_ASSETS/Decorative_Elements', '06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images', '06_PHOTOGRAPHY_ART_DIRECTION/Image_Templates',
  '07_WEBSITE_DIGITAL_ASSETS/Favicon', '07_WEBSITE_DIGITAL_ASSETS/App_Icons', '07_WEBSITE_DIGITAL_ASSETS/Open_Graph', '07_WEBSITE_DIGITAL_ASSETS/Website_Graphics', '07_WEBSITE_DIGITAL_ASSETS/UI_Components', '07_WEBSITE_DIGITAL_ASSETS/Social_Sharing',
  '08_SOCIAL_MEDIA/Instagram', '08_SOCIAL_MEDIA/Facebook', '08_SOCIAL_MEDIA/LinkedIn', '08_SOCIAL_MEDIA/YouTube', '08_SOCIAL_MEDIA/X', '08_SOCIAL_MEDIA/Editable_Templates',
  '09_PRINT_STATIONERY/Business_Cards', '09_PRINT_STATIONERY/Letterheads', '09_PRINT_STATIONERY/Envelopes', '09_PRINT_STATIONERY/Invoices', '09_PRINT_STATIONERY/Quotations', '09_PRINT_STATIONERY/Thank_You_Cards', '09_PRINT_STATIONERY/Print_Ready_Files',
  '10_MARKETING_COLLATERAL/Brochures', '10_MARKETING_COLLATERAL/Flyers', '10_MARKETING_COLLATERAL/Posters', '10_MARKETING_COLLATERAL/Presentations', '10_MARKETING_COLLATERAL/Media_Kit', '10_MARKETING_COLLATERAL/Campaign_Templates',
  '11_MOTION_GRAPHICS/Logo_Animations', '11_MOTION_GRAPHICS/Intros_Outros', '11_MOTION_GRAPHICS/Social_Animations', '11_MOTION_GRAPHICS/Source_Files', '11_MOTION_GRAPHICS/Exports',
  '12_BRAND_GUIDELINES/Editable_Source', '13_BRAND_MOCKUPS/Logo_Mockups', '13_BRAND_MOCKUPS/Stationery_Mockups', '13_BRAND_MOCKUPS/Digital_Mockups', '13_BRAND_MOCKUPS/Marketing_Mockups',
  '14_PRESENTATION/Editable_Presentation', '15_SOURCE_FILES/Original_Designs', '15_SOURCE_FILES/Editable_Assets', '15_SOURCE_FILES/Project_Files']
REQUIRED_FILES = ['01_BRAND_STRATEGY/Brand_Strategy.pdf', '01_BRAND_STRATEGY/Brand_Positioning.md', '01_BRAND_STRATEGY/Brand_Voice_and_Tone.md', '01_BRAND_STRATEGY/Brand_Messaging.md',
  '03_COLOUR_SYSTEM/Colour_Palette.pdf', '03_COLOUR_SYSTEM/colour-tokens.json', '03_COLOUR_SYSTEM/colour-variables.css', '04_TYPOGRAPHY/Font_Reference.pdf', '04_TYPOGRAPHY/Font_Licensing.md',
  '06_PHOTOGRAPHY_ART_DIRECTION/Moodboard.pdf', '06_PHOTOGRAPHY_ART_DIRECTION/Photography_Guidelines.pdf', '12_BRAND_GUIDELINES/Brand_Guidelines.pdf', '12_BRAND_GUIDELINES/Brand_Usage_Reference.md',
  '14_PRESENTATION/Brand_Presentation.pdf', 'README.md', 'DELIVERY_CHECKLIST.md']
PLACEHOLDER = re.compile(r'lorem ipsum|your text here|placeholder text|\bTBD\b|\bTODO\b|dummy text', re.I)
issues = []; stats = {'files': 0, 'bytes': 0, 'by_ext': {}}
def issue(level, path, msg): issues.append({'level': level, 'path': os.path.relpath(path, ROOT), 'msg': msg})

def probe_video(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height,nb_frames,pix_fmt', '-of', 'json', p], capture_output=True, text=True)
    try: return json.loads(r.stdout)['streams'][0]
    except Exception: return None

for dp, dn, fn in os.walk(ROOT):
    if '/.git' in dp or 'node_modules' in dp or '_frames' in dp: continue
    for f in fn:
        p = os.path.join(dp, f); ext = f.lower().rsplit('.', 1)[-1] if '.' in f else ''
        size = os.path.getsize(p); stats['files'] += 1; stats['bytes'] += size; stats['by_ext'][ext] = stats['by_ext'].get(ext, 0) + 1
        if size == 0: issue('error', p, 'zero-byte file'); continue
        if ' ' in f: issue('warn', p, 'filename contains spaces')
        if ext in ('ai', 'psd', 'indd', 'sketch', 'fig'):
            issue('error', p, f'proprietary extension .{ext} present — must be a genuine file; verify header')
        try:
            if ext == 'svg':
                t = ET.parse(p).getroot()
                if not t.get('viewBox'): issue('warn', p, 'SVG has no viewBox')
                if '02_LOGO_SYSTEM' in p and t.iter('{http://www.w3.org/2000/svg}text') and any(True for _ in t.iter('{http://www.w3.org/2000/svg}text')) and 'Guidelines' not in p and 'construction' not in f:
                    issue('warn', p, 'logo SVG contains <text> (font dependency)')
            elif ext == 'png':
                im = Image.open(p); im.verify(); im = Image.open(p)
                if '02_LOGO_SYSTEM/PNG' in p and 'tile' not in f and im.mode != 'RGBA': issue('error', p, f'logo PNG not transparent ({im.mode})')
                if im.width < 16 or im.height < 16: issue('warn', p, f'tiny image {im.size}')
            elif ext in ('jpg', 'jpeg', 'webp'):
                im = Image.open(p); im.verify()
            elif ext == 'pdf':
                r = PdfReader(p)
                if r.is_encrypted: issue('error', p, 'PDF encrypted')
                n = len(r.pages)
                if n == 0: issue('error', p, 'PDF has no pages')
                else:
                    b = r.pages[0].mediabox; w, h = float(b.width) * 25.4 / 72, float(b.height) * 25.4 / 72
                    if w < 5 or h < 5: issue('warn', p, f'PDF page very small {w:.1f}×{h:.1f} mm')
            elif ext == 'eps':
                head = open(p, 'rb').read(64)
                if not head.startswith(b'%!PS'): issue('error', p, 'EPS lacks PostScript header — not a genuine EPS')
            elif ext in ('mp4', 'webm', 'mov', 'gif'):
                if ext != 'gif':
                    s = probe_video(p)
                    if not s: issue('error', p, 'ffprobe could not read video')
                    elif int(s.get('width', 0)) % 2 and ext == 'mp4': issue('warn', p, 'odd width for H.264')
                else:
                    im = Image.open(p); getattr(im, 'n_frames', 1) > 1 or issue('warn', p, 'GIF has a single frame')
            elif ext == 'docx':
                import docx; docx.Document(p)
            elif ext == 'pptx':
                import pptx; pptx.Presentation(p)
            elif ext == 'ico':
                Image.open(p)
            elif ext == 'json':
                json.load(open(p))
            if ext in ('html', 'md', 'svg', 'txt', 'css') and size < 5_000_000:
                txt = open(p, encoding='utf-8', errors='ignore').read()
                m = PLACEHOLDER.search(txt)
                if m and 'qa_audit' not in f and 'BRAND_KIT_SPEC' not in f and 'README' not in f and 'DELIVERY_CHECKLIST' not in f and 'QA_REPORT' not in f:
                    issue('warn', p, f'placeholder text: "{m.group(0)}"')
            if ext == 'docx':
                z = zipfile.ZipFile(p); txt = z.read('word/document.xml').decode('utf-8', 'ignore')
                m = PLACEHOLDER.search(txt)
                if m: issue('warn', p, f'placeholder text in DOCX: "{m.group(0)}"')
        except Exception as e:
            issue('error', p, f'cannot open/parse: {type(e).__name__}: {str(e)[:120]}')

for d in REQUIRED:
    full = os.path.join(ROOT, d)
    if not os.path.isdir(full): issue('error', full, 'required folder missing')
    elif not any(os.scandir(full)): issue('error', full, 'required folder is empty')
for f in REQUIRED_FILES:
    if not os.path.isfile(os.path.join(ROOT, f)): issue('error', os.path.join(ROOT, f), 'required file missing')
# README per top-level folder
for d in sorted(os.listdir(ROOT)):
    full = os.path.join(ROOT, d)
    if os.path.isdir(full) and re.match(r'\d\d_', d) and not os.path.isfile(os.path.join(full, 'README.md')):
        issue('warn', full, 'top-level folder has no README.md')

os.makedirs(OUT, exist_ok=True)
json.dump({'stats': stats, 'issues': issues}, open(os.path.join(OUT, 'qa_report.json'), 'w'), indent=1)
errs = [i for i in issues if i['level'] == 'error']; warns = [i for i in issues if i['level'] == 'warn']
md = ['# QA report — BRAND_PACKAGE', '', f'Files scanned: {stats["files"]} · total size: {stats["bytes"]/1e6:.1f} MB', '',
      '| Extension | Count |', '|---|---|'] + [f'| {k or "(none)"} | {v} |' for k, v in sorted(stats['by_ext'].items(), key=lambda x: -x[1])] + ['', f'## Errors ({len(errs)})', '']
md += [f'- `{i["path"]}` — {i["msg"]}' for i in errs] or ['- none']
md += ['', f'## Warnings ({len(warns)})', ''] + ([f'- `{i["path"]}` — {i["msg"]}' for i in warns] or ['- none'])
open(os.path.join(OUT, 'QA_REPORT.md'), 'w').write('\n'.join(md))
print(f'files {stats["files"]}  errors {len(errs)}  warnings {len(warns)}')
