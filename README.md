# Polyglot Poster

OCR photos of a French textbook, fill the holes, and hang the result on a wall:
six languages in one 3×5 grid.

```
English  ·  Spanish  ·  Portuguese  ·  Italian  ·  French  ·  Korean
```

The source pages are torn leaves from *French: A Self-Teaching Guide*,
photographed as HEIC files. Thirteen categories come straight off those
pages. Two more — **clothes** and **weather & time** — are added because
the book never taught a wardrobe or the forecast, and you need both the
moment you step outside.

## The grid

| | | |
|---|---|---|
| Au restaurant | Au grand magasin | À l'aéroport |
| La famille | À l'hôtel | Une fête d'anniversaire |
| L'épicerie du coin | À la banque | À la gare |
| Les parties du corps | Santé et toilette | La voiture |
| L'informatique | **Les vêtements** *(added)* | **Le temps qu'il fait** *(added)* |

Each card: a color title, a vocab table in the six-language column order,
then **three** everyday sentences translated across the same columns.
French is the source column (tinted).

`IMG_1502` has page 10 folded over the left edge of page 9, upside down.
The OCR path rotates that flap 180°; the function words on it (`déjà`,
`maintenant`, `depuis`) land in the weather & time card.

## Setup

Needs Python 3.10+, [Tesseract](https://github.com/tesseract-ocr/tesseract)
with French `fra` data, and a folder of chapter photos.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
brew install tesseract          # macOS
# French model, once:
curl -L -o /opt/homebrew/share/tessdata/fra.traineddata \
  https://github.com/tesseract-ocr/tessdata/raw/main/fra.traineddata
```

Noto Sans (Latin + Korean) downloads into `fonts/` on the first poster build.

## Commands

Render the 48×64 inch white-canvas poster:

```bash
python -m polyglot_poster poster -o output/polyglot-poster.pdf
```

OCR a folder of HEIC/JPEG pages (tries 0/90/180/270, keeps the rotation
with the most letters; special-cases the folded flap on `IMG_1502`):

```bash
python -m polyglot_poster ocr "/path/to/input-heic's" -o data/ocr
```

## Layout

- One page, 48 inches wide × 64 inches tall — a print-shop wall sheet.
- 3 columns × 5 rows of cards.
- Inside every card, rows are **English / Spanish / Portuguese / Italian / French / Korean**.
- Portuguese is Brazilian. Korean is polite informal (해요체). Service phrases use the formal “you”; family and birthday use the familiar.

## License

MIT. The textbook photographs are your copies; they are not shipped in this repo.
