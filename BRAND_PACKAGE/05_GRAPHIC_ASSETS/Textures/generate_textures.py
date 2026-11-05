#!/usr/bin/env python3
"""
generate_textures.py — procedural brand textures (numpy + Pillow). Deterministic (fixed seeds).

  python3 generate_textures.py        # writes every texture into this folder

  sanzeed-texture-grain--tile-1024.png     1024 x 1024 transparent grain for `mix-blend-mode: soft-light`
                                           at 7 % opacity on dark backgrounds only (the brand `.grain`).
                                           Seamless: white noise has no low frequency, so it tiles.
  sanzeed-texture-grain--fine-1024.png     finer, lower-amplitude variant for small screens / print proofs
  sanzeed-texture-paper--plaster-2048.jpg  2048 x 2048 Plaster (#F5F0E7) with a subtle laid-paper fibre,
                                           for documents and light backgrounds (q 90)
  sanzeed-texture-paper--paper-2048.jpg    the same fibre on Paper (#FBF8F2)
  sanzeed-texture-lamp-glow--2048.png      2048 x 2048 transparent radial Lamp Gold glow = --sz-gradient-lamp
                                           (centre at 50 % / 40 %), to place behind a single lit object
  sanzeed-texture-lamp-glow--light-2048.png the Old Gold version for Plaster backgrounds
  sanzeed-texture-vignette--1920x1080.png  transparent black vignette (edges 0 -> ~62 % at the corners)
  sanzeed-texture-vignette--1080x1920.png  portrait version
  sanzeed-texture-vignette--1080x1080.png  square version
Edit the parameters in the functions and re-run.
"""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
HERE = Path(__file__).resolve().parent
LAMP, OLD = (233, 178, 90), (184, 134, 59)

def grain(size=1024, sigma=46.0, seed=7, name='tile'):
    """Transparent grain: luminance noise around mid-grey, carried as white/black pixels whose alpha
    is the distance from neutral, so `soft-light` at 7 % reproduces the brand `.grain` exactly."""
    rng = np.random.default_rng(seed)
    n = rng.normal(0, sigma, (size, size)).clip(-127, 127)
    rgb = np.where(n[..., None] >= 0, 255, 0).astype(np.uint8).repeat(3, axis=2)
    a = (np.abs(n) * 2).clip(0, 255).astype(np.uint8)
    Image.fromarray(np.dstack([rgb, a]), 'RGBA').save(HERE / f'sanzeed-texture-grain--{name}-1024.png', optimize=True)

def _fbm(size, rng, octaves=(4, 8, 16, 32, 64), weights=(1, .7, .5, .35, .25)):
    """value-noise fractal: upsampled random grids summed, zero-mean, unit-ish amplitude."""
    out = np.zeros((size, size), np.float32)
    for o, w in zip(octaves, weights):
        g = rng.random((o, o)).astype(np.float32)
        im = Image.fromarray((g*255).astype(np.uint8)).resize((size, size), Image.BICUBIC)
        out += (np.asarray(im).astype(np.float32)/255 - .5) * w
    return out / sum(weights)

def paper(size=2048, base=(245, 240, 231), name='plaster', seed=11, strength=5.5):
    rng = np.random.default_rng(seed)
    fibre = _fbm(size, rng)                                             # soft mottle
    # laid lines: faint horizontal fibre, stretched noise
    laid = rng.normal(0, 1, (size // 16, size)).astype(np.float32)
    laid = np.asarray(Image.fromarray(((laid*40)+128).clip(0,255).astype(np.uint8)).resize((size, size), Image.BILINEAR)).astype(np.float32)/255 - .5
    fine = rng.normal(0, 1, (size, size)).astype(np.float32) * .35     # tooth
    tex = fibre*1.0 + laid*.45 + fine*.6
    img = np.array(base, np.float32)[None, None, :] + tex[..., None] * strength
    Image.fromarray(img.clip(0, 255).astype(np.uint8), 'RGB').save(HERE / f'sanzeed-texture-paper--{name}-2048.jpg', quality=90, subsampling=0, optimize=True, progressive=True)

def lamp_glow(size=2048, colour=LAMP, name='', cx=.5, cy=.4, rx=.6, ry=.6):
    """Matches --sz-gradient-lamp: radial 60 % x 60 % at 50 % 40 %, .55 -> .12 at 28 % -> 0 at 70 %."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float32) / size
    d = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)          # 0 at centre, 1 at the ellipse edge
    stops = [(0, .55), (.28, .12), (.70, 0), (1.0, 0)]
    a = np.interp(d, [s[0] for s in stops], [s[1] for s in stops]).astype(np.float32)
    a = (a * 255).clip(0, 255).astype(np.uint8)
    rgb = np.empty((size, size, 3), np.uint8); rgb[...] = colour
    Image.fromarray(np.dstack([rgb, a]), 'RGBA').save(HERE / f'sanzeed-texture-lamp-glow--{name + "-" if name else ""}2048.png', optimize=True)

def vignette(w=1920, h=1080, strength=.62, start=.55):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    nx, ny = (x / w - .5) * 2, (y / h - .5) * 2
    d = np.sqrt(nx*nx + ny*ny) / np.sqrt(2)                              # 0 centre -> 1 corner
    t = ((d - start) / (1 - start)).clip(0, 1); t = t*t*(3-2*t)          # smoothstep
    a = (t * strength * 255).astype(np.uint8)
    rgb = np.zeros((h, w, 3), np.uint8)
    Image.fromarray(np.dstack([rgb, a]), 'RGBA').save(HERE / f'sanzeed-texture-vignette--{w}x{h}.png', optimize=True)

if __name__ == '__main__':
    grain(); grain(sigma=30.0, seed=9, name='fine')
    paper(); paper(base=(251, 248, 242), name='paper', seed=13, strength=4.5)
    lamp_glow(); lamp_glow(colour=OLD, name='light')
    vignette(); vignette(1080, 1920); vignette(1080, 1080)
    print('textures written to', HERE)
