"""Six equal language columns, one tint per situation.

Words sheet: 3 rows of 5 cards. Phrases sheet: 5 rows of 3.
"""

from __future__ import annotations

import re
from functools import lru_cache
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

# Card title bar: (height, English size, translations size). Phrases are set
# far larger than words, so their titles scale up to stay above the body.
WORDS_TITLE = (0.66 * inch, 21.0, 10.5)
PHRASES_TITLE = (0.90 * inch, 30.0, 14.0)

# Type sizes to try, largest first. The first one where nothing spills wins.
VOCAB_SIZES = [round(10.0 - 0.2 * i, 1) for i in range(18)]  # 10.0 … 6.6
PHRASE_SIZES = [30.0 - 0.5 * i for i in range(39)]  # 30.0 … 11.0
VOCAB_LEADING = 1.15
PHRASE_LEADING = 1.22
VOCAB_PAD_X = 2
PHRASE_PAD_X = 14
PHRASE_PAD_Y = 5

# French sets ? ! ; : off with a space. Glue it so the mark never wraps alone.
_SPACED_PUNCT = re.compile(r" (?=[?!;:])")


def _register_fonts() -> None:
    paths = ensure_fonts()
    pdfmetrics.registerFont(TTFont("NS", str(paths["NotoSans-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("NSB", str(paths["NotoSans-Bold.ttf"])))
    pdfmetrics.registerFont(TTFont("KR", str(paths["NotoSansKR-Regular.ttf"])))
    pdfmetrics.registerFont(TTFont("KRB", str(paths["NotoSansKR-Bold.ttf"])))


def _esc(text: str) -> str:
    text = text.replace("'", "’")
    text = _SPACED_PUNCT.sub(" ", text)
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


def _styles(tag: str, size: float, leading: float) -> dict[str, ParagraphStyle]:
    latin = _style(f"{tag}lat", "NS", size, leading)
    korean = _style(f"{tag}ko", "KR", size, leading + 0.2)
    return {lang: korean if lang == "ko" else latin for lang in LANGS}


def _para(text: str, style: ParagraphStyle, width: float) -> tuple[Paragraph, float]:
    p = Paragraph(_esc(text), style)
    _, h = p.wrap(max(width, 8), 800)
    return p, h


def _largest_fit(
    rows: list[dict[str, str]],
    width: float,
    max_h: float,
    sizes: list[float],
    leading: float,
    tag: str,
) -> dict[str, ParagraphStyle]:
    """Styles at the largest of `sizes` where no cell is taller than `max_h`."""
    for size in sizes:
        styles = _styles(tag, size, size * leading)
        if all(_para(row[lang], styles[lang], width)[1] <= max_h for row in rows for lang in LANGS):
            break
    return styles


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
    _draw_tracked_centered(c, "POLYGLOT POSTER", cx, top - 34, "NSB", 40, 4.0)
    c.setFillColor(MUTED)
    _draw_tracked_centered(c, kicker, cx, top - 54, "NSB", 12, 5.6)
    # The only key to column order on the sheet, so it reads as ink, not as a caption.
    ribbon_size = 13
    sep = "   ·   "
    pieces = []
    for i, lang in enumerate(LANGS):
        if i:
            pieces.append(("NS", sep))
        font = "KR" if lang == "ko" else "NS"
        pieces.append((font, LANG_NATIVE[lang]))
    ribbon_w = sum(c.stringWidth(text, font, ribbon_size) for font, text in pieces)
    x = cx - ribbon_w / 2
    y_ribbon = top - 77
    c.setFillColor(INK)
    for font, text in pieces:
        c.setFont(font, ribbon_size)
        c.drawString(x, y_ribbon, text)
        x += c.stringWidth(text, font, ribbon_size)
    return y_ribbon - 0.18 * inch


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
        pieces.append((font, titles[lang].replace("'", "’")))
    return pieces


def _draw_title_banner(c, x, y, w, h, cat, title: tuple[float, float, float]) -> None:
    """Dark accent bar: English title, then the other five languages."""
    title_h, en_size, sub_size = title
    dark = _darken(cat["color"], 0.40)
    radius = 7
    c.saveState()
    path = c.beginPath()
    path.roundRect(x, y, w, h, radius)
    c.clipPath(path, stroke=0, fill=0)
    c.setFillColor(dark)
    c.rect(x, y + h - title_h, w, title_h, fill=1, stroke=0)
    c.restoreState()

    pad = 14
    max_w = w - 2 * pad
    en = cat["titles"]["en"].replace("'", "’")
    while en_size > 12.0 and c.stringWidth(en, "NSB", en_size) > max_w:
        en_size -= 0.25

    pieces = _subtitle_pieces(cat["titles"])
    while sub_size > 6.0:
        total = sum(c.stringWidth(text, font, sub_size) for font, text in pieces)
        if total <= max_w:
            break
        sub_size -= 0.25
    total = sum(c.stringWidth(text, font, sub_size) for font, text in pieces)

    banner_top = y + h
    gap = en_size * 0.22
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


def _draw_stack(c, x, y_top, y_bot, w, entries, n_rows, stripe, styles):
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
            p, ph = _para(entry[lang], styles[lang], col_w - 2 * VOCAB_PAD_X)
            draw_y = (row_top - row_h) + max(0, (row_h - ph) / 2)
            p.drawOn(c, x + i * col_w + VOCAB_PAD_X, draw_y)


def _vocab_frame(x: float, y: float, w: float, h: float, n_words: int) -> dict:
    """Where the two stacks sit inside a words card, and how tall a row is."""
    pad = 0.08 * inch
    gap = 0.09 * inch
    inner_x = x + pad
    stack_w = (w - 2 * pad - gap) / 2
    stack_top = y + h - WORDS_TITLE[0] - 0.04 * inch
    stack_bot = y + pad * 0.4
    n_rows = max((n_words + 1) // 2, 1)
    return {
        "left_x": inner_x,
        "right_x": inner_x + stack_w + gap,
        "rule_x": inner_x + stack_w + gap / 2,
        "stack_w": stack_w,
        "top": stack_top,
        "bot": stack_bot,
        "n_rows": n_rows,
        "row_h": (stack_top - stack_bot) / n_rows,
        "text_w": stack_w / 6 - 2 * VOCAB_PAD_X,
    }


def _draw_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    wash = _tint(cat["color"], 0.88)
    stripe = _tint(cat["color"], 0.78)
    edge = _tint(cat["color"], 0.52)

    _round_card(c, x, y, w, h, wash, edge)
    _draw_title_banner(c, x, y, w, h, cat, WORDS_TITLE)

    vocab = cat["vocab"]
    f = _vocab_frame(x, y, w, h, len(vocab))
    left, right = vocab[: f["n_rows"]], vocab[f["n_rows"] :]
    styles = _largest_fit(vocab, f["text_w"], f["row_h"], VOCAB_SIZES, VOCAB_LEADING, "v")

    for stack_x, entries in ((f["left_x"], left), (f["right_x"], right)):
        _draw_stack(c, stack_x, f["top"], f["bot"], f["stack_w"], entries, f["n_rows"], stripe, styles)
    c.setStrokeColor(edge)
    c.setLineWidth(0.5)
    c.line(f["rule_x"], f["bot"], f["rule_x"], f["top"] - 2)


def _phrase_frame(x: float, y: float, w: float, h: float) -> dict:
    """Where the three phrase columns sit inside a phrases card."""
    pad = 0.10 * inch
    top = y + h - PHRASES_TITLE[0] - 0.05 * inch
    bot = y + pad * 0.4
    inner_w = w - 2 * pad
    return {
        "x": x + pad,
        "w": inner_w,
        "col_w": inner_w / 3,
        "top": top,
        "bot": bot,
        "row_h": (top - bot) / len(LANGS),
    }


@lru_cache(maxsize=None)
def _phrase_styles(col_w: float, row_h: float) -> dict[str, ParagraphStyle]:
    """One type size for the sheet: the largest at which every phrase fits its row."""
    rows = [phrase for cat in CATEGORIES for phrase in cat["phrases"]]
    return _largest_fit(
        rows, col_w - 2 * PHRASE_PAD_X, row_h - 2 * PHRASE_PAD_Y, PHRASE_SIZES, PHRASE_LEADING, "p"
    )


def _draw_phrase_card(c: canvas.Canvas, x: float, y: float, w: float, h: float, cat: dict) -> None:
    """Three phrase columns, six languages stacked. One type size for the sheet."""
    wash = _tint(cat["color"], 0.88)
    stripe = _tint(cat["color"], 0.78)
    edge = _tint(cat["color"], 0.52)

    _round_card(c, x, y, w, h, wash, edge)
    _draw_title_banner(c, x, y, w, h, cat, PHRASES_TITLE)

    f = _phrase_frame(x, y, w, h)
    styles = _phrase_styles(f["col_w"], f["row_h"])

    for r, lang in enumerate(LANGS):
        row_top = f["top"] - r * f["row_h"]
        if r % 2 == 1:
            c.setFillColor(stripe)
            c.rect(f["x"], row_top - f["row_h"], f["w"], f["row_h"], fill=1, stroke=0)
        for i, entry in enumerate(cat["phrases"]):
            p, ph = _para(entry[lang], styles[lang], f["col_w"] - 2 * PHRASE_PAD_X)
            draw_y = (row_top - f["row_h"]) + max(PHRASE_PAD_Y, (f["row_h"] - ph) / 2)
            p.drawOn(c, f["x"] + i * f["col_w"] + PHRASE_PAD_X, draw_y)

    c.setStrokeColor(edge)
    c.setLineWidth(0.45)
    for i in range(1, 3):
        rx = f["x"] + i * f["col_w"]
        c.line(rx, f["bot"], rx, f["top"])


def _cells(cols: int, rows: int, grid_top: float) -> list[tuple[float, float, float, float]]:
    """(x, y, w, h) of every card, reading order."""
    margin = 0.42 * inch
    grid_bot = 0.30 * inch
    gutter = 0.14 * inch
    cell_w = (PAGE_W - 2 * margin - (cols - 1) * gutter) / cols
    cell_h = (grid_top - grid_bot - (rows - 1) * gutter) / rows
    return [
        (
            margin + (i % cols) * (cell_w + gutter),
            grid_top - (i // cols + 1) * cell_h - (i // cols) * gutter,
            cell_w,
            cell_h,
        )
        for i in range(cols * rows)
    ]


def _render(path: Path, draw_fn, kicker: str, cols: int, rows: int) -> Path:
    validate()
    _register_fonts()
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # invariant: the same lexicon always writes the same bytes, so the
    # checked-in PDFs only change when the poster does.
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), invariant=1)
    c.setTitle(f"Polyglot Poster — {kicker.lower()} — EN / ES / PT / IT / FR / KO")
    c.setAuthor("polyglot-poster")
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    grid_top = _draw_header(c, kicker)
    for (x, y, w, h), cat in zip(_cells(cols, rows, grid_top), CATEGORIES):
        draw_fn(c, x, y, w, h, cat)
    c.save()
    return path


def render(path: Path) -> Path:
    return _render(path, _draw_card, "WORDS", cols=5, rows=3)


def render_phrases(path: Path) -> Path:
    return _render(path, _draw_phrase_card, "PHRASES", cols=3, rows=5)
