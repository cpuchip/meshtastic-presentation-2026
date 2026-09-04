# Handout - editorial record

*The exact wording lives in `../handout/handout.template.html`, which is the single
source of truth. This file records what is on the sheet, why, and what was verified,
so the two never drift apart.*

Print target: **US Letter, two sides, one sheet**, black and white on a cheap printer,
~50 copies. Build with:

```sh
python scripts/make-qr.py        # only when a link changes
python scripts/build-handout.py  # -> handout/handout.html
```

Then open `handout/handout.html` in Chrome, Ctrl-P, Paper: Letter, Background
graphics: ON.

## What is on the front

The what-it-is paragraph, the buy table, the antenna rule, and the five setup steps.
Nine QR codes total, each pointing at something we opened ourselves.

**The buy table uses Amazon prices on purpose.** A $39.90 vendor price arrives as $50
once shipping lands, and a handout that quotes the pre-shipping number makes us look
wrong in front of the person who bought one. Each row carries its own QR to that
product, so prices stay current even after this sheet is printed.

| Item | On the sheet | Verified 2026-09-04 |
|---|---|---|
| SenseCAP T1000-E | $50 | $50.99, in stock (ASIN B0DJ6KGXKB) |
| Heltec V4 2-pack complete kit | $90 | $89.99, in stock (ASIN B0FY2WL3MN). Two nodes, batteries, cases, antennas: about $45 a node |
| SenseCAP Solar Node P1-Pro | $140 | $139.99, in stock (ASIN B0FMDHBWX8) |
| Same solar node from Seeed direct | ~$115 delivered | $93.90 list. Worth its own QR: $25 is real money on the expensive item |

The Heltec 2-pack is the value pick and it lines up exactly with the closing
assignment (buy two), so it is called out as **Best value** rather than just listed.

## What is on the back

The channel material, which is the part beginners actually get wrong and the part
Michael flagged as his weak spot. Full research and sources: `channels.md`.

The back is built on one idea: **two questions, not one.** Can our radios hear each
other (region + preset + frequency), and can we read what we hear (channel name + key).
Everything else on that side hangs off it.

The load-bearing warnings:

1. **Renaming the primary channel changes your frequency.** A hash of the primary
   channel name picks the frequency slot, so renaming it silently moves you off the
   air your neighbours are on. This is the single most useful thing on the sheet.
2. **Get a private channel by adding a second one**, never by renaming the first.
3. **LongFast is not private.** Its key is published. Keep it anyway, for reach.
4. **Messages relay even when they cannot be read** (the header is in the clear), so a
   private family channel rides on strangers' radios and owning a node is a
   contribution.
5. **An empty node list is a settings mismatch, not a dead mesh.**

## Still open

- **Two placeholders in the footer**, marked bold on the sheet: Michael's and Max's
  node names / contact for "find us after the talk."
- Whether LZMesh's `CHAOS JLN Main` is a primary or a secondary channel changes the
  advice slightly. Asked in `channels.md`; worth a Discord question before Saturday.
