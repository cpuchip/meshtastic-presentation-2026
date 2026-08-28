# Slides — draft v0.1 (source of truth for the deck)

One `---`-separated block per slide. Format-agnostic on purpose: this adapts to
a cpuchip.net slide view, reveal.js, or print without rework. Images referenced
from `../assets/images/`. Speaker beats in *italics* under each slide are notes,
not slide text.

---

## SLIDE 1 — Title

# Off-Grid Communication with Meshtastic

**Max Brixey · Michael Puchol** — Ozarks Homesteading Expo 2026

(mesh logo + a node photo on a fence post)

*While people settle: two live nodes on the table, messages flowing on screen
if there is one.*

---

## SLIDE 2 — The question

# The storm takes the cell tower.
# How do you tell your family you're okay?

*Everyone here has lost power. Most have lost bars. Landlines are gone. What's
your plan — for the people on your own land?*

---

## SLIDE 3 — The answer, held up in one hand

# This is a $40 radio.
### No tower. No subscription. No license. Weeks on a charge.

(photo: T1000-E next to a deck of cards)

*Send the live message across the pavilion here if rehearsed.*

---

## SLIDE 4 — What is LoRa?

# A whisper that carries.

- Tiny messages, sent slowly, heard for **miles**
- Unlicensed band (902–928 MHz) — same legal territory as your garage remote
- Battery sips: days to weeks per charge

*Trade-off framing: you give up voice and pictures; you get range and battery
that feel like magic.*

---

## SLIDE 5 — What is a mesh?

# Every radio repeats what it hears.

(diagram: house → hilltop node → neighbor; the middle node relaying)

- You don't need to reach everyone — just **somebody**
- More nodes = stronger network, automatically
- A bucket brigade for text messages

---

## SLIDE 6 — What Meshtastic actually is

# Free, open-source firmware for cheap radios.

- Your phone is the screen & keyboard (Bluetooth, free app, iOS/Android)
- Texts + GPS locations, **encrypted**
- The radio does the long haul — no internet anywhere in the loop

### It is NOT: voice · internet · Starlink. It's texting, off-grid, done right.

---

## SLIDE 7 — Why we do it (Michael)

# Several nodes. One 35-foot pole. Zero utility bills.

(photo: Michael's solar node on the pole — TODO take this photo)

- Solar node has run untouched for months
- Coverage across the property and beyond
- The kids' backpacks have trackers on the family channel

*Max's story here too — his slide, his words.*

---

## SLIDE 8 — What it's good for out here

- Family texting across the property & into town
- Hunting, hiking, trail rides — GPS built in
- Neighborhood resilience net for storm days
- Later: gate sensors, tank levels, weather stations
- All of it keeps working when the grid doesn't

---

## SLIDE 9 — Hardware tier 1: zero effort

# SenseCAP T1000-E — $40

(image: sensecap-t1000e.webp)

- Credit-card size, waterproof, GPS
- **Meshtastic already installed** — charge, pair, done
- Buy two: you're a network

---

## SLIDE 10 — Hardware tier 2: the classic

# Heltec V4 — $27

(image: heltec-v4.webp)

- The hobbyist favorite, now with real power (27 dBm)
- Little screen, USB-C, solder-free
- Amazon 2-packs with case + battery + antenna

---

## SLIDE 11 — Hardware tier 3: set-and-forget

# SenseCAP Solar Node P1-Pro — ~$90–100

(image: sensecap-solar-node.webp)

- 5W solar + four 18650 batteries, weatherproof
- Pole-mount it once, forget it
- This is the one on Michael's pole

---

## SLIDE 12 — The rabbit hole (one slide, fast)

(4-up: rak-wisblock.webp · lilygo-t-deck.webp · lilygo-t-echo.webp · wio-tracker-l1.webp)

- **RAK WisBlock** — modular, sips power, the serious solar builder's pick
- **T-Deck** — keyboard + screen, no phone needed
- **T-Echo** — e-ink, always-on readout
- 3D-printed cases, DIY antennas, GitHub all the way down

---

## SLIDE 13 — What it costs to start

| You want | Buy | Cost |
|---|---|---|
| Just me, joining a friend | 1× Heltec V4 | **$27** |
| Me + spouse/kid | 2× T1000-E | **~$80** |
| Cover the farm | + Solar node on a pole | **+$90–100** |

### Less than one year of a satellite messenger subscription.

---

## SLIDE 14 — Setup: the whole thing

1. Charge it. **Antenna on before power.**
2. Update: drag-and-drop (T1000-E) or flasher.meshtastic.org (Heltec)
3. Phone app → pair → region **US**
4. You're on **LongFast** — the public channel — with everyone in range
5. Make a private family channel: scan one QR code. Encrypted.

*Live-walk this on screen; screenshots as backup.*

---

## SLIDE 15 — Range: the honest slide

# Height beats power. Every time.

- Window beats desk; pole beats window; **hilltop beats everything**
- Miles line-of-sight is normal; hollers and oaks eat signal
- Don't need range to everyone — just to somebody (that's the mesh)
- Stock antenna is fine to start

---

## SLIDE 16 — The neighbors: MeshCore

# Same radios, different philosophy.

- Meshtastic: everyone repeats — simple, self-organizing
- MeshCore: planned repeaters, learned routes — tighter at scale, more setup
- Young and moving fast; worth watching

---

## SLIDE 17 — The neighbors: Reticulum

# Not a chat app — a whole network stack.

- Encrypted networking over ANY radio (LoRa, packet, WiFi, internet)
- "Not one network — a tool for building thousands of networks"
- The deep end, when you outgrow everything else

---

## SLIDE 18 — The neighbors: ham radio + APRS

# The licensed path: voice, power, repeaters.

- Technician license = a weekend of study, one exam
- Study **FREE**: **hamstudy.org** — built by our friend Richard, KD7BBC
- APRS has done position + messages for decades
- Meshtastic is the on-ramp. Ham is the highway. Run both.

---

## SLIDE 19 — Do this today

# Buy two. Put one in a kid's backpack. Text them from the house.

(QR codes: meshtastic.org/docs · flasher · handout PDF · hamstudy.org)

*Point to the printed handouts. Where to find us after.*

---

## SLIDE 20 — Q&A

# Questions?

(node map + both presenters' node names on screen)
