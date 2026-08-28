"""Download OFL Noto Sans (Latin + Korean) into ./fonts on first run."""

from __future__ import annotations

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


def ensure_fonts() -> dict[str, Path]:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, url in FILES.items():
        dest = FONT_DIR / name
        if not dest.exists() or dest.stat().st_size < 10_000:
            urllib.request.urlretrieve(url, dest)
        paths[name] = dest
    return paths
