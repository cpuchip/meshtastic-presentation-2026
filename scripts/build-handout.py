"""Build the print-ready handout by inlining QR SVGs into the template.

Same idiom as sync-to-site.py's {{diagram:name}} tokens: the template carries
{{qr:slug}} placeholders, and each resolves to the matching SVG in assets/qr/.
Inlined rather than <img>-linked so the finished handout is ONE file that
prints correctly from a thumb drive, a phone, or a library computer.

Run:  python scripts/make-qr.py && python scripts/build-handout.py
Fails loudly if a token does not resolve or a QR file is missing.
"""

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "handout" / "handout.template.html"
OUTPUT = ROOT / "handout" / "handout.html"
QR_DIR = ROOT / "assets" / "qr"

TOKEN = re.compile(r"\{\{qr:([a-z0-9-]+)\}\}")


def load_qr(slug: str) -> str:
    path = QR_DIR / f"{slug}.svg"
    if not path.is_file():
        raise SystemExit(f"FAIL: no QR for '{slug}' at {path}\n       run: python scripts/make-qr.py")
    svg = path.read_text(encoding="utf-8")
    # Drop the XML prolog/doctype; an inline SVG in HTML must not carry them.
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg, flags=re.I)
    # Let CSS size it; the generator hardcodes mm dimensions we don't want.
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return svg.strip()


def main() -> int:
    if not TEMPLATE.is_file():
        print(f"FAIL: template not found at {TEMPLATE}")
        return 1

    html = TEMPLATE.read_text(encoding="utf-8")
    used: list[str] = []

    def sub(m: re.Match) -> str:
        slug = m.group(1)
        used.append(slug)
        return load_qr(slug)

    html = TOKEN.sub(sub, html)

    leftover = TOKEN.search(html)
    if leftover:
        print(f"FAIL: unresolved token {leftover.group(0)}")
        return 1

    OUTPUT.write_text(html, encoding="utf-8", newline="\n")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built {OUTPUT.relative_to(ROOT)}  ({size_kb:.0f} KB)")
    print(f"  inlined {len(used)} QR codes: {', '.join(used)}")
    print("\nTo print: open handout/handout.html in Chrome, Ctrl-P,")
    print("  Paper = Letter, Margins = Default, Background graphics = ON.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
