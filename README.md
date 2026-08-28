# Polyglot Poster

Fifteen everyday situations on a wall sheet. Six equal columns:

```
English  ·  Spanish  ·  Portuguese  ·  Italian  ·  French  ·  Korean
```

Grid: **3 rows of 5**. Each card is washed in its own light color. Titles
are translated across all six languages.

Two sheets:

1. **Vocabulary** — ~60 words per situation
2. **Phrases** — three everyday sentences per situation

## The grid

| | | | | |
|---|---|---|---|---|
| Restaurant | Department store | Airport | Family | Hotel |
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

## Commands

```bash
python -m polyglot_poster poster -o output/polyglot-poster.pdf \
  --phrases output/polyglot-poster-phrases.pdf

python -m polyglot_poster ocr "/path/to/photos" -o data/ocr
```

Portuguese is Brazilian. Korean is polite informal (해요체). Service
phrases use the formal “you”; family and birthday use the familiar.

## License

MIT.
