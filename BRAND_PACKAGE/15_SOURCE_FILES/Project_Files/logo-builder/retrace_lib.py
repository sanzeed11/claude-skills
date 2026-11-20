import re, json, subprocess, io, os, sys
import cairosvg
from PIL import Image, ImageFilter
SC = 6            # raster scale (units -> px)
PAD = 40          # units of padding around each letter
def f(v): return f"{v:.2f}".rstrip('0').rstrip('.')

def parse_potrace(svgtxt):
    """Return list of absolute path strings in raster px (y down) from potrace SVG output."""
    g = re.search(r'<g transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([-\d.]+),([-\d.]+)\)"', svgtxt)
    tx, ty, sx, sy = map(float, g.groups())
    paths = re.findall(r'<path d="([^"]+)"', svgtxt, re.S)
    out = []
    for d in paths:
        toks = re.findall(r'[MmLlCcZz]|-?\d+\.?\d*', d)
        i = 0; cmd = None; cx = cy = 0; sx0 = sy0 = 0; segs = []
        T = lambda x, y: (tx + sx * x, ty + sy * y)
        while i < len(toks):
            t = toks[i]
            if t in 'MmLlCcZz':
                cmd = t; i += 1
                if t in 'Zz':
                    segs.append('Z'); cx, cy = sx0, sy0
                continue
            if cmd in 'Mm':
                x, y = float(toks[i]), float(toks[i+1]); i += 2
                if cmd == 'm': x += cx; y += cy
                cx, cy = x, y; sx0, sy0 = x, y
                X, Y = T(x, y); segs.append(f'M{f(X)} {f(Y)}'); cmd = 'l' if cmd == 'm' else 'L'
            elif cmd in 'Ll':
                x, y = float(toks[i]), float(toks[i+1]); i += 2
                if cmd == 'l': x += cx; y += cy
                cx, cy = x, y; X, Y = T(x, y); segs.append(f'L{f(X)} {f(Y)}')
            elif cmd in 'Cc':
                v = [float(t) for t in toks[i:i+6]]; i += 6
                if cmd == 'c': v = [v[0]+cx, v[1]+cy, v[2]+cx, v[3]+cy, v[4]+cx, v[5]+cy]
                pts = [T(v[k], v[k+1]) for k in (0, 2, 4)]
                segs.append('C' + ' '.join(f'{f(a)} {f(b)}' for a, b in pts)); cx, cy = v[4], v[5]
        out.append(''.join(segs))
    return out

def retrace(shape_svg_body, bbox, blur_units=2.2, alphamax=1.0, opttol=0.4, name='x', workdir='.'):
    """Render the given SVG fragment (in wordmark units) inside bbox, smooth, potrace, return path in wordmark units."""
    x0, y0, x1, y1 = bbox[0]-PAD, bbox[1]-PAD, bbox[2]+PAD, bbox[3]+PAD
    W, H = x1-x0, y1-y0
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {W} {H}" width="{W*SC}" height="{H*SC}"><rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="#fff"/><g fill="#000">{shape_svg_body}</g></svg>'
    png = cairosvg.svg2png(bytestring=svg.encode())
    im = Image.open(io.BytesIO(png)).convert('L')
    if blur_units > 0: im = im.filter(ImageFilter.GaussianBlur(blur_units * SC))
    im = im.point(lambda v: 0 if v < 128 else 255).convert('1')
    pbm = os.path.join(workdir, f'_{name}.pbm'); im.save(pbm)
    out = os.path.join(workdir, f'_{name}.svg')
    subprocess.run(['potrace', pbm, '-s', '-o', out, '-a', str(alphamax), '-O', str(opttol), '-t', '20', '--flat'], check=True)
    paths = parse_potrace(open(out).read())
    # raster px -> wordmark units
    def back(p):
        def rep(m):
            X, Y = float(m.group(1)), float(m.group(2))
            return f'{f(x0 + X / SC)} {f(y0 + Y / SC)}'
        return re.sub(r'(-?\d+\.?\d*) (-?\d+\.?\d*)', rep, p)
    return ' '.join(back(p) for p in paths)
