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


def _draw_header(c: canvas.Canvas, margin: float, title: str, subtitle: str) -> float:
    """Returns the y of the bottom of the header band."""
    top = PAGE_H - 0.42 * inch
    c.setFillColor(INK)
    c.setFont("NSB", 22)
    c.drawString(margin, top - 22, title)
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
    c.drawString(margin, top - 56, subtitle)
    c.setStrokeColor(HEADER_RULE)
    c.setLineWidth(1.1)
    y = top - 68
    c.line(margin, y, PAGE_W - margin, y)
    return y - 0.18 * inch


def _draw_footer(c: canvas.Canvas, margin: float, note: str) -> None:
    c.setFillColor(MUTED)
    c.setFont("NS", 7)
    c.drawString(margin, 0.28 * inch, note)
    c.drawRightString(PAGE_W - margin, 0.28 * inch, "polyglot-poster")


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
    c.setFont("NS", 8)
    c.drawString(inner_x + 12 + fr_w, title_y - 1, f"{t_en}  ·  {len(cat['vocab'])} words")

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

    vocab_top = header_y - 0.10 * inch
    vocab_bot = y + pad * 0.55
    n = max(1, len(cat["vocab"]))
    row_h = (vocab_top - vocab_bot) / n

    latin = _style("vlat", "NS", 5.9, 7.2, INK)
    korean = _style("vko", "KR", 5.9, 7.4, INK)

    for r, entry in enumerate(cat["vocab"]):
        row_top = vocab_top - r * row_h
        if r % 2 == 1:
            c.setFillColor(HexColor("#FAFAFA"))
            c.rect(inner_x, row_top - row_h, inner_w, row_h, fill=1, stroke=0)
            c.setFillColor(FR_WASH)
            c.rect(fr_col_x, row_top - row_h, col_w, row_h, fill=1, stroke=0)
        for i, lang in enumerate(LANGS):
            st = korean if lang == "ko" else latin
            p, ph = _para(entry[lang], st, col_w - 6)
            draw_y = (row_top - row_h) + max(0, (row_h - ph) / 2)
            p.drawOn(c, inner_x + i * col_w + 3, draw_y)


def _grid(c: canvas.Canvas, draw_fn, title: str, subtitle: str, footer: str, pdf_title: str) -> None:
    c.setTitle(pdf_title)
    c.setAuthor("polyglot-poster")
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 0.42 * inch
    grid_top = _draw_header(c, margin, title, subtitle)
    _draw_footer(c, margin, footer)
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
        draw_fn(c, x, y, cell_w, cell_h, cat)


def _draw_phrase_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    accent = HexColor(cat["color"])
    pad = 0.18 * inch
    inner_x = x + pad
    inner_w = w - 2 * pad

    c.setFillColor(white)
    c.setStrokeColor(HexColor("#D8D8D8"))
    c.setLineWidth(0.6)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    c.setFillColor(accent)
    c.rect(x, y, 6, h, fill=1, stroke=0)

    title_y = y + h - 0.32 * inch
    t_fr = cat["titles"]["fr"].replace("'", "\u2019")
    t_en = cat["titles"]["en"].replace("'", "\u2019")
    c.setFillColor(accent)
    c.setFont("NSB", 14)
    c.drawString(inner_x + 4, title_y, t_fr)
    fr_w = c.stringWidth(t_fr, "NSB", 14)
    c.setFillColor(MUTED)
    c.setFont("NS", 9)
    c.drawString(inner_x + 12 + fr_w, title_y + 1, t_en)

    col_w = inner_w / 6
    header_y = title_y - 0.32 * inch
    c.setFillColor(HexColor("#F4F4F4"))
    c.rect(inner_x, header_y - 4, inner_w, 16, fill=1, stroke=0)
    fr_col_x = inner_x + 4 * col_w
    c.setFillColor(FR_WASH)
    c.rect(fr_col_x, y + pad, col_w, header_y - 4 - (y + pad), fill=1, stroke=0)
    for i, lang in enumerate(LANGS):
        font = "KRB" if lang == "ko" else "NSB"
        c.setFont(font, 8)
        c.setFillColor(INK if lang != "fr" else accent)
        c.drawString(inner_x + i * col_w + 4, header_y, LANG_NATIVE[lang].upper())

    phrase_top = header_y - 0.18 * inch
    phrase_h = 2.35 * inch
    latin = _style("plat", "NS", 9.4, 12.2, INK)
    korean = _style("pko", "KR", 9.4, 12.4, INK)

    for r, entry in enumerate(cat["phrases"]):
        row_top = phrase_top - r * phrase_h
        band_bot = row_top - phrase_h + 0.12 * inch
        if r % 2 == 0:
            c.setFillColor(HexColor("#FBF8F4"))
            c.rect(inner_x, band_bot, inner_w, phrase_h - 0.14 * inch, fill=1, stroke=0)
            c.setFillColor(Color(0.95, 0.96, 0.99))
            c.rect(fr_col_x, band_bot, col_w, phrase_h - 0.14 * inch, fill=1, stroke=0)
        c.setFillColor(accent)
        c.setFont("NSB", 8)
        c.drawString(inner_x + 4, row_top - 14, f"{r + 1}  ·")
        for i, lang in enumerate(LANGS):
            st = korean if lang == "ko" else latin
            p, ph = _para(entry[lang], st, col_w - 10)
            p.drawOn(c, inner_x + i * col_w + 4, row_top - 16 - ph)


def render(path: Path) -> Path:
    validate()
    _register_fonts()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    n = sum(len(cat["vocab"]) for cat in CATEGORIES)
    _grid(
        c,
        _draw_card,
        "POLYGLOT POSTER",
        "Vocabulary  ·  every word from the photographed pages, plus the gaps they left  ·  15 situations × 6 languages",
        f"{n} entries. Clothes and weather are the two added categories. Phrases live on the companion sheet.",
        "Polyglot Poster — vocabulary — EN / ES / PT / IT / FR / KO",
    )
    c.save()
    return path


def render_phrases(path: Path) -> Path:
    validate()
    _register_fonts()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    _grid(
        c,
        _draw_phrase_card,
        "POLYGLOT POSTER  ·  PHRASES",
        "Three everyday sentences per situation, same six-language columns as the vocabulary sheet",
        "Companion to the vocabulary sheet. Same 3 × 5 grid, same six-language columns.",
        "Polyglot Poster — phrases — EN / ES / PT / IT / FR / KO",
    )
    c.save()
    return path
