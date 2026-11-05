"""pptx_kit.py — python-pptx helpers that reproduce the brand on 16:9 slides (13.333 x 7.5 in).
Fonts: Fraunces Light (display), Inter Tight SemiBold (eyebrows/labels), Inter (body). Static instances for Office
are in 10_MARKETING_COLLATERAL/_shared/fonts-static (derived from 04_TYPOGRAPHY)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

BLACK = RGBColor(0, 0, 0); WHITE = RGBColor(0xF5, 0xF5, 0xF7); SILVER = RGBColor(0xA1, 0xA1, 0xA6); MIST = RGBColor(0x80, 0x80, 0x86)
GOLD = RGBColor(0xE9, 0xB2, 0x5A); CHARCOAL = RGBColor(0x1C, 0x1C, 0x1E); GRAPHITE = RGBColor(0x2A, 0x2A, 0x2D)
PLASTER = RGBColor(0xF5, 0xF0, 0xE7); SOOT = RGBColor(0x1A, 0x18, 0x16); UMBER = RGBColor(0x66, 0x5F, 0x55); GOLD_INK = RGBColor(0x8A, 0x61, 0x24); OLD_GOLD = RGBColor(0xB8, 0x86, 0x3B); STONE = RGBColor(0xEC, 0xE7, 0xDC)
DISPLAY = "Fraunces Light"; HEAD = "Inter Tight SemiBold"; TEXT = "Inter"; TEXT_M = "Inter Medium"
W, H = 13.333, 7.5; M = 0.7

class Deck:
    def __init__(self, light=False):
        self.prs = Presentation(); self.prs.slide_width = Inches(W); self.prs.slide_height = Inches(H)
        self.light = light
        self.bg = PLASTER if light else BLACK; self.fg = SOOT if light else WHITE; self.fg2 = UMBER if light else SILVER
        self.fg3 = RGBColor(0x6D, 0x66, 0x5C) if light else MIST; self.accent = OLD_GOLD if light else GOLD
        self.accent_text = GOLD_INK if light else GOLD; self.line = STONE if light else GRAPHITE; self.card_bg = RGBColor(0xFB, 0xF8, 0xF2) if light else CHARCOAL
    def slide(self, notes=None):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6]); f = s.background.fill; f.solid(); f.fore_color.rgb = self.bg
        if notes: s.notes_slide.notes_text_frame.text = notes
        return s
    def text(self, s, x, y, w, h, runs, size=14, font=TEXT, color=None, align=PP_ALIGN.LEFT, line=1.3, anchor=MSO_ANCHOR.TOP, spacing_after=0):
        """runs: str, or list of paragraphs; each paragraph is a str or list of (text, dict(font,size,color,bold,italic)) tuples."""
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = anchor
        paras = runs if isinstance(runs, list) else [runs]
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); para.alignment = align; para.line_spacing = line
            if spacing_after: para.space_after = Pt(spacing_after)
            segs = p if isinstance(p, list) else [(p, {})]
            for txt, st in segs:
                r = para.add_run(); r.text = txt; f = r.font
                f.name = st.get("font", font); f.size = Pt(st.get("size", size)); f.color.rgb = st.get("color", color or self.fg)
                f.bold = st.get("bold", False); f.italic = st.get("italic", False)
                if st.get("tracking"):
                    rPr = r._r.get_or_add_rPr(); rPr.set("spc", str(int(st["tracking"] * 100)))
                if st.get("caps"):
                    rPr = r._r.get_or_add_rPr(); rPr.set("cap", "all")
        return tb
    def eyebrow(self, s, x, y, w, txt, quiet=False):
        return self.text(s, x, y, w, 0.3, [[(txt.upper(), dict(font=HEAD, size=10, color=(self.fg3 if quiet else self.accent_text), tracking=1.4, caps=True))]])
    def headline(self, s, x, y, w, h, txt, size=48, color=None, point=True, line=1.02):
        segs = [(txt.rstrip("."), dict(font=DISPLAY, size=size, color=color or self.fg))]
        if point: segs.append((".", dict(font=DISPLAY, size=size, color=self.accent)))
        return self.text(s, x, y, w, h, [segs], line=line)
    def rule(self, s, x, y, w, point=False, end=False):
        ln = s.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y)); ln.line.color.rgb = self.line; ln.line.width = Pt(0.75)
        if point:
            d = 0.09; px = x + w - d if end else x
            dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(px), Inches(y - d / 2), Inches(d), Inches(d)); dot.fill.solid(); dot.fill.fore_color.rgb = self.accent; dot.line.fill.background()
        return ln
    def dot(self, s, x, y, d=0.1):
        o = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d)); o.fill.solid(); o.fill.fore_color.rgb = self.accent; o.line.fill.background(); return o
    def picture(self, s, path, x, y, w, h, radius=0.028, crop_focus=0.5):
        """Picture masked to a rounded rectangle (the room). Crops to fill w x h."""
        from PIL import Image
        iw, ih = Image.open(path).size; target = w / h; src = iw / ih
        pic = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
        if src > target:   # too wide: crop sides
            keep = target / src; pic.crop_left = (1 - keep) / 2; pic.crop_right = (1 - keep) / 2
        else:              # too tall: crop top/bottom around focus
            keep = src / target; off = (1 - keep); pic.crop_top = off * crop_focus; pic.crop_bottom = off * (1 - crop_focus)
        pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
        prst = pic._element.find(".//" + qn("a:prstGeom")); av = prst.find(qn("a:avLst"))
        if av is None: av = etree.SubElement(prst, qn("a:avLst"))
        for g in list(av): av.remove(g)
        gd = etree.SubElement(av, qn("a:gd")); gd.set("name", "adj"); gd.set("fmla", f"val {int(radius * 100000 * (min(w, h) / min(w, h)))}")
        pic.line.color.rgb = self.line; pic.line.width = Pt(0.75)
        return pic
    def wall_label(self, s, x, y, w, title, place):
        return self.text(s, x, y, w, 0.3, [[(title, dict(font=HEAD, size=11, color=self.fg)), ("  ·  " + place, dict(font=TEXT, size=11, color=self.fg3))]])
    def logo(self, s, path, x, y, w):
        from PIL import Image
        iw, ih = Image.open(path).size; return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(w * ih / iw))
    def footer(self, s, left, right):
        self.text(s, M, H - 0.55, 6, 0.3, [[(left, dict(font=TEXT, size=9, color=self.fg3))]])
        self.text(s, W - M - 6, H - 0.55, 6, 0.3, [[(right, dict(font=TEXT, size=9, color=self.fg3))]], align=PP_ALIGN.RIGHT)
    def card(self, s, x, y, w, h):
        c = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)); c.adjustments[0] = 0.06
        c.fill.solid(); c.fill.fore_color.rgb = self.card_bg; c.line.color.rgb = self.line; c.line.width = Pt(0.75); c.shadow.inherit = False; return c
    def save(self, path): self.prs.save(path); return path
