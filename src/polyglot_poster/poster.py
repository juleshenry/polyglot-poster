"""3 rows of 5: six equal language columns, one tint per situation."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from polyglot_poster.fonts import ensure_fonts
from polyglot_poster.lexicon import CATEGORIES, LANGS, LANG_NATIVE, validate

PAGE_W = 72 * inch
PAGE_H = 42 * inch

INK = HexColor("#1A1A1A")
MUTED = HexColor("#4A4A4A")


def _register_fonts() -> None:
    paths = ensure_fonts()
    pdfmetrics.registerFont(TTFont("NS", str(paths["NotoSans-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("NSB", str(paths["NotoSans-Bold.ttf"])))
    pdfmetrics.registerFont(TTFont("KR", str(paths["NotoSansKR-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("KRB", str(paths["NotoSansKR-Bold.ttf"])))


def _esc(text: str) -> str:
    text = text.replace("'", "\u2019")
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _tint(hex_color: str, white_mix: float) -> Color:
    c = HexColor(hex_color)
    m = white_mix
    return Color(c.red * (1 - m) + m, c.green * (1 - m) + m, c.blue * (1 - m) + m)


def _style(name: str, font: str, size: float, leading: float, color=INK) -> ParagraphStyle:
    return ParagraphStyle(
        name=name,
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=0,
        encoding="utf-8",
    )


def _para(text: str, style: ParagraphStyle, width: float) -> tuple[Paragraph, float]:
    p = Paragraph(_esc(text), style)
    _, h = p.wrap(max(width, 8), 800)
    return p, h


def _draw_header(c: canvas.Canvas, margin: float, title: str) -> float:
    top = PAGE_H - 0.28 * inch
    cx = PAGE_W / 2
    c.setFillColor(INK)
    c.setFont("NSB", 18)
    c.drawCentredString(cx, top - 16, title)
    sep = "   ·   "
    pieces = []
    for i, lang in enumerate(LANGS):
        if i:
            pieces.append(("NS", sep))
        font = "KR" if lang == "ko" else "NS"
        pieces.append((font, LANG_NATIVE[lang]))
    ribbon_w = sum(c.stringWidth(text, font, 9) for font, text in pieces)
    x = cx - ribbon_w / 2
    y_ribbon = top - 34
    c.setFillColor(MUTED)
    for font, text in pieces:
        c.setFont(font, 9)
        c.drawString(x, y_ribbon, text)
        x += c.stringWidth(text, font, 9)
    y = top - 44
    c.setStrokeColor(HexColor("#222222"))
    c.setLineWidth(0.9)
    c.line(margin, y, PAGE_W - margin, y)
    return y - 0.10 * inch


def _round_card(c: canvas.Canvas, x, y, w, h, fill, stroke) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 7, fill=1, stroke=1)


def _lang_and_title_rows(c, inner_x, inner_w, title_top, col_w, cat, accent, wash, title_h):
    """Situation title in every language — column order is the page header."""
    c.setFillColor(wash)
    c.rect(inner_x, title_top - title_h, inner_w, title_h, fill=1, stroke=0)
    latin = _style("ttl", "NSB", 9.4, 11.4, accent)
    korean = _style("ttk", "KRB", 9.4, 11.6, accent)
    for i, lang in enumerate(LANGS):
        st = korean if lang == "ko" else latin
        p, ph = _para(cat["titles"][lang], st, col_w - 7)
        p.drawOn(c, inner_x + i * col_w + 3, title_top - 4 - ph)
    return title_top - title_h


def _draw_stack(c, x, y_top, y_bot, w, entries, n_rows, accent, stripe, latin, korean):
    """One six-language vocab stack. n_rows keeps left/right stacks aligned."""
    col_w = w / 6
    body_top = y_top
    row_h = (body_top - y_bot) / n_rows
    for r in range(n_rows):
        row_top = body_top - r * row_h
        if r % 2 == 1:
            c.setFillColor(stripe)
            c.rect(x, row_top - row_h, w, row_h, fill=1, stroke=0)
        if r >= len(entries):
            continue
        entry = entries[r]
        for i, lang in enumerate(LANGS):
            st = korean if lang == "ko" else latin
            p, ph = _para(entry[lang], st, col_w - 4)
            draw_y = (row_top - row_h) + max(0, (row_h - ph) / 2)
            p.drawOn(c, x + i * col_w + 2, draw_y)


def _draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    accent = HexColor(cat["color"])
    wash = _tint(cat["color"], 0.90)
    stripe = _tint(cat["color"], 0.82)
    edge = _tint(cat["color"], 0.55)
    pad = 0.08 * inch
    inner_x = x + pad
    inner_w = w - 2 * pad

    _round_card(c, x, y, w, h, wash, edge)

    title_col_w = inner_w / 6
    title_top = y + h - 0.08 * inch
    body_top = _lang_and_title_rows(
        c, inner_x, inner_w, title_top, title_col_w, cat, accent, stripe, 0.42 * inch
    )

    vocab = cat["vocab"]
    mid = (len(vocab) + 1) // 2
    left, right = vocab[:mid], vocab[mid:]
    n_rows = max(len(left), len(right), 1)
    gap = 0.09 * inch
    stack_w = (inner_w - gap) / 2
    stack_top = body_top - 0.04 * inch
    stack_bot = y + pad * 0.4

    row_h = (stack_top - stack_bot) / n_rows
    font = min(10.0, max(6.6, row_h * 0.50))
    leading = font * 1.15
    latin = _style("vlat", "NS", font, leading, INK)
    korean = _style("vko", "KR", font, leading + 0.2, INK)

    _draw_stack(c, inner_x, stack_top, stack_bot, stack_w, left, n_rows, accent, stripe, latin, korean)
    _draw_stack(
        c, inner_x + stack_w + gap, stack_top, stack_bot, stack_w, right, n_rows,
        accent, stripe, latin, korean,
    )
    c.setStrokeColor(edge)
    c.setLineWidth(0.5)
    rule_x = inner_x + stack_w + gap / 2
    c.line(rule_x, stack_bot, rule_x, stack_top - 2)


def _draw_phrase_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    accent = HexColor(cat["color"])
    wash = _tint(cat["color"], 0.90)
    stripe = _tint(cat["color"], 0.80)
    band_a = _tint(cat["color"], 0.86)
    band_b = _tint(cat["color"], 0.92)
    edge = _tint(cat["color"], 0.55)
    pad = 0.10 * inch
    inner_x = x + pad
    inner_w = w - 2 * pad

    _round_card(c, x, y, w, h, wash, edge)

    col_w = inner_w / 6
    title_top = y + h - 0.10 * inch
    body_top = _lang_and_title_rows(
        c, inner_x, inner_w, title_top, col_w, cat, accent, stripe, 0.42 * inch
    )

    phrase_top = body_top - 0.06 * inch
    phrase_bot = y + pad * 0.4
    phrase_h = (phrase_top - phrase_bot) / 3
    font = min(15.5, max(11.5, phrase_h * 0.13))
    leading = font * 1.26
    latin = _style("plat", "NS", font, leading, INK)
    korean = _style("pko", "KR", font, leading + 0.2, INK)

    for r, entry in enumerate(cat["phrases"]):
        row_top = phrase_top - r * phrase_h
        c.setFillColor(band_a if r % 2 == 0 else band_b)
        c.rect(inner_x, row_top - phrase_h + 1, inner_w, phrase_h - 2, fill=1, stroke=0)
        for i, lang in enumerate(LANGS):
            st = korean if lang == "ko" else latin
            p, ph = _para(entry[lang], st, col_w - 8)
            draw_y = (row_top - phrase_h) + max(4, (phrase_h - ph) / 2)
            p.drawOn(c, inner_x + i * col_w + 3, draw_y)


def _grid(c: canvas.Canvas, draw_fn, title: str, pdf_title: str) -> None:
    c.setTitle(pdf_title)
    c.setAuthor("polyglot-poster")
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 0.22 * inch
    grid_top = _draw_header(c, margin, title)
    grid_bot = 0.16 * inch
    gutter = 0.08 * inch
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


def render(path: Path) -> Path:
    validate()
    _register_fonts()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
    _grid(
        c,
        _draw_card,
        "POLYGLOT POSTER",
        "Polyglot Poster — EN / ES / PT / IT / FR / KO",
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
        "POLYGLOT POSTER",
        "Polyglot Poster — phrases — EN / ES / PT / IT / FR / KO",
    )
    c.save()
    return path
