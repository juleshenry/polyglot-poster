"""Read HEIC photos of French textbook pages.

Pages were shot on a leather sofa, often rotated. IMG_1502 has the top
of page 10 folded over the left edge of page 9, and that flap is upside
down — we OCR it a second time after a 180° rotation.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except ImportError:
    register_heif_opener = None  # type: ignore

import pytesseract

IMAGE_EXTS = {".heic", ".heif", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def _open(path: Path) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    return img.convert("RGB")


def _ocr(img: Image.Image, psm: int = 6) -> str:
    return pytesseract.image_to_string(img, lang="fra+eng", config=f"--psm {psm}")


def _best_rotation(img: Image.Image) -> tuple[Image.Image, int, str]:
    """Try 0/90/180/270 and keep the rotation with the most letters."""
    best_img, best_rot, best_text, best_score = img, 0, "", -1
    for rot in (0, 90, 180, 270):
        candidate = img.rotate(-rot, expand=True) if rot else img
        text = _ocr(candidate)
        letters = sum(ch.isalpha() for ch in text)
        if letters > best_score:
            best_img, best_rot, best_text, best_score = candidate, rot, text, letters
    return best_img, best_rot, best_text


def ocr_file(path: Path) -> dict:
    path = Path(path)
    img = _open(path)
    oriented, rotation, text = _best_rotation(img)
    result = {
        "file": path.name,
        "rotation_degrees": rotation,
        "text": text.strip(),
        "flap_upside_down": None,
    }
    if "1502" in path.stem:
        # Folded header strip of page 10, photographed upside down.
        flap = oriented.crop((0, 0, max(1, oriented.width // 4), oriented.height))
        flap180 = flap.rotate(180, expand=True)
        result["flap_upside_down"] = _ocr(flap180, psm=6).strip()
    return result


def ocr_dir(src: Path, dest: Path | None = None) -> list[dict]:
    src = Path(src)
    files = sorted(
        p for p in src.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )
    if not files:
        raise FileNotFoundError(f"no images in {src}")
    rows = [ocr_file(p) for p in files]
    if dest:
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "ocr.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        for row in rows:
            stem = Path(row["file"]).stem
            (dest / f"{stem}.txt").write_text(row["text"] + "\n", encoding="utf-8")
            if row.get("flap_upside_down"):
                (dest / f"{stem}.flap.txt").write_text(
                    row["flap_upside_down"] + "\n", encoding="utf-8"
                )
    return rows
