# Outline — "Off-Grid Communication with Meshtastic" (working title)

**Ozarks Homesteading Expo · Saturday Sept 5, 2026 · 2:30 PM · Pavilion in Park**
Presenters: Max Brixey + Michael. ~60 minutes including Q&A.
Audience: homesteaders and self-reliance folks who know little or nothing about
Meshtastic. Goal: they leave knowing what it is, why it matters, what to buy
(under $100), and exactly where to go next.

Shape follows the curiosity structure: open with something they've *lived*,
explain the mechanism, land the click, end smaller.

---

## 1. The hook — when the towers go quiet (5 min)

Marshfield sits in tornado alley. Everyone in the room has lost power; most
have lost cell service. The question that opens the talk: **when the grid and
the towers are down, how do you tell your family you're okay?**

Then the reveal: a $30–40 radio that fits in a pocket, texts your family miles
away, needs no tower, no subscription, no license, and runs weeks on a battery.
Hold one up. (If the live demo is rehearsed: send a message across the pavilion
right now, first minute of the talk.)

## 2. What it is and how it works (8 min)

- **LoRa** in plain words: a whisper that carries. Tiny amounts of data, sent
  slowly, heard miles away. Same unlicensed band your garage door opener uses
  (902–928 MHz ISM — no license, legally, for anyone).
- **Mesh** in plain words: every node repeats what it hears. Your radio doesn't
  have to reach your neighbor directly — it hops. A bucket-brigade for text.
- Your phone connects by Bluetooth for the keyboard and screen; the radio does
  the long haul. Free app, iOS and Android. Encrypted by default.
- What it is NOT: not voice, not internet, not Starlink. Text and location,
  done extremely well, for almost nothing.

## 3. Why we do it — the lived story (7 min)

Michael's home mesh: several nodes, one on a 35-ft pole, a solar-powered
SenseCAP P1-Pro that has run untouched for months. Max's story (his section —
coordinate). Use cases that land with this audience:

- Family off-grid texting (kids in the woods, spouse in town)
- Farm/property coverage where cell never reached
- Hunting, hiking, trail rides
- Neighborhood/community resilience net
- Sensors later: gate open, tank level, weather (mention, don't dwell)
- Storm-day comms when everything else is down

## 4. The hardware tour — what to buy (10 min)

One slide per tier, image-forward (all images in assets/):

1. **Easiest: SenseCAP T1000-E** — $39.90, credit-card size, GPS, waterproof,
   Meshtastic already installed. Charge it, pair it, done.
2. **Classic tinkerer: Heltec V4** — $26.97, the hobbyist favorite, now with
   real transmit power (27 dBm). 2-pack kits with case/battery/antenna on
   Amazon. (V3 still fine at ~$18 if you find one.)
3. **Set-and-forget: SenseCAP Solar Node P1 / P1-Pro** — $70–100, solar +
   18650s, weatherproof, pole-mount. This is Michael's roof node. The
   "cover the whole farm" piece.
4. **Builder's row (one slide, fast):** RAK WisBlock (lowest power, modular),
   LILYGO T-Deck (standalone with keyboard — no phone), T-Echo (e-ink),
   Wio Tracker L1. DIY 3D-printed cases, the whole rabbit hole.
5. **The cost slide:** get on the mesh for $27; you + a partner for ~$80.
   Compare: one month of a satellite messenger subscription.

## 5. Setup, live (10 min)

Walk it on screen (screenshots as backup if no screen/no volunteer):

1. Buy → charge → **antenna on before power** (the one hardware rule).
2. Flash/update: T1000-E & friends = drag-and-drop like a USB stick;
   Heltec = flasher.meshtastic.org in Chrome. Nobody installs a toolchain.
3. Phone app → pair → set region **US** → you're on **LongFast**, the public
   channel, with everyone in range.
4. Name your node something memorable (the expo will remember a good one).
5. Make a **private family channel** — share the QR between phones; that
   channel is encrypted end-to-end.
6. Updates: same flasher, twice a year, optional.

## 6. Range reality — the honest slide (5 min)

- Height beats power. The 35-ft pole story. A node in a window beats a node on
  a desk; a node on a pole beats both.
- Real expectations: line-of-sight miles are easy; Ozarks hollers and oak trees
  eat signal. Hilltop repeaters stitch a county together.
- Antenna matters more than the board. Stock antennas are fine to start.
- This is why mesh: you don't need range to everyone — just to somebody.

## 7. The wider world — one slide each (8 min)

- **MeshCore**: same radios, different philosophy — planned repeaters instead
  of everyone-repeats. Tighter at scale, more setup. Watch this space.
- **Reticulum**: not a chat app — a whole encrypted networking stack over any
  radio. The deep end, for when you outgrow everything else.
- **Ham radio + APRS**: the licensed path — voice, real power, repeaters,
  decades of infrastructure. Technician license is a weekend of study, and
  **hamstudy.org is free** — built by Michael's friend Richard, KD7BBC.
  Meshtastic is the on-ramp; ham is the highway. Many run both.

## 8. Start today + handout (5 min)

- The QR slide / printed handout: docs, flasher, buy links, local groups,
  hamstudy.org. (handout.md → print ~50 copies.)
- The one-sentence assignment: **buy two, put one in a kid's backpack, and
  text them from the house.**
- Where to find us afterward.

## 9. Q&A (remainder, ~10 min)

Prepped answers: "Will I hear anyone out here?" (local mesh status — research
open item) · "Range on flat vs. hills?" · "Phone required?" (no — T-Deck, or
node-to-node canned messages) · "Legal?" (yes — ISM band) · "Privacy?" (AES
encrypted channels; LongFast is public) · "Solar longevity?" (Michael's P1-Pro
uptime).

---

## Coordination with Max

- [ ] Split sections — suggestion: Max opens (hook + why), Michael runs
      mechanism + hardware + setup, both on Q&A.
- [ ] Who brings which demo nodes; agree channel + node names beforehand.
- [ ] Confirm what the pavilion actually has: screen? power? Plan A (screen) /
      Plan B (radios + handouts only — the talk must survive with no slides).
