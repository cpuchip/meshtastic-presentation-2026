# Outline - "Off-Grid Communication with Meshtastic" (working title)

**Ozarks Homesteading Expo · Saturday Sept 5, 2026 · 2:30 PM · Pavilion in Park**
Presenter: Michael Stufflebeam, solo (Max is no longer presenting). ~60 minutes
including Q&A.
Audience: homesteaders and self-reliance folks who know little or nothing about
Meshtastic. Goal: they leave knowing what it is, why it matters, what to buy
(under $100), and exactly where to go next.

Shape follows the curiosity structure: open with something they've *lived*,
explain the mechanism, land the click, end smaller.

---

## 1. The hook - when the towers go quiet (4 min)

Marshfield sits in tornado alley. Everyone in the room has lost power; most
have lost cell service. The question that opens the talk: **when the grid and
the towers are down, how do you tell your family you're okay?**

Then the reveal: a $50 radio that fits in a pocket, texts your family miles
away, needs no tower, no subscription, no license, and runs weeks on a battery.
Hold one up. (If the live demo is rehearsed: send a message across the pavilion
right now, first minute of the talk.)

## 2. What it is and how it works (7 min)

- **LoRa** in plain words: a whisper that carries. Tiny amounts of data, sent
  slowly, heard miles away. Same unlicensed band your garage door opener uses
  (902–928 MHz ISM - no license, legally, for anyone).
- **Mesh** in plain words: every node repeats what it hears. Your radio doesn't
  have to reach your neighbor directly - it hops. A bucket-brigade for text.
- Your phone connects by Bluetooth for the keyboard and screen; the radio does
  the long haul. Free app, iOS and Android. Encrypted by default.
- What it is NOT: not voice, not internet, not Starlink. Text and location,
  done extremely well, for almost nothing.

## 3. Why we do it - the lived story (5 min)

Michael's home mesh: several nodes, one on a 35-ft pole, a solar-powered
SenseCAP P1-Pro that has run untouched for months. Solo now, so there is room to
let this run. Use cases that land with this audience:

- Family off-grid texting (kids in the woods, spouse in town)
- Farm/property coverage where cell never reached
- Hunting, hiking, trail rides
- Neighborhood/community resilience net
- Sensors later: gate open, tank level, weather (mention, don't dwell)
- Storm-day comms when everything else is down

## 4. The hardware tour - what to buy (8 min)

One slide per tier, image-forward (all images in assets/):

1. **Easiest: SenseCAP T1000-E** - $50 delivered, credit-card size, GPS, waterproof,
   Meshtastic already installed. Charge it, pair it, done.
2. **Best value: Heltec V4 2-pack kit** - $90 (about $45 a node, batteries and
   cases included). Single board is $26.97 bare. The hobbyist favorite, now with
   real transmit power (27 dBm). 2-pack kits with case/battery/antenna on
   Amazon. (V3 still fine at ~$18 if you find one.)
3. **Set-and-forget: SenseCAP Solar Node P1-Pro** - $140 delivered ($115 direct
   from Seeed), solar +
   18650s, weatherproof, pole-mount. This is Michael's roof node. The
   "cover the whole farm" piece.
4. **Builder's row (one slide, fast):** RAK WisBlock (lowest power, modular),
   LILYGO T-Deck (standalone with keyboard - no phone), T-Echo (e-ink),
   Wio Tracker L1. DIY 3D-printed cases, the whole rabbit hole.
5. **The cost slide:** you and a partner on the air for $90; solar node +$140.
   Compare: one month of a satellite messenger subscription.

## 5. Setup, live (7 min)

Walk it on screen (screenshots as backup if no screen/no volunteer):

1. Buy → charge → **antenna on before power** (the one hardware rule).
2. Flash/update: T1000-E & friends = drag-and-drop like a USB stick;
   Heltec = flasher.meshtastic.org in Chrome. Nobody installs a toolchain.
3. Phone app → pair → set region **US** → you're on **LongFast**, the public
   channel, with everyone in range.
4. Name your node something memorable (the expo will remember a good one).
5. Make a **private family channel** - share the QR between phones; that
   channel is encrypted end-to-end.
6. Updates: same flasher, twice a year, optional.

## 6. Channels: what to set, and what not to touch (7 min)

*Michael's section. This is new, it is the highest-value seven minutes in the
talk, and it is the thing most likely to keep someone on the mesh past week one.
Full research and sources in [channels.md](channels.md).*

Build it on **one idea, then two consequences**:

**The idea: two questions, not one.**
- Can our radios *hear* each other? Region + preset + frequency.
- Can we *read* what we hear? Channel name + key.
- Same room, different language: you hear nothing useful. Different room:
  nothing helps. So get the radio settings right first.

**Consequence 1: renaming your main channel changes your frequency.**
Meshtastic hashes the *primary* channel's name to pick the frequency slot. Rename
it and you silently move off the air everyone else is on. This is the reason
people buy a radio, see an empty screen, and quit. Say it plainly, twice.
So: want privacy? **Add a second channel. Never rename the first.**

**Consequence 2: your private messages ride on strangers' radios.**
The header is unencrypted, so a node that cannot read your message still carries
it. Your family channel gets everyone's range, and your node is doing the same
for people you have never met. That reframes buying one as a contribution.

Then the practical close:
- LongFast is public (its key is in the docs). Keep it for reach.
- Private family channel = second channel, **random** key, share by QR.
- The QR *is* the key. Do not photograph it onto a slide or Facebook.
- Leave rebroadcast on ALL and role on CLIENT. Router/Repeater is a pole node's
  job, and a badly placed one hurts the mesh.

Callback to section 5: "region US" and "do not rename the primary" are the two
settings that decide whether any of this works.

**Optional 4th slide, marked CUT IF TIGHT: "does this broadcast my address?"**
No - the public channel blurs your position into a box roughly three miles across and sends
the center, and precision is set per channel. It answers a question this room
will actually have, and it has a true story attached (it fooled us this week).
If the section is running long, drop it and keep it in the Q&A pocket instead.
Full mechanism: [channels.md](channels.md).

## 7. What range actually looks like (4 min)

- Height beats power. The 35-ft pole story. A node in a window beats a node on
  a desk; a node on a pole beats both.
- Real expectations: line-of-sight miles are easy; Ozarks hollers and oak trees
  eat signal. Hilltop repeaters stitch a county together.
- Antenna matters more than the board. Stock antennas are fine to start.
- This is why mesh: you don't need range to everyone - just to somebody.

## 8. The wider world - one slide each (6 min)

- **MeshCore**: same radios, different philosophy - planned repeaters instead
  of everyone-repeats. Tighter at scale, more setup. Watch this space.
- **Reticulum**: not a chat app - a whole encrypted networking stack over any
  radio. The deep end, for when you outgrow everything else.
- **Ham radio + APRS**: the licensed path - voice, real power, repeaters,
  decades of infrastructure. Technician license is a weekend of study, and
  **hamstudy.org is free** - built by Michael's friend Richard, KD7BBC.
  Meshtastic is the on-ramp; ham is the highway. Many run both.

## 9. Start today + handout (4 min)

- The QR slide / printed handout: docs, flasher, buy links, local groups,
  hamstudy.org. (handout.md → print ~50 copies.)
- The one-sentence assignment: **buy two and play: leave one at home and see
  how far you get, or keep one in the car for emergencies.**
- Where to find us afterward.

## 10. Q&A (remainder, ~8 min)

Prepped answers: "Will I hear anyone out here?" (LZMesh ~60 live nodes; and my
own radio heard a stranger at one hop this week) · "Range on flat vs. hills?" · "Phone required?" (no - T-Deck, or
node-to-node canned messages) · "Legal?" (yes - ISM band) · "Privacy?" (AES
encrypted channels; LongFast is public) · "Solar longevity?" (Michael's P1-Pro
uptime).

---

## Solo logistics (Max is no longer presenting)

The whole hour is Michael's. What that changes:

- **No section split to negotiate.** The timings in this outline are now one
  person's pacing, not two. Sixty minutes of solo talking is real work: build in
  water, and let the live demo and the setup walk-through carry some of the load.
- **Max is in the room, just not presenting.** So there IS a second person for
  hands-on help: passing radios round, handing out sheets, catching a side question
  while Michael keeps the thread. Agree beforehand what he is picking up, so it happens
  by arrangement rather than improvisation.
- **But the talk itself is one voice.** Q&A still lands on Michael, and "I don't know,
  come find me after" is a fine answer. The Q&A pockets in [channels.md](channels.md)
  and [range-test.md](range-test.md) matter more now than when the hour was split.
- **The printed schedule still says "Max Brixey - Mashtastic Off-Grid
  Communication"** (their typo on Meshtastic too). Clear that up in the opening
  fifteen seconds so nobody thinks they are in the wrong room.
- **All demo nodes are Michael's**, which removes the "agree channel and node
  names beforehand" problem entirely. Everything is already on one mesh.

- [x] ~~Confirm what the pavilion has.~~ **CONFIRMED 2026-09-04: power and a TV
      screen.** Plan A is on.

### What a TV screen changes (it is not a projector)

- **A TV is smaller than a projector image.** The back row is the constraint. Anything
  that matters must survive being read from ~25 feet: prices, the two frequencies, the
  channel rules. Fine on our deck (big type, few words), but **do not add dense tables**.
- **Take the adapter and a spare.** Laptop to TV is HDMI; a pavilion TV may present
  HDMI only, and a dongle failure is a Plan B trigger with power sitting right there.
  Test the actual cable at home first.
- **Test it before the room fills.** Slot before ours ends at 2:30, so arrive early
  enough to plug in during the changeover, not during the talk.
- **Plan B still stands** and is now cheap insurance rather than the expected case:
  two radios and the printed handout carry the hour with no screen at all.
