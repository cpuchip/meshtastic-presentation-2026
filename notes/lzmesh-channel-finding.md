# LZMesh: primary or secondary? — SETTLED 2026-09-04

> **Written by the `meshtastic` seat (fermion) for `yogachip`, who asked and then
> went offline before it could be delivered. This file is the watch point.**
>
> **It contradicts two lines currently in `notes/research.md` and
> `notes/resources.md`. Those lines are heading for the stage tomorrow.**
> They are yogachip's files; I have not edited them. See "What needs fixing".

## The answer

**`CHAOS JLN Main` is not LZMesh's primary — and by their own published setup,
LZMesh does not rename the primary at all.** Channel index 0 stays **blank**.

## The evidence (authoritative — LZMesh's own setup page)

Source: <https://lzmesh.com/resources/lz-quick-setup/>, read in a real browser
2026-09-04. (A plain HTTP fetch returns **403**; use a browser.)

Their "CHANNEL LAYOUT — Recommended local channels", verbatim:

| # | Label | NAME | Their stated use | PSK |
|---|---|---|---|---|
| **0** | Default Meshtastic | **(blank)** | "Default public Meshtastic channel" | `AQ==` |
| **1** | LZMesh | `LZMesh` | "Primary LZMesh network" · "the main channel most people should use every day" | `uLT6S8kQlQHjA7yEtBkzIj3zm6K6lE55mulplDZyF/0=` |
| 2 | Private | `Private` | "Personal or group-specific communication" | user defined |
| 3 | LZRF | `LZRF` | "RF-only testing" (no MQTT) | `dTEweE82YjhWc1pRS1dzY1FESEk4dnlBcVM2SUxmV3c=` |

Also on the page: "Leave downlink disabled on Channel 0."

### The word that causes the confusion

LZMesh calls channel 1 the *"Primary LZMesh network"*. That is **"main / most-used"**,
not Meshtastic's **index-0 PRIMARY**. Meshtastic's primary is channel 0, and theirs
is blank — the stock default.

## Why this is good news, three ways

1. **Our headline advice is correct AND has a local worked example.** "Never rename
   your primary; add a secondary" is precisely what the regional network does. We can
   now say: *"here's how the sixty-node network west of us is set up — exactly this."*
2. **A factory-fresh radio in Marshfield is already on their frequency.** Blank primary
   hashes to slot 20, same as stock. So a newcomer *hears* LZMesh nodes without
   changing a thing; they only need the channel added to *read* them. This also
   explains the RAK4631 our demo node heard at zero hops on stock LongFast.
3. **The failure mode is smaller than we wrote.** Not "you're on the wrong frequency
   and deaf" — just "you can't decrypt that traffic yet." One QR scan fixes it.

## What needs fixing (yogachip's call — I have not touched these)

- `notes/research.md` (~line 121) — the blockquote *"most LZMesh nodes run a named
  channel, `CHAOS JLN Main`, not the stock LongFast… Being in radio range is not
  enough"*. The frequency-exclusion implication is now contradicted by the source.
- `notes/resources.md` (~line 43) — same claim, same fix.
- `notes/channels.md` §"Our demo node…" — the open either/or can be closed: it is the
  secondary branch, and the outcome is the reassuring one.
- `notes/research.md` open items — the "ask LZMesh primary or secondary" item closes.

Where `CHAOS JLN Main` came from is unresolved. **JLN is the Joplin airport code**, so
it is plausibly a legacy or neighbouring-group channel name seen on the map. It is not
in LZMesh's current published setup.

## Honest limit of this finding

This is what LZMesh **publishes**, not a survey of what every deployed node **runs**.
Some nodes may still carry older channel config. Stage-safe phrasing that is true
either way:

> "The regional network's own setup guide keeps the default channel intact — so a
> brand-new radio out of the box is already on their frequency. To read their traffic
> you scan one QR code off their site."

## Two riders for the handout

- **Their QR replaces channels.** Their own warning: *"scanning this QR code can
  replace existing channels, so save anything custom first."* Say that out loud if you
  send the room to scan it.
- **Keep MQTT off a beginner handout.** Their page publishes MQTT settings
  (`mqtt.lzmesh.com`, credentials in the clear). MQTT backhauls over the internet,
  which cuts against the off-grid thesis of the talk. Advanced-topic material, not
  first-node material.
