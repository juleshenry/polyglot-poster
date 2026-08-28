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

PAPER = HexColor("#F7F4EE")
INK = HexColor("#1A1A1A")
MUTED = HexColor("#5C574E")
TITLE_SUB = Color(1, 1, 1, alpha=0.72)


def _register_fonts() -> None:
    paths = ensure_fonts()
    pdfmetrics.registerFont(TTFont("NS", str(paths["NotoSans-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("NSB", str(paths["NotoSans-Bold.ttf"])))
    pdfmetrics.registerFont(TTFont("KR", str(paths["NotoSansKR-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("KRB", str(paths["NotoSansKR-Bold.ttf"])))


def _esc(text: str) -> str:
    text = text.replace("'", "\u2019")
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _tint(hex_color: str, paper_mix: float) -> Color:
    c = HexColor(hex_color)
    m = paper_mix
    return Color(
        c.red * (1 - m) + PAPER.red * m,
        c.green * (1 - m) + PAPER.green * m,
        c.blue * (1 - m) + PAPER.blue * m,
    )


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


def _draw_tracked_centered(
    c: canvas.Canvas, text: str, cx: float, y: float, font: str, size: float, tracking: float
) -> None:
    widths = [c.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + tracking * max(len(text) - 1, 0)
    x = cx - total / 2
    c.setFont(font, size)
    for ch, w in zip(text, widths):
        c.drawString(x, y, ch)
        x += w + tracking


def _draw_header(c: canvas.Canvas, kicker: str) -> float:
    top = PAGE_H - 0.34 * inch
    cx = PAGE_W / 2
    c.setFillColor(INK)
    _draw_tracked_centered(c, "POLYGLOT POSTER", cx, top - 22, "NSB", 26, 2.6)
    c.setFillColor(MUTED)
    _draw_tracked_centered(c, kicker, cx, top - 40, "NSB", 9.5, 4.4)
    sep = "   ·   "
    pieces = []
    for i, lang in enumerate(LANGS):
        if i:
            pieces.append(("NS", sep))
        font = "KR" if lang == "ko" else "NS"
        pieces.append((font, LANG_NATIVE[lang]))
    ribbon_w = sum(c.stringWidth(text, font, 8.5) for font, text in pieces)
    x = cx - ribbon_w / 2
    y_ribbon = top - 56
    c.setFillColor(MUTED)
    for font, text in pieces:
        c.setFont(font, 8.5)
        c.drawString(x, y_ribbon, text)
        x += c.stringWidth(text, font, 8.5)
    return y_ribbon - 0.16 * inch


def _darken(hex_color: str, amount: float = 0.38) -> Color:
    c = HexColor(hex_color)
    f = 1 - amount
    return Color(c.red * f, c.green * f, c.blue * f)


def _round_card(c: canvas.Canvas, x, y, w, h, fill, stroke) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 7, fill=1, stroke=1)


def _subtitle_pieces(titles) -> list[tuple[str, str]]:
    sep = "  ·  "
    pieces = []
    for lang in LANGS:
        if lang == "en":
            continue
        if pieces:
            pieces.append(("NSB", sep))
        font = "KRB" if lang == "ko" else "NSB"
        pieces.append((font, titles[lang].replace("'", "\u2019")))
    return pieces


def _draw_title_banner(c, x, y, w, h, cat, title_h: float) -> float:
    """Dark accent bar: English title, then the other five languages."""
    dark = _darken(cat["color"], 0.40)
    radius = 7
    c.saveState()
    path = c.beginPath()
    path.roundRect(x, y, w, h, radius)
    c.clipPath(path, stroke=0, fill=0)
    c.setFillColor(dark)
    c.rect(x, y + h - title_h, w, title_h, fill=1, stroke=0)
    c.restoreState()

    pad = 10
    max_w = w - 2 * pad
    en = cat["titles"]["en"].replace("'", "\u2019")
    en_size = 12.4
    while en_size > 8.6 and c.stringWidth(en, "NSB", en_size) > max_w:
        en_size -= 0.2

    pieces = _subtitle_pieces(cat["titles"])
    sub_size = 7.2
    while sub_size > 5.4:
        total = sum(c.stringWidth(text, font, sub_size) for font, text in pieces)
        if total <= max_w:
            break
        sub_size -= 0.15
    total = sum(c.stringWidth(text, font, sub_size) for font, text in pieces)

    banner_top = y + h
    gap = 3.2
    block = en_size + gap + sub_size
    top_pad = (title_h - block) / 2
    en_base = banner_top - top_pad - en_size * 0.82
    sub_base = en_base - gap - sub_size * 0.78

    c.setFillColor(white)
    c.setFont("NSB", en_size)
    c.drawCentredString(x + w / 2, en_base, en)

    c.setFillColor(TITLE_SUB)
    tx = x + (w - total) / 2
    for font, text in pieces:
        c.setFont(font, sub_size)
        c.drawString(tx, sub_base, text)
        tx += c.stringWidth(text, font, sub_size)
    return y + h - title_h


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


TITLE_H = 0.50 * inch


def _draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    accent = HexColor(cat["color"])
    wash = _tint(cat["color"], 0.88)
    stripe = _tint(cat["color"], 0.78)
    edge = _tint(cat["color"], 0.52)
    pad = 0.08 * inch
    inner_x = x + pad
    inner_w = w - 2 * pad

    _round_card(c, x, y, w, h, wash, edge)
    body_top = _draw_title_banner(c, x, y, w, h, cat, TITLE_H)

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
    """Three phrase columns, six languages stacked. One type size for the sheet."""
    wash = _tint(cat["color"], 0.88)
    stripe = _tint(cat["color"], 0.78)
    edge = _tint(cat["color"], 0.52)
    pad = 0.10 * inch
    inner_x = x + pad
    inner_w = w - 2 * pad

    _round_card(c, x, y, w, h, wash, edge)
    body_top = _draw_title_banner(c, x, y, w, h, cat, TITLE_H)

    phrases = cat["phrases"]
    col_w = inner_w / 3
    phrase_top = body_top - 0.05 * inch
    phrase_bot = y + pad * 0.4
    row_h = (phrase_top - phrase_bot) / 6
    font = min(15.5, max(11.0, row_h * 0.175))
    leading = font * 1.22
    latin = _style("plat", "NS", font, leading, INK)
    korean = _style("pko", "KR", font, leading + 0.2, INK)

    for r, lang in enumerate(LANGS):
        row_top = phrase_top - r * row_h
        if r % 2 == 1:
            c.setFillColor(stripe)
            c.rect(inner_x, row_top - row_h, inner_w, row_h, fill=1, stroke=0)
        for i, entry in enumerate(phrases):
            st = korean if lang == "ko" else latin
            p, ph = _para(entry[lang], st, col_w - 12)
            draw_y = (row_top - row_h) + max(2, (row_h - ph) / 2)
            p.drawOn(c, inner_x + i * col_w + 6, draw_y)

    c.setStrokeColor(edge)
    c.setLineWidth(0.45)
    for i in range(1, 3):
        rx = inner_x + i * col_w
        c.line(rx, phrase_bot, rx, phrase_top)


def _grid(c: canvas.Canvas, draw_fn, kicker: str, pdf_title: str, cols: int = 5, rows: int = 3) -> None:
    c.setTitle(pdf_title)
    c.setAuthor("polyglot-poster")
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 0.42 * inch
    grid_top = _draw_header(c, kicker)
    grid_bot = 0.30 * inch
    gutter = 0.14 * inch
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
        "WORDS",
        "Polyglot Poster — words — EN / ES / PT / IT / FR / KO",
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
        "PHRASES",
        "Polyglot Poster — phrases — EN / ES / PT / IT / FR / KO",
        cols=3,
        rows=5,
    )
    c.save()
    return path
