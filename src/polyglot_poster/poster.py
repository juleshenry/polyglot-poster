"""One huge white canvas: 3 rows of 5 category cards, six language columns."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from polyglot_poster.fonts import ensure_fonts
from polyglot_poster.lexicon import CATEGORIES, LANGS, LANG_NATIVE, validate

# Landscape wall sheet: 5 cards across, 3 down.
PAGE_W = 72 * inch
PAGE_H = 42 * inch

INK = HexColor("#1A1A1A")
MUTED = HexColor("#5C5C5C")
RULE = HexColor("#E6E6E6")
FR_WASH = HexColor("#F3F7FC")
HEADER_RULE = HexColor("#111111")


def _register_fonts() -> None:
    paths = ensure_fonts()
    pdfmetrics.registerFont(TTFont("NS", str(paths["NotoSans-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("NSB", str(paths["NotoSans-Bold.ttf"])))
    pdfmetrics.registerFont(TTFont("KR", str(paths["NotoSansKR-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("KRB", str(paths["NotoSansKR-Bold.ttf"])))


def _esc(text: str) -> str:
    # Typographic apostrophe so French l’addition survives font subsetting.
    text = text.replace("'", "\u2019")
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _style(name: str, font: str, size: float, leading: float, color=INK, align=0) -> ParagraphStyle:
    return ParagraphStyle(
        name=name,
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=align,
        encoding="utf-8",
    )


def _para(text: str, style: ParagraphStyle, width: float) -> tuple[Paragraph, float]:
    p = Paragraph(_esc(text), style)
    _, h = p.wrap(width, 400)
    return p, h


def _draw_header(c: canvas.Canvas, margin: float) -> float:
    """Returns the y of the bottom of the header band."""
    top = PAGE_H - 0.42 * inch
    c.setFillColor(INK)
    c.setFont("NSB", 22)
    c.drawString(margin, top - 22, "POLYGLOT POSTER")
    x = margin
    y_ribbon = top - 40
    c.setFillColor(MUTED)
    for i, lang in enumerate(LANGS):
        if i:
            c.setFont("NS", 10)
            sep = "   ·   "
            c.drawString(x, y_ribbon, sep)
            x += c.stringWidth(sep, "NS", 10)
        font = "KR" if lang == "ko" else "NS"
        label = LANG_NATIVE[lang]
        c.setFont(font, 10)
        c.drawString(x, y_ribbon, label)
        x += c.stringWidth(label, font, 10)
    c.setFont("NS", 8)
    c.drawString(
        margin,
        top - 56,
        "Torn pages of French: A Self-Teaching Guide  ·  restored, translated, and hung on one wall  ·  15 situations × 6 languages",
    )
    c.setStrokeColor(HEADER_RULE)
    c.setLineWidth(1.1)
    y = top - 68
    c.line(margin, y, PAGE_W - margin, y)
    return y - 0.18 * inch


def _draw_footer(c: canvas.Canvas, margin: float) -> None:
    c.setFillColor(MUTED)
    c.setFont("NS", 7)
    c.drawString(
        margin,
        0.28 * inch,
        "Clothes and weather are the two added categories — the photographed chapters never taught a wardrobe or the forecast.  French is the source column.",
    )
    c.drawRightString(
        PAGE_W - margin,
        0.28 * inch,
        "polyglot-poster",
    )


def _draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    accent = HexColor(cat["color"])
    pad = 0.14 * inch
    inner_x = x + pad
    inner_w = w - 2 * pad

    # card
    c.setFillColor(white)
    c.setStrokeColor(HexColor("#D8D8D8"))
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)

    # left accent
    c.setFillColor(accent)
    c.rect(x, y, 5, h, fill=1, stroke=0)

    # title
    title_y = y + h - 0.24 * inch
    t_fr = cat["titles"]["fr"].replace("'", "\u2019")
    t_en = cat["titles"]["en"].replace("'", "\u2019")
    c.setFillColor(accent)
    c.setFont("NSB", 13)
    c.drawString(inner_x + 4, title_y - 2, t_fr)
    fr_w = c.stringWidth(t_fr, "NSB", 13)
    c.setFillColor(MUTED)
    c.setFont("NS", 8.5)
    c.drawString(inner_x + 12 + fr_w, title_y - 1, t_en)

    # language headers
    col_w = inner_w / 6
    header_y = title_y - 0.28 * inch
    c.setFillColor(HexColor("#F4F4F4"))
    c.rect(inner_x, header_y - 3, inner_w, 14, fill=1, stroke=0)
    # French column wash through the card body
    fr_col_x = inner_x + 4 * col_w
    body_top = header_y - 3
    body_bot = y + pad
    c.setFillColor(FR_WASH)
    c.rect(fr_col_x, body_bot, col_w, body_top - body_bot, fill=1, stroke=0)

    for i, lang in enumerate(LANGS):
        font = "KRB" if lang == "ko" else "NSB"
        c.setFont(font, 7.2)
        c.setFillColor(INK if lang != "fr" else accent)
        label = LANG_NATIVE[lang].upper()
        cx = inner_x + i * col_w + 4
        c.drawString(cx, header_y, label)

    # phrases live at the bottom; vocab fills the rest
    phrase_block_h = 1.9 * inch
    vocab_top = header_y - 0.16 * inch
    vocab_bot = y + pad + phrase_block_h
    n = max(1, len(cat["vocab"]))
    row_h = (vocab_top - vocab_bot) / n

    latin = _style("vlat", "NS", 8.2, 10.4, INK)
    korean = _style("vko", "KR", 8.2, 10.6, INK)
    latin_b = _style("vlatb", "NS", 7.6, 9.6, INK)
    korean_b = _style("vkob", "KR", 7.6, 9.8, INK)

    for r, entry in enumerate(cat["vocab"]):
        row_top = vocab_top - r * row_h
        if r % 2 == 1:
            c.setFillColor(HexColor("#FAFAFA"))
            c.rect(inner_x, row_top - row_h, inner_w, row_h, fill=1, stroke=0)
            # restore french wash
            c.setFillColor(FR_WASH)
            c.rect(fr_col_x, row_top - row_h, col_w, row_h, fill=1, stroke=0)
        for i, lang in enumerate(LANGS):
            st = korean if lang == "ko" else latin
            p, ph = _para(entry[lang], st, col_w - 8)
            draw_y = (row_top - row_h) + (row_h - ph) / 2
            p.drawOn(c, inner_x + i * col_w + 3, draw_y)

    # divider + phrases
    div_y = vocab_bot - 0.04 * inch
    c.setStrokeColor(accent)
    c.setLineWidth(0.8)
    c.line(inner_x, div_y, inner_x + inner_w, div_y)
    c.setFillColor(accent)
    c.setFont("NSB", 6.2)
    c.drawString(inner_x + 3, div_y - 11, "3 PHRASES")

    phrase_top = div_y - 0.20 * inch
    phrase_h = (phrase_top - (y + pad + 0.04 * inch)) / 3
    for r, entry in enumerate(cat["phrases"]):
        row_top = phrase_top - r * phrase_h
        if r % 2 == 0:
            c.setFillColor(HexColor("#FBF8F4"))
            c.rect(inner_x, row_top - phrase_h + 1, inner_w, phrase_h - 2, fill=1, stroke=0)
            c.setFillColor(Color(0.95, 0.96, 0.99))
            c.rect(fr_col_x, row_top - phrase_h + 1, col_w, phrase_h - 2, fill=1, stroke=0)
        for i, lang in enumerate(LANGS):
            st = korean_b if lang == "ko" else latin_b
            p, ph = _para(entry[lang], st, col_w - 8)
            draw_y = (row_top - phrase_h) + (phrase_h - ph) / 2
            p.drawOn(c, inner_x + i * col_w + 3, draw_y)


def render(path: Path) -> Path:
    validate()
    _register_fonts()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(
        str(path),
        pagesize=(PAGE_W, PAGE_H),
    )
    c.setTitle("Polyglot Poster — English / Spanish / Portuguese / Italian / French / Korean")
    c.setAuthor("polyglot-poster")
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 0.42 * inch
    grid_top = _draw_header(c, margin)
    _draw_footer(c, margin)
    grid_bot = 0.48 * inch
    gutter = 0.16 * inch
    cols, rows = 5, 3
    grid_w = PAGE_W - 2 * margin
    grid_h = grid_top - grid_bot
    cell_w = (grid_w - (cols - 1) * gutter) / cols
    cell_h = (grid_h - (rows - 1) * gutter) / rows

    for i, cat in enumerate(CATEGORIES):
        col = i % cols
        row = i // cols
        x = margin + col * (cell_w + gutter)
        y = grid_top - (row + 1) * cell_h - row * gutter
        _draw_card(c, x, y, cell_w, cell_h, cat)

    c.save()
    return path
