---
title: "Off-Grid Communication with Meshtastic"
date: "2026-09-05"
event: "Ozarks Homesteading Expo · Marshfield, MO"
presenters: "Max Brixey · Michael Stufflebeam"
---

# Off-Grid Communication<br>with Meshtastic

![Meshtastic](/images/presentations/meshtastic/meshtastic-logo.svg)

**Max Brixey · Michael Stufflebeam**

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

<!-- TODO: Michael's pole photo goes here -->

- The solar node has run **untouched for months**
- Coverage across the property and beyond
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
- Buy two: you're a network

---

# The best value: Heltec V4 2-pack - $90

<div class="img-row">

![Heltec V4](/images/presentations/meshtastic/heltec-v4.webp)

</div>

- The hobbyist favorite, now with real power (27 dBm)
- Little screen, USB-C, no soldering
- Amazon 2-packs with case + battery + antenna

---

# Set-and-forget: SenseCAP Solar Node - $70–100

<div class="img-row">

![SenseCAP Solar Node](/images/presentations/meshtastic/sensecap-solar-node.webp)

</div>

- 5W solar + four 18650 batteries, weatherproof
- Pole-mount it once, forget it
- **This is the one on our 35-ft pole**

---

# The rabbit hole runs deep

<div class="img-grid">

![RAK WisBlock](/images/presentations/meshtastic/rak-wisblock.webp)
![LILYGO T-Deck](/images/presentations/meshtastic/lilygo-t-deck.webp)
![LILYGO T-Echo](/images/presentations/meshtastic/lilygo-t-echo.webp)
![WisMesh Pocket](/images/presentations/meshtastic/rak-wismesh-pocket.webp)
![Heltec MeshPocket](/images/presentations/meshtastic/heltec-meshpocket.webp)
![muzi R1 Neo](/images/presentations/meshtastic/muzi-r1-neo.webp)

</div>

**RAK WisBlock** modular builder · **T-Deck** no phone needed · **T-Echo** e-ink · pocket nodes, 3D-printed cases, DIY antennas - GitHub all the way down

---

# What it costs to start

| You want | Buy | Cost |
|---|---|---|
| Me and one other person | Heltec V4 **2-pack kit** | **$90** |
| The no-fuss option | 1× SenseCAP T1000-E | **$50** |
| Cover the farm | add a solar node on a pole | **+$90–100** |

## Less than a year of a satellite messenger subscription.

---

# Setup: the whole thing

1. Charge it. **Antenna on before power.**
2. Update: drag-and-drop (T1000-E) or **flasher.meshtastic.org** (Heltec)
3. Phone app → pair → region **US**
4. You're on **LongFast** - the public channel - with everyone in range
5. Private family channel: scan one QR code. **Encrypted.**

---

# Can we hear each other?
# Can we read each other?

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

# Renaming your main channel
# changes your frequency.

- Meshtastic hashes your **primary** channel's name to pick the frequency slot
- Rename it and you quietly move off the air your neighbours are on
- Not a different chat room. A different **frequency**. No key will fix it

## Want privacy? Add a SECOND channel. Never rename the first.

---

# A node that cannot read your message
# still carries it.

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
- Study **FREE** at **hamstudy.org** - built by our friend Richard, KD7BBC
- Meshtastic is the on-ramp. Ham is the highway. **Run both.**

---

# Do this today

## Buy two. Put one in a kid's backpack.<br>Text them from the house.

**meshtastic.org/docs** · **flasher.meshtastic.org** · **hamstudy.org**

Grab a handout on your way out - every link is on it.

---

# Questions?

![Meshtastic](/images/presentations/meshtastic/meshtastic-logo.svg)

Find us after - we'll get your node on the mesh right here.
