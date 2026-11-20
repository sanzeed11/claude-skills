#!/usr/bin/env python3
"""build_lottie.py — hand-authored Lottie (Bodymovin v5.7) JSON for the Sanzeed motion identity.

Writes:
  sanzeed-logo-reveal.json   1920x1080, 30 fps, 120 frames — the same choreography as logo-reveal/index.html
  sanzeed-loader.json        480x48,    30 fps,  60 frames — the website loader: the point travels the beam, 2 s loop
  player--logo-reveal.html / player--loader.html — self-contained players (lottie-web + the JSON inlined)

Shapes only (ellipses, rectangles, béziers); position / scale / opacity keyframes; the brand easing
cubic-bezier(.22,.8,.2,1) written as keyframe handles o={x:.22,y:.8} i={x:.2,y:1}. No expressions, no effects.
Letter geometry comes from ../_shared/wordmark-letters-unioned.svg (one unioned outline per letter of the approved refined original
wordmark, written by ../_shared/build_shared_logo.py from 02_LOGO_SYSTEM/Source_Files; M/L/C/Z); the points, the Z's ring radius and the
reveal windows come from ../_shared/logo-geometry.json. Three points settle (A, Z, D); a layer mask keeps the Z's ring open (no halo or
glow is ever drawn inside it).
Run:  python3 build_lottie.py
"""
import json, math, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30
GOLD = [233/255, 178/255, 90/255]      # Lamp Gold #E9B25A
WHITE = [245/255, 245/255, 247/255]    # Gallery White #F5F5F7
EASE = {"o": {"x": [0.22], "y": [0.8]}, "i": {"x": [0.2], "y": [1]}}       # light: fast out, long settle
EASE_IO = {"o": {"x": [0.65], "y": [0]}, "i": {"x": [0.2], "y": [1]}}      # symmetrical-ish, for the pulse
EASE_IN = {"o": {"x": [0.6], "y": [0]}, "i": {"x": [0.9], "y": [0.4]}}
LINEAR = {"o": {"x": [0.167], "y": [0.167]}, "i": {"x": [0.833], "y": [0.833]}}

# ------------------------------------------------------------ SVG path -> Lottie bézier
def arc_to_cubics(p0, rx, ry, phi, large, sweep, p1):
    """SVG arc (endpoint parameterisation) -> list of cubic segments (c1, c2, end). Spec F.6.5 + split at <= 90°."""
    x1, y1 = p0; x2, y2 = p1
    if (x1, y1) == (x2, y2): return []
    if rx == 0 or ry == 0: return [((x1, y1), (x2, y2), (x2, y2))]
    phi = math.radians(phi); cp, sp = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p = cp * dx + sp * dy; y1p = -sp * dx + cp * dy
    rx, ry = abs(rx), abs(ry)
    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1: rx *= math.sqrt(lam); ry *= math.sqrt(lam)
    num = rx ** 2 * ry ** 2 - rx ** 2 * y1p ** 2 - ry ** 2 * x1p ** 2
    den = rx ** 2 * y1p ** 2 + ry ** 2 * x1p ** 2
    coef = math.sqrt(max(num / den, 0)) * (-1 if large == sweep else 1)
    cxp = coef * rx * y1p / ry; cyp = -coef * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2; cy = sp * cxp + cp * cyp + (y1 + y2) / 2
    def ang(ux, uy, vx, vy):
        d = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy); return d
    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not sweep and dt > 0: dt -= 2 * math.pi
    if sweep and dt < 0: dt += 2 * math.pi
    n = max(1, math.ceil(abs(dt) / (math.pi / 2)))
    segs = []; a0 = t1; step = dt / n
    for k in range(n):
        a1 = a0 + step
        t = 4 / 3 * math.tan((a1 - a0) / 4)
        def pt(a): return (cx + cp * rx * math.cos(a) - sp * ry * math.sin(a), cy + sp * rx * math.cos(a) + cp * ry * math.sin(a))
        def dv(a): return (-cp * rx * math.sin(a) - sp * ry * math.cos(a), -sp * rx * math.sin(a) + cp * ry * math.cos(a))
        P0 = pt(a0); P3 = pt(a1); D0 = dv(a0); D3 = dv(a1)
        C1 = (P0[0] + t * D0[0], P0[1] + t * D0[1]); C2 = (P3[0] - t * D3[0], P3[1] - t * D3[1])
        segs.append((C1, C2, P3)); a0 = a1
    return segs

def svg_path_to_lottie(d):
    """Absolute M/L/H/V/C/A/Z (what build_shared_logo.py writes). Returns a list of closed Lottie shapes."""
    toks = re.findall(r"[MLHVCAZz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    i = 0; cur = None; start = None; shapes = []; v = []; ins = []; outs = []
    def flush():
        nonlocal v, ins, outs
        if v: shapes.append({"c": True, "v": [list(p) for p in v], "i": [list(p) for p in ins], "o": [list(p) for p in outs]})
        v, ins, outs = [], [], []
    def add_vertex(p, in_t=(0, 0)):
        v.append(p); ins.append(in_t); outs.append((0, 0))
    while i < len(toks):
        c = toks[i]; i += 1
        if c == "M":
            flush(); cur = (float(toks[i]), float(toks[i + 1])); i += 2; start = cur; add_vertex(cur)
        elif c == "L":
            cur = (float(toks[i]), float(toks[i + 1])); i += 2; add_vertex(cur)
        elif c == "H":
            cur = (float(toks[i]), cur[1]); i += 1; add_vertex(cur)
        elif c == "V":
            cur = (cur[0], float(toks[i])); i += 1; add_vertex(cur)
        elif c == "C":
            c1x, c1y, c2x, c2y, x, y = [float(t) for t in toks[i:i + 6]]; i += 6
            outs[-1] = (c1x - v[-1][0], c1y - v[-1][1])
            cur = (x, y); add_vertex(cur, (c2x - x, c2y - y))
        elif c == "A":
            rx, ry, rot, la, sw, x, y = [float(t) for t in toks[i:i + 7]]; i += 7
            for (C1, C2, P3) in arc_to_cubics(cur, rx, ry, rot, int(la), int(sw), (x, y)):
                outs[-1] = (C1[0] - v[-1][0], C1[1] - v[-1][1])
                add_vertex(P3, (C2[0] - P3[0], C2[1] - P3[1]))
            cur = (x, y)
        elif c in "Zz":
            if v and len(v) > 1 and math.dist(v[0], v[-1]) < 1e-6: ins[0] = ins[-1]; v.pop(); ins.pop(); outs.pop()
            flush(); cur = start
    flush()
    return shapes

# ------------------------------------------------------------ Lottie helpers
def kf(frames, ease=EASE):
    """frames: list of (t, value) with value scalar or list; same easing on every segment."""
    out = []
    for n, (t, val) in enumerate(frames):
        k = {"t": round(t, 3), "s": val if isinstance(val, list) else [val]}
        if n < len(frames) - 1: k.update(ease)
        out.append(k)
    return {"a": 1, "k": out}

def static(val): return {"a": 0, "k": val}
def fill(rgb, opacity=100): return {"ty": "fl", "c": static(rgb + [1]), "o": static(opacity), "r": 1, "nm": "fill"}
def radial(cx, cy, r, rgb, a0=0.6, a1=0.2):
    return {"ty": "gf", "t": 2, "s": static([cx, cy]), "e": static([cx + r, cy]), "o": static(100), "h": static(0), "a": static(0),
            "g": {"p": 3, "k": static([0] + rgb + [0.35] + rgb + [1] + rgb + [0, a0, 0.35, a1, 1, 0])}, "nm": "halo"}
def transform(p=(0, 0), s=(100, 100), o=100, a=(0, 0)):
    return {"ty": "tr", "p": static(list(p)) if not isinstance(p, dict) else p, "a": static(list(a)),
            "s": static(list(s)) if not isinstance(s, dict) else s, "r": static(0), "o": static(o) if not isinstance(o, dict) else o, "sk": static(0), "sa": static(0)}
def ellipse(cx, cy, r): return {"ty": "el", "p": static([cx, cy]), "s": static([2 * r, 2 * r]), "d": 1}
def rect(cx, cy, w, h): return {"ty": "rc", "p": static([cx, cy]), "s": static([w, h]), "r": static(0), "d": 1}
def group(name, items, tr): return {"ty": "gr", "nm": name, "it": items + [tr]}
def path_shape(sh): return {"ty": "sh", "ks": static(sh), "d": 1}
def layer(ind, name, shapes, ip, op, p=(0, 0), s=100, o=100, a=(0, 0)):
    return {"ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1, "ao": 0, "ip": ip, "op": op, "st": 0, "bm": 0,
            "ks": {"o": static(o) if not isinstance(o, dict) else o, "r": static(0), "p": static([p[0], p[1], 0]) if not isinstance(p, dict) else p,
                   "a": static([a[0], a[1], 0]), "s": static([s, s, 100])}, "shapes": shapes}
def sec(t): return t * FPS

# ------------------------------------------------------------ the wordmark geometry
def read_letters():
    src = open(os.path.join(HERE, "..", "_shared", "wordmark-letters-unioned.svg")).read()
    letters = {}
    for m in re.finditer(r'<path id="wordmark-([A-Z0-9]+)" d="([^"]+)"', src):
        letters[m.group(1)] = svg_path_to_lottie(m.group(2))
    return letters   # S, A, N, Z, E1, E2, D in source order — one unioned outline each

def read_geometry():
    return json.load(open(os.path.join(HERE, "..", "_shared", "logo-geometry.json")))

KAPPA = 0.5522847498
def circle_path(cx, cy, r):
    k = KAPPA * r
    return {"c": True, "v": [[cx, cy - r], [cx + r, cy], [cx, cy + r], [cx - r, cy]],
            "i": [[-k, 0], [0, -k], [k, 0], [0, k]], "o": [[k, 0], [0, k], [-k, 0], [0, -k]]}
def rect_path(x0, y0, x1, y1):
    return {"c": True, "v": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], "i": [[0, 0]] * 4, "o": [[0, 0]] * 4}
def ring_masks(cx, cy, r_out, r_in):
    """layer masks (layer space = logo units): everything, minus the Z's ring (r_in .. r_out) — the ring always shows the background."""
    m = lambda nm, mode, sh: {"inv": False, "mode": mode, "pt": static(sh), "o": static(100), "x": static(0), "nm": nm}
    return [m("all", "a", rect_path(-2000, -2000, 6000, 2600)), m("Z ring out", "s", circle_path(cx, cy, r_out)), m("Z point in", "a", circle_path(cx, cy, r_in))]

# ------------------------------------------------------------ 1. logo reveal
def build_reveal():
    W, H, OP = 1920, 1080, 120
    g = read_geometry(); VW, VH = g["viewBox"][2], g["viewBox"][3]
    scale = 720 / VW * 100                             # logo 720 px wide, as in logo-reveal/index.html
    lx, ly = (W - 720) / 2, H / 2 - VH / 2 * scale / 100  # top-left of the logo on the comp (logo centred)
    BY = g["beam_y"]                                   # the beam runs through the Z and D points
    letters = read_letters()
    T = g["reveal_timings_s"]
    windows = {k: T[f"{k}-start"] for k in letters}    # from the easing curve (see index.html / build_shared_logo.py)
    P = {k: (g["dots"][k]["cx"], g["dots"][k]["cy"]) for k in ("A", "Z", "D")}
    zr = (P["Z"][0], P["Z"][1], g["z_ring_inner_r"], 45.5)
    layers = []; ind = 1

    # the lamp (behind everything: last in the array = lowest)
    lamp = layer(ind, "lamp", [group("lamp", [ellipse(0, 0, 1), radial(0, 0, 1, GOLD, .5, .11)], transform(s=(1300 / 2 * 100, 900 / 2 * 100)))],
                 0, OP, p=(W / 2, H * .46), o=kf([(0, 0), (sec(.8), 100), (sec(2), 100), (sec(2.8), 70)]))
    # the beam hairline
    ind += 1
    beam = layer(ind, "beam", [group("beam", [rect(0, 0, W, 1), fill(WHITE, 10)], transform())], 0, OP, p=(W / 2, ly + BY * scale / 100),
                 o=kf([(0, 0), (sec(.6), 100), (sec(2), 100), (sec(2.8), 0)]))
    # letters: one layer, a group per letter with animated opacity
    ind += 1
    groups = []
    for name, shapes in letters.items():
        t0 = windows[name]
        groups.append(group("letter " + name, [path_shape(s) for s in shapes] + [fill(WHITE)], transform(o=kf([(sec(t0), 0), (sec(t0 + .4), 100)]))))
    word = layer(ind, "wordmark letters", groups, 0, OP, p=(lx, ly), s=scale)
    # the logo's three points and their pulses (D, Z, A), masked so the Z's ring stays open
    ind += 1
    pulse = lambda cx, cy, t: group("pulse", [ellipse(0, 0, 200), radial(0, 0, 200, GOLD, .6, .2)],
                                    transform(p=(cx, cy), s=kf([(sec(t), [100, 100]), (sec(t + .36), [150, 150]), (sec(t + .8), [110, 110])], EASE_IO),
                                              o=kf([(sec(t), 0), (sec(t + .36), 90), (sec(t + .8), 28)], EASE_IO)))
    settle = lambda nm, c, t: group(nm, [ellipse(0, 0, 45), fill(GOLD)], transform(p=c, s=kf([(sec(t), [160, 160]), (sec(t + .4), [100, 100])]), o=kf([(sec(t), 0), (sec(t + .4), 100)])))
    dots = layer(ind, "points", [
        pulse(*P["A"], 1.8), pulse(*P["Z"], 1.75), pulse(*P["D"], 1.7),
        settle("point A", P["A"], T["A-dot"]),
        settle("point Z", P["Z"], T["Z-dot"]),
        group("point D", [ellipse(0, 0, 45), fill(GOLD)], transform(p=P["D"], o=kf([(sec(1.5), 0), (sec(1.7), 100)]))),
    ], 0, OP, p=(lx, ly), s=scale)
    dots["hasMask"] = True; dots["masksProperties"] = ring_masks(*zr)
    # the travelling point: a static layer in logo units (so the ring mask stays put); the group travels x 0 -> D point
    ind += 1
    trav = layer(ind, "travelling point", [
        group("traveller", [
            group("halo", [ellipse(0, 0, 230), radial(0, 0, 230, GOLD, .6, .2)], transform(o=kf([(sec(.4), 0), (sec(.64), 95), (sec(1.6), 95), (sec(1.8), 0)]))),
            group("point", [ellipse(0, 0, 45), fill(GOLD)], transform(o=kf([(sec(.4), 0), (sec(.56), 100), (sec(1.6), 100), (sec(1.8), 0)]))),
        ], transform(p=kf([(sec(.5), [0, BY]), (sec(1.6), [P["D"][0], BY])]))),
    ], 0, OP, p=(lx, ly), s=scale)
    trav["hasMask"] = True; trav["masksProperties"] = ring_masks(*zr)
    return {"v": "5.7.4", "fr": FPS, "ip": 0, "op": OP, "w": W, "h": H, "nm": "Sanzeed — logo reveal", "ddd": 0, "assets": [],
            "layers": [trav, dots, word, beam, lamp]}

# ------------------------------------------------------------ 2. website loader
def build_loader():
    W, H, OP = 480, 48, 60
    y = H / 2
    beam = layer(2, "beam", [group("beam", [rect(0, 0, W, 1), fill(WHITE, 10)], transform())], 0, OP, p=(W / 2, y))
    point = layer(1, "point", [
        group("halo", [ellipse(0, 0, 22), radial(0, 0, 22, GOLD, .55, .18)], transform(o=kf([(0, 0), (sec(.2), 90), (sec(1.1), 90), (sec(1.4), 0), (sec(2), 0)], LINEAR))),
        group("point", [ellipse(0, 0, 5), fill(GOLD)], transform(o=kf([(0, 0), (sec(.2), 100), (sec(1.1), 100), (sec(1.4), 0), (sec(2), 0)], LINEAR))),
    ], 0, OP, p=kf([(0, [0, y, 0]), (sec(1.1), [W, y, 0]), (sec(2), [W, y, 0])]))
    return {"v": "5.7.4", "fr": FPS, "ip": 0, "op": OP, "w": W, "h": H, "nm": "Sanzeed — loader (point on beam)", "ddd": 0, "assets": [], "layers": [point, beam]}

PLAYER = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>%(title)s — Lottie player — Sanzeed</title>
<style>html,body{margin:0;height:100%%;background:%(bg)s;display:grid;place-items:center;font:14px/1.4 Inter,system-ui,sans-serif;color:#808086}
#anim{width:min(92vw, %(w)spx);aspect-ratio:%(w)s/%(h)s}p{position:fixed;left:16px;bottom:12px;margin:0}</style></head>
<body><div id="anim" role="img" aria-label="%(title)s"></div><p>%(title)s · %(w)s×%(h)s · %(fps)s fps · %(frames)s frames · lottie-web %(lv)s · the JSON is inlined below for a zero-setup preview; the editable file is %(file)s</p>
<script src="lottie.min.js"></script>
<script>var SZ_LOTTIE=%(json)s;
window.anim=lottie.loadAnimation({container:document.getElementById('anim'),renderer:'svg',loop:true,autoplay:!matchMedia('(prefers-reduced-motion: reduce)').matches,animationData:SZ_LOTTIE});
if(matchMedia('(prefers-reduced-motion: reduce)').matches){window.anim.goToAndStop(SZ_LOTTIE.op-1,true);}</script></body></html>"""

if __name__ == "__main__":
    lv = re.search(r"5\.\d+\.\d+", open(os.path.join(HERE, "lottie.min.js")).read(2000)) or ["5.12"]
    for name, data, bg in (("logo-reveal", build_reveal(), "#000"), ("loader", build_loader(), "#000")):
        fn = f"sanzeed-{name}.json"
        json.dump(data, open(os.path.join(HERE, fn), "w"), separators=(",", ":"))
        open(os.path.join(HERE, f"player--{name}.html"), "w").write(PLAYER % dict(
            title=data["nm"], bg=bg, w=data["w"], h=data["h"], fps=data["fr"], frames=data["op"], lv=lv[0], file=fn, json=json.dumps(data, separators=(",", ":"))))
        print("wrote", fn, os.path.getsize(os.path.join(HERE, fn)), "bytes,", len(data["layers"]), "layers")
