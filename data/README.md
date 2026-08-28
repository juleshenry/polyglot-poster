Drop chapter photos here when running OCR:

```
python -m polyglot_poster ocr "/path/to/input-heic's" -o data/ocr
```

`IMG_1502` has page 10 folded over the left edge of page 9, upside down.
The OCR command rotates that flap 180° and writes `IMG_1502.flap.txt`.
