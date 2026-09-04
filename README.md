# Meshtastic Presentation 2026

Source repo for the **"Off-Grid Communication with Meshtastic"** talk at the
[Ozarks Homesteading Expo](https://ozarkshomesteading.com/2026-homesteading-expo)
— **Saturday, September 5, 2026, 2:30 PM, Pavilion in Park, Marshfield MO** —
presented solo by Michael Stufflebeam. One hour, aimed at complete newcomers.
(The printed schedule still lists Max Brixey, who is no longer presenting.)

The delivered presentation gets adapted into
[cpuchip.net](https://github.com/cpuchip/cpuchip.net)'s presentations tab
(matching the site theme); this repo keeps the mesh-specific source, research,
and assets out of the site repo so it can be reused year to year.

## Layout

| Path | What |
|---|---|
| `notes/research.md` | Verified facts + sources (every claim checked against a live source, dated) |
| `notes/outline.md` | The one-hour talk structure + solo logistics checklist |
| `notes/resources.md` | The audience "where to go next" list — feeds the handout |
| `notes/handout.md` | The one-page take-home, in markdown — source of truth for its wording |
| `handout/handout.html` | **Print-ready handout.** Built; do not hand-edit. Open in Chrome → Ctrl-P |
| `handout/handout.template.html` | The handout's layout + `{{qr:slug}}` tokens — edit this |
| `scripts/make-qr.py` | Regenerates `assets/qr/*.svg` from the link list |
| `scripts/build-handout.py` | Inlines the QR SVGs into the template → `handout/handout.html` |
| `slides/slides.md` | Slide deck source (format-agnostic markdown, one `---` per slide) |
| `assets/images/` | Device photos (from the Meshtastic docs repo, GPL-3.0 — see SOURCES.md) |
| `reference/` | Shallow clones of meshtastic firmware + docs, MeshCore, Reticulum (gitignored) |

## Re-cloning the references

```sh
cd reference
git clone --depth 1 https://github.com/meshtastic/firmware
git clone --depth 1 https://github.com/meshtastic/meshtastic meshtastic-docs
git clone --depth 1 https://github.com/meshcore-dev/MeshCore
git clone --depth 1 https://github.com/markqvist/Reticulum
```

## Printing the handout

```sh
python scripts/make-qr.py        # only when a link changes
python scripts/build-handout.py  # -> handout/handout.html
```

Open `handout/handout.html` in Chrome, Ctrl-P, **Paper: Letter · Margins: Default ·
Background graphics: ON**. One page, single-sided, designed to survive a cheap
black-and-white printer. Target ~50 copies.

## Presenting offline

The venue is a park pavilion — assume no internet. The talk must run from a
local build (cpuchip.net `vite preview`, or a static export of the deck) and
survive with no screen at all: two live nodes and the printed handout carry the
core even if every pixel fails.
