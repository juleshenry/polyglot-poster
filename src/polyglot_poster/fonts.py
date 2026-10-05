"""Download OFL Noto Sans (Latin + Korean) into ./fonts on first run."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = ROOT / "fonts"

FILES = {
    "NotoSans-Regular.ttf": "https://fonts.gstatic.com/s/notosans/v42/o-0mIpQlx3QUlC5A4PNB6Ryti20_6n1iPHjcz6L1SoM-jCpoiyD9A99d.ttf",
    "NotoSans-Bold.ttf": "https://fonts.gstatic.com/s/notosans/v42/o-0mIpQlx3QUlC5A4PNB6Ryti20_6n1iPHjcz6L1SoM-jCpoiyAaBN9d.ttf",
    "NotoSansKR-Regular.ttf": "https://fonts.gstatic.com/s/notosanskr/v39/PbyxFmXiEBPT4ITbgNA5Cgms3VYcOA-vvnIzzuoyeLQ.ttf",
    "NotoSansKR-Bold.ttf": "https://fonts.gstatic.com/s/notosanskr/v39/PbyxFmXiEBPT4ITbgNA5Cgms3VYcOA-vvnIzzg01eLQ.ttf",
}


def _download(url: str, dest: Path) -> None:
    # Write beside the target and rename, so a dropped connection never
    # leaves a truncated font that the next run would trust.
    tmp = dest.with_name(dest.name + ".part")
    with urllib.request.urlopen(url, timeout=60) as resp, tmp.open("wb") as fh:
        shutil.copyfileobj(resp, fh)
    tmp.replace(dest)


def ensure_fonts() -> dict[str, Path]:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, url in FILES.items():
        dest = FONT_DIR / name
        if not dest.exists() or dest.stat().st_size < 10_000:
            _download(url, dest)
        paths[name] = dest
    return paths
