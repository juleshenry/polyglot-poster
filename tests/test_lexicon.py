import re
from collections import Counter

from polyglot_poster.lexicon import CATEGORIES, LANGS, validate


def test_grid_is_three_rows_of_five():
    validate()
    assert len(CATEGORIES) == 15


def test_column_order():
    assert LANGS == ("en", "es", "pt", "it", "fr", "ko")


def test_three_phrases_and_six_languages():
    for cat in CATEGORIES:
        assert len(cat["phrases"]) == 3, cat["id"]
        assert len(cat["vocab"]) >= 40, cat["id"]
        for row in cat["vocab"] + cat["phrases"] + [cat["titles"]]:
            assert tuple(row) == LANGS, (cat["id"], row)
            for lang in LANGS:
                assert row[lang] and row[lang] == row[lang].strip(), (cat["id"], row)


def test_no_alternative_listed_twice():
    # "la caja / la caja" says nothing the first half didn't.
    for cat in CATEGORIES:
        for row in cat["vocab"]:
            for lang in LANGS:
                parts = [part.strip() for part in row[lang].split("/")]
                assert len(parts) == len(set(parts)), (cat["id"], lang, row[lang])


def test_no_headword_twice_on_the_poster():
    # Every row should teach something new, so a word lives on one card only.
    counts = Counter(row["en"] for cat in CATEGORIES for row in cat["vocab"])
    assert not [en for en, n in counts.items() if n > 1]


def test_no_two_rows_are_the_same_word_under_two_names():
    # "to go up" and "to get on" were subir / subir / salire / monter twice over.
    seen = {}
    for cat in CATEGORIES:
        for row in cat["vocab"]:
            key = (row["es"], row["pt"], row["it"], row["fr"])
            assert key not in seen, (seen.get(key), cat["id"], row["en"])
            seen[key] = (cat["id"], row["en"])


def test_spanish_is_latin_american():
    peninsular = re.compile(
        r"\b(coger|zumo|patatas?|ordenador|aparcar|aparcamiento|vaqueros|gafas|jersey"
        r"|bañador|cremallera|nevera|tarta|enhorabuena|visado|altavoz|maletero"
        r"|matrícula|neumático|ratón|portátil|auriculares|vosotros)\b",
        re.IGNORECASE,
    )
    for cat in CATEGORIES:
        for row in cat["vocab"] + cat["phrases"] + [cat["titles"]]:
            assert not peninsular.search(row["es"]), (cat["id"], row["es"])
