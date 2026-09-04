# Resources — the "point the way" list

The audience-facing shortlist. This file feeds the handout and the final slide.
Rule: nothing goes on the handout we haven't personally opened; YouTube picks
get watched before we endorse them (open item in research.md).

## Start here (the big three)

| What | Where |
|---|---|
| Official docs — start to finish | https://meshtastic.org/docs/getting-started/ |
| Flash/update your radio (Chrome) | https://flasher.meshtastic.org |
| Use it from a browser | https://client.meshtastic.org |

## Buy your first node

- **Zero-effort**: Seeed SenseCAP T1000-E ($39.90, Meshtastic preinstalled) —
  seeedstudio.com, GigaParts, Rokland
- **Classic + cheap**: Heltec WiFi LoRa 32 V4 ($26.97) — Rokland, Amazon
  (2-pack kits with case/battery/antenna)
- **Whole-property node**: SenseCAP Solar Node P1-Pro ($140 Amazon, ~$115 direct) —
  setup guide: https://wiki.seeedstudio.com/meshtastic_solar_node/
- US vendors worth knowing: Rokland (store.rokland.com), GigaParts, Seeed direct

## Guides we recommend

- Rokland: Complete Beginner's Guide to Your First Meshtastic Node —
  https://store.rokland.com/pages/complete-beginners-guide-to-your-first-meshtastic-node
- Adrelien: Meshtastic — The Complete Getting Started Guide (2026) —
  https://adrelien.com/meshtastic-the-complete-getting-started-guide/
- Seeed: The Complete Guide to Meshtastic Nodes — Basics & Deployment —
  https://www.seeedstudio.com/blog/2026/03/17/meshtastic-node-guide/

## Find the mesh near you  ← the local answer, verified 2026-09-03

**Our regional network: LZMesh (Southwest Missouri)** — listed in the official
Meshtastic local-groups directory.

- Live node map: **https://map.lzmesh.com** (59 nodes live / 284 in 24 h, 2026-09-03)
- Community Discord: **https://discord.lzarc.com**
- Site: https://lzmesh.com

> **LZMesh keeps the default channel intact.** Their published setup leaves channel 0
> blank with the stock key and adds `LZMesh` as a secondary, so a brand-new radio is
> already on their frequency. To *read* their traffic you add their channel from their
> site. **Their QR replaces existing channels** - save any custom channel first.

Other Missouri groups (from meshtastic.org/docs/community/local-groups/):
Missouri Mesh (https://missourimesh.org) · Show Me Mesh, Jefferson City
(https://www.mo-mesh.com) · MeshSTL, St. Louis · Kansas City Meshtastic Group

- Everywhere else: https://meshmap.net (opt-in, incomplete by design) ·
  r/meshtastic · forum: https://meshtastic.discourse.group

## The neighbors (when you're ready for more)

- **MeshCore** — https://meshcore.co.uk · github.com/meshcore-dev/MeshCore ·
  honest comparison: https://www.austinmesh.org/about/meshcore-vs-meshtastic/
- **Reticulum** — https://reticulum.network · manual:
  https://markqvist.github.io/Reticulum/manual/
- **Ham radio** — study FREE at **https://hamstudy.org** (built by Richard
  Bateman, KD7BBC). Find an exam session near you from the same site.
  APRS intro: http://www.aprs.org

## YouTube - watched and ruled on 2026-09-04

Transcripts pulled with `yt-dlp` and read in full (kept in gitignored
`reference/yt/`, never committed). The file rule is satisfied: these were
actually opened, not just linked.

**RECOMMEND - put on the handout / mention from stage:**

- **"Meshtastic For Dummies in 2026 - Heltec V4 Setup & Wio Tracker Build"**
  (DoItYourselfDad, 24 min) - `youtube.com/watch?v=MN4YUHjJtrk`
  Genuinely beginner-shaped. Explains the mesh with a pass-it-on-in-class
  analogy, and he is honest about prices having risen since his older video
  instead of quietly leaving the old number up. Good match for our room.

- **"Best LoRa Meshtastic Devices Of 2026"** (Ham Radio Crash Course, 21 min) -
  `youtube.com/watch?v=VGiNDgdkyhs`
  Not on the original list, found while searching. Well-known, credible ham
  channel with a thoughtful read on why the device landscape is so scattered.
  Doubles as a natural bridge to our ham radio slide.

**CUT - do not put on the handout:**

- **"Best Meshtastic Devices for Beginners (2026 Off Grid Comms Starter Guide)"**
  (GhostStrats, 12.5 min). The device information is fine, but it opens on
  cellular-outage news clips and a "safety is nothing more than an illusion"
  framing, and it carries affiliate links, a discount code and a sponsor read.
  That is a fear register we are deliberately not using, and we should not send
  a room full of newcomers to a monetised pitch. Cut on tone, not on accuracy.
