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

What's the plan for the people on your own land?

---

# This is a $50 radio.

<div class="img-hero">

![SenseCAP T1000-E](/images/presentations/meshtastic/sensecap-t1000e.webp)

</div>

## No tower. No subscription. No license. Days on a charge.

---

# LoRa: a whisper that carries.

- Tiny messages, sent **slowly**, heard for **miles**
- Unlicensed band (902-928 MHz), the same legal territory as your garage remote
- Sips battery: **about two days** in your pocket, **indefinitely** on solar

You give up voice and pictures. You get miles of range from a radio in your shirt pocket.

---

# A mesh: every radio repeats what it hears.

{{diagram:mesh-hops}}

---

# Meshtastic: free, open-source firmware for cheap radios.

{{diagram:how-it-works}}

**It is NOT** voice, internet, or Starlink. It's texting that works when nothing else does.

---

# Why I do it.

## Several nodes. One 35-foot pole.

![Solar node on the flagpole](/images/presentations/meshtastic/solar-node-pole.webp)

- **It's a hobby.** I want to see how far I can connect
- **It's a public service.** The pole node extends the mesh toward Springfield and the rest of LZMesh
- The solar node up there has run **untouched for months**

---

# The network I'm extending: LZMesh

<div class="img-full">

![LZMesh live node map: southwest Missouri and the four-state corner, the morning of the talk](/images/presentations/meshtastic/lzmesh-map.webp)

</div>

**316 nodes heard in the last 24 hours** this morning, Joplin to Rolla and down into Arkansas. Marshfield sits in the thin stretch east of Springfield; filling it in is what my pole is for. Live at [map.lzmesh.com](https://map.lzmesh.com).

---

# What it's good for out here

- **Family texting** across the property and into town
- **Hunting, hiking, trail rides**, with GPS built in
- **Neighborhood resilience net** for storm days
- Later: gate sensors, tank levels, weather stations
- All of it keeps working **when the grid doesn't**

---

# Easiest start: SenseCAP T1000-E, $50

<div class="img-row">

![T1000-E](/images/presentations/meshtastic/sensecap-t1000e.webp)

</div>

- Credit-card size, waterproof, GPS
- **Meshtastic already installed**: charge it, pair it, done
- **About two days** per charge, by Seeed's own math and my own use. Charge it with your phone

**Buy:** [Amazon](https://www.amazon.com/dp/B0DJ6KGXKB) · [Seeed direct](https://www.seeedstudio.com/SenseCAP-Card-Tracker-T1000-E-for-Meshtastic-p-5913.html)

---

# The best value: Heltec V4 2-pack, $90

<div class="img-row">

![Heltec V4](/images/presentations/meshtastic/heltec-v4.webp)

</div>

- The hobbyist favorite, now with real power (27 dBm)
- Little screen, USB-C, no soldering
- **The kit is the deal:** 2 boards, 2 batteries, cases, antennas
- **About a day** on the kit battery. Charge it nightly, or feed it a solar panel

**Buy:** [Amazon 2-pack kit](https://www.amazon.com/dp/B0FY2WL3MN) · [Bare board at Rokland](https://store.rokland.com/products/heltec-wifi-lora-32v4-esp32s3-sx1262-lora-node-meshtastic-lorawan)

---

# Set-and-forget: SenseCAP Solar Node <span style="white-space: nowrap">P1-Pro</span>, $140

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

# Can we hear each other?<br>Can we read each other?

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
- Rename it and you quietly move off the air your neighbors are on
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

# Does this broadcast my address?

## No. It broadcasts a box about three miles across.

- On the public channel your position is **deliberately blurred**
- The default rounds you into a **box roughly three miles across** and sends its center
- Everyone at my house publishes the identical point, and so does anyone else inside the box

## Precision is per channel. On my family channel, I set it to exact.

---

# Height beats power.

{{diagram:height-wins}}

---

# Same radios, different philosophy: MeshCore

- Meshtastic: **everyone repeats**. Simple, and it organizes itself
- MeshCore: **planned repeaters** and learned routes. Tighter at scale, more setup
- Young and moving fast; worth watching

---

# Not a chat app: Reticulum

- Encrypted networking over **any** radio: LoRa, packet, WiFi, even the internet
- Their own words: *"Reticulum is not one network. It is a tool for building thousands of networks."*
- The deep end, for when you outgrow everything else

---

# The licensed path: ham radio + APRS

- Voice, real power, repeaters, decades of infrastructure
- Technician license = a weekend of study, one exam
- Study **FREE** at [hamstudy.org](https://hamstudy.org), built by my friend Richard, KD7BBC
- Meshtastic is the on-ramp. Ham is the highway. **Run both.**

---

# Do this today

## Buy two and play. Leave one at home and see how far you get.<br>Or keep one in the car for emergencies.

[meshtastic.org/docs](https://meshtastic.org/docs/getting-started/) · [flasher.meshtastic.org](https://flasher.meshtastic.org) · [hamstudy.org](https://hamstudy.org) · [cpuchip.net/presentations](https://cpuchip.net/presentations/meshtastic)

**Our local mesh: [LZMesh](https://lzmesh.com)**, four states around us. The channel QR and their beginner guide are in the [Discord](https://discord.lzarc.com).

Grab a handout on your way out: every link is on it.

---

# Questions?

![The base station on the shelf: 18 of 21 nodes online on 906.875 MHz](/images/presentations/meshtastic/base-station.webp)

Find me after. I'll get your node on the mesh right here.

---

# Appendix: for the questions

## Deeper answers, in case they come up.

- Ham radio and Meshtastic, side by side
- The walkie-talkies on the shelf: FRS, GMRS, MURS
- How the mesh actually decides who repeats
- Radio roles, and why the wrong one hurts everybody
- Using an AI to help you set up, and where it will lie to you
- When the towers went down: ham radio, and Meshtastic, in real emergencies
- Why now, and not during the emergency

---

# Ham radio and Meshtastic, side by side

| | Meshtastic | Ham radio |
|---|---|---|
| License | None. Unlicensed 902-928 MHz band | Technician exam, FCC fee $35, study free at hamstudy.org |
| Carries | Text and location | Voice, data, images, and APRS for position and messages |
| Encryption | On by default, per channel | Not allowed on ham bands, so hams running Meshtastic there turn it off |
| Power | Up to 30 dBm here, a fraction of a watt to one watt | A handheld runs about 5 watts; base stations far more |
| Infrastructure | Your own nodes, plus everyone else's | Repeaters on towers, maintained by clubs |
| Reach | Miles line of sight, farther through the mesh | A county through a repeater, the world on HF |

## Different tools. The people who run both have the most options when the towers go down.

---

# The walkie-talkies on the shelf: FRS, GMRS, MURS

| | FRS | GMRS | MURS | Meshtastic |
|---|---|---|---|---|
| License | None | $35 for ten years, no exam, covers your family | None | None |
| Band | 22 UHF channels, shared with GMRS | The same channels, plus repeater pairs | 5 VHF channels | 902-928 MHz, unlicensed |
| Power | 2 W, or 0.5 W on channels 8 to 14 | Up to 50 W | 2 W | Up to 30 dBm, about 1 W |
| Carries | Voice, some data | Voice, text and GPS | Voice or data | Text and location, encrypted |
| Repeaters | No | Yes, never internet-linked | No | Every node is one |
| Reach | Half a mile to two | 1 to 25 miles with a repeater | A few miles, more with an antenna | Miles line of sight, more through the mesh |

## They are voice; this is text. The blister-pack radio in your truck and a mesh node solve different halves of the same storm.

---

# How the mesh decides who repeats

- Every radio that hears a new packet **may** rebroadcast it, once
- The **farthest** listener goes first: weaker signal, shorter wait
- A radio that hears someone else's rebroadcast **stays quiet**
- Each hop counts down. **Default 3 hops**, never more than 7. Three is fine
- The sender counts a message as delivered when it hears **anyone** repeat it, even a stranger's node that cannot read it

## Managed flooding: no map, no central brain, and it still finds the way.

---

# Radio roles, and why the wrong one hurts everybody

| Role | What it does | Use it when |
|---|---|---|
| **CLIENT** | Repeats only when nobody else has. The default | Almost always. This is you |
| **CLIENT_MUTE** | Never repeats for others | A second radio in the same house, so only one talks |
| **CLIENT_BASE** | Always repeats for its favorited nodes | An attic radio backing up your weaker handhelds |
| **ROUTER** | Always repeats, once, first | A high, well-placed pole or hilltop node, and nothing else |
| **ROUTER_LATE** | Always repeats, but after everyone else | Filling a dead spot for a cluster |
| **REPEATER** | Router that hides from node lists | Infrastructure you do not want on the map |

## A ROUTER on a windowsill repeats everything, first, into a wall. Leave it on CLIENT unless you own the pole.

---

# Using an AI to help you set up

- **What works:** paste the exact screen or setting and ask why the radio finds nobody. Ask it to explain a setting before you change it
- **Keep the official docs open beside it.** meshtastic.org/docs is the source; the AI is the reader
- **It will state numbers confidently and wrong.** This deck had a battery life, a price and a privacy-cell size wrong until each was checked against the maker's page, the maker's spreadsheet and the firmware source
- Change **one setting at a time**, and never paste your private channel key into anything

## Ask it to explain. Make it show its source. You decide.

---

# When the towers went down: ham radio

- **Joplin, May 22, 2011.** The EF5 took the phone lines and the cell towers. That night, hams were the **only link between Freeman Hospital and the Springfield hospitals**, and between the Red Cross offices in Joplin and Springfield until Tuesday. More than 1,900 volunteer hours
- **Puerto Rico, Hurricane Maria, 2017.** The Red Cross asked for 50 hams; 22 flew in with radio kits for three weeks: **hospital links, the power utility's repair crews, FEMA liaison**, and the only link from Mayaguez to San Juan
- **Western North Carolina, Helene, 2024.** All three fiber trunks destroyed. One repeater on Mount Mitchell carried **supply requests, road closures, helicopter evacuations**, and "Mom, your son is OK. No phone service."

## The role, every time: the link between a hospital, a shelter or a family and the outside, when nothing else was one.

---

# When the towers went down: Meshtastic

- **Helene, 2024, honestly.** The neighborhoods that got through used voice radios and a repeater. Meshtastic came **after**: Swannanoa neighbors wanted a permanent off-grid net anyone could join without a license, and a Florida county's emergency team is now hanging **solar nodes on water towers** before the next storm
- **Search, rescue and fire drills.** A New York fire company tracked its UTV and rescue truck through the woods on **$50 card trackers**, positions landing on the team map with no cell service. The role: knowing where your people are when they are out of sight
- **Your street.** Text and positions for the household and the neighbors, no operator needed, while the licensed folks carry the hospital link

## The lesson from Helene: the mesh you build after the storm helps with the next one. Build it now.

---

# Why now, and not during the emergency

## Three is two. Two is one. One is none.

- The radio you configure during the storm is a brick. **Configure it on a sunny afternoon**
- A family channel you have never used is a plan, not a skill. **Text on it this week**
- The mesh only reaches you if you were already on it. **Every node added in good weather is range in bad**
- Drive a range test once, so you know the real number, not the box number

## Practice is the whole difference between a gadget and a plan.
