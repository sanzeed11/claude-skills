#!/usr/bin/env python3
"""build_campaign.py — writes the HTML sources in Campaign_Templates/src and renders PNG (2x) + JPG exports.
Re-run after editing this file; or edit any HTML in src/ directly and re-run render.js on it (see README)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C

OUT = f"{MC}/Campaign_Templates"; SRC = f"{OUT}/src"
os.makedirs(SRC, exist_ok=True)

EYEBROW = "Sanzeed Mirza · Experiential Design Consultant"

KV = {
 "carry-the-light": dict(
    head="Carry the light across", sub=C.BETWEEN_SUB, img=shared_img("hero-object--dark-2400.jpg"), img45=shared_img("hero-object--dark-4x5-1600.jpg"),
    label=("Between two points of light", "sanzeed.com"), alt="The point of light: a black glass sphere with a gold ring on a dark plinth"),
 "walk-into": dict(
    head="Experiential design you can walk into", sub="Museums, experience centres, pavilions, memorials and shows — one vision from the brief to opening night.",
    img=jimg("case/prime-minister-museum-03"), img45=jimg("case/prime-minister-museum-03"),   # tone-restored copy (common.TONE_FIX), not the raw webp
    label=("Prime Minister Museum", "New Delhi"), alt="The tricolour corridor of the Prime Minister Museum, New Delhi"),
 "tell-me": dict(
    head="Tell me about the room", sub="A few lines are enough. I reply within two working days. The first conversation is always free.",
    img=shared_img("portrait--4x5-2000.jpg"), img45=shared_img("portrait--4x5-2000.jpg"), portrait=True,
    label=("Sanzeed Mirza", "New Delhi"), alt="Portrait of Sanzeed Mirza", contact=True),
}

KV_CSS = """
.kv { font-family: var(--font-text); }
.kv header { position: absolute; z-index: 2; }
.kv header img { display: block; }
.kv .copy .eyebrow-quiet { font-size: 14px; margin-bottom: 28px; }
.kv .copy .hl { color: var(--fg); }
.kv .copy .sub { font-size: 22px; line-height: 1.5; color: var(--fg-2); margin-top: 28px; max-width: 30em; }
.kv .copy .contact { margin-top: 36px; font-size: 17px; line-height: 1.7; color: var(--fg-2); }
.kv .copy .contact b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.kv figure { position: absolute; margin: 0; }
.kv figure .plate { width: 100%; height: 100%; }
.kv figcaption { margin-top: 18px; font-size: 15px; }
.kv footer { position: absolute; display: flex; justify-content: space-between; font-size: 14px; color: var(--fg-3); letter-spacing: .02em; }
/* 16:9 */
.r169 { width: 1920px; height: 1080px; }
.r169 header { left: 96px; top: 84px; } .r169 header img { width: 230px; }
.r169 .copy { position: absolute; left: 96px; top: 290px; width: 820px; }
.r169 .copy .hl { font-size: 104px; }
.r169 figure { left: 1016px; top: 285px; width: 808px; height: 454px; }
.r169.portrait figure { left: 1216px; top: 160px; width: 608px; height: 760px; }
.r169.portrait .copy { width: 980px; top: 250px; }
.r169 footer { left: 96px; right: 96px; bottom: 84px; }
/* 1:1 */
.r11 { width: 1080px; height: 1080px; }
.r11 header { left: 72px; top: 66px; } .r11 header img { width: 190px; }
.r11 figure { left: 72px; top: 150px; width: 936px; height: 526px; }
.r11 figure figcaption { font-size: 14px; }
.r11 .copy { position: absolute; left: 72px; top: 760px; width: 936px; }
.r11 .copy .eyebrow-quiet { display: none; }
.r11 .copy .hl { font-size: 72px; }
.r11 .copy .sub { font-size: 20px; margin-top: 20px; max-width: 40em; }
.r11.portrait figure { left: 456px; top: 150px; width: 552px; height: 690px; }
.r11.portrait .copy { left: 72px; top: 160px; width: 350px; }
.r11.portrait .copy .hl { font-size: 58px; }
.r11.portrait .copy .sub { font-size: 18px; }
.r11.portrait .copy .contact { font-size: 15px; margin-top: 28px; }
.r11 footer { left: 72px; right: 72px; bottom: 66px; }
/* 9:16  — keep text inside the centre-safe 1080x1420 band (y 250–1670) */
.r916 { width: 1080px; height: 1920px; }
.r916 header { left: 72px; top: 290px; } .r916 header img { width: 200px; }
.r916 figure { left: 164px; top: 390px; width: 752px; height: 940px; }
.r916 .copy { position: absolute; left: 72px; top: 1400px; width: 936px; }
.r916 .copy .eyebrow-quiet { display: none; }
.r916 .copy .hl { font-size: 76px; }
.r916 .copy .sub { font-size: 21px; margin-top: 20px; max-width: 36em; }
.r916.portrait figure { left: 220px; top: 400px; width: 640px; height: 800px; }
.r916.portrait .copy { top: 1270px; }
.r916.portrait .copy .hl { font-size: 72px; }
.r916.portrait .copy .contact { font-size: 17px; margin-top: 22px; }
.r916 footer { left: 72px; right: 72px; bottom: 150px; }
"""

def kv_html(key, ratio):
    d = KV[key]; cls = {"16x9": "r169", "1x1": "r11", "9x16": "r916"}[ratio]
    portrait = d.get("portrait", False)
    src = d["img45"] if (portrait or ratio == "9x16") else d["img"]
    contact = ""
    if d.get("contact"):
        contact = f'<p class="contact"><b>{C.EMAIL}</b><br>WhatsApp · {C.PHONE}<br>{C.SITE}</p>'
    body = f"""<body>
<div class="page grain kv {cls}{' portrait' if portrait else ''}">
  <header><img src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed"></header>
  <div class="copy">
    <div class="eyebrow-quiet">{esc(EYEBROW)}</div>
    <h1 class="hl">{esc(d['head'])}<span class="pt">.</span></h1>
    <p class="sub">{esc(d['sub'])}</p>
    {contact}
  </div>
  <figure>
    <div class="plate"><img src="{src}" alt="{esc(d['alt'])}"></div>
    <figcaption class="wl"><b>{esc(d['label'][0])}</b><span class="sep">·</span>{esc(d['label'][1])}</figcaption>
  </figure>
  <footer><span>{C.SITE}</span><span>New Delhi</span></footer>
</div>
</body>
</html>
"""
    return head(f"Sanzeed — key visual — {d['head']}. ({ratio})", "dark", KV_CSS) + body

# ---------------- Digital ads (IAB) ----------------
AD_CSS = """
.ad { position: relative; overflow: hidden; background: var(--bg); color: var(--fg); font-family: var(--font-text); }
.ad .logo { position: absolute; display: block; }
.ad .hl { color: var(--fg); }
.ad .sub { color: var(--fg-2); line-height: 1.4; }
.ad .plate { position: absolute; }
.ad .cta { position: absolute; }
.ad .url { position: absolute; color: var(--fg-3); font-size: 11px; letter-spacing: .02em; }
.ad .arrow { display: inline-block; }
"""
ADS = {
 "300x250": dict(w=300, h=250, logo=("simplified-small-size", 112), css="""
   .logo { left: 18px; top: 18px; }
   .plate { left: 18px; top: 48px; width: 264px; height: 86px; border-radius: 12px; }
   .hl { position: absolute; left: 18px; top: 144px; width: 270px; font-size: 22px; line-height: 1.05; }
   .cta { left: 18px; bottom: 16px; padding: 8px 13px; font-size: 12px; }
   .url { right: 18px; bottom: 23px; }""",
   head="Experiential design you can walk into", image=True),
 "728x90": dict(w=728, h=90, logo=("simplified-small-size", 112), css="""
   .logo { left: 22px; top: 37px; }
   .hl { position: absolute; left: 160px; top: 0; height: 90px; display: flex; align-items: center; font-size: 26px; white-space: nowrap; }
   .cta { right: 22px; top: 27px; padding: 10px 16px; font-size: 13px; }
   .url { display: none; }""",
   head="Experiential design you can walk into"),
 "160x600": dict(w=160, h=600, logo=("simplified-small-size", 112), css="""
   .logo { left: 24px; top: 24px; }
   .plate { left: 16px; top: 62px; width: 128px; height: 160px; border-radius: 12px; }
   .hl { position: absolute; left: 16px; top: 244px; width: 128px; font-size: 24px; line-height: 1.08; }
   .sub { position: absolute; left: 16px; top: 396px; width: 128px; font-size: 12px; }
   .cta { left: 16px; bottom: 44px; padding: 9px 13px; font-size: 12px; white-space: nowrap; }
   .url { left: 16px; bottom: 20px; }""",
   head="Experiential design you can walk into", sub="Museums, pavilions and shows.", image=True, img45=True, cta="Get in touch →"),
 "320x50": dict(w=320, h=50, logo=("simplified-small-size", 96), css="""
   .logo { left: 12px; top: 18px; }
   .hl { position: absolute; left: 122px; top: 0; height: 50px; display: flex; align-items: center; font-size: 16px; white-space: nowrap; }
   .cta { right: 12px; top: 13px; width: 24px; height: 24px; padding: 0; justify-content: center; font-size: 14px; }
   .url { display: none; }""",
   head="Vision you can walk into", cta="→"),
 "970x250": dict(w=970, h=250, logo=("primary-wordmark", 150), css="""
   .logo { left: 40px; top: 40px; }
   .hl { position: absolute; left: 40px; top: 88px; width: 520px; font-size: 36px; line-height: 1.04; }
   .sub { position: absolute; left: 40px; top: 160px; width: 520px; font-size: 14px; display: none; }
   .cta { left: 40px; bottom: 34px; padding: 10px 16px; font-size: 13px; }
   .url { left: 250px; bottom: 45px; }
   .plate { right: 40px; top: 30px; width: 338px; height: 190px; border-radius: 20px; }""",
   head="Experiential design you can walk into", image=True),
 "300x600": dict(w=300, h=600, logo=("primary-wordmark", 130), css="""
   .logo { left: 24px; top: 28px; }
   .plate { left: 24px; top: 72px; width: 252px; height: 200px; border-radius: 20px; }
   .wl { position: absolute; left: 24px; top: 284px; font-size: 11px; }
   .hl { position: absolute; left: 24px; top: 322px; width: 252px; font-size: 34px; line-height: 1.05; }
   .sub { position: absolute; left: 24px; top: 440px; width: 252px; font-size: 13px; }
   .cta { left: 24px; bottom: 28px; padding: 10px 16px; font-size: 13px; }
   .url { display: none; }""",
   head="Experiential design you can walk into", sub="Museums, pavilions and shows — one vision from the brief to opening night.", image=True, label=True),
 "1080x1080": dict(w=1080, h=1080, logo=("primary-wordmark", 190), css="""
   .logo { left: 72px; top: 66px; }
   .plate { left: 72px; top: 150px; width: 936px; height: 526px; }
   .wl { position: absolute; left: 72px; top: 696px; font-size: 14px; }
   .hl { position: absolute; left: 72px; top: 760px; width: 936px; font-size: 72px; line-height: 1.02; }
   .sub { position: absolute; left: 72px; top: 930px; width: 600px; font-size: 20px; display: none; }
   .cta { left: 72px; bottom: 66px; padding: 14px 22px; font-size: 15px; }
   .url { right: 72px; bottom: 78px; font-size: 14px; }""",
   head="Experiential design you can walk into", image=True, label=True),
}

def ad_html(size):
    a = ADS[size]; lv, lw = a["logo"]
    src = shared_img("hero-object--dark-4x5-1600.jpg") if a.get("img45") else shared_img("hero-object--dark-2400.jpg")
    parts = [f'<img class="logo" src="{logo(lv, "full-colour-dark")}" alt="Sanzeed" style="width:{lw}px">']
    if a.get("image"): parts.append(f'<div class="plate"><img src="{src}" alt="The point of light: a black glass sphere with a gold ring on a dark plinth"></div>')
    if a.get("label"): parts.append('<div class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</div>')
    parts.append(f'<div class="hl">{esc(a["head"])}<span class="pt">.</span></div>')
    if a.get("sub"): parts.append(f'<div class="sub">{esc(a["sub"])}</div>')
    cta = a.get("cta", "Tell me about the room →")
    parts.append(f'<a class="cta" href="https://sanzeed.com">{cta}</a>')
    parts.append('<span class="url">sanzeed.com</span>')
    css = AD_CSS + f".ad {{ width:{a['w']}px; height:{a['h']}px; }}\n" + a["css"]
    return head(f"Sanzeed — digital ad {size}", "dark", css) + f'<body><div class="ad">\n  ' + "\n  ".join(parts) + "\n</div></body>\n</html>\n"

# ---------------- Promotional web banners ----------------
BANNER_CSS = """
.bn { position: relative; overflow: hidden; background: var(--bg); color: var(--fg); font-family: var(--font-text); }
.bn .logo { position: absolute; display: block; }
.bn .copy { position: absolute; }
.bn .copy .eyebrow-quiet { font-size: 13px; margin-bottom: 20px; }
.bn .copy .hl { color: var(--fg); }
.bn .copy .sub { color: var(--fg-2); line-height: 1.5; margin-top: 20px; }
.bn .copy .cta { margin-top: 28px; }
.bn figure { position: absolute; margin: 0; }
.bn figure .plate { width: 100%; height: 100%; }
.bn figcaption { margin-top: 14px; font-size: 13px; }
.bn .url { position: absolute; color: var(--fg-3); font-size: 13px; }
"""
BANNERS = {
 "1920x600": dict(w=1920, h=600, css="""
   .logo { left: 96px; top: 72px; width: 200px; }
   .copy { left: 96px; top: 190px; width: 820px; }
   .copy .hl { font-size: 76px; }
   .copy .sub { font-size: 19px; max-width: 32em; }
   figure { left: 1120px; top: 72px; width: 704px; height: 396px; }
   .url { right: 96px; bottom: 60px; }"""),
 "1440x500": dict(w=1440, h=500, css="""
   .logo { left: 72px; top: 60px; width: 180px; }
   .copy { left: 72px; top: 160px; width: 640px; }
   .copy .hl { font-size: 60px; }
   .copy .sub { font-size: 17px; max-width: 30em; }
   figure { left: 820px; top: 60px; width: 548px; height: 308px; }
   .url { right: 72px; bottom: 52px; }"""),
}
def banner_html(size, theme):
    b = BANNERS[size]
    if theme == "dark": src, lg = shared_img("hero-object--dark-2400.jpg"), logo("primary-wordmark", "full-colour-dark")
    else: src, lg = shared_img("hero-object--light-2400.jpg"), logo("primary-wordmark", "full-colour-light")
    css = BANNER_CSS + f".bn {{ width:{b['w']}px; height:{b['h']}px; }}\n" + b["css"]
    grain = " grain" if theme == "dark" else ""
    body = f"""<body><div class="bn{grain}">
  <img class="logo" src="{lg}" alt="Sanzeed">
  <div class="copy">
    <div class="eyebrow-quiet">{esc(EYEBROW)}</div>
    <h1 class="hl">{esc(C.MASTER_LINE[:-1])}<span class="pt">.</span></h1>
    <p class="sub">Museums, experience centres, pavilions, memorials and shows — one vision from the brief to opening night.</p>
    <a class="cta" href="https://sanzeed.com">Tell me about the room →</a>
  </div>
  <figure>
    <div class="plate"><img src="{src}" alt="The point of light: a glass sphere with a gold ring on a plinth"></div>
    <figcaption class="wl"><b>Between two points of light</b><span class="sep">·</span>sanzeed.com</figcaption>
  </figure>
  <span class="url">{C.SITE}</span>
</div></body>
</html>
"""
    return head(f"Sanzeed — web banner {size} ({theme})", theme, css) + body

if __name__ == "__main__":
    jobs = []; post = []
    for key in KV:
        for ratio, (w, h) in {"16x9": (1920, 1080), "1x1": (1080, 1080), "9x16": (1080, 1920)}.items():
            stem = f"sanzeed-key-visual--{key}-{ratio}"
            hp = write(f"{SRC}/{stem}.html", kv_html(key, ratio))
            out = f"{OUT}/{stem}-{w*2}x{h*2}.png"
            jobs.append(png(hp, out, w, h, 2)); post.append((out, f"{OUT}/{stem}-{w}x{h}.jpg", w))
    for size in ADS:
        a = ADS[size]; stem = f"sanzeed-ad--{size}"
        hp = write(f"{SRC}/{stem}.html", ad_html(size))
        out = f"{OUT}/{stem}@2x.png"; jobs.append(png(hp, out, a["w"], a["h"], 2)); post.append((out, f"{OUT}/{stem}.jpg", a["w"]))
    for size in BANNERS:
        for theme in ("dark", "light"):
            b = BANNERS[size]; stem = f"sanzeed-web-banner--{theme}-{size}"
            hp = write(f"{SRC}/{stem}.html", banner_html(size, theme))
            out = f"{OUT}/{stem}@2x.png"; jobs.append(png(hp, out, b["w"], b["h"], 2)); post.append((out, f"{OUT}/{stem}.jpg", b["w"]))
    render_jobs(jobs)
    for p, j, w in post: to_jpg(p, j, 88, width=w, bg=(0,0,0) if "light" not in j else (245,240,231))
    print("campaign done", folder_size_mb(OUT), "MB")
