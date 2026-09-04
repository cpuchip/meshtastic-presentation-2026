"""Generate the handout's QR codes as SVG.

SVG on purpose: sharp at any print size and clean on a cheap black-and-white
printer, which is what a park pavilion handout gets printed on.

Run:  python scripts/make-qr.py
Regenerate whenever a link in notes/resources.md changes.
"""

import sys
from pathlib import Path

import qrcode
import qrcode.image.svg

sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).resolve().parent.parent / "assets" / "qr"

# slug -> (url, what it is on the handout)
LINKS = {
    "start-here":  ("https://meshtastic.org/docs/getting-started/", "Official getting-started docs"),
    "flasher":     ("https://flasher.meshtastic.org",               "Flash/update your radio in Chrome"),
    "local-map":   ("https://map.lzmesh.com",                       "LZMesh live local node map"),
    "local-chat":  ("https://discord.lzarc.com",                    "LZMesh community Discord"),
    "hamstudy":    ("https://hamstudy.org",                         "Free ham licence study"),
    # Board store pages. Amazon by ASIN: short, stable, and it dodges the
    # shipping surprise that makes a $39.90 vendor price arrive as $50.
    "buy-t1000e":  ("https://www.amazon.com/dp/B0DJ6KGXKB",          "SenseCAP T1000-E"),
    "buy-heltec":  ("https://www.amazon.com/dp/B0FY2WL3MN",          "Heltec V4 2-pack kit"),
    "buy-solar":   ("https://www.amazon.com/dp/B0FMDHBWX8",          "SenseCAP Solar Node P1-Pro"),
    "buy-seeed":   ("https://www.seeedstudio.com/SenseCAP-Solar-Node-P1-Pro-for-Meshtastic-LoRa-p-6412.html", "Solar node direct from Seeed (cheaper)"),
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, (url, label) in LINKS.items():
        qr = qrcode.QRCode(
            version=None,
            # High correction: handouts get folded, rained on, and set down on hay bales.
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
        path = OUT / f"{slug}.svg"
        img.save(str(path))
        print(f"  {path.name:16} {url}  ({label})")
    print(f"\n{len(LINKS)} QR codes -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
