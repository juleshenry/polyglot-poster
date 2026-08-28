"""Command line: ocr photos, then print the wall poster."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from polyglot_poster.lexicon import CATEGORIES, validate


def _cmd_poster(args: argparse.Namespace) -> int:
    from polyglot_poster.poster import render, render_phrases

    validate()
    out = Path(args.output)
    n = sum(len(c["vocab"]) for c in CATEGORIES)
    render(out)
    print(f"wrote {out}  ({n} words, 15 categories, 3 rows × 5)")
    if args.phrases:
        phrases_out = Path(args.phrases)
        render_phrases(phrases_out)
        print(f"wrote {phrases_out}  (3 phrases × 15)")
    return 0


def _cmd_phrases(args: argparse.Namespace) -> int:
    from polyglot_poster.poster import render_phrases

    validate()
    out = Path(args.output)
    render_phrases(out)
    print(f"wrote {out}  (3 phrases × 15)")
    return 0


def _cmd_ocr(args: argparse.Namespace) -> int:
    from polyglot_poster.ocr import ocr_dir

    rows = ocr_dir(Path(args.input), Path(args.output) if args.output else None)
    for row in rows:
        n = len(row["text"])
        extra = ""
        if row.get("flap_upside_down"):
            extra = f"  flap={len(row['flap_upside_down'])} chars"
        print(f"{row['file']}: rot={row['rotation_degrees']}  {n} chars{extra}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="polyglot-poster",
        description="OCR French textbook photos into a six-language wall poster (3 rows of 5).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_poster = sub.add_parser("poster", help="render the dense vocabulary wall sheet")
    p_poster.add_argument(
        "-o",
        "--output",
        default="output/polyglot-poster.pdf",
        help="PDF path (default: output/polyglot-poster.pdf)",
    )
    p_poster.add_argument(
        "--phrases",
        default="output/polyglot-poster-phrases.pdf",
        help="also write the companion phrases sheet (default: output/polyglot-poster-phrases.pdf)",
    )
    p_poster.set_defaults(func=_cmd_poster)

    p_phrases = sub.add_parser("phrases", help="render only the companion phrases sheet")
    p_phrases.add_argument(
        "-o",
        "--output",
        default="output/polyglot-poster-phrases.pdf",
        help="PDF path",
    )
    p_phrases.set_defaults(func=_cmd_phrases)

    p_ocr = sub.add_parser("ocr", help="OCR a folder of HEIC/JPEG chapter photos")
    p_ocr.add_argument("input", help="folder of photos (HEIC, JPEG, PNG)")
    p_ocr.add_argument("-o", "--output", default="data/ocr", help="where to write ocr.json")
    p_ocr.set_defaults(func=_cmd_ocr)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
