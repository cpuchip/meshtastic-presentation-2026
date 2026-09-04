# Research — verified facts and sources

Every claim below was checked against the named source on 2026-08-28. Anything
marked ~ is approximate or was seen on a reseller page and should be re-checked
the week of the expo (prices move).

## The event

- **Ozarks Homesteading Expo — September 4–5, 2026, Marshfield, MO**
  (https://ozarkshomesteading.com/2026-homesteading-expo)
- **Our slot: Saturday Sept 5, 2:30 PM, Pavilion in Park** — listed as
  "Max Brixey — Mashtastic Off-Grid Communication" (their typo). Schedule image
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
(Tri-State) Mining District**, so the network's centre of gravity is the Joplin corner —
but mapped nodes reach Springfield (~28 mi from Marshfield), Bolivar, and Buffalo.

> **The catch worth saying out loud on stage:** most LZMesh nodes run a named channel,
> **`CHAOS JLN Main`**, *not* the stock LongFast. Being in radio range is not enough —
> you have to be on the same channel to see anyone. This is the single most likely reason
> a newcomer gets a radio, sees an empty node list, and concludes "it doesn't work here."

**2. Our own radio hears a stranger, unprompted.** Read off the demo node near Marshfield
on 2026-09-03, on the stock public LongFast channel: the node database held **6 nodes**,
and one of them is **not ours** — a RAK4631 heard **directly, zero hops**. Also present:
our SenseCAP Solar Node (the pole node), a Heltec Wireless Tracker, a T1000-E, and a Wio
Tracker L1.

So the honest stage answer is: *"Right now, on the default channel, my radio in Marshfield
hears a neighbour I've never met. Thirty miles west in Springfield there's a network of
about sixty live nodes. It's thin out here — and that's the argument for you getting one."*

Other Missouri groups (official directory): Missouri Mesh (missourimesh.org), MeshSTL —
St. Louis, Show Me Mesh — Jefferson City (mo-mesh.com), Kansas City Meshtastic Group.

## Prices re-verified 2026-09-03 (week-of check)

| Item | Repo said | Verified now | Source |
|---|---|---|---|
| SenseCAP T1000-E | $39.90 | **$39.90** — unchanged | Seeed product page |
| Heltec WiFi LoRa 32 V4 | $26.97 | **$26.97, in stock** at Rokland. Includes LoRa antenna; **no battery, no case**. Listed 28 ±1 dBm. | store.rokland.com |
| SenseCAP Solar Node P1-Pro | $89.90 launch / ~$100.99 seen | **$93.90** per Seeed's own datasheet dated 2026-08-06 | files.seeedstudio.com datasheet |

Deck slide 13's "$27 / ~$80 / +$90–100" tiers all still hold. Slide 10 should not imply the
$26.97 Rokland unit ships with a battery and case — the Amazon 2-pack kits do, that listing
does not.

**FCC amateur licence application fee: $35** (Congressionally mandated, in force since
2022; covers new licence, renewal, vanity call sign; administrative updates are free).
hamstudy.org itself remains free — the $35 is the FCC's fee, not a study cost.

## Open items

- [ ] Confirm with **Max Brixey** who covers what (he's the listed presenter). *Still the
      longest pole — external dependency, and it gates the Plan A / Plan B decision.*
- [x] ~~Re-verify all prices week-of.~~ Done 2026-09-03, table above.
- [ ] Watch/endorse the two YouTube candidates before the handout goes to print.
      *Cannot be delegated to a text tool — someone has to actually watch them, or we cut
      them from the handout. Recommend cutting: the three written guides already cover it.*
- [x] ~~Local mesh check.~~ Done 2026-09-03, section above.
- [x] ~~Verify current FCC licence fee.~~ $35, confirmed.
- [ ] Decide the live-demo shape: two nodes messaging in the pavilion is cheap
      and reliable (no internet needed) — but rehearse it.
