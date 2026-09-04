# Slides - draft v0.1 (source of truth for the deck)

One `---`-separated block per slide. Format-agnostic on purpose: this adapts to
a cpuchip.net slide view, reveal.js, or print without rework. Images referenced
from `../assets/images/`. Speaker beats in *italics* under each slide are notes,
not slide text.

---

## SLIDE 1 - Title

# Off-Grid Communication with Meshtastic

**Max Brixey · Michael Stufflebeam** - Ozarks Homesteading Expo 2026

(mesh logo + a node photo on a fence post)

*While people settle: two live nodes on the table, messages flowing on screen
if there is one.*

---

## SLIDE 2 - The question

# The storm takes the cell tower.
# How do you tell your family you're okay?

*Everyone here has lost power. Most have lost bars. Landlines are gone. What's
your plan - for the people on your own land?*

---

## SLIDE 3 - The answer, held up in one hand

# This is a $50 radio.
### No tower. No subscription. No license. Weeks on a charge.

(photo: T1000-E next to a deck of cards)

*Send the live message across the pavilion here if rehearsed.*

---

## SLIDE 4 - What is LoRa?

# A whisper that carries.

- Tiny messages, sent slowly, heard for **miles**
- Unlicensed band (902–928 MHz) - same legal territory as your garage remote
- Battery sips: days to weeks per charge

*Trade-off framing: you give up voice and pictures; you get range and battery
that feel like magic.*

---

## SLIDE 5 - What is a mesh?

# Every radio repeats what it hears.

(diagram: house → hilltop node → neighbor; the middle node relaying)

- You don't need to reach everyone - just **somebody**
- More nodes = stronger network, automatically
- A bucket brigade for text messages

---

## SLIDE 6 - What Meshtastic actually is

# Free, open-source firmware for cheap radios.

- Your phone is the screen & keyboard (Bluetooth, free app, iOS/Android)
- Texts + GPS locations, **encrypted**
- The radio does the long haul - no internet anywhere in the loop

### No voice. No internet. No Starlink.
### Texting that works when nothing else does.

---

## SLIDE 7 - Why we do it (Michael)

# Several nodes. One 35-foot pole. Zero utility bills.

(image: solar-node-pole.webp - full bleed, portrait, node at the top clear
of the treeline)

- **SNST_cb53**, solar, on a 35-foot flagpole. No wires, no bill
- The base station has been up **82 days straight** on one charge
  (4.16 volts, still going)
- The kids' backpacks have trackers on the family channel
- **John down the street is one hop away.** That is the mesh, already working

*Those numbers are real, read off my own node this week. Say the reading, not
"months". The photo does the height argument for me, so do not narrate it.*

*Max's story here too - his slide, his words.*

---

## SLIDE 8 - What it's good for out here

- Family texting across the property & into town
- Hunting, hiking, trail rides - GPS built in
- Neighborhood resilience net for storm days
- Later: gate sensors, tank levels, weather stations
- All of it keeps working when the grid doesn't

---

## SLIDE 9 - Hardware tier 1: zero effort

# SenseCAP T1000-E - $50

(image: sensecap-t1000e.webp)

- Credit-card size, waterproof, GPS
- **Meshtastic already installed.** Charge, pair, done
- Buy two and you are a network

---

## SLIDE 10 - Hardware tier 2: the classic

# Heltec V4 2-pack - $90

(image: heltec-v4.webp)

- The hobbyist favorite, now with real power (27 dBm)
- Little screen, USB-C, no soldering
- **The kit is the deal: 2 boards, 2 batteries, cases, antennas.**
  About $45 a node, and it is exactly "buy two"

*Single board alone is $27 from Rokland, but you still need a battery
and a case, so the kit wins for a beginner.*

---

## SLIDE 11 - Hardware tier 3: set-and-forget

# SenseCAP Solar Node P1-Pro - ~$90–100

(image: sensecap-solar-node.webp)

- 5W solar + four 18650 batteries, weatherproof
- Pole-mount it once, forget it
- This is the one on Michael's pole
- **$115 direct from Seeed** if you can wait on shipping

---

## SLIDE 12 - The rabbit hole (one slide, fast)

(4-up: rak-wisblock.webp · lilygo-t-deck.webp · lilygo-t-echo.webp · wio-tracker-l1.webp)

- **RAK WisBlock** - modular, sips power, the serious solar builder's pick
- **T-Deck** - keyboard + screen, no phone needed
- **T-Echo** - e-ink, always-on readout
- 3D-printed cases, DIY antennas, GitHub all the way down

---

## SLIDE 13 - What it costs to start

| You want | Buy | Cost |
|---|---|---|
| Me and one other person | Heltec V4 **2-pack kit** | **$90** |
| The no-fuss option | 1× SenseCAP T1000-E | **$50** |
| Cover the whole place | + Solar node on a pole | **+$140** |

### Two of you on the air for $90. No bill after that.

*Delivered prices, checked this week. A satellite messenger costs more
than the 2-pack every single year you keep it.*

---

## SLIDE 14 - Setup: the whole thing

1. Charge it. **Antenna on before power.**
2. Update: drag-and-drop (T1000-E) or flasher.meshtastic.org (Heltec)
3. Phone app → pair → **check TWO settings:**
   ### Region = US.  Preset = LongFast.
4. That puts you on the public channel with everyone in range
5. Make a private family channel: scan one QR code. Encrypted.

*Two settings, not one. Region wrong = it never transmits. Preset wrong = it
transmits into an empty room. Both look like a dead radio to a beginner, and
I hit the second one on a new board this week.*

*Live-walk this on screen; screenshots as backup.*

---

## SLIDE 15 - Channels: two questions, not one

# Can we hear each other?
# Can we read each other?

- **Hearing** = region + preset + frequency. The radio settings.
- **Reading** = channel name + key. The lock on the box.

### On my own bench this week:

| Preset | Frequency |
|---|---|
| LongFast (all my old nodes) | **906.875 MHz** |
| LongTurbo (one new board) | **908.750 MHz** |

### 1.5 MHz apart. Same table. Zero contact.

*Same room, different language: you hear nothing useful. Different room:
nothing helps. Get the radio settings right first. This slide is the whole
section; the next two are just consequences.*

*If the room is quiet, this is the moment to hold up the new board and say it
found nobody sitting next to three working radios.*

---

## SLIDE 16 - The trap nobody warns you about

# Renaming your main channel
# changes your frequency.

- Meshtastic hashes your **primary** channel's name to pick the frequency slot
- Rename it and you quietly move off the air your neighbours are on
- Not a different chat room. A different **frequency**. No key will fix it

### Want privacy? Add a SECOND channel. Never rename the first.

*This is the one thing I most want them to walk out with. It is the reason
someone buys a radio, sees an empty screen, and gives up in week one.*

---

## SLIDE 17 - Your private messages ride on strangers' radios

# A node that cannot read your message still carries it.

- The address is on the outside; only the contents are locked
- So your family channel gets the range of **everybody's** nodes
- And your node is carrying messages for people you have never met, right now

### That is why owning one is a contribution, not just a purchase.

- Leave rebroadcast on **ALL**, role on **CLIENT**
- Do not set Router or Repeater because it sounds stronger. That is a pole
  node's job, and a badly placed one makes the mesh worse

*LongFast is public: its key is printed in the docs. Keep it for reach,
add a channel for privacy.*

---

## SLIDE 18 - Range: the honest slide

# Height beats power. Every time.

(callback to the pole photo from slide 7 - the node is above the treeline)

- Window beats desk; pole beats window; **hilltop beats everything**
- Miles line-of-sight is normal; hollers and oaks eat signal
- Don't need range to everyone - just to somebody (that's the mesh)
- Stock antenna is fine to start

---

## SLIDE 19 - The neighbors: MeshCore

# Same radios, different philosophy.

- Meshtastic: everyone repeats - simple, self-organizing
- MeshCore: planned repeaters, learned routes - tighter at scale, more setup
- Young and moving fast; worth watching

---

## SLIDE 20 - The neighbors: Reticulum

# Not a chat app - a whole network stack.

- Encrypted networking over ANY radio (LoRa, packet, WiFi, internet)
- "Not one network - a tool for building thousands of networks"
- The deep end, when you outgrow everything else

---

## SLIDE 21 - The neighbors: ham radio + APRS

# The licensed path: voice, power, repeaters.

- Technician license = a weekend of study, one exam
- Study **FREE**: **hamstudy.org** - built by our friend Richard, KD7BBC
- APRS has done position + messages for decades
- Meshtastic is the on-ramp. Ham is the highway. Run both.

---

## SLIDE 22 - Do this today

# Buy two. Put one in a kid's backpack. Text them from the house.

(QR codes: meshtastic.org/docs · flasher · handout PDF · hamstudy.org)

*Point to the printed handouts. Where to find us after.*

---

## SLIDE 23 - Q&A

# Questions?

(node map + both presenters' node names on screen)
