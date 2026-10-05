# Polyglot Poster

Fifteen everyday situations on a wall sheet. Six equal columns:

```
English  ·  Spanish  ·  Portuguese  ·  Italian  ·  French  ·  Korean
```

Each card is washed in its own light color. Titles are translated across
all six languages.

Two sheets, each 72 × 42 in:

1. **Vocabulary** — one card per situation, **3 rows of 5**
2. **Phrases** — three everyday sentences per situation, **5 rows of 3**,
   set in the largest type at which every sentence still fits its row

## The grid

| | | | | |
|---|---|---|---|---|
| Restaurant | Department Store | Airport | Family | Hotel |
| Birthday | Grocery | Bank | Train | Body |
| Health | Car | Computers | Clothes | Weather |

## Setup

Python 3.10+ and [Tesseract](https://github.com/tesseract-ocr/tesseract)
if you want to OCR chapter photos.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
brew install tesseract          # macOS; optional, for OCR
```

Noto Sans (Latin + Korean) downloads into `fonts/` on the first poster build.

The same lexicon always writes the same bytes, so the PDFs in `output/`
only show up in `git status` when the poster itself changed.

## Commands

```bash
python -m polyglot_poster poster -o output/polyglot-poster.pdf \
  --phrases output/polyglot-poster-phrases.pdf

python -m polyglot_poster ocr "/path/to/photos" -o data/ocr
```

## Tests

```bash
pip install -e ".[dev]"
pytest
```

They check the lexicon (six languages everywhere, nothing listed twice) and
the layout (every character has a glyph, nothing spills out of its row).

Portuguese is Brazilian. Spanish is Latin American; where the region
itself disagrees (*ejotes*, *cajuela*, *cobija*) it takes the Mexican word.
Korean is polite informal (해요체). Service phrases use the formal “you”;
family and birthday use the familiar.

No headword appears twice: each of the 958 rows is a different word. Where
one French word has two meanings (*la glace*, *voler*, *la serviette*) each
meaning gets its own row.

## License

MIT.
