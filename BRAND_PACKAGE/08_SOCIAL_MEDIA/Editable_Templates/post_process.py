#!/usr/bin/env python3
"""post_process.py — the non-Chromium exports: profile images copied / resampled from 02_LOGO_SYSTEM/Social_Profile,
the Instagram 3×3 grid preview, and JPG q90 beside every PNG that a platform size-limits (covers, banners, thumbnails).
Run from this folder (render-all.sh does)."""
import pathlib
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parent; SP = ROOT.parent / '02_LOGO_SYSTEM' / 'Social_Profile'

PROFILES = [  # (source tile, destination, resample to)
  ('instagram-profile-320--dark.png',  'Instagram/sanzeed-ig-profile--dark-320x320.png', None),
  ('instagram-profile-320--light.png', 'Instagram/sanzeed-ig-profile--light-320x320.png', None),
  ('universal-profile-1024--dark.png', 'Instagram/sanzeed-ig-profile--dark-1024x1024.png', None),
  ('universal-profile-1024--light.png','Instagram/sanzeed-ig-profile--light-1024x1024.png', None),
  ('facebook-profile-320--dark.png',   'Facebook/sanzeed-fb-profile--dark-320x320.png', None),
  ('facebook-profile-320--light.png',  'Facebook/sanzeed-fb-profile--light-320x320.png', None),
  ('universal-profile-1024--dark.png', 'Facebook/sanzeed-fb-profile--dark-720x720.png', 720),
  ('universal-profile-1024--light.png','Facebook/sanzeed-fb-profile--light-720x720.png', 720),
  ('linkedin-profile-400--dark.png',   'LinkedIn/sanzeed-li-profile--dark-400x400.png', None),
  ('linkedin-profile-400--light.png',  'LinkedIn/sanzeed-li-profile--light-400x400.png', None),
  ('universal-profile-1024--dark.png', 'LinkedIn/sanzeed-li-company-logo--dark-300x300.png', 300),
  ('universal-profile-1024--light.png','LinkedIn/sanzeed-li-company-logo--light-300x300.png', 300),
  ('youtube-profile-800--dark.png',    'YouTube/sanzeed-yt-profile--dark-800x800.png', None),
  ('youtube-profile-800--light.png',   'YouTube/sanzeed-yt-profile--light-800x800.png', None),
  ('x-profile-400--dark.png',          'X/sanzeed-x-profile--dark-400x400.png', None),
  ('x-profile-400--light.png',         'X/sanzeed-x-profile--light-400x400.png', None),
  ('pinterest-profile-165--dark.png',  'Pinterest/sanzeed-pin-profile--dark-165x165.png', None),
  ('pinterest-profile-165--light.png', 'Pinterest/sanzeed-pin-profile--light-165x165.png', None),
  ('universal-profile-1024--dark.png', 'Pinterest/sanzeed-pin-profile--dark-600x600.png', 600),
  ('universal-profile-1024--light.png','Pinterest/sanzeed-pin-profile--light-600x600.png', 600),
]
for src, dst, size in PROFILES:
    im = Image.open(SP / src)
    if size: im = im.resize((size, size), Image.LANCZOS)
    im.save(ROOT / dst, optimize=True); print('  wrote', dst)

GRID = ['sanzeed-ig-post--project-1080x1080.png', 'sanzeed-ig-post--quote-1080x1080.png', 'sanzeed-ig-post--announcement-1080x1080.png',
        'sanzeed-ig-post--project--buddha-park-1080x1080.png', 'sanzeed-ig-post--stat-1080x1080.png', 'sanzeed-ig-post--project--yuge-yugeen-bharat-1080x1080.png',
        'sanzeed-ig-post--announcement--g20-tree-show-1080x1080.png', 'sanzeed-ig-post--quote--whole-room-1080x1080.png', 'sanzeed-ig-post--project--india-pavilion-1080x1080.png']
cell, gap = 540, 6
S = Image.new('RGB', (3 * cell + 2 * gap, 3 * cell + 2 * gap), '#0D0D0F')
for i, f in enumerate(GRID):
    S.paste(Image.open(ROOT / 'Instagram' / f).convert('RGB').resize((cell, cell), Image.LANCZOS), ((i % 3) * (cell + gap), (i // 3) * (cell + gap)))
S.save(ROOT / 'Instagram/sanzeed-ig-grid-preview--3x3-1632x1632.png', optimize=True); print('  wrote Instagram/sanzeed-ig-grid-preview--3x3-1632x1632.png')

JPG = ['Facebook/sanzeed-fb-cover-1640x624.png', 'Facebook/sanzeed-fb-event-cover-1920x1005.png', 'LinkedIn/sanzeed-li-banner--personal-1584x396.png',
       'LinkedIn/sanzeed-li-banner--company-1128x191.png', 'YouTube/sanzeed-yt-banner-2560x1440.png', 'YouTube/sanzeed-yt-thumbnail--project-1280x720.png',
       'YouTube/sanzeed-yt-thumbnail--talk-1280x720.png', 'YouTube/sanzeed-yt-thumbnail--process-1280x720.png', 'YouTube/sanzeed-yt-end-screen-1920x1080.png',
       'X/sanzeed-x-header-1500x500.png']
for f in JPG:
    p = ROOT / f; Image.open(p).convert('RGB').save(p.with_suffix('.jpg'), quality=90, subsampling=0, optimize=True); print('  wrote', f[:-4] + '.jpg')
