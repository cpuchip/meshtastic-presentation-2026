# Handout — source of truth

*The one-page take-home. Print target: US Letter, single side, black and white
on a cheap printer, ~50 copies. Print-ready page is `handout/handout.html` —
open it in Chrome and Ctrl-P. Every link here was opened and verified
2026-09-03; QR codes regenerate with `python scripts/make-qr.py`.*

**Rule this file inherits from `resources.md`: nothing goes on the handout we
haven't personally opened.**

---

## Off-Grid Communication with Meshtastic

**Ozarks Homesteading Expo · September 5, 2026 · Marshfield, MO**
Max Brixey · Michael Stufflebeam

> A $27 radio that texts your family for miles. No tower, no subscription,
> no licence, no monthly bill. Runs for days on a charge.

---

### Start here  `[QR: start-here]` `[QR: flasher]`

- **Learn it:** meshtastic.org/docs/getting-started/
- **Update your radio (in Chrome):** flasher.meshtastic.org
- **Use it from a browser:** client.meshtastic.org

### What to buy — prices checked Sept 3, 2026

| If you want… | Get | Cost |
|---|---|---|
| Zero effort — it just works | **SenseCAP T1000-E** (Meshtastic preinstalled, GPS, waterproof, credit-card size) | **$39.90** |
| Cheapest way on | **Heltec WiFi LoRa 32 V4** (antenna included; **no** battery or case) | **$26.97** |
| Cover the whole place | **SenseCAP Solar Node P1-Pro** (5 W solar + 18650s, pole-mount, weatherproof) | **$93.90** |

Where: seeedstudio.com · store.rokland.com · GigaParts · Amazon (2-pack kits
include case + battery)

**You and one other person, on the air, for about $80.** Less than a year of a
satellite-messenger subscription.

### The one hardware rule

**Screw the antenna on BEFORE you power it up.** Transmitting with no antenna
can damage the radio. Everything else is forgiving.

### Setup, start to finish

1. Charge it.
2. Update it — drag-and-drop (T1000-E) or flasher.meshtastic.org (Heltec).
3. Install the free Meshtastic app (iOS/Android) → pair over Bluetooth.
4. Set your region to **US**. Give the node a name you'll recognise.
5. You're on **LongFast**, the public channel. To go private: make a channel
   and share its QR with your family — that one is encrypted end to end.

### Is anyone out here?  `[QR: local-map]` `[QR: local-chat]`

**Yes.** Our regional network is **LZMesh (Southwest Missouri)** — about
**60 nodes live** on any given day.

- **Live map:** map.lzmesh.com
- **Community:** discord.lzarc.com

> ⚠ **If your node list looks empty, read this.** Most local nodes run a named
> channel — **`CHAOS JLN Main`** — not the stock LongFast. Being in range is not
> enough; you have to be on the same channel. Ask in their Discord for current
> settings before you decide the mesh is dead out here.

### When you want more

- **MeshCore** — same radios, planned repeaters instead of everyone-repeats.
  Tighter at scale, more setup. meshcore.co.uk
- **Reticulum** — a whole encrypted network stack over any radio. The deep end.
  reticulum.network
- **Ham radio** — voice, real power, repeaters, decades of infrastructure.
  Technician licence is a weekend of study. `[QR: hamstudy]`
  **Study free at hamstudy.org** (built by our friend Richard Bateman, KD7BBC).
  The FCC charges **$35** for the licence itself; studying costs nothing.
  *Meshtastic is the on-ramp. Ham is the highway. Plenty of us run both.*

### Do this today

## Buy two. Put one in a kid's backpack. Text them from the house.

---

**Find us after the talk:** `TODO — Michael's node name / contact`
· `TODO — Max's node name / contact`

*Everything on this sheet: github.com/cpuchip/meshtastic-presentation-2026*
