# Brand Audit — sanzeed.com

**Prepared:** 5 November 2026 · **Subject:** Sanzeed Mirza, Experiential Design Consultant · **Source of truth:** the live website at https://sanzeed.com (fetched 5 Nov 2026, last modified 21 Oct 2026 per sitemap), its three case-study pages, its vCard, JSON-LD, favicon and inline CSS/JS.

This audit separates **confirmed facts** (taken verbatim or directly measured from the site) from **assumptions and recommendations** (the agency's reading). Nothing in the "confirmed" column was invented.

---

## 1. Confirmed facts

### 1.1 Identity and business
| Item | Evidence |
|---|---|
| Brand name | **Sanzeed** (wordmark), **Sanzeed Mirza** (full name, JSON-LD `Person`) |
| Descriptor | **Experiential Design Consultant** (title tag, JSON-LD `jobTitle`, vCard `TITLE`) |
| Status | Independent consultant since **Aug 2026** ("Experiential Design Consultant · Independent Consultant · Aug 2026 — Present") |
| Location | **New Delhi, India** (JSON-LD address, vCard, footer "Studio New Delhi") |
| Contact | sanzeed@gmail.com · +91 7827051270 (call and WhatsApp) · linkedin.com/in/sanzeed · sanzeed-mirza.vcf |
| Headline | "Experiential design you can walk into." (H1, OG image alt) |
| Short line | "Vision you can walk into." (footer) |
| Positioning sentence | "A visual storyteller drawn to the pursuit of distinct, impactful experiences — those that challenge convention and connect deeply with audiences." |
| About | "I'm an experiential design consultant based in New Delhi, working with institutions and brands wherever the project is. Fifteen years in: first as a concept artist and VFX lead on films and animation, then eight years directing museums, experience centres, pavilions and shows. I lead the whole room — story, space, graphics, media and the team that builds it. The work I want to make is calm to run and impossible to forget once you have walked through it." |
| Proof numbers | 15+ years of experience · 8+ years experiential & museum · 90+ projects directed · 60+ museums & centres |
| Trust line | "Trusted by PwC, Microsoft, Discovery and National Museums, from concept to public unveiling." |
| Three pillars | i. Strategic Vision · ii. Immersive Craft · iii. Calm Leadership |
| Personal quote | "The most powerful stories aren't just told — they're felt, lived, and remembered through the spaces we design and the moments we shape." |
| Commercial promises | "Available for new projects and collaborations. The first conversation is always free." · "I reply within two working days." · "If it is urgent, WhatsApp is fastest." |
| Rights notice | "Employee work for Tagbin, Sociopixel, DWS and B2W; rights remain with those companies." |

### 1.2 Services (seven, as listed)
1. Experiential Design & Creative Direction — "One vision from brief to opening night: narrative, space, media and the team that builds it." (as in Prime Minister Museum)
2. Museum & Cultural Exhibition Planning — "Galleries planned as a route, not a floor plan." (Yuge Yugeen Bharat Museum)
3. Immersive Storytelling & Narrative Architecture — "The script comes first." (Ram Katha Show)
4. Spatial Experience & Environmental Branding — "Brands you can stand inside." (India Pavilion Expo 2025)
5. Event Production & Brand Activation — "Shows, launches and tableaux where light and timing do the talking." (G20 Tree Show)
6. Digital ↔ Physical Experience Integration — "Projection, AR and VR, sensors and data brought into real rooms and real crowds." (Viratswaroop Kinetic Projection)
7. Cross-Functional Leadership & Mentorship — "Designers, writers, architects, producers and technologists moved toward one outcome, calmly." (Buddha Park)

Closing line: "All seven, every time. Every room needs the whole list, held in one hand. That is the job, and the pleasure of it."

### 1.3 Method (four steps, with stated deliverables)
| Step | Promise | "You receive" |
|---|---|---|
| 01 Discover | Immersion in the subject until the central story reveals itself | a research deck and the one central story |
| 02 Direct | A unifying creative vision that aligns designers, architects, writers, producers and technologists | a concept book and a walkthrough film |
| 03 Craft | Space, light, motion and interaction composed into environments | detail drawings, media scripts and a prototype room |
| 04 Deliver | Concept to launch — on scale, on story, on time | a built, tested and opened experience |

### 1.4 Career timeline
| Dates | Role | Organisation |
|---|---|---|
| Aug 2026 – present | Experiential Design Consultant | Independent |
| Jun 2018 – Jul 2026 | Creative Director | Tagbin |
| Apr 2018 – May 2018 | Creative Head | Digital Web Solutions |
| Feb 2017 – Mar 2018 | Creative Director | SocioPixels |
| Sep 2011 – Dec 2016 | Lead Concept Artist | Broadcast2world |
| Sep 2011 – Dec 2016 (in parallel) | VFX Artist | Prime Focus |

### 1.5 Portfolio
- 90 projects in three galleries: **Museums & Experience Centres (60)**, **Projection Mapping & Shows (15)**, **Explainer Videos & Others (15)**.
- Featured "Now showing" set: Prime Minister Museum (New Delhi), Buddha Park (Uttarakhand), India Pavilion Expo 2025 (concept), Yuge Yugeen Bharat Museum (New Delhi), Tribal Museum (New Delhi), RBI Museum Interior (Mumbai), Ram Katha Show (Ayodhya), G20 Tree Show (New Delhi).
- Three written case studies: Prime Minister Museum, Ram Katha Show, Buddha Park, each structured as The brief · The idea · Inside (8 images, numbered 001–008) · The walk · What visitors do · The film · Type / Location / Role.
- Geography: predominantly India (New Delhi, Uttar Pradesh, Uttarakhand, Gujarat, Maharashtra, Punjab, Bihar, Karnataka, Tamil Nadu, Rajasthan, Madhya Pradesh, Goa, Kashmir, Kolkata) plus Abu Dhabi and Dubai.
- Enquiry form: project type (museum or experience centre · pavilion or exhibition · show, launch or event · projection or light show · something else), timeline, budget band (Under ₹25 lakh → Over ₹5 crore).

### 1.6 Existing visual identity (measured)
| Element | Finding |
|---|---|
| Wordmark | Custom geometric uppercase **SANZEED** as inline SVG (viewBox 3729×561, cap height 500 units, stroke ≈ 64 units). Letterforms: S built from two arcs; A as a crossbar-less triangle; N as an arch; Z; two open three-bar E's; D as a half-round. Two static gold dots (inside the A at its base, inside the D's counter) and an animated gold "beam dot" that travels across the mark with a glow. Fill follows `--fg`, dots follow `--accent`. |
| Symbol / favicon | `favicon.svg`: a dark rounded square (#1d1d1f, radius 14.1/64) carrying the S (two arcs, #f5f5f7) and a gold dot (#e9b25a) at lower right. Also PNG 64 px and 180 px apple-touch-icon embedded as data URIs. |
| Signature | Hand-lettered script "Sanzeed." with a flourish underline, shipped as `signature-dark.png` / `signature-light.png` (raster only, used on case-study pages). |
| Hero object | Real-time three.js scene: black glass sphere with a gold orbit ring on a dark plinth, surrounded by gold and black particle "lights"; WebP poster fallbacks (`poster-dark.webp`, `poster-light.webp`, 1600×900). |
| Colour — dark theme (default) | bg #000000 · bg2 #0d0d0f · card #1c1c1e · card2 #2a2a2d · fg #f5f5f7 · fg2 #a1a1a6 · fg3 #808086 · accent #e9b25a · accent2 #f4c97a · lines rgba(255,255,255,.10/.06) |
| Colour — light theme | bg #f5f0e7 · bg2/card #fbf8f2 · card2 #ece7dc · fg #1a1816 · fg2 #665f55 · fg3 #6d665c · accent #b8863b · accent2 #d9a64a · accent-text #8a6124 · lines rgba(40,30,10,.10/.055) |
| Functional colour | error #c0392b only; no success/warning/info defined |
| Typography | `--serif` Fraunces 300 + 300 italic (display headings, stats, pull quote) · `--display` Inter Tight 400–800 (UI headings) · `--text` Inter 400–600 (body). All three are Google Fonts under the SIL Open Font License, embedded as data-URI woff2/woff. |
| Shape language | Radius 28 px (cards) and 20 px (small), fully rounded pill buttons, glass header (`--glass`), thin 1 px hairlines, 16:9 project cards (960×540). |
| Motion | Easing `cubic-bezier(.22,.8,.2,1)`, base duration .4 s, dot pulse 1.1 s, dot idle 6 s loop, line-by-line heading reveal, scroll-pinned Method section that fades steps in sequence. |
| Editorial devices | Gold eyebrow labels in small caps (NOW SHOWING, METHOD, ABOUT, JOURNEY, GET IN TOUCH); last word of headings set in muted grey or gold ("Eight rooms, **lit.**"); three-digit counters "001"; museum vocabulary ("wall label", "visitor's book", "the room", "galleries"). |
| Portrait | One portrait on the About section: subject in black shirt and glasses, night bokeh lights behind, warm key light. |
| Tech stack | Static HTML on **Netlify** (headers), single 1.3 MB `index.html` with inline CSS (244 KB) and JS (≈ 0.9 MB incl. three.js module), `data-theme` dark/light toggle, GoatCounter analytics, Netlify-style enquiry form, `/work/*.html` case pages, `/img/*.webp` (960×540) and `/img/case/*.webp`, sitemap.xml, robots.txt, vCard. No web manifest, no `favicon.ico`, no PWA icons, no `og.jpg` variants per page. |

---

## 2. Strengths (evidence-based)
1. **A real idea, already in the copy.** "Between two points of light. A brief on one side, a visitor on the other. Seven ways to carry the light across." The gold dot, the travelling beam and the word "lit." all serve this one idea. Few consultancies have a conceptual core this clear.
2. **Premium restraint.** Black, cream and a single gold accent; a light serif for display; generous space. It reads like an institution, which matches the clientele (ministries, national museums).
3. **Voice with a point of view.** First person, short declaratives, spatial metaphors, specific deliverables ("You receive a concept book and a walkthrough film"). It is confident without hype.
4. **Proof at scale.** 90 catalogued projects, three deep case studies, a 15-year timeline, named institutions.
5. **Working dark/light system** already tokenised in CSS custom properties — a head start for a full design-token system.

## 3. Weaknesses and gaps (evidence-based)
1. **Wordmark is hand-traced, not constructed.** Node data is jittery; stroke weight drifts between letters (S heavier than the E bars); the arch-N can be read as a second A ("SAΛZEED") at small sizes. There is no vertical/stacked lockup, no monogram, no clear-space or minimum-size rule, no black/white/grayscale set, and no print format at all.
2. **The symbol exists only as a 64-px favicon.** The S-and-dot has no formal construction, no standalone colour versions, no social-profile version, no app-icon set.
3. **The signature is raster only** — unusable for print at size and inconsistent with the vector system.
4. **Colour has no production values** (no CMYK, no Pantone guidance) and no functional palette beyond one red.
5. **Typography has no documented scale**; sizes are ad hoc `clamp()` values in CSS.
6. **No application system**: nothing exists for social media, stationery, documents, presentations, motion exports, signage or print.
7. **Digital hygiene gaps:** missing `favicon.ico`, web manifest and maskable PWA icons; single OG image for every page; `apple-touch-icon` inlined as base64 rather than served as a file; 1.3 MB HTML because fonts and icons are inlined.
8. **Brand naming is split** between "Sanzeed" (mark) and "Sanzeed Mirza" (SEO, OG, legal). This is fine, but it needs a rule.

## 4. Opportunities
- Codify the existing idea into a complete, ownable system — "the point of light" — instead of inventing a new one. Equity is preserved; recognition compounds.
- Clean the existing wordmark (smooth edges, straight lines, exact bars) so it survives embroidery, engraving, 16-px favicons and 10-m signage without losing its hand-drawn character.
- Promote the S-and-dot to a true brand mark, and derive a monogram, app icons and social avatars from it.
- Vectorise the signature as the "personal" layer (letters, thank-you cards, certificates) distinct from the "institutional" layer (wordmark, stationery).
- Build a token-driven website design system so the live site, documents and templates share one source of truth.
- Use the client's own project photography (owned or credited work) as the image library — no stock.

## 5. Assumptions and open questions (not confirmed by the site)
| Topic | Assumption used in this package | To confirm with Sanzeed |
|---|---|---|
| Legal entity | Sole proprietor trading as "Sanzeed Mirza"; no registered company name, GSTIN or address beyond "New Delhi" | Registered name, GSTIN, PAN, postal address and bank details for invoice/quotation templates (left as fillable fields) |
| Audience | Government ministries and cultural institutions, museum authorities, corporate experience-centre owners, event and exhibition agencies, architects and fabricators who need a creative lead | Confirm priority segments and any sectors to avoid |
| Pricing | Budget bands from the enquiry form imply projects from ₹25 lakh to ₹5 crore+ | Confirm whether day-rate consulting is also offered |
| Competitors | Indian experiential studios (including the former employer Tagbin), international museum-design practices | Confirm whom the client is most often compared with in pitches |
| Image rights | Project images shown on the site are used here as "approved imagery"; the site itself states rights remain with the former employers | Confirm which images may appear in marketing beyond the portfolio |
| Social accounts | Only LinkedIn is confirmed; Instagram, X, YouTube, Facebook, Pinterest are assumed to be new or future accounts | Confirm handles (recommended handle: @sanzeed everywhere) |
| Name usage | Wordmark "SANZEED" for the brand, "Sanzeed Mirza" for formal/legal/SEO | Confirm |

---
*Next: `Brand_Strategy.md` builds on this audit. Nothing in that document contradicts a confirmed fact above; where it goes beyond the site, it is labelled as a recommendation.*
