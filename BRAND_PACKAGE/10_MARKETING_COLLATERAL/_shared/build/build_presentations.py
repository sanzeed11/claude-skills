#!/usr/bin/env python3
"""build_presentations.py — Presentations/: sales presentation (PPTX, 16 slides) + PDF + PNG per slide;
marketing proposal template (PPTX, 12 slides) + PDF + PNG; case-study template (A4 PDF from HTML: filled + blank);
portfolio template (A4 landscape PDF, cover + 10 projects + contact)."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
import brandcopy as C
from docstyle import A4_CSS, page
from pptx_kit import *
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

OUT = f"{MC}/Presentations"; SRC = f"{OUT}/src"; ASSETS = f"{SRC}/assets"; os.makedirs(ASSETS, exist_ok=True)
LOGO_DARK = f"{B}/02_LOGO_SYSTEM/PNG/sanzeed-primary-wordmark--full-colour-dark-1200w.png"
LOCK_DARK = f"{B}/02_LOGO_SYSTEM/PNG/sanzeed-horizontal-descriptor--full-colour-dark-1200w.png"
LOGO_LIGHT = f"{B}/02_LOGO_SYSTEM/PNG/sanzeed-primary-wordmark--full-colour-light-1200w.png"

def asset(name):
    """JPEG copy of a project image for PPTX (1600 px wide, q84) in src/assets."""
    stem = name.replace("/", "--").removesuffix(".jpg"); out = f"{ASSETS}/{stem}.jpg"
    if not os.path.exists(out):
        src = f"{IMG}/{name}.webp" if not name.startswith("_") else f"{MC}/_shared/img/{name[1:]}"
        im = Image.open(src).convert("RGB")
        if im.width > 1400: im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(out, quality=82, subsampling=0, optimize=True)
    return out

def stats_row(d, s, y):
    for i, (n, l) in enumerate(C.PROOF):
        x = M + i * 3.0
        d.text(s, x, y, 2.8, 1.0, [[(n, dict(font=DISPLAY, size=60, color=d.fg)), ("+", dict(font=DISPLAY, size=60, color=d.accent))]], line=1.0)
        d.text(s, x, y + 1.05, 2.8, 0.4, [[(l, dict(font=TEXT, size=12, color=d.fg2))]])

def sales_deck():
    d = Deck(); path = f"{OUT}/sanzeed-sales-presentation--16-slides.pptx"
    # 1 cover
    s = d.slide("Cover. Read the master line, pause, then the name."); d.logo(s, LOGO_DARK, M, M, 2.6)
    d.picture(s, asset("_hero-object--dark-2400.jpg"), 7.0, 1.3, 5.63, 3.17)
    d.wall_label(s, 7.0, 4.58, 5.6, "Between two points of light", "sanzeed.com")
    d.eyebrow(s, M, 3.0, 6, "Sanzeed Mirza · Experiential Design Consultant", quiet=True)
    d.headline(s, M, 3.35, 6.2, 2.2, C.MASTER_LINE, 54)
    d.footer(s, C.SITE, "New Delhi · 2026")
    # 2 the one idea
    s = d.slide(); d.eyebrow(s, M, M, 6, "The one idea"); d.headline(s, M, 1.1, 7, 1.4, C.BETWEEN, 48)
    d.text(s, M, 2.6, 6.2, 1.2, C.BETWEEN_SUB, size=18, color=d.fg2, line=1.4)
    d.text(s, M, 4.0, 6.2, 2.4, [C.STORY[3], " ", "The point of light, the beam it travels and the room it lights: that is the whole identity, and the whole job."], size=14, color=d.fg2, line=1.5)
    d.picture(s, asset("_hero-object--dark-4x5-1600.jpg"), 8.4, M, 4.23, 5.3); d.wall_label(s, 8.4, 6.15, 4.2, "Between two points of light", "sanzeed.com")
    d.footer(s, "02", "The one idea")
    # 3 about
    s = d.slide(); d.eyebrow(s, M, M, 6, "About"); d.headline(s, M, 1.1, 7.4, 1.5, C.PERSONAL_LINE, 40)
    d.text(s, M, 2.9, 7.0, 3.5, [C.ABOUT_1, "", C.ABOUT_2], size=15, color=d.fg2, line=1.45)
    d.picture(s, asset("_portrait--4x5-2000.jpg"), 8.8, M, 3.83, 4.8); d.wall_label(s, 8.8, 5.65, 3.8, "Sanzeed Mirza", "New Delhi")
    d.footer(s, "03", "About")
    # 4 proof
    s = d.slide(); d.eyebrow(s, M, M, 6, "Proof"); d.headline(s, M, 1.1, 9, 1.4, C.PROOF_LINE, 48)
    stats_row(d, s, 3.0); d.rule(s, M, 5.0, W - 2 * M, point=True)
    d.text(s, M, 5.3, 10, 0.5, C.TRUST, size=15, color=d.fg2); d.footer(s, "04", "Proof")
    # 5 pillars
    s = d.slide(); d.eyebrow(s, M, M, 6, "Three pillars"); d.headline(s, M, 1.1, 9, 1.3, "Strategic vision, immersive craft, calm leadership", 40)
    for i, (r, t, desc) in enumerate(C.PILLARS):
        x = M + i * 4.0; d.text(s, x, 3.1, 3.6, 0.6, [[(r, dict(font=DISPLAY, size=30, color=d.accent))]]); d.rule(s, x, 3.85, 3.6)
        d.text(s, x, 4.0, 3.6, 0.5, [[(t, dict(font=HEAD, size=18, color=d.fg))]]); d.text(s, x, 4.5, 3.6, 1.6, desc, size=14, color=d.fg2, line=1.45)
    d.footer(s, "05", "Three pillars")
    # 6 services
    s = d.slide(); d.eyebrow(s, M, M, 6, "Seven services"); d.headline(s, M, 1.1, 9, 1.2, C.BETWEEN, 40)
    for i, (n, t, l, a, _) in enumerate(C.SERVICES):
        col = i % 2; row = i // 2; x = M + col * 6.0; y = 2.55 + row * 1.08
        d.text(s, x, y, 0.5, 0.4, [[(n, dict(font=HEAD, size=11, color=d.accent_text))]]); d.text(s, x + 0.5, y - 0.02, 5.3, 0.4, [[(t, dict(font=HEAD, size=14, color=d.fg))]])
        d.text(s, x + 0.5, y + 0.33, 5.3, 0.7, [[(l + "  ", dict(font=TEXT, size=11, color=d.fg2)), ("As in " + a, dict(font=TEXT, size=10, color=d.fg3))]], line=1.3)
    d.text(s, M + 6.0, 2.55 + 3 * 1.08, 5.6, 0.9, [[("All seven, every time. ", dict(font=DISPLAY, size=16, color=d.fg)), (C.ALL_SEVEN_SUB, dict(font=TEXT, size=11, color=d.fg2))]], line=1.35)
    d.footer(s, "06", "Seven services")
    # 7 now showing
    s = d.slide(); d.eyebrow(s, M, M, 6, "Now showing"); d.headline(s, M, 1.05, 9, 1.0, "Eight rooms, lit", 40)
    for i, (im, t, p, cat) in enumerate(C.FEATURED):
        col = i % 4; row = i // 4; x = M + col * 3.05; y = 2.3 + row * 2.25
        d.picture(s, asset(im), x, y, 2.9, 1.63); d.wall_label(s, x, y + 1.7, 2.9, t, p)
    d.footer(s, "07", "Now showing")
    # 8 method
    s = d.slide(); d.eyebrow(s, M, M, 6, "Method"); d.headline(s, M, 1.05, 9, 1.0, C.METHOD_LINE, 40)
    d.text(s, M, 2.1, 9, 0.6, C.METHOD_SUB, size=13, color=d.fg2, line=1.4)
    d.rule(s, M, 3.1, W - 2 * M)
    for i, (n, t, desc, rec) in enumerate(C.METHOD):
        x = M + i * 3.0; d.dot(s, x - 0.05, 3.05); d.text(s, x, 3.3, 2.7, 0.3, [[("Step " + n, dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]])
        d.text(s, x, 3.6, 2.7, 0.7, [[(t, dict(font=DISPLAY, size=30, color=d.fg))]]); d.text(s, x, 4.3, 2.7, 1.5, desc, size=11.5, color=d.fg2, line=1.4)
        d.text(s, x, 5.85, 2.7, 0.8, [[("You receive ", dict(font=TEXT, size=11, color=d.fg3)), (rec, dict(font=HEAD, size=11, color=d.fg))]], line=1.35)
    d.footer(s, "08", "Method")
    # 9-12 cases
    def case_slide(key, n, pno, hero, grid):
        c = C.CASES[key]; s = d.slide()
        d.eyebrow(s, M, M, 8, f"Case study · {n:03d} · {c['type']}"); d.headline(s, M, 1.05, 6.2, 1.0, c["title"], 40)
        d.text(s, M, 1.95, 6, 0.4, c["place"], size=14, color=d.fg2)
        d.text(s, M, 2.55, 5.6, 0.3, [[("The brief", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]]); d.text(s, M, 2.85, 5.6, 1.5, c["brief"], size=12, color=d.fg2, line=1.4)
        d.text(s, M, 4.45, 5.6, 0.3, [[("The idea", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]]); d.text(s, M, 4.75, 5.6, 0.6, [[(c["idea"], dict(font=DISPLAY, size=22, color=d.fg))]])
        d.text(s, M, 5.35, 5.6, 1.4, c["idea_text"], size=11.5, color=d.fg2, line=1.4)
        d.picture(s, asset(f"case/{key}-{hero:02d}"), 6.9, M, 5.73, 3.22); d.wall_label(s, 6.9, 3.97, 5.7, c["title"], c["place"])
        for i, g in enumerate(grid): d.picture(s, asset(f"case/{key}-{g:02d}"), 6.9 + i * 1.95, 4.5, 1.83, 1.03)
        d.text(s, 6.9, 5.65, 5.7, 1.0, [[("What visitors do  ", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))], [(c["visitors"], dict(font=DISPLAY, size=16, color=d.fg))]], line=1.3)
        d.footer(s, f"{pno:02d}", f"{c['title']} · {c['place']}")
    case_slide("prime-minister-museum", 1, 9, 3, [1, 4, 7])
    s = d.slide(); c = C.CASES["prime-minister-museum"]; d.eyebrow(s, M, M, 8, "Case study · 001 · the walk")
    d.headline(s, M, 1.05, 8, 1.0, "A corridor you walk in order", 40)
    for i, g in enumerate([2, 5, 6]): d.picture(s, asset(f"case/prime-minister-museum-{g:02d}"), M + i * 4.0, 2.2, 3.85, 2.17); d.text(s, M + i * 4.0, 4.45, 3.85, 0.5, [[(f"{g:03d}  ", dict(font=HEAD, size=10, color=d.accent_text)), (c["captions"][g-1], dict(font=TEXT, size=10, color=d.fg3))]])
    d.text(s, M, 5.2, 7.5, 0.3, [[("The walk", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]]); d.text(s, M, 5.5, 7.5, 1.3, c["walk"], size=12.5, color=d.fg2, line=1.4)
    d.text(s, 8.6, 5.2, 4, 0.3, [[("Role", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]]); d.text(s, 8.6, 5.5, 4, 1.0, [c["role"], c["type"], c["place"]], size=12.5, color=d.fg2, line=1.4)
    d.footer(s, "10", "Prime Minister Museum · New Delhi")
    case_slide("ram-katha-show", 2, 11, 7, [1, 2, 3]); case_slide("buddha-park", 3, 12, 8, [2, 5, 6])
    # 13 journey
    s = d.slide(); d.eyebrow(s, M, M, 6, "Journey"); d.headline(s, M, 1.05, 9, 1.0, "Fifteen years, one through-line", 40)
    d.rule(s, M, 2.6, W - 2 * M, point=True)
    for i, (dte, role, org, desc) in enumerate(C.TIMELINE):
        x = M + i * 2.0; d.dot(s, x - 0.05, 2.55, 0.1); d.text(s, x, 2.8, 1.9, 0.5, [[(dte, dict(font=HEAD, size=9, color=d.accent_text))]], line=1.2)
        d.text(s, x, 3.3, 1.85, 0.8, [[(role, dict(font=HEAD, size=12, color=d.fg))], [(org, dict(font=TEXT, size=11, color=d.fg2))]], line=1.25)
        d.text(s, x, 4.2, 1.85, 2.2, desc, size=9.5, color=d.fg3, line=1.35)
    d.footer(s, "13", "Journey")
    # 14 how a project starts
    s = d.slide(); d.eyebrow(s, M, M, 6, "How a project starts"); d.headline(s, M, 1.05, 9, 1.0, "Tell me about the room", 40)
    d.text(s, M, 2.1, 7, 0.6, C.CALL_SUB + " " + C.PROMISES[0], size=14, color=d.fg2, line=1.4)
    cols = [("Type of project", C.PROJECT_TYPES), ("Timeline", ["Not fixed yet"] + C.TIMELINES), ("Budget band", ["Not fixed yet"] + C.BUDGET_BANDS)]
    for i, (t, items) in enumerate(cols):
        x = M + i * 4.0; d.text(s, x, 3.2, 3.6, 0.3, [[(t, dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]]); d.rule(s, x, 3.55, 3.6)
        d.text(s, x, 3.7, 3.6, 2.5, [[(it, dict(font=TEXT, size=13, color=d.fg2))] for it in items], line=1.6)
    d.text(s, M, 6.1, 11, 0.5, [[("Then: ", dict(font=HEAD, size=12, color=d.fg)), ("Step 01 Discover — you receive a research deck and the one central story. " + C.PROMISES[1] + " " + C.PROMISES[2], dict(font=TEXT, size=12, color=d.fg2))]], line=1.4)
    d.footer(s, "14", "How a project starts")
    # 15 quote
    s = d.slide(); d.text(s, M, 2.3, 11.5, 2.4, [[("“" + C.QUOTE + "”", dict(font=DISPLAY, size=30, color=d.fg, italic=True))]], line=1.25)
    d.text(s, M, 5.0, 8, 0.4, "— Sanzeed Mirza", size=13, color=d.fg3); d.rule(s, M, 5.6, 3.0, point=True); d.footer(s, "15", "")
    # 16 contact
    s = d.slide(); d.eyebrow(s, M, M, 6, "Get in touch"); d.headline(s, M, 1.05, 9, 1.2, C.ENDURES, 44)
    d.text(s, M, 2.6, 7, 0.5, C.AVAILABLE, size=15, color=d.fg2)
    d.text(s, M, 3.5, 6, 2.2, [[(C.EMAIL, dict(font=HEAD, size=18, color=d.fg))], [(C.WHATSAPP + " · Call " + C.PHONE, dict(font=TEXT, size=15, color=d.fg2))], [(C.LINKEDIN, dict(font=TEXT, size=15, color=d.fg2))], [(C.SITE + " · " + C.CITY, dict(font=TEXT, size=15, color=d.fg2))]], line=1.6)
    d.text(s, 8.2, 3.5, 4.4, 1.5, [[(p, dict(font=TEXT, size=13, color=d.fg3))] for p in C.PROMISES], line=1.6)
    d.logo(s, LOCK_DARK, M, 5.9, 3.0); d.text(s, W - M - 5, 6.4, 5, 0.4, C.SHORT_LINE, size=13, color=d.fg3, align=PP_ALIGN.RIGHT)
    return d.save(path)

def proposal_deck():
    d = Deck(); path = f"{OUT}/sanzeed-proposal-template--12-slides.pptx"; F = lambda t: dict(font=TEXT, size=14, color=d.fg2)
    s = d.slide("Replace every bracketed field. Keep the headline in sentence case with a full stop."); d.logo(s, LOGO_DARK, M, M, 2.6)
    d.eyebrow(s, M, 2.7, 8, "Proposal · [Client] · [Project]", quiet=True); d.headline(s, M, 3.05, 8, 1.8, "One vision, from the brief to opening night", 46)
    d.text(s, M, 5.0, 8, 0.8, [[("Prepared for [Name], [Title], [Organisation]  ·  [Date]  ·  Valid until [Date]", dict(font=TEXT, size=13, color=d.fg2))], [("Sanzeed Mirza · Experiential Design Consultant · New Delhi", dict(font=TEXT, size=13, color=d.fg3))]], line=1.5)
    d.picture(s, asset("_hero-object--dark-2400.jpg"), 9.0, M, 3.63, 2.04); d.footer(s, C.SITE, "Proposal · 01")
    s = d.slide(); d.eyebrow(s, M, M, 6, "The room"); d.headline(s, M, 1.05, 9, 1.0, "What you asked for", 40)
    d.text(s, M, 2.2, 7.2, 3.6, ["[The brief in the client’s words: the site, the audience, the opening date, what must be true on opening night.]", "", "[What is fixed: building, budget band, dates. What is open: story, media, route.]"], size=14, color=d.fg2, line=1.5)
    d.card(s, 8.4, 2.2, 4.2, 3.3); d.text(s, 8.7, 2.5, 3.6, 3.0, [[("Project", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))], [("[Project name]", dict(font=HEAD, size=14, color=d.fg))], [("[City]", dict(font=TEXT, size=12, color=d.fg2))], [(" ", {})], [("Type", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))], [("[Museum or experience centre / Pavilion or exhibition / Show, launch or event / Projection or light show]", dict(font=TEXT, size=12, color=d.fg2))], [(" ", {})], [("Opening", dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))], [("[Month Year]", dict(font=TEXT, size=12, color=d.fg2))]], line=1.3)
    d.footer(s, "02", "The room")
    s = d.slide(); d.eyebrow(s, M, M, 6, "The story"); d.headline(s, M, 1.05, 10, 1.0, "The one central story", 40)
    d.text(s, M, 2.2, 10, 1.2, [[("[The story in one sentence — what a visitor should know by heart when they walk out.]", dict(font=DISPLAY, size=24, color=d.fg))]], line=1.25)
    d.text(s, M, 3.8, 7.2, 2.5, ["[Why this story: the research, the subject, the audience.]", "", "[How it will be carried: the route, the rooms, the media, the light.]"], size=14, color=d.fg2, line=1.5)
    d.rule(s, M, 6.5, 4, point=True); d.footer(s, "03", "The story")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Approach"); d.headline(s, M, 1.05, 9, 1.0, C.METHOD_LINE, 40); d.rule(s, M, 2.6, W - 2 * M)
    for i, (n, t, desc, rec) in enumerate(C.METHOD):
        x = M + i * 3.0; d.dot(s, x - 0.05, 2.55); d.text(s, x, 2.8, 2.7, 0.3, [[("Step " + n, dict(font=HEAD, size=10, color=d.accent_text, tracking=1.4, caps=True))]])
        d.text(s, x, 3.1, 2.7, 0.7, [[(t, dict(font=DISPLAY, size=30, color=d.fg))]]); d.text(s, x, 3.8, 2.7, 1.5, desc, size=11.5, color=d.fg2, line=1.4)
        d.text(s, x, 5.3, 2.7, 1.0, [[("You receive ", dict(font=TEXT, size=11, color=d.fg3)), (rec, dict(font=HEAD, size=11, color=d.fg))]], line=1.35)
    d.footer(s, "04", "Approach")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Scope"); d.headline(s, M, 1.05, 9, 1.0, "Seven services, held in one hand", 40)
    for i, (n, t, l, a, _) in enumerate(C.SERVICES):
        y = 2.2 + i * 0.58; d.text(s, M, y, 0.5, 0.4, [[(n, dict(font=HEAD, size=11, color=d.accent_text))]]); d.text(s, M + 0.5, y, 6.5, 0.4, [[(t, dict(font=HEAD, size=13, color=d.fg))]])
        d.text(s, 7.9, y, 4.7, 0.4, [[("[Included / Not in scope] — [what it covers on this project]", dict(font=TEXT, size=11, color=d.fg3))]])
        d.rule(s, M, y + 0.5, W - 2 * M)
    d.footer(s, "05", "Scope")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Deliverables"); d.headline(s, M, 1.05, 9, 1.0, "Named at every step", 40)
    dl = [("01 Discover", ["Research deck", "The one central story"]), ("02 Direct", ["Concept book", "Walkthrough film"]), ("03 Craft", ["Detail drawings", "Media scripts", "Prototype room"]), ("04 Deliver", ["Built, tested and opened experience", "[Handover documents]"])]
    for i, (t, items) in enumerate(dl):
        x = M + i * 3.0; d.text(s, x, 2.3, 2.7, 0.4, [[(t, dict(font=HEAD, size=13, color=d.fg))]]); d.rule(s, x, 2.75, 2.7, point=True)
        d.text(s, x, 2.95, 2.7, 2.5, [[(it, dict(font=TEXT, size=13, color=d.fg2))] for it in items] + [[("[Review: date]", dict(font=TEXT, size=11, color=d.fg3))]], line=1.6)
    d.footer(s, "06", "Deliverables")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Timeline"); d.headline(s, M, 1.05, 9, 1.0, "From the brief to opening night", 40); d.rule(s, M, 2.9, W - 2 * M, point=True, end=True)
    for i, (n, t, _, _) in enumerate(C.METHOD):
        x = M + i * 3.0; d.dot(s, x - 0.05, 2.85); d.text(s, x, 3.1, 2.7, 0.9, [[(t, dict(font=DISPLAY, size=24, color=d.fg))], [("[n] weeks · [start] – [end]", dict(font=TEXT, size=12, color=d.fg2))]], line=1.3)
        d.text(s, x, 4.1, 2.7, 1.2, [[("[Milestone and review date]", dict(font=TEXT, size=11, color=d.fg3))]])
    d.text(s, M, 5.6, 11, 0.8, [[("Opening night: [date]. ", dict(font=HEAD, size=13, color=d.fg)), ("Dates assume [client inputs: site access, content approvals] by [date].", dict(font=TEXT, size=13, color=d.fg2))]], line=1.4)
    d.footer(s, "07", "Timeline")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Investment"); d.headline(s, M, 1.05, 9, 1.0, "Investment bands", 40)
    d.text(s, M, 2.1, 9, 0.5, "Projects are scoped in one of four bands. The band for this proposal is marked; the fee below it is exclusive of applicable taxes.", size=13, color=d.fg2, line=1.4)
    for i, band in enumerate(C.BUDGET_BANDS):
        x = M + i * 3.0; d.card(s, x, 3.0, 2.8, 1.6); d.text(s, x + 0.25, 3.25, 2.4, 1.2, [[(band, dict(font=DISPLAY, size=20, color=d.fg))], [("[Selected / —]", dict(font=TEXT, size=11, color=d.fg3))]], line=1.3)
    d.text(s, M, 4.9, 11.5, 1.6, [[("Fee for this scope: [₹ amount] ", dict(font=HEAD, size=14, color=d.fg)), ("· [payment schedule by step: % at Discover, Direct, Craft, Deliver] · excludes fabrication, AV hardware and travel unless stated · [GSTIN] · [Bank name]", dict(font=TEXT, size=12, color=d.fg2))]], line=1.5)
    d.footer(s, "08", "Investment")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Team"); d.headline(s, M, 1.05, 9, 1.0, "One creative lead, the right partners", 40)
    d.picture(s, asset("_portrait--1x1-2000.jpg"), M, 2.3, 2.2, 2.2); d.text(s, M + 2.5, 2.4, 5, 2.0, [[("Sanzeed Mirza", dict(font=HEAD, size=16, color=d.fg))], [("Experiential Design Consultant · creative lead, story, space, media and the team", dict(font=TEXT, size=12, color=d.fg2))], [("15+ years · 90+ projects · 60+ museums and centres", dict(font=TEXT, size=12, color=d.fg3))]], line=1.4)
    for i, role in enumerate(["[Architect / exhibition designer]", "[Fabricator]", "[AV and projection integrator]", "[Content and research partner]"]):
        x = M + i * 3.0; d.rule(s, x, 5.0, 2.8, point=True); d.text(s, x, 5.15, 2.8, 1.2, [[(role, dict(font=HEAD, size=12, color=d.fg))], [("[Firm, city]", dict(font=TEXT, size=11, color=d.fg3))]], line=1.4)
    d.footer(s, "09", "Team")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Why Sanzeed"); d.headline(s, M, 1.05, 10, 1.0, "The whole room in one hand", 40)
    stats_row(d, s, 2.5)
    for i, (r, t, desc) in enumerate(C.PILLARS):
        x = M + i * 4.0; d.rule(s, x, 4.6, 3.6); d.text(s, x, 4.75, 3.6, 1.6, [[(t, dict(font=HEAD, size=14, color=d.fg))], [(desc, dict(font=TEXT, size=11.5, color=d.fg2))]], line=1.4)
    d.text(s, M, 6.35, 11, 0.4, C.TRUST, size=12, color=d.fg3); d.footer(s, "10", "Why Sanzeed")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Selected work"); d.headline(s, M, 1.05, 9, 1.0, "Three rooms, three ideas", 40)
    for i, key in enumerate(C.CASE_ORDER):
        c = C.CASES[key]; im = {"prime-minister-museum": 3, "ram-katha-show": 7, "buddha-park": 5}[key]; x = M + i * 4.0
        d.picture(s, asset(f"case/{key}-{im:02d}"), x, 2.2, 3.85, 2.17); d.wall_label(s, x, 4.45, 3.85, c["title"], c["place"])
        d.text(s, x, 4.85, 3.85, 1.6, [[(c["idea"] + " ", dict(font=DISPLAY, size=15, color=d.fg)), (c["visitors"], dict(font=TEXT, size=11, color=d.fg2))]], line=1.35)
    d.footer(s, "11", "Selected work")
    s = d.slide(); d.eyebrow(s, M, M, 6, "Next step"); d.headline(s, M, 1.05, 9, 1.2, "Tell me about the room", 44)
    d.text(s, M, 2.5, 7, 1.6, [[("Step 01 begins with a [n]-week Discover phase; you receive a research deck and the one central story. ", dict(font=TEXT, size=14, color=d.fg2)), ("To start: [confirm scope and band] · [sign the engagement letter] · [share the brief, site drawings and content].", dict(font=TEXT, size=14, color=d.fg2))]], line=1.5)
    d.text(s, M, 4.3, 6, 1.8, [[(C.EMAIL, dict(font=HEAD, size=16, color=d.fg))], [(C.WHATSAPP + " · Call " + C.PHONE, dict(font=TEXT, size=13, color=d.fg2))], [(C.LINKEDIN + " · " + C.SITE, dict(font=TEXT, size=13, color=d.fg2))]], line=1.6)
    d.text(s, 8.2, 4.3, 4.4, 1.5, [[(p, dict(font=TEXT, size=12, color=d.fg3))] for p in C.PROMISES], line=1.6)
    d.logo(s, LOCK_DARK, M, 6.0, 3.0); d.footer(s, "", "Proposal · 12 · valid until [Date]")
    return d.save(path)

# ---------------- Case-study template (A4, HTML) ----------------
CASE_CSS = A4_CSS + """
.sheet .lock { left: 18mm; top: 18mm; width: 46mm; }
.sheet .top { position: absolute; left: 18mm; right: 18mm; top: 40mm; bottom: 18mm; }
.n { font-family: var(--font-heading); font-weight: 500; font-size: 6.5pt; letter-spacing: .12em; text-transform: uppercase; color: var(--fg-3); }
.title { font-size: 34pt; margin: 2mm 0 1mm; }
.place { font-size: 9pt; color: var(--fg-2); margin-bottom: 6mm; }
.idea-l { font-family: var(--font-display); font-weight: 300; font-size: 18pt; color: var(--fg); margin: 1mm 0 2mm; font-variation-settings: "opsz" 72; }
.p1 .plate { position: absolute; left: 0; right: 0; bottom: 8mm; height: 108mm; border-radius: 6mm; }
.p1 .wl { position: absolute; left: 0; bottom: 0; }
.p2 .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5mm; }
.p2 .plate { height: 56mm; border-radius: 4mm; }
.p2 .cap { font-size: 6.5pt; color: var(--fg-3); margin-top: 1.5mm; line-height: 1.4; }
.p2 .cap b { font-family: var(--font-heading); font-weight: 500; color: var(--accent-text); letter-spacing: .08em; margin-right: 1.5mm; }
.meta { position: absolute; left: 0; right: 0; bottom: 0; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; border-top: 1px solid var(--line); padding-top: 3mm; font-size: 7.5pt; color: var(--fg-2); }
.meta b { display: block; font-family: var(--font-heading); font-weight: 600; font-size: 6.5pt; letter-spacing: .1em; text-transform: uppercase; color: var(--fg-3); margin-bottom: 1mm; }
.slot { display: flex; align-items: center; justify-content: center; font-size: 7pt; color: var(--fg-3); }
"""
def case_template(filled=True):
    if filled:
        c = C.CASES["prime-minister-museum"]; key = "prime-minister-museum"; hero = 3; grid = [1, 4, 5, 7]
        img_hero = f'<img src="{jimg(f"case/{key}-{hero:02d}")}" alt="{esc(c["captions"][hero-1])}">'
        grid_html = "".join(f'<div><div class="plate"><img src="{jimg(f"case/{key}-{i:02d}")}" alt=""></div><div class="cap"><b>{i:03d}</b>{esc(c["captions"][i-1])}</div></div>' for i in grid)
        wl = f'<b>{esc(c["title"])}</b><span class="sep">·</span>{esc(c["place"])}<span class="sep">·</span>{hero:03d} {esc(c["captions"][hero-1])}'
        n = "Case study · 001 · " + c["type"]
    else:
        c = dict(title="[Project title]", place="[City]", type="[Museums & Experience Centres / Projection Mapping & Shows / Explainer Videos & Others]", role="[Role: concept & creative direction / show concept & direction]",
                 brief="[The brief — what the client asked for, where, for whom, by when. Two or three sentences.]", idea="[The idea, in one line.]",
                 idea_text="[How the idea works in the room: the route, the spine, the light, the sequence. Three sentences.]",
                 walk="[The walk — what changes from room to room; who stands where; what the floor, the walls and the ceiling do.]",
                 visitors="[What visitors do — one sentence, ending on the image.]")
        img_hero = '<div class="slot" style="position:absolute;inset:0">[Hero image · 16:9 · 1600 × 900 px minimum]</div>'
        grid_html = "".join(f'<div><div class="plate"><div class="slot" style="position:absolute;inset:0">[Image {i:03d} · 16:9]</div></div><div class="cap"><b>{i:03d}</b>[Caption: what the visitor sees]</div></div>' for i in (1, 2, 3, 4))
        wl = '<b>[Project title]</b><span class="sep">·</span>[City]<span class="sep">·</span>001 [Caption]'
        n = "Case study · [001] · [Category]"
    p1 = f"""<section class="sheet grain p1" id="p1"><img class="mark lock" src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed"><div class="top">
    <div class="n">{esc(n)}</div><h2 class="hl title">{esc(c['title'])}<span class="pt">.</span></h2><div class="place">{esc(c['place'])}</div>
    <h3>The brief</h3><p class="body">{esc(c['brief'])}</p><h3>The idea</h3><div class="idea-l">{esc(c['idea'])}</div><p class="body">{esc(c['idea_text'])}</p>
    <div class="plate">{img_hero}</div><div class="wl">{wl}</div></div>
    <div class="folio"><span>Sanzeed Mirza · Experiential Design Consultant</span><span>01</span></div></section>"""
    p2 = f"""<section class="sheet grain p2" id="p2"><img class="mark lock" src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed"><div class="top">
    <div class="grid">{grid_html}</div>
    <h3>The walk</h3><p class="body">{esc(c['walk'])}</p>
    <h3>What visitors do</h3><p class="body" style="font-family:var(--font-display);font-weight:300;font-size:13pt;line-height:1.3;color:var(--fg);font-variation-settings:'opsz' 72">{esc(c['visitors'])}</p>
    <div class="meta"><div><b>Type</b>{esc(c['type'])}</div><div><b>Location</b>{esc(c['place'])}</div><div><b>Role</b>{esc(c['role'])}</div></div></div>
    <div class="folio"><span>{esc(c['title'])} · {esc(c['place'])}</span><span>02</span></div></section>"""
    return head("Sanzeed — case-study template (A4)", "dark", CASE_CSS) + "<body>\n" + p1 + "\n" + p2 + "\n</body>\n</html>\n"

# ---------------- Portfolio template (A4 landscape, HTML) ----------------
PORT_CSS = """
@page { size: 297mm 210mm; margin: 0; }
body { background: #000; }
.sheet { width: 297mm; height: 210mm; font-family: var(--font-text); }
.mark { position: absolute; display: block; }
.hl { color: var(--fg); line-height: 1.02; }
.folio { position: absolute; left: 16mm; right: 16mm; bottom: 9mm; display: flex; justify-content: space-between; font-size: 6.5pt; color: var(--fg-3); }
.cover .mark { left: 16mm; top: 16mm; width: 44mm; }
.cover .plate { position: absolute; left: 150mm; top: 16mm; width: 131mm; height: 164mm; border-radius: 7mm; }
.cover .wl { position: absolute; left: 150mm; top: 183mm; font-size: 6.5pt; }
.cover .eyebrow-quiet { position: absolute; left: 16mm; top: 92mm; font-size: 6.5pt; }
.cover .hl { position: absolute; left: 16mm; top: 99mm; width: 125mm; font-size: 38pt; }
.cover .sub { position: absolute; left: 16mm; top: 150mm; width: 120mm; font-size: 9pt; line-height: 1.5; color: var(--fg-2); }
.proj .plate { position: absolute; left: 16mm; top: 16mm; width: 187mm; height: 178mm; border-radius: 6mm; }
.proj .side { position: absolute; left: 213mm; top: 16mm; width: 68mm; bottom: 32mm; }
.proj .c { font-family: var(--font-heading); font-weight: 500; font-size: 7pt; letter-spacing: .12em; color: var(--accent-text); font-variant-numeric: tabular-nums; }
.proj .t { font-size: 22pt; margin: 3mm 0 1mm; }
.proj .p { font-size: 9pt; color: var(--fg-2); }
.proj .cat { font-family: var(--font-heading); font-weight: 600; font-size: 6.5pt; letter-spacing: .1em; text-transform: uppercase; color: var(--fg-3); margin-top: 8mm; border-top: 1px solid var(--line); padding-top: 3mm; }
.proj .line { font-size: 8pt; line-height: 1.5; color: var(--fg-2); margin-top: 3mm; }
.proj .line b { font-family: var(--font-display); font-weight: 300; font-size: 12pt; color: var(--fg); display: block; margin-bottom: 1mm; }
.proj .wl { position: absolute; left: 0; bottom: 0; font-size: 6.5pt; }
.proj .mark { left: 213mm; bottom: 20mm; width: 30mm; top: auto; }
.contact .mark { left: 16mm; top: 16mm; width: 44mm; }
.contact .hl { position: absolute; left: 16mm; top: 60mm; width: 160mm; font-size: 40pt; }
.contact .lines { position: absolute; left: 16mm; top: 96mm; width: 150mm; font-size: 11pt; line-height: 1.8; color: var(--fg-2); }
.contact .lines b { font-family: var(--font-heading); font-weight: 600; color: var(--fg); }
.contact .promises { position: absolute; left: 180mm; top: 96mm; width: 100mm; font-size: 9pt; line-height: 1.8; color: var(--fg-3); }
.contact .lock { left: 16mm; bottom: 18mm; top: auto; width: 56mm; }
"""
PORTFOLIO = [("prime-minister-museum", "prime-minister-museum"), ("buddha-park", "buddha-park"), ("ram-katha-show", "ram-katha-show"), ("yuge-yugin-bharat-museum", None), ("india-pavilion-expo-2025", None), ("tribal-museum", None), ("rbi-museum-interior", None), ("g20-tree-show", None), ("army-museum-abu-dhabi", None), ("dubai-police-control-center", None)]
def portfolio():
    G = {g["img"]: g for g in C.GALLERY}; pages = []
    pages.append(f"""<section class="sheet grain cover" id="p1"><img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
    <div class="plate"><img src="{jimg('case/prime-minister-museum-03')}" alt="Prime Minister Museum"></div><div class="wl"><b>Prime Minister Museum</b><span class="sep">·</span>New Delhi</div>
    <div class="eyebrow-quiet">Sanzeed Mirza · Experiential Design Consultant · Portfolio</div><h1 class="hl">Vision you can walk into<span class="pt">.</span></h1>
    <p class="sub">Ten rooms from ninety. Museums, experience centres, pavilions, memorials and shows — each with its wall label. The films and the full galleries are at {C.SITE}.</p>
    <div class="folio"><span>{C.SITE}</span><span>Portfolio · 2026</span></div></section>""")
    for i, (im, case) in enumerate(PORTFOLIO):
        g = G[im]; n = i + 1
        line = f'<div class="line"><b>{esc(C.CASES[case]["idea"])}</b>{esc(C.CASES[case]["visitors"])}</div>' if case else ""
        src = jimg(f"case/{case}-{ {'prime-minister-museum':3,'buddha-park':5,'ram-katha-show':7}[case]:02d}") if case else jimg(im)
        pages.append(f"""<section class="sheet grain proj" id="p{n+1}"><div class="plate"><img src="{src}" alt="{esc(g['title'])}"></div>
        <div class="side"><div class="c">{n:03d}</div><h2 class="hl t">{esc(g['title'])}<span class="pt">.</span></h2><div class="p">{esc(g['place'])}</div>
        <div class="cat">{esc(g['cat'])}</div>{line}<div class="wl"><b>{esc(g['title'])}</b><span class="sep">·</span>{esc(g['place'])}</div></div>
        <img class="mark" src="{logo('simplified-small-size','full-colour-dark')}" alt="Sanzeed">
        <div class="folio"><span>Sanzeed Mirza · Experiential Design Consultant</span><span>{n+1:02d}</span></div></section>""")
    pages.append(f"""<section class="sheet grain contact" id="p12"><img class="mark" src="{logo('primary-wordmark','full-colour-dark')}" alt="Sanzeed">
    <h2 class="hl">Tell me about the room<span class="pt">.</span></h2>
    <div class="lines">{esc(C.CALL_SUB)}<br><b>{C.EMAIL}</b><br>{C.WHATSAPP} · Call {C.PHONE}<br>{C.LINKEDIN} · {C.SITE}<br>{C.CITY}</div>
    <div class="promises">{'<br>'.join(esc(p) for p in C.PROMISES)}<br><br>{esc(C.RIGHTS)}</div>
    <img class="mark lock" src="{logo('horizontal-descriptor','full-colour-dark')}" alt="Sanzeed — Experiential Design Consultant">
    <div class="folio"><span>{C.SITE}</span><span>12</span></div></section>""")
    return head("Sanzeed — portfolio template (A4 landscape)", "dark", PORT_CSS) + "<body>\n" + "\n".join(pages) + "\n</body>\n</html>\n"

def pptx_exports(pptx_path, stem):
    run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", OUT, pptx_path])
    pdfp = f"{OUT}/{stem}.pdf"; tmp = f"{OUT}/_s"; os.makedirs(tmp, exist_ok=True)
    pages = pdf_pages_png(pdfp, f"{tmp}/s", 96)
    for i, p in enumerate(pages): os.replace(p, f"{OUT}/{stem}--slide-{i+1:02d}.png")
    os.rmdir(tmp); return pdfp

if __name__ == "__main__":
    sales = sales_deck(); prop = proposal_deck()
    pptx_exports(sales, "sanzeed-sales-presentation--16-slides"); pptx_exports(prop, "sanzeed-proposal-template--12-slides")
    jobs = []
    for stem, html_ in [("sanzeed-case-study-template--filled-prime-minister-museum", case_template(True)), ("sanzeed-case-study-template--blank", case_template(False))]:
        hp = write(f"{SRC}/{stem}.html", html_); jobs.append(pdf(hp, f"{OUT}/{stem}-a4.pdf", 210, 297))
    hp = write(f"{SRC}/sanzeed-portfolio-template--a4-landscape.html", portfolio()); jobs.append(pdf(hp, f"{OUT}/sanzeed-portfolio-template--a4-landscape.pdf", 297, 210))
    render_jobs(jobs)
    for stem in ("sanzeed-case-study-template--filled-prime-minister-museum-a4", "sanzeed-case-study-template--blank-a4", "sanzeed-portfolio-template--a4-landscape"):
        tmp = f"{OUT}/_p"; os.makedirs(tmp, exist_ok=True)
        for i, p in enumerate(pdf_pages_png(f"{OUT}/{stem}.pdf", f"{tmp}/p", 80)): os.replace(p, f"{OUT}/{stem}--page-{i+1:02d}.png")
        os.rmdir(tmp)
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".pdf"): print(f, len(page_sizes(f"{OUT}/{f}")), page_sizes(f"{OUT}/{f}")[0])
    print("presentations done", folder_size_mb(OUT), "MB")
