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
        for row in cat["vocab"] + cat["phrases"]:
            assert list(row) == list(LANGS) or set(row) >= set(LANGS)
