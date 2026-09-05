# Research — verified facts and sources

Every claim below was checked against the named source on 2026-08-28. Anything
marked ~ is approximate or was seen on a reseller page and should be re-checked
the week of the expo (prices move).

## The event

- **Ozarks Homesteading Expo — September 4–5, 2026, Marshfield, MO**
  (https://ozarkshomesteading.com/2026-homesteading-expo)
- **Our slot: Saturday Sept 5, 2:30 PM, Pavilion in Park** — listed as
  "Max Brixey — Mashtastic Off-Grid Communication" (their typo on Meshtastic too).
  **The schedule is out of date: Max is not presenting, Michael is, solo.** Worth
  clearing up in the first fifteen seconds on the day. Schedule image
  saved at `assets/expo-saturday-schedule-2026.png`. Blocks run 1:00 / 2:30 /
  4:00, so ~60–75 min usable with changeover.
- **Venue is a park pavilion** — plan for no reliable internet and possibly no
  projector. The presentation must run offline (local build of cpuchip.net or a
  static export), and a printed QR handout covers the "where do I go next"
  problem regardless of screens.

## Radio / regulatory basics (official Meshtastic docs, read locally in `reference/meshtastic-docs`)

- North America uses the **902–928 MHz ISM band**; max output **+30 dBm ERP**.
  No license required (unlicensed ISM operation). Source:
  `docs/about/overview/radio-settings.mdx`.
- Default radio preset is **LongFast**; after factory reset the radio sits on
  frequency slot 20, centered **906.875 MHz** (104 slots in the US at LongFast
  bandwidth). Same source.
- Channel names must match to communicate — the default public channel is
  `LongFast`. Source: `docs/configuration/radio/channels`.
- Flashing: **ESP32 boards** (Heltec) use the web flasher at
  **https://flasher.meshtastic.org** (Chrome/Edge, no toolchain).
  **nRF52 boards** (T1000-E, RAK, Wio Tracker, Solar Node) flash by
  **drag-and-drop UF2** — even easier. Web client: **https://client.meshtastic.org**.
- Community-supported high-power gear exists for licensed hams (e.g. Station G2,
  listed in the docs' hardware index as "for licensed ham operation") — a nice
  bridge line for the ham section.

## Hardware — the boards we'll show (images in `assets/images/`)

| Device | Price (verified) | Chips | Notes |
|---|---|---|---|
| **Heltec WiFi LoRa 32 V4** | **$26.97** (Rokland) | ESP32-S3 + SX1262 | ~27–28 dBm TX (vs ~20 on V3), OLED, pin-compatible with V3, needs firmware ≥2.7.20. The classic tinkerer entry. |
| Heltec V3 | ~$18 bare (Meshnology guide) | ESP32-S3 + SX1262 | The budget floor; superseded by V4 but everywhere. |
| **Seeed SenseCAP T1000-E Card Tracker** | **$39.90** (Seeed) | nRF52840 + LR1110 + AG3335 GPS | Credit-card size, IP65, buzzer, **ships with Meshtastic preloaded** — the "no soldering, no flashing" answer. |
| **Seeed SenseCAP Solar Node P1** | $69.90 launch (Hackster) | XIAO nRF52840 + Wio-SX1262 | 5W solar panel, 18650s, IPX6. |
| **Seeed SenseCAP Solar Node P1-Pro** | $89.90 launch; ~$100.99 seen July 2026 | + GNSS (GPS/GLONASS/Galileo) | 4×3350 mAh 18650s, 2 dBi rod antenna, 8–9 km open-area claim. **Michael runs one** — the 35-ft pole node. Wiki: https://wiki.seeedstudio.com/meshtastic_solar_node/ |
| Seeed Wio Tracker L1 | (check current) | nRF52840 + SX1262 | Tracker family, low power. |
| RAK WisBlock (RAK4631 kit) | (check current) | nRF52840 + SX1262 | Modular, lowest sleep power — the serious-solar-builder choice. |
| LILYGO T-Deck / T-Echo / T-Beam | (check current) | various | T-Deck = standalone keyboard device (no phone needed); T-Echo = e-ink; T-Beam = the old GPS classic. |

- Amazon carries a **Heltec V4 2-pack kit** (2 boards + 3000 mAh batteries +
  cases + antennas, ASIN B0FY2WL3MN) — the "one purchase, you and your spouse
  are on the mesh" answer. Price to re-check.
- Realistic entry cost story: **two T1000-Es ≈ $80** (Seeed gives 10% off at
  2+), or **the Heltec 2-pack kit**, or **one Heltec V4 + your phone ≈ $27**
  if a friend already has a node.
- Safety line every guide repeats: **never power a board without its antenna
  attached** — TX into no antenna can kill the radio chip.

## MeshCore (repo cloned at `reference/MeshCore`)

- Different philosophy from Meshtastic: **Meshtastic floods** (every node
  rebroadcasts; simple, self-organizing); **MeshCore routes** — first packet
  floods to discover a path, then the learned path is embedded in subsequent
  packets; falls back to flood if the route dies.
- **Device roles split**: *Companions* (end-user devices, do NOT relay) vs
  *Repeaters* (planned infrastructure that does). Better airtime and
  predictability at scale; less "it just works out of the box."
- Good comparison writeups: Austin Mesh (austinmesh.org/about/meshcore-vs-meshtastic),
  adrelien.com "I run both" (2026), meshamerica.com (2026-04-26).

## Reticulum (repo cloned at `reference/Reticulum`, README read this session)

- Not a LoRa firmware — a **cryptography-based networking stack** that runs
  over almost any medium (LoRa via RNode, packet radio, WiFi, serial, TCP over
  the internet). End-to-end encryption, initiator anonymity, multi-hop
  transport, runs in userland Python.
- Its own words: "Reticulum **is not** *one* network. It is **a tool** for
  building *thousands of networks*... Networks for the people."
- Apps: Sideband (phone/desktop messenger), MeshChat, NomadNet. Positioning for
  our talk: "the deep end — when you outgrow a chat app and want a whole
  independent network."

## Ham radio / APRS (the licensed path)

- **HamStudy.org** — flash cards + practice exams **developed by Richard
  Bateman, KD7BBC** (Michael's friend), sponsored by ICOM America; the same team
  built ExamTools for remote exam administration. Sources: arrl.org
  instruction-exam-practice-and-review; blog.hamstudy.org.
- Talk framing: Meshtastic = no license, low power, text only. A **Technician
  license** opens voice, real power, repeaters, APRS position/messaging on
  2m — and studying is free at hamstudy.org. (Verify current FCC exam/license
  fee before stating a number out loud.)
- APRS: the ham world's decades-old position + short-message network — the
  spiritual ancestor of what Meshtastic does unlicensed.

## Getting-started resources shortlist (candidates for the handout — see resources.md)

- Official docs: https://meshtastic.org/docs/getting-started/
- Web flasher: https://flasher.meshtastic.org · Web client: https://client.meshtastic.org
- Node map: https://meshmap.net (community-populated; only opted-in nodes show)
- Rokland beginner guide: store.rokland.com/pages/complete-beginners-guide-to-your-first-meshtastic-node
- Adrelien complete getting-started guide (2026): adrelien.com/meshtastic-the-complete-getting-started-guide/
- Seeed node deployment guide: seeedstudio.com/blog/2026/03/17/meshtastic-node-guide/
- Communities: r/meshtastic, Meshtastic Discord, forum at meshtastic.discourse.group
- YouTube: "Meshtastic For Dummies in 2026 — Heltec V4 Setup & Wio Tracker Build"
  (MN4YUHjJtrk); "Best Meshtastic Devices for Beginners (2026)" (N8OOw5HIfA8)
  — both surfaced top in 2026 searches; watch before endorsing on the handout.

## Local mesh — the "will I hear anyone out here?" answer (verified 2026-09-03)

**Yes, and we can prove it from our own radio.** Two independent lines of evidence:

**1. There is an organized regional mesh: LZMesh (SWMO).** Listed in the official
Meshtastic local-groups directory. Live regional node map at https://map.lzmesh.com
showed, on 2026-09-03: **59 nodes live, 284 in the last 24 hours, 2,239 over 90 days.**
Community Discord at https://discord.lzarc.com. The "LZ" is the historic **Lead-Zinc
(Tri-State) Mining District**, so the network's center of gravity is the Joplin corner —
but mapped nodes reach Springfield (~28 mi from Marshfield), Bolivar, and Buffalo.

> **SETTLED 2026-09-04 (see [lzmesh-channel-finding.md](lzmesh-channel-finding.md)):**
> LZMesh **does not rename the primary.** Their published setup keeps channel 0 blank
> with the default key, and puts `LZMesh` at index 1 as a *secondary*. They call channel 1
> their "Primary LZMesh network", meaning main/most-used, not Meshtastic's index-0 PRIMARY.
>
> **So a factory-fresh radio in Marshfield is already on their frequency.** Blank primary
> hashes to the same slot as stock. You *hear* LZMesh nodes with no changes at all; you
> add their channel only in order to *read* that traffic. This also explains the stranger's
> RAK4631 our own node heard at zero hops on stock LongFast.
>
> An earlier draft of this file claimed their nodes ran a named primary called
> `CHAOS JLN Main` and that range therefore was not enough. **That was wrong** and is
> struck. Where `CHAOS JLN Main` comes from is unresolved; JLN is the Joplin airport code,
> so it is plausibly a legacy or neighboring-group channel seen on the map. It is not in
> LZMesh's current published setup.

**2. Our own radio hears a stranger, unprompted.** Read off the demo node near Marshfield
on 2026-09-03, on the stock public LongFast channel: the node database held **6 nodes**,
and one of them is **not ours** — a RAK4631 heard **directly, zero hops**. Also present:
our SenseCAP Solar Node (the pole node), a Heltec Wireless Tracker, a T1000-E, and a Wio
Tracker L1.

So the honest stage answer is: *"Right now, on the default channel, my radio in Marshfield
hears a neighbor I've never met. Thirty miles west in Springfield there's a network of
about sixty live nodes. It's thin out here — and that's the argument for you getting one."*

Other Missouri groups (official directory): Missouri Mesh (missourimesh.org), MeshSTL —
St. Louis, Show Me Mesh — Jefferson City (mo-mesh.com), Kansas City Meshtastic Group.

## Prices re-verified 2026-09-03 (week-of check)

| Item | Repo said | Verified now | Source |
|---|---|---|---|
| SenseCAP T1000-E | $39.90 | **$39.90** — unchanged | Seeed product page |
| Heltec WiFi LoRa 32 V4 | $26.97 | **$26.97, in stock** at Rokland. Includes LoRa antenna; **no battery, no case**. Listed 28 ±1 dBm. | store.rokland.com |
| SenseCAP Solar Node P1-Pro | $89.90 launch / ~$100.99 seen | **$93.90** per Seeed's own datasheet dated 2026-08-06 | files.seeedstudio.com datasheet |

~~Deck slide 13's "$27 / ~$80 / +$90-100" tiers all still hold.~~ **Superseded 2026-09-04**:
all audience-facing prices moved to delivered Amazon figures ($50 / $90 / $140). Slide 10 should not imply the
$26.97 Rokland unit ships with a battery and case — the Amazon 2-pack kits do, that listing
does not.

**FCC amateur license application fee: $35** (Congressionally mandated, in force since
2022; covers new license, renewal, vanity call sign; administrative updates are free).
hamstudy.org itself remains free — the $35 is the FCC's fee, not a study cost.

## Open items

- [x] ~~Confirm with Max Brixey who covers what.~~ **Moot 2026-09-04: Max is no longer
      presenting.** The hour is Michael's, solo. All demo nodes are his, so there is no
      channel or node-name coordination either. See outline "Solo logistics".
- [x] ~~Re-verify all prices week-of.~~ Done 2026-09-03, table above.
- [x] ~~Watch/endorse the two YouTube candidates.~~ **Done 2026-09-04** via yt-dlp
      transcripts, read in full. Keep DoItYourselfDad, add Ham Radio Crash Course, cut
      GhostStrats on tone and monetisation. Verdicts in [resources.md](resources.md).
      Neither made the printed handout.
- [x] ~~Local mesh check.~~ Done 2026-09-03, section above.
- [x] ~~Verify current FCC license fee.~~ $35, confirmed.
- [x] ~~Decide the live-demo shape.~~ **DONE 2026-09-04: the preset A/B.** Positive arm
      (LongFast radio reaches the phone, DM and broadcast) plus a **negative control**
      (LongTurbo radio on the same table reaches nothing). All three arms run live today.
      Runbook with exact commands, the failure branch and a fallback:
      [demo-runbook.md](demo-runbook.md). Still needs one rehearsal pass.

## Antenna upgrade for the solar node (LZMesh Discord pick, relayed 2026-09-04)

- **ALFA Network AOA-915-5ACM**, 5 dBi omni outdoor, 902–928 MHz, 7 in tall, N-male
  connector. **$18.97 in stock, sold by Rokland via Amazon**, verified on the product page
  2026-09-04: https://www.amazon.com/dp/B08H8J6ZV6. Needs an N-female pigtail to the node's SMA cable; reviewers say seal
  the joint. Michael's Amazon history shows two ordered 2026-09-04. On slide 11 and the
  cpuchip.net take-home page.

## LZMesh Beginner Guide (PDF, 10 pp., by Jonathan Jones AF0EC/WRMK568; Michael received it in their Discord 2026-09-04)

Read in full 2026-09-04. Not hosted on lzmesh.com as far as a fetch of the front page shows; it
lives in the Discord, so the deck points there rather than redistributing it. What it says, and
where it corroborates the deck:
- LZMesh covers SW Missouri, SE Kansas, NE Oklahoma, NW Arkansas; started early 2025 by Chris
  ("Hoser"); Discord mid-2025; LZARC (LZ Amateur Radio Club) late 2025. They rely on MQTT as
  backup and aim for full RF coverage; "one more node instantly increases our coverage".
- Devices it recommends: RAK4631 + 19007/19003, Heltec V3, XIAO ESP32S3 + Wio-SX1262 ("Smallest
  and cheapest node available"); pre-built Wio L1 Pro, T1000-E, WisMesh Pocket v2, WisMesh Tag;
  with screens/keyboards T-Deck, NRF-TXT. Overlaps slides 9, 12 and the take-home page.
- Setup: antenna (IPEX) on before power (slide 14 step 1); flash the latest stable from the web
  flasher (step 2); Region = United States, "Use Preset", Long Range - Fast (step 3); Role Client,
  Rebroadcast All (slide 17); hops 5; node-info interval 3 h.
- Channels: LZMesh is added as a NEW channel with its own PSK (iOS steps say "Channel Role to
  Secondary"); channel 0 is not renamed. Confirms notes/lzmesh-channel-finding.md and the
  take-home page's worked example. The guide prints the channel PSK and the MQTT credentials
  (mqtt.lzmesh.com, root msh/LZ); those are public by their choice and are NOT copied here.
- Testing: send "Test" on LongFast; checkmark/"Acknowledged" = heard; slash/"Max Retransmission
  Reached" = nobody heard, "that's why you are here".
- Privacy FAQ: what a node sends (names, telemetry, location if enabled, node ID) and does not
  (WiFi credentials, IP addresses, disabled location).

## Battery life, honestly (checked 2026-09-04 after Michael flagged "weeks on a charge")

"Weeks on a charge" is true of the solar node and of nothing else on the deck. Now: "days".
- **T1000-E (700 mAh)**: Seeed's own spreadsheet, "T1000-E for Meshtastic Consumption Test and
  Battery Life Calculation" (linked from the product page; files.seeedstudio.com/wiki/SenseCAP/
  Meshtastic/), computes **1.93 days GPS off / 1.91 days GPS on** at US915 LongFast, 50 packets
  an hour, 12.05 mA baseline, 148.5 mA on transmit, 53 mA GPS. Seeed's Amazon comparison table
  says "2-4 Days". Owners: ~2 days GPS on, ~3 off, 5-7 in deep sleep (getupandgocamping.com);
  "about a day per charge with GPS on as an active client" (nodakmesh.org); "GPS off 5+, GPS on
  2-3" (r/meshtastic). Michael's own carry: 24-48 h. Deck says "about two days".
- **Heltec V4 kit (one 3000 mAh cell)**: Heltec's own test (wiki.heltec.org/news/heltec-v4-test-
  result) ran 2 x 3000 mAh in parallel with Bluetooth on for **46 h 40 min** at ~95 mA average,
  "roughly double the consumption measured with Bluetooth disabled"; below 3.45 V the ESP32
  reboots. One cell, Bluetooth on: about a day. Hexaspot's product page: "Expect 1-2 days on
  battery". nepamesh.com: Heltec V3 ~19 h on 1100 mAh, ~44 h with light sleep. Deck says
  "about a day; charge it nightly, or feed it a solar panel".
- **Wio Tracker L1 Pro (2000 mAh, nRF52)**: Seeed blog 2025-06-25 "up to 5 days"; Seeed's
  comparison table "5-7 Days".
- **Solar Node P1-Pro (4 x 3350 mAh + 5 W panel)**: Seeed's table "Unlimited, Solar Power".
  Amazon reviewer (FreeLancer75, 2026-03-11): 4.15 V -> 3.88 V over 16 days indoors with no sun;
  on a pole, 4.16-4.20 V constant through April. Michael's: months untouched. Deck says
  "indefinitely on solar".
- Why the gap: nRF52 sleeps at microamps; ESP32 boards with Bluetooth on idle at tens of mA.
  That is the real reason the T1000-E outlasts a Heltec on a smaller battery.

## Real emergencies, sourced (added talk day, appendix slides)

Ham radio:
- **Joplin tornado, 2011-05-22.** ARRL News 2011-05-25 "Radio Amateurs Assist American Red Cross,
  Served Agencies During Joplin Storm" and "ARES Stands Down After Joplin Storms": hams provided the
  only communication link between Freeman Hospital (Joplin) and hospitals in Springfield on Sunday
  night, stood down 9 AM Monday; the Red Cross Springfield-Joplin link plus the MSSU shelter link
  stayed open until Tuesday May 24 "as it was the only reliable method of communications"; Missouri
  SEC Ken Baremore W0KRB: "more than 1900 hours" through the EOC. Both arrl.org pages fetched.
- **Hurricane Maria, 2017.** ARRL "Force of 50" pages and the 2017 Hurricane Season AAR
  (arrl.org/files): the Red Cross asked ARRL for 50 volunteers; 465 volunteered; 22 deployed
  Sept 28 with Ham Aid kits for about 3 weeks; hospital VHF links (asked to cover 51 hospitals),
  power utility AEE crews, FEMA ESF-2 liaison at the PREOC, the Mayaguez team "the only emergency
  communication link from that city to San Juan"; 131 local hams at AEE technical plazas.
- **Hurricane Helene, 2024.** WIRED 2024-10-08 (Makena Kelly): Mt. Mitchell repeater at 6,600 ft,
  supply requests and road closures read over it, "Mom, your son is OK. No phone service. Happy
  birthday."; Thomas Witherspoon K4SWL (swling.com 2024-10-18): passed wellness checks, coordinated
  helicopter evacuations and supply drops via the N2GE repeater, handed handhelds to unlicensed
  neighbors; RARS statement 2024-10-09: Tar Heel Emergency Net activated at NCEM's request; Farmer
  et al. 2025 case study: all three WNC fiber trunks destroyed; a ham brought two radios to the
  iHeart Asheville studios on day one.

Meshtastic (thin, and honest about it):
- **Helene, after the fact.** Witherspoon, qrper.com 2024-10-24: neighbors wanted a permanent
  off-grid net; he planned Meshtastic test nodes, and the community chose a GMRS repeater for voice.
  Asheville Watchdog 2025-10-01: a year on, "many have radios, Starlink or Meshtastic devices".
  WTXL 2025-03-11: Jefferson County FL CERT proposes solar Meshtastic nodes on water towers, citing
  deployments in NC and TN after Helene (their claim, as reported). A LinkedIn post claiming a
  23-node Swannanoa mesh ran rescues during the storm is contradicted by Witherspoon's own account
  from Swannanoa and was NOT used.
- **Drills and tracking.** BuffaLoRa (N2WLS) 2025-09-14: fire company plus Civil Air Patrol drill,
  T1000-E trackers on a UTV and a light rescue truck in TAK_TRACKER role, positions on ATAK
  off-grid; the same setup at a Sept 2024 park drill. Cameron Highlands ARC 2026: LoRa APRS
  trackers (ham, not Meshtastic) in a real missing-hiker search.
- Not found with a source good enough for a slide: Meshtastic in the Jan 2025 LA fires (ARES LAX
  NE mentions "text-based coordination" without naming it).
