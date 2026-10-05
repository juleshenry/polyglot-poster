"""Layout checks. They need the Noto fonts on disk and never download them."""

import io

import pytest
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from polyglot_poster import poster
from polyglot_poster.fonts import FILES, FONT_DIR
from polyglot_poster.lexicon import CATEGORIES, LANGS

pytestmark = pytest.mark.skipif(
    not all((FONT_DIR / name).exists() for name in FILES),
    reason="fonts not downloaded yet; run the poster command once",
)


@pytest.fixture(scope="module")
def grid_top():
    poster._register_fonts()
    c = canvas.Canvas(io.BytesIO(), pagesize=(poster.PAGE_W, poster.PAGE_H))
    return poster._draw_header(c, "WORDS")


def test_every_character_has_a_glyph(grid_top):
    faces = {lang: pdfmetrics.getFont("KR" if lang == "ko" else "NS").face for lang in LANGS}
    for cat in CATEGORIES:
        for row in cat["vocab"] + cat["phrases"] + [cat["titles"]]:
            for lang in LANGS:
                drawn = row[lang].replace("'", "’") + " "
                missing = [ch for ch in drawn if ord(ch) not in faces[lang].charToGlyph]
                assert not missing, (cat["id"], lang, row[lang], missing)


def test_no_word_spills_out_of_its_row(grid_top):
    for cell, cat in zip(poster._cells(5, 3, grid_top), CATEGORIES):
        f = poster._vocab_frame(*cell, len(cat["vocab"]))
        styles = poster._largest_fit(
            cat["vocab"], f["text_w"], f["row_h"], poster.VOCAB_SIZES, poster.VOCAB_LEADING, "v"
        )
        for row in cat["vocab"]:
            for lang in LANGS:
                _, height = poster._para(row[lang], styles[lang], f["text_w"])
                assert height <= f["row_h"], (cat["id"], lang, row[lang])


def test_no_phrase_spills_out_of_its_row(grid_top):
    f = poster._phrase_frame(*poster._cells(3, 5, grid_top)[0])
    styles = poster._phrase_styles(f["col_w"], f["row_h"])
    width = f["col_w"] - 2 * poster.PHRASE_PAD_X
    for cat in CATEGORIES:
        for phrase in cat["phrases"]:
            for lang in LANGS:
                _, height = poster._para(phrase[lang], styles[lang], width)
                assert height <= f["row_h"] - 2 * poster.PHRASE_PAD_Y, (cat["id"], lang, phrase[lang])


def test_french_punctuation_stays_with_its_word():
    assert poster._esc("s'il vous plaît ?") == "s’il vous plaît ?"
    assert poster._esc("zut !") == "zut !"
    assert poster._esc("pedir / preguntar") == "pedir / preguntar"


def test_same_lexicon_writes_the_same_bytes(tmp_path):
    first = poster.render_phrases(tmp_path / "a.pdf").read_bytes()
    second = poster.render_phrases(tmp_path / "b.pdf").read_bytes()
    assert first == second
