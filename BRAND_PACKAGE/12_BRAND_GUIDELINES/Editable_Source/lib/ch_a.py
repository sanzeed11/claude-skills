"""Chapters 00 (cover, contents placeholder) and 01–11."""
from guide import *

WM_D = lambda: logo('primary-wordmark', 'full-colour-dark')
WM_L = lambda: logo('primary-wordmark', 'full-colour-light')

# ------------------------------------------------------------------ 00 cover
def cover():
    inner = (f'<div class="cover-top"><span class="eyebrow">Sanzeed Mirza · Experiential Design Consultant · New Delhi</span>'
             f'<span class="cover-meta">Brand package · 12 Brand Guidelines</span></div>'
             f'<div class="cover-title"><h1 class="doc-display">Brand <span class="lit">Guidelines</span>.</h1>'
             f'<p class="cover-sub">The standards manual for the Sanzeed identity: strategy, logo system, colour, typography, graphic language, photography, website, digital, social, print, marketing, signage, motion, voice and production — with every asset shown as it is delivered.</p>'
             f'<p class="cover-meta">Brand Guidelines · Version 1.0 · November 2026</p></div>'
             f'<div class="cover-foot"><div class="wordmark"><img src="{WM_D()}" alt="Sanzeed"></div><span class="cover-meta">sanzeed.com</span></div>')
    return page('Cover', inner, cls='cover theme-dark')

def contents(entries):
    """entries: list of (num, title, pageno) — written last by the generator."""
    lis = ''.join(f'<li><span class="n">{esc(n)}</span><span class="t">{esc(t)}</span><span class="p">{p:02d}</span></li>' for n, t, p in entries)
    inner = head('Contents', 'Twenty-six chapters, one <span class="lit">idea</span>.',
                 'Carry the light across. Each chapter opens on a dark divider, shows the real asset it governs, and ends with the rules that keep it whole. Page numbers refer to this PDF.', solo=False)
    inner += body(f'<ol class="toc">{lis}</ol>')
    return page('Contents', inner)

# ------------------------------------------------------------------ 01 Brand introduction
def ch01():
    P = []
    P.append(divider('01', 'Brand <span class="lit">introduction</span>.',
        'A brief on one side, a visitor on the other. Sanzeed’s work carries the light across — and so does every rule in this manual.',
        [('1.1', 'The one idea'), ('1.2', 'The identity at a glance'), ('1.3', 'How to use this manual')], '01 · Brand introduction'))
    # 1.1 the one idea
    ill = A('05_GRAPHIC_ASSETS/Illustrations/png/sanzeed-illustration-between-two-points--dark.png', 1800)
    left = ('<p class="lead-sm">The site already says it: <em>“Between two points of light. A brief on one side, a visitor on the other. Seven ways to carry the light across.”</em> A client arrives with an intention; a visitor leaves with a memory. Everything in between — the story, the room, the light, the timing, the team — is carried across without dropping it.</p>'
            '<p class="mt-3">Every part of this identity serves that idea. The system is built from three things, and only three:</p>'
            '<dl class="kv mt-2"><dt>The point</dt><dd>The gold dot — the point of light. The brand’s smallest unit and its most recognisable: it sits in the wordmark, ends the signature (“Sanzeed<b class="gold">.</b>”), closes headlines (“lit<b class="gold">.</b>”) and becomes the symbol.</dd>'
            '<dt>The beam</dt><dd>The hairline the point travels along. The route through a museum, the timeline of a career, the rule in a document.</dd>'
            '<dt>The room</dt><dd>The dark field everything sits in. Black is not a background colour here; it is the gallery before the lights come up.</dd></dl>')
    demo = ('<div class="g3 gap-sm mt-3">'
            '<div class="demo dark" style="height:20mm;display:flex;align-items:center;justify-content:center"><span class="pt glow" style="width:4mm;height:4mm"></span><span class="lbl" style="position:absolute;left:3mm;bottom:2.4mm;font:500 6.5pt/1 var(--font-heading);letter-spacing:.08em;color:#808086">THE POINT</span></div>'
            '<div class="demo dark" style="height:20mm;display:flex;align-items:center;padding:0 5mm"><div class="beamline" style="width:100%"><span class="pt glow"></span></div><span style="position:absolute;left:3mm;bottom:2.4mm;font:500 6.5pt/1 var(--font-heading);letter-spacing:.08em;color:#808086">THE BEAM</span></div>'
            '<div class="demo dark" style="height:20mm;display:flex;align-items:center;justify-content:center"><div class="room-demo" style="width:60%;height:60%"></div><span style="position:absolute;left:3mm;bottom:2.4mm;font:500 6.5pt/1 var(--font-heading);letter-spacing:.08em;color:#808086">THE ROOM</span></div></div>')
    right = fig(ill, 'Between two points of light', 'Illustration · 05_GRAPHIC_ASSETS/Illustrations', 'The brief (left, low) and the visitor (right, high); one line of light between them and six fainter ways behind it — “Seven ways to carry the light across.”', plate='dark pad-sm', h='h66') + demo
    P.append(page('01 · Brand introduction', head('1.1 · The one idea', 'Carry the light <span class="lit">across</span>.', 'The brand idea, derived from confirmed copy on sanzeed.com and recorded in 01_BRAND_STRATEGY/Brand_Strategy.md §1.') + body(f'<div class="split"><div>{left}</div><div>{right}</div></div>')))
    # 1.2 at a glance
    img = A('06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/JPG/sanzeed-img-prime-minister-museum--museum.jpg', 1200)
    glance = (f'<div class="g4 gap-md stretch">'
              f'<div class="plate dark h60"><img src="{WM_D()}" alt="Primary wordmark" style="width:76%;height:auto"><span class="lbl">Primary wordmark · full-colour-dark</span></div>'
              f'<div class="plate plaster h60"><img src="{WM_L()}" alt="Primary wordmark on light" style="width:76%;height:auto"><span class="lbl">Primary wordmark · full-colour-light</span></div>'
              f'<div class="plate dark h60 c2" style="display:grid;grid-template-columns:repeat(5,1fr);padding:0;gap:0">'
              + ''.join(f'<div style="background:{c};display:flex;align-items:flex-end;padding:2.5mm;font:500 6.2pt/1.3 var(--font-heading);letter-spacing:.06em;color:{t}"><span>{n}<br>{c}</span></div>' for n, c, t in [('Gallery Black', '#000000', '#808086'), ('Night', '#0D0D0F', '#808086'), ('Lamp Gold', '#E9B25A', '#1A1816'), ('Plaster', '#F5F0E7', '#665F55'), ('Old Gold', '#B8863B', '#1A1816')])
              + '</div></div>')
    typ = ('<div class="g3 gap-md mt-3" style="align-items:end">'
           '<div><div class="ff-display" style="font-size:26pt">Experiential design you can walk <span class="lit">into</span>.</div><p class="xs mt-1 faint">Fraunces 300 · opsz 144 · sentence case, full stop, the last word may be lit</p></div>'
           '<div><div class="eyebrow">Now showing</div><div class="ff-heading mt-1" style="font-size:13pt">Prime Minister Museum</div><div class="ff-text muted" style="font-size:9pt">New Delhi · A corridor you walk in order.</div><p class="xs mt-1 faint">Inter Tight 600 eyebrows and titles · Inter 400 for everything read</p></div>'
           '<div><div class="stat">90<span class="plus">+</span> <span style="font-size:14pt;color:var(--fg-2)">projects directed</span></div><p class="xs mt-1 faint">15+ years · 8+ years experiential &amp; museum · 60+ museums &amp; centres</p></div></div>')
    right = fig(img, 'Prime Minister Museum', 'New Delhi', 'A long corridor of every Prime Minister, walked beneath a tricolour canopy of light. The client’s own imagery, always with a wall label.', plate='dark cover', h='h56')
    P.append(page('01 · Brand introduction', head('1.2 · The identity at a glance', 'The whole room, on one <span class="lit">page</span>.', 'Wordmark, colour, type, imagery and voice — the five things every piece is checked against.') + body(glance + '<div class="split wide mt-3">' + typ + right + '</div>')))
    # 1.3 how to use
    rows = [('01–04', 'Why', 'Strategy, positioning, personality and voice: what the identity means and how it sounds.'),
            ('05–11', 'The mark', 'Logo system, construction, colour versions, clear space, minimum sizes, misuse, signature and monogram.'),
            ('12–16', 'The system', 'Colour, typography, graphic elements, iconography and photography — the material every application is built from.'),
            ('17–23', 'Applications', 'Website, digital assets, social, print, marketing, signage and motion — each shown as delivered, with its specifications.'),
            ('24–26', 'Words and production', 'Voice and communication, the applications gallery, file formats, naming and production specifications.'),
            ('A', 'Appendix', 'Delivery index of the package folders, so every file in this manual can be found.')]
    t = table(['Chapters', 'Part', 'What it governs'], rows, widths=['16mm', '26mm', 'auto'])
    howto = '<div class="mt-2">' + rules(['<b>Start with the rule, then look at the asset.</b> Every page shows the file it governs, with its wall label and its path in the package.',
             '<b>Use the delivered files; never redraw.</b> Logos, patterns, icons and templates are in their folders as SVG, PDF, PNG, HTML, DOCX and PPTX. Link or copy them.',
             '<b>Dark is the gallery, Plaster is the label.</b> Screens, social, video and covers are dark; documents and print are light. The pairing rules in chapter 07 follow from this.',
             '<b>One gold accent per composition.</b> If you have added a second, remove one.',
             '<b>Real copy, real rooms.</b> Only confirmed copy from 01_BRAND_STRATEGY; only the client’s own project imagery. Fields the client must fill are bracketed, never invented.',
             '<b>Verify by looking.</b> Render, open, check the logo variant, clear space, accent, type and clipping before anything leaves the studio.'], cls='tight') + '</div>'
    quick = A('16_WEBSITE_IMPLEMENTATION/screenshots/after-index-desktop-dark.jpg', 1440)
    right = fig(quick, 'sanzeed.com', 'The live site, rebuilt with the identity applied (16_WEBSITE_IMPLEMENTATION)', 'The reference every other application is measured against: everything here should look like it came from the same studio.', plate='dark cover top', h='h46')
    right += ('<div class="callout mt-3"><b class="k">Quick reference.</b> The ten rules, which logo goes where, colour values, the type scale and file locations are condensed in <span class="mono">12_BRAND_GUIDELINES/Brand_Usage_Reference.md</span> — two pages for anyone who will not read the manual.</div>')
    P.append(page('01 · Brand introduction', head('1.3 · How to use this manual', 'Read the rule, look at the <span class="lit">room</span>.', 'The manual is organised from meaning to mark to material to application. Each chapter is self-contained; the appendix indexes the package.') + body(f'<div class="split wide"><div>{t}{howto}</div><div>{right}</div></div>')))
    return P

# ------------------------------------------------------------------ 02 Brand strategy
def ch02():
    P = []
    P.append(divider('02', 'Brand <span class="lit">strategy</span>.', 'Vision, mission and purpose; five values; the archetype. Everything marked Confirmed is taken from sanzeed.com; everything else is the agency’s recommendation, accepted for this version.',
        [('2.1', 'Vision · mission · purpose'), ('2.2', 'Values and personality'), ('2.3', 'Archetype, audience and promise')], '02 · Brand strategy'))
    portrait = A('06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/Portrait/sanzeed-portrait--4x5-2000.jpg', 1000)
    stm = ('<div class="stack-lg">'
           '<div><span class="eyebrow">Vision <span class="tag tag-rec">Recommendation</span></span><div class="ff-display mid mt-1" style="font-size:20pt">Experiences people walk into and never quite <span class="lit">leave</span>.</div><p class="xs faint mt-1">Compresses “impossible to forget once you have walked through it” (confirmed).</p></div>'
           '<div><span class="eyebrow">Mission <span class="tag tag-confirmed">Confirmed wording</span></span><p class="mt-1" style="font-size:10pt;line-height:1.5;max-width:150mm">To lead the whole room — story, space, graphics, media and the team that builds it — so that institutions and brands open experiences that are calm to run and impossible to forget.</p></div>'
           '<div><span class="eyebrow">Purpose <span class="tag tag-confirmed">Confirmed · Sanzeed’s own words</span></span><p class="doc-quote mt-1" style="font-size:15pt;max-width:160mm">“Because the most powerful stories aren’t just told — they’re felt, lived and remembered through the spaces we design and the moments we shape.”</p></div></div>')
    right = fig(portrait, 'Sanzeed Mirza', 'Portrait, 4:5 crop (06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/Portrait)', 'The brand is the person: first person singular, one steady creative hand from the brief to opening night.', plate='night cover', h='h120')
    P.append(page('02 · Brand strategy', head('2.1 · Vision, mission, purpose', 'Three statements, one <span class="lit">through-line</span>.', 'From 01_BRAND_STRATEGY/Brand_Strategy.md §2. Use them verbatim; do not paraphrase the mission or the purpose.') + body(f'<div class="split wide">{stm}{right}</div>')))
    vals = [('Story first.', '“The script comes first. Every room, screen and surface carries a line of it.”'),
            ('The route, not the floor plan.', 'Experiences are sequenced for a human walking through them, in order, with dwell time.'),
            ('Whole-room responsibility.', '“All seven, every time. Every room needs the whole list, held in one hand.”'),
            ('Calm leadership.', 'Designers, writers, architects, producers and technologists “moved toward one outcome, calmly.”'),
            ('Built, tested, opened.', '“On scale, on story, on time.” Ambition is only real once the doors open.')]
    vl = rules([f'<b>{esc(a)}</b> {esc(b)}' for a, b in vals])
    traits = table(['Trait', 'What it looks like', 'What it never looks like'], [
        ('<b>Calm</b>', 'Space, one accent colour, short sentences', 'Shouting, gradients everywhere, exclamation marks'),
        ('<b>Precise</b>', 'Numbered steps, named deliverables, 001 counters, wall-label captions', 'Vague adjectives (“innovative”, “cutting-edge”)'),
        ('<b>Monumental</b>', 'Large light serif headlines, a single object on a dark field', 'Clutter, many small things competing'),
        ('<b>Warm</b>', 'Gold light, first person, “the first conversation is always free”', 'Corporate distance, “we at our firm”'),
        ('<b>Curious</b>', '“Every environment begins as a question”', 'Pre-packaged solutions')], widths=['22mm', 'auto', 'auto'])
    P.append(page('02 · Brand strategy', head('2.2 · Values and personality', 'Five values, five <span class="lit">traits</span>.', 'Each value is anchored in confirmed copy from the site. The five traits are a checklist for every piece: if one is missing, the piece is not finished.') + body(f'<div class="split even"><div><div class="doc-h3">Values</div>{vl}</div><div><div class="doc-h3">Personality</div>{traits}</div></div>')))
    arch = ('<p><b class="k">The Creator</b>, tempered by <b class="k">The Sage</b>. The Creator makes things of enduring value; the Sage brings calm, research and judgement. Together: a maker who thinks before building and stays composed while building at monumental scale.</p>'
            '<p class="mt-2 muted">Not <em>The Magician</em>: the brand does not sell spectacle; it sells spectacle held in a steady hand.</p>'
            '<div class="hr"></div><div class="doc-h3">Brand promise</div><div class="ff-display mid" style="font-size:17pt">One vision, carried across — from the brief to opening <span class="lit">night</span>.</div>'
            '<p class="sm mt-2 muted">Supported by three confirmed commitments: the first conversation is free · a reply within two working days · a named deliverable at every step of the method.</p>'
            '<div class="hr"></div><div class="doc-h3">USP</div><p><b class="k">The whole room in one hand.</b> A single consultant who has personally done every layer — concept art, VFX, animation, museum narrative, spatial design, show direction, team leadership — and therefore holds the entire experience together without hand-offs.</p>')
    aud = table(['Segment', 'Who', 'What they need', 'Proof they look for'], [
        ('<b>Institutional commissioners</b>', 'Ministries, museum authorities, cultural trusts, state tourism boards', 'A creative lead trusted with national-scale, politically visible projects', 'Prime Minister Museum, Yuge Yugeen Bharat, Ram Katha Show; the method'),
        ('<b>Corporate experience owners</b>', 'Brands building experience centres, pavilions, boardrooms, launches', '“Brands you can stand inside”', 'Experience-centre gallery; Digital ↔ Physical integration'),
        ('<b>Delivery partners</b>', 'Architects, fabricators, AV and projection integrators, event agencies', 'A creative director who leads the narrative and media design', 'Cross-functional leadership; projection shows'),
        ('<b>Former-employer ecosystem</b>', 'Studios needing a senior independent director', 'Availability for select consulting and creative-direction mandates', 'Timeline, seven services')], cls='xs')
    method = A('05_GRAPHIC_ASSETS/Illustrations/png/sanzeed-illustration-method-diagram--light.png', 1800)
    right = aud + fig(method, 'The method', 'Discover → Direct → Craft → Deliver, with the deliverable named under each step (05_GRAPHIC_ASSETS/Illustrations)', None, plate='paper pad-sm', h='h44', cls='mt-3')
    P.append(page('02 · Brand strategy', head('2.3 · Archetype, audience, promise', 'A maker who thinks before <span class="lit">building</span>.', 'Archetype and promise from Brand_Strategy.md §5–8; audience segments are a recommendation to be confirmed by Sanzeed.') + body(f'<div class="split">{"<div>"+arch+"</div>"}<div>{right}</div></div>')))
    return P

# ------------------------------------------------------------------ 03 Positioning
def ch03():
    P = []
    P.append(divider('03', '<span class="lit">Positioning</span>.', 'Story-led and whole-room: the one independent consultant who carries a single creative vision from the brief to opening night.',
        [('3.1', 'Statement and map'), ('3.2', 'Pillars, proof and naming')], '03 · Positioning'))
    pm = L('01_BRAND_STRATEGY/src/positioning-map.svg')
    stmt = ('<p style="font-size:10.5pt;line-height:1.55"><b class="k">For</b> museums, cultural institutions, government bodies and brands that must open a public experience at national scale, <b class="k">Sanzeed Mirza is</b> the independent experiential design consultant <b class="k">who</b> carries one creative vision from the brief to opening night — narrative, space, media and the team — in one person, <b class="k">unlike</b> large studios where strategy, design and delivery are handed between departments, or architects and AV integrators who each own only part of the room.</p>'
            '<dl class="kv mt-3"><dt>Category</dt><dd>Experiential design and creative direction (museums, experience centres, pavilions, memorials, projection and light shows).</dd>'
            '<dt>Frame of reference</dt><dd>Museum-design and experiential studios; the client’s prior employer Tagbin sits in the same frame.</dd>'
            '<dt>Point of difference</dt><dd>Fifteen years that run from VFX and concept art to directing 60+ museums and centres — one person who can write the story, draw the room, script the media and run the floor.</dd>'
            '<dt>Reason to believe</dt><dd>90 projects directed, three published case studies, Prime Minister Museum / Ram Katha Show / Buddha Park, institutional commissioners, a method with named deliverables at each step.</dd></dl>')
    right = fig(pm, 'Positioning map', 'Story-led ↔ spectacle-led · part of the room ↔ whole room (01_BRAND_STRATEGY/src/positioning-map.svg)', 'Sanzeed sits bottom-right. The nearest neighbours are full-service museum-design studios; the difference is that breadth offered as an individual creative lead, with film/VFX craft most studios buy in.', plate='paper pad-sm', h='h104')
    P.append(page('03 · Positioning', head('3.1 · Statement and map', 'The whole room, in one <span class="lit">hand</span>.', 'The positioning statement is used in proposals, the media kit and the About page. Do not shorten the “unlike” clause.') + body(f'<div class="split even">{"<div>"+stmt+"</div>"}{right}</div>')))
    pillars = table(['Pillar', 'Confirmed source', 'Expression in the identity'], [
        ('<b>Strategic Vision</b>', '“Transforming complex ideas into cohesive, purposeful stories — concept through launch.”', 'The beam: one line from brief to visitor'),
        ('<b>Immersive Craft</b>', '“Environments that engage intellectually, emotionally, and physically across every touchpoint.”', 'The room: dark field, single lit object, large serif'),
        ('<b>Calm Leadership</b>', '“Guiding designers, writers, architects, producers and technologists toward unified outcomes.”', 'Restraint: one accent, measured motion, precise labels')], widths=['28mm', 'auto', '58mm'])
    proof = ('<div class="g4 gap-sm mt-2">' + ''.join(f'<div><div class="stat">{n}<span class="plus">+</span></div><p class="xs muted mt-1">{l}</p></div>' for n, l in [('15', 'years'), ('8', 'years experiential &amp; museum'), ('90', 'projects directed'), ('60', 'museums &amp; centres')]) + '</div>'
             '<p class="sm mt-3">Prime Minister Museum, New Delhi · Ram Katha Show, Ayodhya · Buddha Park, Uttarakhand · Yuge Yugeen Bharat Museum · India Pavilion Expo 2025 (concept) · G20 Tree Show · Army Museum Abu Dhabi · Dubai Police Control Center. “Trusted by PwC, Microsoft, Discovery and National Museums.”</p>')
    naming = table(['Context', 'Use'], [
        ('Brand mark, wordmark, social handles, domain', '<b>SANZEED</b> / <b>Sanzeed</b> / @sanzeed'),
        ('Formal, legal, SEO, bylines, invoices, proposals', '<b>Sanzeed Mirza</b>'),
        ('Descriptor (always with the full name on first use)', '<b>Experiential Design Consultant</b>'),
        ('Never', '“Sanzeed Studio”, “Sanzeed Design”, “Mirza Design” — the brand is the person')], cls='xs')
    imgs = [('ram-katha-show--projection', 'Ram Katha Show', 'Ayodhya'), ('buddha-park-stupa-path--museum', 'Buddha Park', 'Uttarakhand'), ('yuge-yugeen-bharat-museum--museum', 'Yuge Yugeen Bharat Museum', 'New Delhi')]
    gal = '<div class="g3 gap-sm mt-3">' + ''.join(fig(A(f'06_PHOTOGRAPHY_ART_DIRECTION/Approved_Images/JPG/sanzeed-img-{s}.jpg', 900), t, p, None, plate='dark cover', h='h32') for s, t, p in imgs) + '</div>'
    P.append(page('03 · Positioning', head('3.2 · Pillars, proof and naming', 'Three pillars, four <span class="lit">numbers</span>.', 'All proof points are confirmed on sanzeed.com. Never round the numbers up, never invent a client or an award.') + body(f'<div class="split even"><div><div class="doc-h3">Brand pillars</div>{pillars}<div class="doc-h3 mt-4">Proof points</div>{proof}</div><div><div class="doc-h3">Naming rules</div>{naming}{gal}</div></div>')))
    return P

# ------------------------------------------------------------------ 04 Personality & voice summary
def ch04():
    P = []
    P.append(divider('04', 'Personality &amp; voice <span class="lit">summary</span>.', 'A museum’s wall label, written by the person who built the room. Precise, calm, first person, short. The full voice guide is chapter 24.',
        [('4.1', 'Personality and voice on one page')], '04 · Personality & voice'))
    traits = ''.join(f'<div><div class="ff-display mid" style="font-size:22pt">{t}<span class="lit">.</span></div><p class="sm mt-1">{d}</p></div>' for t, d in [
        ('Calm', 'Space, one accent, short sentences. Nothing shouts.'), ('Precise', 'Numbered steps, named deliverables, 001 counters, wall labels.'),
        ('Monumental', 'A large light serif, a single object on a dark field.'), ('Warm', 'Gold light, first person, “the first conversation is always free”.'),
        ('Curious', '“Every environment begins as a question.”')])
    voice = ('<div class="doc-h3">The voice in one line</div><p class="doc-quote" style="font-size:16pt">A museum’s wall label, written by the person who built the room.</p>'
             '<div class="doc-h3 mt-4">Seven principles</div>' + rules(['<b>First person, singular.</b> “I”, “me”, “my”. The brand is one person.',
             '<b>Short sentences, long ideas.</b> One thought per sentence. Let a full stop land.', '<b>Name the deliverable.</b> Say what the client receives, concretely.',
             '<b>Spatial vocabulary.</b> Rooms, routes, thresholds, galleries, light, dwell time, opening night.', '<b>End on the image.</b> Finish paragraphs on a picture, not a claim.',
             '<b>Plain numbers.</b> Numerals, no inflation. “90 projects, one continuous craft.”', '<b>Warm, not casual.</b> Hospitable; never slangy or jokey.'], cls='tight'))
    tests = ('<div class="callout mt-3"><b class="k">Three tests for any new copy.</b> 1 · Could this be read aloud, calmly, in a museum lobby? 2 · Does it name a room, a route, a light or a deliverable? 3 · Would deleting the adjectives make it stronger? If yes, delete them.</div>')
    P.append(page('04 · Personality & voice', head('4.1 · Personality and voice', 'Five traits, seven <span class="lit">principles</span>.', 'Archetype: the Creator tempered by the Sage. Use this page as the pre-flight check for any piece of writing or design.') + body(f'<div class="split even"><div><div class="g1 stack-lg" style="display:grid;gap:5mm">{traits}</div></div><div>{voice}{tests}</div></div>')))
    return P

# ------------------------------------------------------------------ 05 Logo system
FAMILY = [
    ('1', 'Primary logo', 'primary-wordmark', 'Wordmark with the two points of light. Default everywhere: website header, covers, social banners, signage.'),
    ('2', 'Secondary logo', 'secondary-symbol-wordmark', 'Symbol + wordmark, horizontal. Partner lockups, document footers, when the symbol needs introducing.'),
    ('3', 'Horizontal logo', 'horizontal-descriptor', 'Wordmark with the descriptor justified beneath. Stationery, proposals, invoices, press, anything formal.'),
    ('4', 'Vertical / stacked', 'vertical-stacked', 'Symbol, wordmark, descriptor centred. Square and centred layouts, end cards, stamps, ID cards.'),
    ('5', 'Symbol / icon', 'symbol', 'The S with its full stop (“S.”). Avatars, favicons, app icons, watermarks, pattern.'),
    ('6', 'Monogram', 'monogram', '“SM.” (Sanzeed Mirza). Seals, embossing, ID-card reverse, cufflink-scale uses.'),
    ('7', 'Wordmark (plain)', 'wordmark-plain', 'Letters without dots. Engraving, embroidery, single-tool cutting where a dot cannot be produced.'),
    ('8', 'Simplified / small-size', 'simplified-small-size', 'Heavier stroke (84), larger dots. 24–120 px on screen, 6–28 mm in print.'),
    ('9', 'Small-size symbol', 'symbol-small-size', 'Under 24 px / 6 mm.'),
]
def ch05():
    P = []
    P.append(divider('05', 'Logo <span class="lit">system</span>.', 'Eleven variants generated from one parametric master: a 500-unit cap height, a 64-unit monoline stroke and two 45-unit points of light.',
        [('5.1', 'The family · primary lockups'), ('5.2', 'The family · marks and small sizes'), ('5.3', 'Which logo where')], '05 · Logo system'))
    def tile(n, name, stem, use, h='h48', pad='pad'):
        return (f'<figure class="fig"><div class="plate dark {h} {pad}"><img src="{logo(stem, "full-colour-dark")}" alt="{esc(name)}"><span class="lbl">{n} · {esc(name)}</span></div>'
                f'<figcaption class="wall-label"><span class="title">{esc(name)}</span><span class="place">sanzeed-{stem}</span><span class="line">{esc(use)}</span></figcaption></figure>')
    top = '<div class="g2 gap-md">' + ''.join(tile(*FAMILY[i], h='h52') for i in range(4)) + '</div>'
    P.append(page('05 · Logo system', head('5.1 · The family — primary lockups', 'Four lockups for every <span class="lit">context</span>.', 'Shown in the full-colour-dark version on Gallery Black. Files: 02_LOGO_SYSTEM/SVG/sanzeed-&lt;variant&gt;--&lt;colour&gt;.svg, with PDF, EPS, PNG, JPG and WebP beside them.') + body(top)))
    marks = '<div class="g3 gap-md">' + ''.join(tile(*FAMILY[i], h='h38', pad='pad-lg' if FAMILY[i][2] in ('symbol', 'monogram', 'symbol-small-size') else 'pad') for i in range(4, 9)) + (
        f'<figure class="fig"><div class="plate dark h44" style="gap:4mm"><img src="{L(SVG+"sanzeed-symbol-tile--dark.svg")}" alt="Symbol tile dark" style="width:24%;height:auto"><img src="{L(SVG+"sanzeed-symbol-tile--light.svg")}" alt="Symbol tile light" style="width:24%;height:auto"><img src="{L(SVG+"sanzeed-symbol-tile--gold.svg")}" alt="Symbol tile gold" style="width:24%;height:auto"><span class="lbl">10 · Symbol tiles</span></div>'
        f'<figcaption class="wall-label"><span class="title">Symbol tile</span><span class="place">sanzeed-symbol-tile--dark / --light / --gold (+ -square)</span><span class="line">Rounded square and square tiles. Favicon, app icon, social profile image. The black symbol on the gold tile is the one permitted use of a logo on gold.</span></figcaption></figure>') + '</div>'
    sig = fig(L('02_LOGO_SYSTEM/Signature/sanzeed-signature--white.svg'), 'Signature mark', 'Signature/sanzeed-signature--{ink, white, gold, gold-light, black}', 'The personal layer: letters, thank-you cards, sign-offs. Never in place of the wordmark. See chapter 11.', plate='dark pad', h='h24')
    P.append(page('05 · Logo system', head('5.2 · The family — marks and small sizes', 'The symbol, the monogram and the small <span class="lit">sizes</span>.', 'Variants 5–11. Below 120 px / 28 mm the simplified wordmark replaces the primary; below 24 px / 6 mm the small-size symbol replaces the symbol.') + body(marks + '<div class="g3 gap-md mt-3">' + sig + '<div class="c2 callout" style="align-self:center"><b class="k">The gold dots are part of the logo.</b> In single-colour versions they take the ink colour. The travelling “beam dot” exists only in motion (chapter 23). The plain wordmark is for processes that cannot produce a dot — engraving, embroidery, single-tool cutting — and nowhere else.</div></div>')))
    where = table(['Context', 'Use this variant', 'Colour version', 'Minimum'], [
        ('Website header, social covers, presentation title', '<b>primary-wordmark</b>', 'full-colour-dark on dark · full-colour-light on light', '120 px / 28 mm'),
        ('Stationery header, document covers, signage, press', '<b>horizontal-descriptor</b> (or secondary-symbol-wordmark)', 'full-colour-light on Plaster · full-colour-dark on black', '220 px / 50 mm'),
        ('Square or centred compositions, end cards, stamps, ID cards', '<b>vertical-stacked</b>', 'per background', '90 px / 22 mm'),
        ('Avatars, favicons, app icons, watermarks, stamps', '<b>symbol</b> / <b>symbol-tile</b>', 'tile dark by default; light tile for light surfaces', '16 px / 6 mm'),
        ('Seals, embossing, ID-card reverse, pattern', '<b>monogram</b>', 'single ink', '16 px / 6 mm'),
        ('Engraving, embroidery, single-tool cutting', '<b>wordmark-plain</b>', 'black or white', '28 mm'),
        ('Below 120 px / 28 mm wide', '<b>simplified-small-size</b>', 'per background', '24 px / 6 mm'),
        ('Below 24 px', '<b>symbol-small-size</b>', 'per background', '12 px'),
        ('Letters, thank-you cards, personal sign-offs', '<b>signature</b>', 'ink on light · white on dark · gold for foil', '160 px / 32 mm')], widths=['auto', '56mm', '70mm', '26mm'])
    ex = '<div class="g4 gap-sm mt-3">' + ''.join(fig(A(s, 1000), t, p, None, plate=pl, h='h30') for s, t, p, pl in [
        ('16_WEBSITE_IMPLEMENTATION/screenshots/after-index-desktop-header-2x.png', 'Website header', 'primary-wordmark, 129 px wide', 'dark pad-sm'),
        ('09_PRINT_STATIONERY/Letterheads/sanzeed-letterhead--a4-first.png', 'Letterhead', 'horizontal-descriptor, 56 mm, top-left', 'plaster top'),
        ('09_PRINT_STATIONERY/ID_Card/sanzeed-id-card--back.png', 'ID card reverse', 'monogram, 16 mm', 'night cover'),
        ('02_LOGO_SYSTEM/Social_Profile/universal-profile-1024--dark-circle-preview.png', 'Profile image', 'symbol tile, circle-cropped by the platform', 'charcoal pad-sm')]).replace('h30', 'h26') + '</div>'
    P.append(page('05 · Logo system', head('5.3 · Which logo where', 'The right variant for the <span class="lit">surface</span>.', 'Brand kit rule 1. When in doubt: primary wordmark on screens, horizontal-descriptor on paper, the symbol wherever the space is square.') + body(where + ex)))
    return P

# ------------------------------------------------------------------ 06 Construction
def ch06():
    P = []
    P.append(divider('06', 'Logo <span class="lit">construction</span>.', 'The wordmark is not typeset; it is drawn. Every stroke is generated from a handful of parameters in one Python master, so the geometry is exact in every export.',
        [('6.1', 'Geometry on the 64-unit grid'), ('6.2', 'Parameters and the master file')], '06 · Logo construction'))
    cons = A('02_LOGO_SYSTEM/Guidelines/logo-construction.png', 2400)
    params = table(['Parameter', 'Value', 'What it sets'], [
        ('CAP', '<span class="tnum">500</span>', 'Cap height; the unit everything else is measured against'),
        ('W', '<span class="tnum">64</span>', 'Monoline stroke weight (the grid shown)'),
        ('DOT_R', '<span class="tnum">45</span>', 'Radius of the points of light (0.7 × stroke)'),
        ('S_R · S_D', '<span class="tnum">96 · 192</span>', 'S hook centreline radius; offset between the two hooks (they pass with a 20-unit gap)'),
        ('A_W · N_W · Z_W', '<span class="tnum">560 · 460 · 470</span>', 'A outer width (apex pointed) · N arch width (half-circle) · Z width (vertical-cut diagonal)'),
        ('E_W · D_W', '<span class="tnum">324 · 380</span>', 'E as three detached beams · D built on a half-circle, stem broken 14 units around the point'),
        ('Gaps', '<span class="tnum">S–A 88 · A–N 64 · N–Z 104 · Z–E 118 · E–E 132 · E–D 118</span>', 'Letter spacing in units; never altered'),
        ('Points', '<span class="tnum">A: 88 above baseline · D: mid-height</span>', 'The two points sit on the baseline grid, inside the A and in the stem of the D'),
        ('Descriptor', 'Inter Tight 600, outlined', '“EXPERIENTIAL DESIGN CONSULTANT”, justified to the wordmark width in the lockups'),
        ('Simplified', '<span class="tnum">stroke 84</span>', 'Small-size variant: heavier stroke, larger dots, same construction')], cls='xs', widths=['30mm', '46mm', 'auto'])
    src = ('<div class="callout mt-3"><b class="k">The master.</b> <span class="mono">15_SOURCE_FILES/Project_Files/logo-builder/build_logo.py</span> writes the per-stroke construction SVGs (<span class="mono">02_LOGO_SYSTEM/Source_Files/</span>, every stroke a named sub-path); <span class="mono">export_logo.py</span> unions them with Inkscape and writes SVG, PDF, EPS, PNG, JPG, WebP, favicons and social tiles. Change a parameter, re-run, and the whole family regenerates. Never redraw a letter by hand.</div>')
    P.append(page('06 · Logo construction', head('6.1 · Geometry', 'Drawn on a 64-unit <span class="lit">grid</span>.', 'The construction sheet from 02_LOGO_SYSTEM/Guidelines. Cap height 500; stroke 64; point of light r 45; S hooks r 96; N and D on half-circles; E as three detached beams; Z with a vertical-cut diagonal.') + body(fig(cons, 'Construction', 'Geometry of the wordmark on the 64-unit stroke grid', None, plate='night cover', h='h46') + f'<div class="split mt-2" style="grid-template-columns:1fr 92mm">{params}{src}</div>')))
    return P

# ------------------------------------------------------------------ 07 Colour versions
COLOURWAYS = [
    ('full-colour-dark', 'Full colour · dark', 'dark', 'Gallery White letters, Lamp Gold points. Gallery Black, Night, Charcoal, dark photography. The default on screen.'),
    ('full-colour-light', 'Full colour · light', 'plaster', 'Soot letters, Old Gold points. Plaster, Paper, Stone, white. Documents and print.'),
    ('black', 'Black', 'white', '100 K. Single-ink print, fax, engraving, the gold tile.'),
    ('white', 'White', 'night', 'Reversed out of dark photography or a solid dark colour; cut vinyl.'),
    ('grayscale', 'Grayscale', 'plaster', 'Black letters, 55 % grey points. Mono print on light.'),
    ('grayscale-inverted', 'Grayscale · inverted', 'dark', 'White letters, 55 % grey points. Mono print on dark.'),
    ('single-colour-gold', 'Single colour · gold', 'plaster', 'Old Gold letters and points. Spot colour, foil, metallic Pantone 871 C / 872 C (verify).'),
]
def ch07():
    P = []
    P.append(divider('07', 'Logo variations &amp; colour <span class="lit">versions</span>.', 'Seven colourways of every variant, each with the background it belongs on. The pairing is a rule, not a preference.',
        [('7.1', 'The seven colourways'), ('7.2', 'Pairing matrix and the tiles')], '07 · Colour versions'))
    tiles = '<div class="g4 gap-md">' + ''.join(
        f'<figure class="fig"><div class="plate {pl} h40 pad"><img src="{logo("primary-wordmark", stem)}" alt="{esc(name)}"><span class="lbl">--{stem}</span></div><figcaption class="wall-label"><span class="title">{esc(name)}</span><span class="line">{esc(use)}</span></figcaption></figure>'
        for stem, name, pl, use in COLOURWAYS) + (
        f'<figure class="fig"><div class="plate gold h40 pad"><img src="{logo("primary-wordmark", "black")}" alt="Black on gold"><span class="lbl">black on the gold tile</span></div><figcaption class="wall-label"><span class="title">The one exception</span><span class="line">Gold is never a background for the logo — except the black logo on the gold tile.</span></figcaption></figure>') + '</div>'
    P.append(page('07 · Colour versions', head('7.1 · The seven colourways', 'Seven inks, each on its own <span class="lit">ground</span>.', 'Every variant 1–9 exists in all seven. File suffix --&lt;colour&gt; in 02_LOGO_SYSTEM/SVG and the convenience sets Full_Color / Black / White / Grayscale / Single_Color.') + body(tiles)))
    matrix = table(['Background', 'Use', 'Never'], [
        ('<span class="swatch" style="background:#000"></span>Gallery Black · Night · Charcoal · dark photography (≥ 80 % black under the logo)', '<b>full-colour-dark</b> (or white; grayscale-inverted for mono)', 'full-colour-light, black, grayscale'),
        ('<span class="swatch" style="background:#F5F0E7"></span>Plaster · Paper · Stone · white', '<b>full-colour-light</b> (or black; grayscale for mono)', 'full-colour-dark, white, grayscale-inverted'),
        ('<span class="swatch" style="background:#B8863B"></span>Old Gold tile', '<b>black</b> symbol or wordmark only', 'any full-colour version, white, gold'),
        ('Single-ink print, engraving, stamps', '<b>black</b> or <b>single-colour-gold</b>', 'grayscale (tints do not engrave)'),
        ('Photography', 'full-colour-dark on the veil (≥ 80 % black) or white', 'any logo on busy or light imagery; never on gold or on gradients other than dusk / lamp')], widths=['auto', '64mm', '60mm'])
    tl = '<div class="g3 gap-sm">' + ''.join(fig(L(SVG + f'sanzeed-symbol-tile--{c}.svg'), f'Symbol tile · {c}', 'sanzeed-symbol-tile--' + c, None, plate=pl + ' pad-sm', h='h34') for c, pl in [('dark', 'charcoal'), ('light', 'stone'), ('gold', 'plaster')]) + '</div>'
    tl += '<div class="g3 gap-sm mt-3">' + ''.join(fig(L(SVG + f'sanzeed-symbol-tile-square--{c}.svg'), f'Square tile · {c}', 'sanzeed-symbol-tile-square--' + c, None, plate=pl + ' pad-sm', h='h30') for c, pl in [('dark', 'charcoal'), ('light', 'stone'), ('gold', 'plaster')]) + '</div>'
    P.append(page('07 · Colour versions', head('7.2 · Pairing matrix and the tiles', 'Dark on dark, light on <span class="lit">light</span>.', 'Brand kit rule 2. The tiles carry their own background and are used as delivered: dark by default, light for light interfaces, gold only where a single gold object is wanted.') + body(f'<div class="split even"><div>{matrix}<p class="sm mt-3 muted">Hairlines next to the logo are white at 10 % on dark and Soot at 10 % on light. Nothing else sits inside the clear space (chapter 08).</p></div><div>{tl}</div></div>')))
    return P

# ------------------------------------------------------------------ 08 Clear space & placement
def ch08():
    P = []
    P.append(divider('08', 'Clear space &amp; <span class="lit">placement</span>.', 'x = half the cap height of the logo in use, on all sides. Nothing enters it: no text, no edge, no other logo, no photographic detail.',
        [('8.1', 'Clear space'), ('8.2', 'Placement')], '08 · Clear space & placement'))
    cs = A('02_LOGO_SYSTEM/Guidelines/logo-clear-space.png', 2000)
    txt = ('<p><b class="k">The measure.</b> x is half the height of the wordmark’s capitals in the lockup you are using. For the symbol on its own, x is a quarter of its height. For the stacked lockup, x is measured from the wordmark inside it.</p>'
           '<p class="mt-2"><b class="k">What may not enter.</b> Text, rules, edges of the page or screen, other logos, partner marks, photographic detail, pattern above 12 %.</p>'
           '<p class="mt-2"><b class="k">What may.</b> Flat brand colour, the lamp glow, the veil, grain. The glow in motion stays inside the clear space.</p>'
           '<p class="mt-2"><b class="k">Margins.</b> On documents the lockup sits at the 20 mm margin; the clear space is then automatically satisfied for a 56 mm lockup. On screens the nav wordmark at 18 px cap height carries 9 px of clear space built into its padding.</p>')
    P.append(page('08 · Clear space & placement', head('8.1 · Clear space', 'Half the cap height, all <span class="lit">round</span>.', 'The clear-space sheet from 02_LOGO_SYSTEM/Guidelines, drawn for the primary wordmark, the horizontal-descriptor lockup, the vertical stack and the symbol.') + body(f'<div class="split">{"<div>"+txt+"</div>"}{fig(cs, "Clear space", "02_LOGO_SYSTEM/Guidelines/logo-clear-space.svg / .png", None, plate="night cover", h="h118")}</div>')))
    pl = A('02_LOGO_SYSTEM/Guidelines/logo-placement.png', 2400)
    txt = rules(['<b>Top-left or centred.</b> The logo anchors a composition from the top-left (documents, website, social banners) or from the centre (covers, end cards, square tiles). Never bottom-right unless it is the sign-off on a cover, where it may sit bottom-left or centred with the lamp behind.',
                 '<b>Documents.</b> The horizontal-descriptor lockup sits top-left at the 20 mm margin, 56 mm wide on A4; continuation pages carry the primary wordmark at 30 mm.',
                 '<b>Covers.</b> The primary wordmark sits bottom-left or centred with the lamp glow behind it; the title sits above, never beside.',
                 '<b>Photography.</b> The logo sits on the darkest third, under the veil, on ≥ 80 % black. Measure it; do not guess.',
                 '<b>With partners.</b> Equal cap height, separated by a hairline with 2x between marks; Sanzeed’s mark first when host, last when guest.',
                 '<b>Signage.</b> Centre line 1500 mm above finished floor for door plates; the wordmark centre 1700 mm on backdrops.'], cls='tight')
    P.append(page('08 · Clear space & placement', head('8.2 · Placement', 'Top-left, or <span class="lit">centred</span>.', 'The placement sheet shows the approved positions on a document, a slide, a social post and a cover.') + body(f'<div class="split">{"<div>"+txt+"</div>"}{fig(pl, "Placement", "02_LOGO_SYSTEM/Guidelines/logo-placement.svg / .png", None, plate="night cover", h="h118")}</div>')))
    return P

# ------------------------------------------------------------------ 09 Minimum sizes
def ch09():
    P = []
    P.append(divider('09', 'Minimum <span class="lit">sizes</span>.', 'Below the minimum, switch variant rather than shrink: the simplified wordmark below 120 px / 28 mm, the small-size symbol below 24 px / 6 mm.',
        [('9.1', 'Minimum sizes, at actual size')], '09 · Minimum sizes'))
    ms = A('02_LOGO_SYSTEM/Guidelines/logo-minimum-sizes@2x.png', 2000)
    t = table(['Variant', 'Screen', 'Print', 'Below that'], [
        ('Primary wordmark', '<span class="tnum">120 px</span>', '<span class="tnum">28 mm</span>', 'simplified-small-size'),
        ('Horizontal-descriptor lockup', '<span class="tnum">220 px</span>', '<span class="tnum">50 mm</span>', 'primary wordmark (drop the descriptor)'),
        ('Vertical stack', '<span class="tnum">90 px</span>', '<span class="tnum">22 mm</span>', 'symbol'),
        ('Symbol', '<span class="tnum">16 px</span>', '<span class="tnum">6 mm</span>', 'symbol-small-size (to 12 px)'),
        ('Simplified wordmark', '<span class="tnum">24 px</span>', '<span class="tnum">6 mm</span>', 'symbol'),
        ('Signature', '<span class="tnum">160 px</span>', '<span class="tnum">32 mm</span>', 'do not use')], widths=['auto', '18mm', '18mm', 'auto'])
    actual = ('<div class="doc-h3 mt-4">At actual size on this page</div><p class="xs muted">Printed at 100 % these are the physical minimums.</p>'
              f'<div class="mt-2" style="display:flex;flex-direction:column;gap:3.5mm;align-items:flex-start">'
              f'<div style="display:flex;align-items:center;gap:4mm"><img src="{logo("primary-wordmark","full-colour-light")}" style="width:28mm" alt="wordmark 28 mm"><span class="xs faint tnum">28 mm · primary wordmark</span></div>'
              f'<div style="display:flex;align-items:center;gap:4mm"><img src="{logo("horizontal-descriptor","full-colour-light")}" style="width:50mm" alt="lockup 50 mm"><span class="xs faint tnum">50 mm · horizontal-descriptor</span></div>'
              f'<div style="display:flex;align-items:center;gap:4mm"><img src="{logo("vertical-stacked","full-colour-light")}" style="width:22mm" alt="stack 22 mm"><span class="xs faint tnum">22 mm · vertical stack</span></div>'
              f'<div style="display:flex;align-items:center;gap:4mm"><img src="{logo("symbol","full-colour-light")}" style="width:6mm" alt="symbol 6 mm"><img src="{logo("symbol-small-size","full-colour-light")}" style="width:4mm" alt="small symbol"><span class="xs faint tnum">6 mm · symbol · 4 mm small-size symbol</span></div>'
              f'<div style="display:flex;align-items:center;gap:4mm"><img src="{logo("simplified-small-size","full-colour-light")}" style="width:20mm" alt="simplified 20 mm"><span class="xs faint tnum">20 mm · simplified small-size wordmark</span></div></div>')
    P.append(page('09 · Minimum sizes', head('9.1 · Minimum sizes', 'Switch variant, never <span class="lit">shrink</span>.', 'Brand kit rule 4. The sheet from 02_LOGO_SYSTEM/Guidelines shows each variant at its minimum with the small-size versions beside it.') + body(f'<div class="split" style="grid-template-columns:96mm 1fr">{"<div>"+t+actual+"</div>"}{fig(ms, "Minimum sizes", "02_LOGO_SYSTEM/Guidelines/logo-minimum-sizes.svg / @2x.png", None, plate="night cover", h="h130")}</div>')))
    return P

# ------------------------------------------------------------------ 10 Incorrect usage
def ch10():
    P = []
    P.append(divider('10', 'Incorrect <span class="lit">usage</span>.', 'Twelve things never done to the logo. If a layout needs any of them, the layout is wrong, not the logo.',
        [('10.1', 'The twelve')], '10 · Incorrect usage'))
    iu = A('02_LOGO_SYSTEM/Guidelines/logo-incorrect-usage.png', 2000)
    nevers = rules(['<b>Do not stretch or squash.</b> Scale uniformly only.', '<b>Do not rotate.</b> Horizontal, always; the stacked lockup for vertical spaces.',
                    '<b>Do not outline.</b> The letters are solid; the stroke is the drawing, not a border.', '<b>Do not add shadows, bevels, glows or effects</b> to the letters. Only the points may glow, and only in motion.',
                    '<b>Do not recolour the points of light.</b> Gold, or the ink of a single-colour version.', '<b>Do not typeset the name</b> instead of the wordmark, in any typeface.',
                    '<b>Do not use the light version on dark</b>, or', '<b>the dark version on light.</b>', '<b>Do not place on busy photography</b> without the veil.',
                    '<b>Do not place the full-colour logo on gold.</b>', '<b>Do not fill with gradients</b>, textures or imagery.', '<b>Do not crop the wordmark</b> or the S.'], cls='tight')
    also = '<p class="sm mt-3 muted">Also never: change the letter spacing, pair with the old raster signature, set the descriptor in another font or case, animate the letters by stroke-drawing or particles, or redraw any letter by hand.</p>'
    P.append(page('10 · Incorrect usage', head('10.1 · The twelve', 'Twelve ways to break <span class="lit">it</span>.', 'The sheet from 02_LOGO_SYSTEM/Guidelines; each tile shows the error on the background where it is most tempting.') + body(f'<div class="split" style="grid-template-columns:86mm 1fr">{"<div>"+nevers+also+"</div>"}{fig(iu, "Incorrect usage", "02_LOGO_SYSTEM/Guidelines/logo-incorrect-usage.svg / .png", None, plate="night cover", h="h140")}</div>')))
    return P

# ------------------------------------------------------------------ 11 Signature mark and monogram
def ch11():
    P = []
    P.append(divider('11', 'Signature mark and <span class="lit">monogram</span>.', 'The personal layer and the seal. The signature is Sanzeed’s hand; the monogram is the mark at cufflink scale.',
        [('11.1', 'The signature mark'), ('11.2', 'The monogram')], '11 · Signature & monogram'))
    sigs = [('ink', 'plaster', 'Ink #1A1816 · letters, thank-you cards, certificates on Plaster/Paper'), ('white', 'dark', 'White #F5F5F7 · website case-study sign-off, video end card'),
            ('gold', 'plaster', 'Gold #B8863B · foil or spot gold on light stock'), ('gold-light', 'dark', 'Gold light #E9B25A · gold on dark backgrounds'), ('black', 'white', 'Black #000000 · single-colour print')]
    g = '<div class="g5 gap-sm">' + ''.join(fig(L(f'02_LOGO_SYSTEM/Signature/sanzeed-signature--{c}.svg'), f'--{c}', None, use, plate=pl + ' pad', h='h34') for c, pl, use in sigs) + '</div>'
    rulesx = rules(['<b>Personal, not institutional.</b> Letters, thank-you cards, sign-offs, the end of a case study. Never on invoices, proposals, signage or in place of the wordmark.',
                    '<b>Minimum 32 mm in print, 160 px on screen.</b> Below that the flourish closes up.', '<b>Keep the flourish underline.</b> Never recolour parts of it, never separate the dot.',
                    '<b>Vector only.</b> The traced SVG/PDF/EPS from 02_LOGO_SYSTEM/Signature; the original raster signature is retired.', '<b>Sign-off form.</b> “— Sanzeed Mirza” under quotes; the signature mark alone reads “Sanzeed.”'], cls='tight')
    ty = A('09_PRINT_STATIONERY/Thank_You_Cards/sanzeed-thank-you-card--folded-inside.png', 1200)
    ex = fig(ty, 'Thank-you card, inside', 'A6 folded · 09_PRINT_STATIONERY/Thank_You_Cards', 'The signature mark 40 mm wide with the name line beneath — its canonical use.', plate='plaster cover', h='h52')
    P.append(page('11 · Signature & monogram', head('11.1 · The signature mark', 'The personal <span class="lit">layer</span>.', 'Hand-lettered “Sanzeed.” vectorised from the original artwork (potrace, 300 dpi, editable Béziers). Five colours, 02_LOGO_SYSTEM/Signature.') + body(g + f'<div class="split mt-4" style="grid-template-columns:1fr 96mm"><div>{rulesx}</div>{ex}</div>')))
    mono = '<div class="g4 gap-sm">' + ''.join(fig(logo('monogram', c), f'--{c}', None, None, plate=pl + ' pad-lg', h='h36') for c, pl in [('full-colour-dark', 'dark'), ('full-colour-light', 'plaster'), ('black', 'white'), ('single-colour-gold', 'plaster')]) + '</div>'
    uses = rules(['<b>Seals and embossing.</b> Blind deboss or foil on card stock, wax-seal scale.', '<b>ID-card reverse.</b> 16 mm, with the QR code and contact lines (09_PRINT_STATIONERY/ID_Card).',
                  '<b>Pattern.</b> The monogram-repeat tile at ≤ 12 % opacity (05_GRAPHIC_ASSETS/Patterns).', '<b>Never as the primary mark.</b> The monogram does not replace the symbol on avatars or favicons; it is the mark where “SM.” is read as initials.'], cls='tight')
    idb = A('09_PRINT_STATIONERY/ID_Card/sanzeed-id-card--back.png', 900)
    pat = A('05_GRAPHIC_ASSETS/Patterns/png/sanzeed-pattern-monogram-repeat--light-2048.png', 1024)
    ex = '<div class="g2 gap-sm">' + fig(idb, 'ID card, reverse', 'CR80 · monogram 16 mm', None, plate='night cover', h='h60') + fig(pat, 'Monogram repeat', 'Pattern tile, light ink, shown at full strength', None, plate='plaster cover', h='h60') + '</div>'
    P.append(page('11 · Signature & monogram', head('11.2 · The monogram', 'SM<span class="lit">.</span> — the seal.', 'Sanzeed Mirza’s initials in the construction of the wordmark, with the point as the full stop. Seven colourways like every other variant.') + body(mono + f'<div class="split mt-4"><div>{uses}</div>{ex}</div>')))
    return P

def back():
    wm = L('02_LOGO_SYSTEM/SVG/sanzeed-primary-wordmark--full-colour-dark.svg')
    inner = (f'<div class="cover-top"><span class="eyebrow">Sanzeed Mirza · Experiential Design Consultant</span><span class="cover-meta" style="color:#808086">Brand Guidelines · Version 1.0 · November 2026</span></div>'
             f'<div><p class="doc-quote">A brief on one side. A visitor on the other. Sanzeed carries the light <span class="lit">across</span>.</p>'
             f'<p class="sm mt-4" style="color:#A1A1A6;max-width:150mm">Prepared by the agency from an audit of sanzeed.com, 5 November 2026. Every rule in this manual is derived from the identity as it lives on the site; every asset shown is the delivered file. Questions about the system go to the person who owns it.</p></div>'
             f'<div class="cover-foot"><div class="wordmark" style="width:64mm"><img src="{wm}" alt="Sanzeed"></div><span class="cover-meta" style="color:#808086">{esc(CONTACT)}</span></div>')
    return page('Back cover', inner, cls='back theme-dark no-footer')
