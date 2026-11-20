#!/usr/bin/env python3
"""sync_logo.py — re-inlines the approved primary wordmark into the HTML sources of 07_WEBSITE_DIGITAL_ASSETS.

The wordmark is read at build time from the unioned production artwork
    02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg
(the refined original wordmark, option B, approved 20 Nov 2026: three gold points A, Z, D; the Z point in its ring).
Every inline wordmark SVG — marked with data-logo="primary-wordmark" (or, for sources that predate the marker, the
retired viewBox "0 0 3590 500") — gets the new viewBox, one `currentColor` path for the letters (so it follows the
theme) and one circle.wm-dot per point (CSS fills them with the accent). The opening tag's class/role/aria attributes
are kept. Idempotent; the build scripts (build_og.py, build_share.sh, build_email.sh, render-kit.sh,
render-responsive.sh) call it before rendering.

    python3 sync_logo.py [file-or-folder …]      (default: every .html under this folder)
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
LOGO = HERE.parent / '02_LOGO_SYSTEM' / 'SVG' / 'sanzeed-primary-wordmark--full-colour-dark.svg'
PAT = re.compile(r'<svg(?P<attrs>[^>]*?(?:data-logo="primary-wordmark"|viewBox="0 0 3590 500")[^>]*)>.*?</svg>', re.S)


def wordmark():
    s = re.sub(r'\s+', ' ', LOGO.read_text())
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    ink = re.search(r'id="wordmark-ink"[^>]*>(.*?)</g>', s).group(1)
    d = ' '.join(x.strip() for x in re.findall(r'(?<=\s)d="([^"]+)"', ink))   # (?<=\s) so id="…" is not read as d="…"
    dots = re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)"', s)
    assert d.startswith('M') and len(dots) == 3, 'approved wordmark (three points) not found in ' + str(LOGO)
    return vb, d, dots


def markup(attrs, vb, d, dots):
    attrs = re.sub(r'\s*(?:viewBox|data-logo)="[^"]*"', '', attrs)
    return (f'<svg{attrs} viewBox="{vb}" data-logo="primary-wordmark"><path fill="currentColor" d="{d}"/>'
            + ''.join(f'<circle class="wm-dot" cx="{cx}" cy="{cy}" r="{r}"/>' for cx, cy, r in dots) + '</svg>')


def main(targets):
    vb, d, dots = wordmark()
    files = []
    for t in targets or [HERE]:
        t = pathlib.Path(t).resolve()
        files += sorted(t.rglob('*.html')) if t.is_dir() else [t]
    total = 0
    for f in files:
        html = f.read_text()
        new, n = PAT.subn(lambda m: markup(m.group('attrs'), vb, d, dots), html)
        if n:
            total += n
            if new != html:
                f.write_text(new)
            print(f'  {f}: {n} wordmark(s)')
    print(f'sync_logo: {total} inline wordmark(s) from {LOGO.name} (viewBox {vb}, {len(dots)} points)')


if __name__ == '__main__':
    main(sys.argv[1:])
