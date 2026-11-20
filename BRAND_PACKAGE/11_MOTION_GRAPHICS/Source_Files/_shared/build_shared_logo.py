#!/usr/bin/env python3
"""build_shared_logo.py — the logo geometry every motion source inlines, regenerated from 02_LOGO_SYSTEM.

Reads (never edits):
  02_LOGO_SYSTEM/Source_Files/sanzeed-primary-wordmark--full-colour-dark.svg   letters wordmark-S/A/N/Z/E1/E2/D + three points (A, Z, D)
  02_LOGO_SYSTEM/Source_Files/sanzeed-symbol--full-colour-dark.svg             the refined S + its point
Unions every letter outline with Inkscape (path-union: removes any construction seams / overlapping sub-paths), then writes
  _shared/wordmark-source.svg            the full primary wordmark, one unioned outline per letter, points with ids (dot-A, dot-Z, dot-D)
  _shared/wordmark-letters-unioned.svg   letters only (what the HTML sources and the Lottie builder read)
  _shared/symbol-source.svg              the symbol S. (unioned S + point)
  _shared/logo-geometry.json             viewBox, letter boxes, point centres, the Z ring radius, and the reveal timings derived from them
and rewrites the geometry between the markers in every animation source:
  <!-- @letters:S,A,N,Z,E1,E2,D -->  … <!-- @/letters -->       ->  <g id="L-X" class="L"><path id="wordmark-X" d="…"/></g> per letter
  <!-- @path:S:symbol-S -->           … <!-- @/path -->          ->  <path id="symbol-S" d="…"/>  (any letter, any id)
Run:  python3 Source_Files/_shared/build_shared_logo.py      (Inkscape 1.2 on PATH)
"""
import json, math, os, re, subprocess, tempfile, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, ".."))
LOGO = os.path.normpath(os.path.join(HERE, "..", "..", "..", "02_LOGO_SYSTEM", "Source_Files"))
WM_IN = os.path.join(LOGO, "sanzeed-primary-wordmark--full-colour-dark.svg")
SY_IN = os.path.join(LOGO, "sanzeed-symbol--full-colour-dark.svg")
LETTERS = ["S", "A", "N", "Z", "E1", "E2", "D"]
INK, GOLD = "#F5F5F7", "#E9B25A"

# ---------------------------------------------------------------- path helpers
def tokens(d):
    return re.findall(r"[MmLlHhVvCcSsQqZz]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", d)

def to_absolute(d):
    """-> list of sub-paths, each a list of ('M'|'L'|'C', pts…) in absolute coordinates; Z implied (all outlines are closed)."""
    t = tokens(d); i = 0; cmd = None; cur = (0.0, 0.0); start = cur; subs = []; sub = None; last_c2 = None
    def num():
        nonlocal i; v = float(t[i]); i += 1; return v
    while i < len(t):
        if re.match(r"[A-Za-z]", t[i]): cmd = t[i]; i += 1
        rel = cmd.islower(); C = cmd.upper(); ox, oy = cur if rel else (0.0, 0.0)
        if C == "Z":
            cur = start; last_c2 = None; continue
        if C == "M":
            cur = (ox + num(), oy + num()); start = cur; sub = [("M", cur)]; subs.append(sub); cmd = "l" if rel else "L"; last_c2 = None
        elif C == "L":
            cur = (ox + num(), oy + num()); sub.append(("L", cur)); last_c2 = None
        elif C == "H":
            cur = ((cur[0] if rel else 0) + num(), cur[1]); sub.append(("L", cur)); last_c2 = None
        elif C == "V":
            cur = (cur[0], (cur[1] if rel else 0) + num()); sub.append(("L", cur)); last_c2 = None
        elif C == "C":
            c1 = (ox + num(), oy + num()); c2 = (ox + num(), oy + num()); p = (ox + num(), oy + num())
            sub.append(("C", c1, c2, p)); cur = p; last_c2 = c2
        elif C == "S":
            c1 = (2 * cur[0] - last_c2[0], 2 * cur[1] - last_c2[1]) if last_c2 else cur
            c2 = (ox + num(), oy + num()); p = (ox + num(), oy + num()); sub.append(("C", c1, c2, p)); cur = p; last_c2 = c2
        elif C == "Q":
            q = (ox + num(), oy + num()); p = (ox + num(), oy + num())
            c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1])); c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
            sub.append(("C", c1, c2, p)); cur = p; last_c2 = None
        else:
            raise ValueError("unsupported path command " + cmd)
    return subs

def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip("."); return "0" if s in ("-0", "") else s

def to_d(subs):
    out = []
    for sub in subs:
        for seg in sub:
            out.append(seg[0] + " ".join(f"{fmt(p[0])} {fmt(p[1])}" for p in seg[1:]))
        out.append("Z")
    return "".join(out)

def bbox(subs):
    xs, ys = [], []
    for sub in subs:
        prev = None
        for seg in sub:
            if seg[0] == "C":
                p0, c1, c2, p3 = prev, seg[1], seg[2], seg[3]
                for k in range(17):
                    u = k / 16; a = (1 - u) ** 3; b = 3 * u * (1 - u) ** 2; c = 3 * u * u * (1 - u); e = u ** 3
                    xs.append(a * p0[0] + b * c1[0] + c * c2[0] + e * p3[0]); ys.append(a * p0[1] + b * c1[1] + c * c2[1] + e * p3[1])
            else:
                xs.append(seg[-1][0]); ys.append(seg[-1][1])
            prev = seg[-1]
    return [min(xs), min(ys), max(xs), max(ys)]

def min_dist(subs, c):
    best = 1e9
    for sub in subs:
        prev = None
        for seg in sub:
            pts = [seg[-1]]
            if seg[0] == "C":
                p0, c1, c2, p3 = prev, seg[1], seg[2], seg[3]
                pts = [((1-u)**3*p0[0]+3*u*(1-u)**2*c1[0]+3*u*u*(1-u)*c2[0]+u**3*p3[0], (1-u)**3*p0[1]+3*u*(1-u)**2*c1[1]+3*u*u*(1-u)*c2[1]+u**3*p3[1]) for u in [k/32 for k in range(33)]]
            for p in pts: best = min(best, math.dist(p, c))
            prev = seg[-1]
    return best

# ---------------------------------------------------------------- read + union
def union(svg_path, ids):
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "u.svg")
        acts = "".join(f"select-by-id:{i};path-union;select-clear;" for i in ids)
        subprocess.run(["inkscape", svg_path, f"--actions={acts}export-plain-svg;export-filename:{out};export-do"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        s = open(out).read()
    paths = {}
    for m in re.finditer(r"<path\b(.*?)/?>", s, re.S):
        a = m.group(1); i = re.search(r'\bid="([^"]+)"', a); d = re.search(r'\bd="([^"]+)"', a, re.S)
        if i and d and i.group(1) in ids: paths[i.group(1)] = to_absolute(d.group(1))
    missing = set(ids) - set(paths)
    if missing: raise SystemExit(f"union lost {missing}")
    return paths, s

def circles(svg_text):
    return [tuple(float(re.search(fr'\b{k}="([^"]+)"', c).group(1)) for k in ("cx", "cy", "r"))
            for c in re.findall(r"<circle\b[^>]*>", svg_text)]

def viewbox(svg_text):
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()]

# ---------------------------------------------------------------- easing (reveal windows)
def time_at_progress(p, x1=.22, y1=.8, x2=.2, y2=1):
    lo, hi = 0.0, 1.0
    for _ in range(80):
        m = (lo + hi) / 2; y = 3 * y1 * m * (1 - m) ** 2 + 3 * y2 * m * m * (1 - m) + m ** 3
        lo, hi = (m, hi) if y < p else (lo, m)
    return 3 * x1 * lo * (1 - lo) ** 2 + 3 * x2 * lo * lo * (1 - lo) + lo ** 3

def main():
    wm_txt = open(WM_IN).read(); sy_txt = open(SY_IN).read()
    wm, _ = union(WM_IN, [f"wordmark-{k}" for k in LETTERS])
    sy, _ = union(SY_IN, ["symbol-S"])
    wm_vb, sy_vb = viewbox(wm_txt), viewbox(sy_txt)
    boxes = {k: bbox(wm[f"wordmark-{k}"]) for k in LETTERS}
    # identify the three points by the letter whose box holds them
    dots = {}
    for (cx, cy, r) in circles(wm_txt):
        k = next(k for k in ("A", "Z", "D") if boxes[k][0] - 60 <= cx <= boxes[k][2] + 60)
        dots[k] = {"cx": cx, "cy": cy, "r": r}
    assert set(dots) == {"A", "Z", "D"}, dots
    ring = min_dist(wm["wordmark-Z"], (dots["Z"]["cx"], dots["Z"]["cy"]))     # inner radius of the open ring around the Z point
    sdot = circles(sy_txt)[0]

    # reveal windows: the travelling point runs x = 0 -> D point on --ease in 1.1 s from 0.5 s; a letter blooms when the light
    # (the point plus two radii of lead) reaches its left edge; a point settles when the light reaches its centre.
    T0, DUR, LEAD, X1 = .5, 1.1, 90.0, dots["D"]["cx"]
    win = lambda x: round(T0 + DUR * time_at_progress(max(0.0, min(1.0, x / X1))), 3)
    timings = {f"{k}-start": win(boxes[k][0] - LEAD) for k in LETTERS}
    timings.update({"A-dot": win(dots["A"]["cx"]), "Z-dot": win(dots["Z"]["cx"]), "arrive": T0 + DUR})

    geom = {"source": os.path.relpath(WM_IN, SRC), "viewBox": wm_vb, "letters": {k: [round(v, 2) for v in boxes[k]] for k in LETTERS},
            "dots": dots, "z_ring_inner_r": round(ring, 2), "beam_y": dots["D"]["cy"],
            "symbol": {"source": os.path.relpath(SY_IN, SRC), "viewBox": sy_vb, "S_box": [round(v, 2) for v in bbox(sy["symbol-S"])],
                       "dot": {"cx": sdot[0], "cy": sdot[1], "r": sdot[2]}},
            "reveal_timings_s": timings}
    json.dump(geom, open(os.path.join(HERE, "logo-geometry.json"), "w"), indent=1)

    vb = " ".join(fmt(v) for v in wm_vb); W, H = fmt(wm_vb[2]), fmt(wm_vb[3])
    note = ("the approved logo (20 Nov 2026): the refined original wordmark, option B — hooked S, swooping N, the Z with the N swoop and a third "
            "point of light inside an open ring, three gold points (A, Z, D). Letters unioned with Inkscape path-union by build_shared_logo.py.")
    letters_xml = "\n".join(f'<path id="wordmark-{k}" d="{to_d(wm["wordmark-" + k])}"/>' for k in LETTERS)
    dots_xml = "\n".join(f'<circle id="dot-{k}" cx="{fmt(dots[k]["cx"])}" cy="{fmt(dots[k]["cy"])}" r="{fmt(dots[k]["r"])}"/>' for k in ("A", "Z", "D"))
    open(os.path.join(HERE, "wordmark-source.svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{W}" height="{H}" role="img" aria-label="SANZEED">\n'
        f'<title>Sanzeed — primary wordmark (full-colour-dark), per-letter source for motion</title>\n<desc>From 02_LOGO_SYSTEM/Source_Files/sanzeed-primary-wordmark--full-colour-dark.svg: {note}</desc>\n'
        f'<g id="wordmark-ink" fill="{INK}">\n{letters_xml}\n</g>\n<g id="wordmark-dots" fill="{GOLD}">\n{dots_xml}\n</g>\n</svg>\n')
    open(os.path.join(HERE, "wordmark-letters-unioned.svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{W}" height="{H}">\n'
        f'<!-- primary wordmark letters, one unioned outline per letter — {note} The points: see wordmark-source.svg / logo-geometry.json -->\n'
        f'<g id="wordmark-ink" fill="{INK}">\n{letters_xml}\n</g>\n</svg>\n')
    svb = " ".join(fmt(v) for v in sy_vb)
    open(os.path.join(HERE, "symbol-source.svg"), "w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{svb}" width="{fmt(sy_vb[2])}" height="{fmt(sy_vb[3])}" role="img" aria-label="S.">\n'
        f'<title>Sanzeed — symbol S. (full-colour-dark), source for motion</title>\n<desc>From 02_LOGO_SYSTEM/Source_Files/sanzeed-symbol--full-colour-dark.svg: the refined, hooked S of the wordmark and its full stop. S unioned with Inkscape path-union by build_shared_logo.py.</desc>\n'
        f'<g id="symbol-ink" fill="{INK}"><path id="symbol-S" d="{to_d(sy["symbol-S"])}"/></g>\n'
        f'<g id="symbol-dots" fill="{GOLD}"><circle id="dot-S" cx="{fmt(sdot[0])}" cy="{fmt(sdot[1])}" r="{fmt(sdot[2])}"/></g>\n</svg>\n')

    # ---- inject into the HTML sources
    D = {k: to_d(wm["wordmark-" + k]) for k in LETTERS}
    def rep_letters(m):
        ind = m.group(1); keys = m.group(2).split(",")
        body = "".join(f'\n{ind}<g id="L-{k}" class="L"><path id="wordmark-{k}" d="{D[k]}"/></g>' for k in keys)
        return f"{ind}<!-- @letters:{m.group(2)} -->{body}\n{ind}<!-- @/letters -->"
    def rep_path(m):
        k, pid = m.group(1), m.group(2)
        return f'<!-- @path:{k}:{pid} --><path id="{pid}" d="{D[k]}"/><!-- @/path -->'
    changed = []
    for f in sorted(glob.glob(os.path.join(SRC, "*", "*.html"))):
        s = open(f).read()
        n = re.sub(r"([ \t]*)<!-- @letters:([A-Z0-9,]+) -->.*?<!-- @/letters -->", rep_letters, s, flags=re.S)
        n = re.sub(r"<!-- @path:([A-Z0-9]+):([\w-]+) -->.*?<!-- @/path -->", rep_path, n, flags=re.S)
        if n != s: open(f, "w").write(n); changed.append(os.path.relpath(f, SRC))
    print("viewBox", vb, "| points", {k: (dots[k]["cx"], dots[k]["cy"]) for k in dots}, "| Z ring inner r", round(ring, 2))
    print("reveal timings", timings)
    print("injected into", changed)

if __name__ == "__main__":
    main()
