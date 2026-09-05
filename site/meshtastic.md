---
title: "Off-Grid Communication with Meshtastic"
date: "2026-09-05"
event: "Ozarks Homesteading Expo · Marshfield, MO"
presenters: "Michael Stufflebeam"
---

# Off-Grid Communication<br>with Meshtastic

![Meshtastic](/images/presentations/meshtastic/meshtastic-logo.svg)

**Michael Stufflebeam**

Ozarks Homesteading Expo · September 5, 2026

---

# The storm takes the cell tower.

## How do you tell your family you're okay?

No power. No bars. No landline.

What's the plan - for the people on your own land?

---

# This is a $50 radio.

<div class="img-hero">

![SenseCAP T1000-E](/images/presentations/meshtastic/sensecap-t1000e.webp)

</div>

## No tower. No subscription. No license. Weeks on a charge.

---

# LoRa: a whisper that carries.

- Tiny messages, sent **slowly**, heard for **miles**
- Unlicensed band - 902–928 MHz, same legal territory as your garage remote
- Sips battery: **days to weeks** per charge

You give up voice and pictures. You get range and battery life that feel like magic.

---

# A mesh: every radio repeats what it hears.

{{diagram:mesh-hops}}

---

# Meshtastic: free, open-source firmware for cheap radios.

{{diagram:how-it-works}}

**It is NOT** voice, internet, or Starlink. It's texting, off-grid, done right.

---

# Why we do it.

## Several nodes. One 35-foot pole. Zero utility bills.

![Solar node on the flagpole](/images/presentations/meshtastic/solar-node-pole.webp)

- The solar node has run **untouched for months**
- Kid's backpack has a tracker on the family channel

---

# What it's good for out here

- **Family texting** across the property and into town
- **Hunting, hiking, trail rides** - GPS built in
- **Neighborhood resilience net** for storm days
- Later: gate sensors, tank levels, weather stations
- All of it keeps working **when the grid doesn't**

---

# Easiest start: SenseCAP T1000-E - $50

<div class="img-row">

![T1000-E](/images/presentations/meshtastic/sensecap-t1000e.webp)

</div>

- Credit-card size, waterproof, GPS
- **Meshtastic already installed** - charge it, pair it, done

**Buy:** [Amazon](https://www.amazon.com/dp/B0DJ6KGXKB) · [Seeed direct](https://www.seeedstudio.com/SenseCAP-Card-Tracker-T1000-E-for-Meshtastic-p-5913.html)

---

# The best value: Heltec V4 2-pack - $90

<div class="img-row">

![Heltec V4](/images/presentations/meshtastic/heltec-v4.webp)

</div>

- The hobbyist favorite, now with real power (27 dBm)
- Little screen, USB-C, no soldering
- **The kit is the deal:** 2 boards, 2 batteries, cases, antennas

**Buy:** [Amazon 2-pack kit](https://www.amazon.com/dp/B0FY2WL3MN) · [Bare board at Rokland](https://store.rokland.com/products/heltec-wifi-lora-32v4-esp32s3-sx1262-lora-node-meshtastic-lorawan)

---

# Set-and-forget: SenseCAP Solar Node <span style="white-space: nowrap">P1-Pro</span> - $140

<div class="img-row">

![SenseCAP Solar Node](/images/presentations/meshtastic/sensecap-solar-node.webp)

</div>

- 5W solar + four 18650 batteries, weatherproof
- Pole-mount it once, forget it
- **This is the one on our 35-ft pole**

**Buy:** [Amazon](https://www.amazon.com/dp/B0FMDHBWX8) · [Seeed direct](https://www.seeedstudio.com/SenseCAP-Solar-Node-P1-Pro-for-Meshtastic-LoRa-p-6412.html) · antenna upgrade: [ALFA 5 dBi](https://www.amazon.com/dp/B08H8J6ZV6) $19, LZMesh's pick

---

# The rabbit hole runs deep

<div class="img-grid">

![RAK WisBlock](/images/presentations/meshtastic/rak-wisblock.webp)
![LILYGO T-Deck](/images/presentations/meshtastic/lilygo-t-deck.webp)
![LILYGO T-Echo](/images/presentations/meshtastic/lilygo-t-echo.webp)
![Wio Tracker L1 Pro](/images/presentations/meshtastic/wio-tracker-l1.webp)
![WisMesh Pocket](/images/presentations/meshtastic/rak-wismesh-pocket.webp)
![A bare XIAO + Wio-SX1262 pair on foam with two flex antennas](/images/presentations/meshtastic/diy-xiao-wio-sx1262.webp)

</div>

**RAK WisBlock** modular builder · **T-Deck** no phone needed · **T-Echo** e-ink · [**Wio Tracker L1 Pro**](https://www.seeedstudio.com/Wio-Tracker-L1-Pro-p-6454.html) $60 with GPS · pocket nodes · or a **bare XIAO + Wio-SX1262** with two taped-on antennas, mine · 3D-printed cases, GitHub all the way down

---

# What it costs to start

| You want | Buy | Cost |
|---|---|---|
| Me and one other person | [Heltec V4 2-pack kit](https://www.amazon.com/dp/B0FY2WL3MN) | **$90** |
| The no-fuss option | 1× [SenseCAP T1000-E](https://www.amazon.com/dp/B0DJ6KGXKB) | **$50** |
| Cover the whole place | add a [solar node](https://www.amazon.com/dp/B0FMDHBWX8) on a pole | **+$140** |

## Less than a year of a satellite messenger subscription.

---

# Setup: the whole thing

<div class="split">

1. Charge it. **Antenna on before power.**
2. Update: drag-and-drop (T1000-E) or [flasher.meshtastic.org](https://flasher.meshtastic.org) (Heltec)
3. Phone app → pair → **check TWO settings: Region = US, Preset = LongFast.** That puts you on the public channel with everyone in range
4. Private family channel: scan one QR code. **Encrypted.**

![My carry node, a Wio Tracker L1 in a printed case: Role Client, US/LongFast, 906.875 MHz](/images/presentations/meshtastic/node-printed-case-screen.webp)

</div>

*My carry node, a Wio Tracker L1 in a printed case. Its screen says it all: Client, US/LongFast, 906.875 MHz.*

---

# Two questions, not one

## Can we **hear** each other? Can we **read** each other?

- **Hearing** = region + preset + frequency. The radio settings.
- **Reading** = channel name + key. The lock on the box.

| Preset | Frequency |
|---|---|
| LongFast | **906.875 MHz** |
| LongTurbo | **908.750 MHz** |

## 1.5 MHz apart. Same table. Zero contact.

Same room, different language: you hear nothing useful.
Different room: nothing helps. Get the radio settings right first.

---

# Renaming your main channel<br>changes your frequency.

- Meshtastic hashes your **primary** channel's name to pick the frequency slot
- Rename it and you quietly move off the air your neighbours are on
- Not a different chat room. A different **frequency**. No key will fix it

## Want privacy? Add a SECOND channel. Never rename the first.

---

# A node that cannot read your message<br>still carries it.

- The address is on the outside; only the contents are locked
- Your family channel gets the range of **everybody's** nodes
- Your node is carrying messages for people you have never met, right now

## Owning one is a contribution, not just a purchase.

Leave rebroadcast on **ALL**, role on **CLIENT**.
Router and Repeater are for pole nodes; a badly placed one makes the mesh worse.

---

# Height beats power.

{{diagram:height-wins}}

---

# Same radios, different philosophy: MeshCore

- Meshtastic: **everyone repeats** - simple, self-organizing
- MeshCore: **planned repeaters**, learned routes - tighter at scale, more setup
- Young and moving fast; worth watching

---

# Not a chat app: Reticulum

- Encrypted networking over **any** radio - LoRa, packet, WiFi, even the internet
- *"Not one network - a tool for building thousands of networks"*
- The deep end, for when you outgrow everything else

---

# The licensed path: ham radio + APRS

- Voice, real power, repeaters, decades of infrastructure
- Technician license = a weekend of study, one exam
- Study **FREE** at [hamstudy.org](https://hamstudy.org) - built by my friend Richard, KD7BBC
- Meshtastic is the on-ramp. Ham is the highway. **Run both.**

---

# Do this today

## Buy two. Put one in a kid's backpack.<br>Text them from the house.

[meshtastic.org/docs](https://meshtastic.org/docs/getting-started/) · [flasher.meshtastic.org](https://flasher.meshtastic.org) · [hamstudy.org](https://hamstudy.org) · [cpuchip.net/presentations](https://cpuchip.net/presentations/meshtastic)

**Our local mesh: [LZMesh](https://lzmesh.com)**, four states around us. The channel QR and their beginner guide are in the [Discord](https://discord.lzarc.com).

Grab a handout on your way out - every link is on it.

---

# Questions?

![The base station on the shelf: 18 of 21 nodes online on 906.875 MHz](/images/presentations/meshtastic/base-station.webp)

Find me after - I'll get your node on the mesh right here.
