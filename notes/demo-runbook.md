# Live demo runbook - the preset A/B

*Closes the "decide the live-demo shape, and rehearse it" open item. Built 2026-09-04 from
a thing that actually happened on the bench, not a thing we invented for the stage.*

**Why this demo and not a range demo:** it needs no internet, no volunteer, no line of
sight, and no luck. It works on a table in a pavilion. And it fails *informatively*: if the
negative arm arrives, we learn something real in front of the room instead of dying.

---

## What it shows

Two radios. Same channel name. Same key. Same table. **One reaches the phone, one does
not.** The only difference is the modem preset.

| Arm | Radio | Preset | Frequency | Expected |
|---|---|---|---|---|
| **Positive** | Stuff-Indicator (STID) | LONG_FAST | **906.875 MHz** | **arrives** |
| **Negative** | Seeed XIAO S3 | LONG_TURBO | **908.750 MHz** | **does not arrive** |

1.5 MHz apart. The occupied bands (906.750-907.000 and 908.500-909.000) do not overlap at
all, so this is not a weak signal. It is a different radio channel.

**Michael's phone node:** `!2d21195a` **cpuchip / KV9G**, Wio Tracker L1, on LongFast.

---

## Setup before the talk

1. Plug both radios into the laptop. Confirm the ports, because Windows moves them:

   ```
   python -c "import serial.tools.list_ports as l; [print(p.device,p.hwid) for p in l.comports()]"
   ```

   Known: `1A86:7523` = Stuff-Indicator, `2886:0059` = XIAO S3, `2886:0050` = T1000-E.

2. **Confirm each radio's preset before trusting it.** This is the whole demo; do not
   assume it survived a firmware update.

   ```
   meshtastic --port COM4  --info | findstr modemPreset
   meshtastic --port COM10 --info | findstr modemPreset
   ```

   Want `LONG_FAST` on COM4 and `LONG_TURBO` on COM10.

3. Phone paired to KV9G, Meshtastic app open on the Primary/LongFast channel.

4. **With two or more radios attached the CLI refuses to guess.** Always pass `--port`.

---

## The run, on stage

**Arm 1, the direct message.** Only Michael's phone should buzz.

```
meshtastic --port COM4 --dest '!2d21195a' --sendtext "Direct to KV9G from the table."
```

**Arm 2, the broadcast.** Everyone in range, including John down the street.

```
meshtastic --port COM4 --sendtext "Hello to the whole channel."
```

*Beat worth taking:* those two went out of the same radio on the same channel, and one
reached one person while the other reached the neighbourhood. That is addressing, and it
is the thing people expect to be complicated.

**Arm 3, the negative control - and then FIX IT LIVE.** This is the strongest beat in the
talk. Hold up the third radio first.

```
meshtastic --port COM10 --sendtext "You should not see this one."
```

Show the phone. Nothing arrives. Then show its node list.

> **⚠ Caveat found 2026-09-04, check this before relying on the beat.** The node database
> **persists across a preset change.** After we moved the XIAO to LongFast its list held
> `StuffleJuice` (`!903c20aa`), which is fermion's **LongTurbo** radio, so that entry was
> almost certainly learned while the XIAO was still on LongTurbo. A node list is a record
> of who was ever heard, not who is reachable now.
>
> So "look, it knows nobody" only lands on a radio that has genuinely never heard anything.
> If the list is dirty, either reset the node database first, or skip the list and let the
> *message* carry the point. Do not claim an empty list you have not checked.

Now change one setting, in front of them:

```
meshtastic --port COM10 --set lora.modem_preset LONG_FAST
```

**It reboots (about 15-20 seconds - say what is happening, do not fill the silence).** Then:

```
meshtastic --port COM10 --info
meshtastic --port COM10 --sendtext "Same radio. One setting. Hello."
```

Measured on the bench 2026-09-04: the node list went from **1 node (itself) to 3** within
seconds, and the broadcast arrived. Same radio, same room, same channel, nothing else
touched.

> "That is the whole fix. One dropdown. It was never broken, and it was never out of range."

**⚠ The XIAO is currently ON LongFast**, because we fixed it. To restore the negative
control before the talk:

```
meshtastic --port COM10 --set lora.modem_preset LONG_TURBO
```

**Read the config back AFTER the reboot settles.** A readback taken too early returns the
OLD preset and an empty node list, which looks exactly like a failed write. It bit us once;
check `rebootCount` went up before believing the readback.

> "Same channel name. Same password. Sitting six inches from the other one. It is on
> LongTurbo instead of LongFast, so it is transmitting on 908.750 while everything else
> here is on 906.875. It is not broken. It is not out of range. It is in a different room."

**The line to land, and then stop talking:**

> "This is a brand new radio I flashed two days ago. It came up on the wrong preset and
> found nobody. If you buy one and it sees an empty list, this is what happened to you, and
> it is two settings to check: region and preset."

---

## If the negative control ARRIVES

Do not talk past it. Say plainly that it arrived, that we did not expect it, and that we
will find out why. Then check `--info | findstr modemPreset` on COM10 in front of them: the
likeliest cause by far is that the preset got changed back, not that the physics moved.

An honest "that surprised me, let us look" is a better moment than a smooth demo. The room
is full of people who have had equipment embarrass them.

## Fallback if a radio will not enumerate

Skip to the phone. Show two nodes in the app's node list, send between them, and describe
the negative arm with the two frequencies. The numbers carry it without the hardware.

**Do not use COM3 (the T1000-E) for anything on stage.** `--info` times out on it over USB,
undiagnosed as of 2026-09-04.

---

## Rehearsal checklist

- [ ] Both presets confirmed by `--info`, not by memory
- [ ] All three arms run end to end, phone in hand
- [ ] Phone screen visible on the projector, or big enough to hold up
- [ ] Radios charged; the Indicator reads 0.00 V on USB, so it needs the cable
- [ ] Know which COM port is which **before** standing up

---

## ⚠ Live finding 2026-09-04: the DM arm FAILED, the broadcast arm worked

Ran the real thing against Michael's phone (KV9G, `!2d21195a`). Result:

| Arm | Outcome |
|---|---|
| Broadcast from Stuff-Indicator, LongFast | **arrived** |
| **DM from Stuff-Indicator to KV9G** | **did NOT arrive** |
| Broadcast + DM from fermion's radio | **both arrived** |

Retried the DM with `--ack`, which turns it from a guess into a measurement:

```
Received a NAK, error reason: NO_CHANNEL
```

**What that establishes:** the DM *reached* KV9G. KV9G received it and actively refused
it. So this is not range, not frequency, not preset. Something about the
Stuff-Indicator → KV9G direct path specifically, since fermion's DM to the same phone
worked and our own broadcast on the same channel worked.

**What it does NOT establish:** the cause. `NO_CHANNEL` is Routing.Error **6**. The
PKC-specific failures have their own codes (`PKI_FAILED` 34, `PKI_UNKNOWN_PUBKEY` 35,
`PKI_SEND_FAIL_PUBLIC_KEY` 39) and we did **not** get those, so a stale-public-key story
is a guess, not a reading. Stuff-Indicator does hold a public key for KV9G and did receive
fresh nodeinfo from it during the capture.

**Candidate remedy, untried:** `meshtastic --port COM4 --remove-node '!2d21195a'` so the
node is re-learned from scratch. Cheap and self-healing (it reappears from the next
nodeinfo broadcast), but it is a change to Michael's radio, so it is his call.

### What this means for the stage

**Demote the DM arm.** Lead with the broadcast and the negative control, which both work
and both carry the actual lesson. If the DM is wanted, rehearse it with `--ack` first: an
unacked DM looks identical to a dead radio from the audience's side, and we would be
debugging live for no teaching benefit.

Silver lining worth one sentence if it comes up: *"a direct message that fails while the
channel message works is a real thing, and the radio will tell you why if you ask it for
an acknowledgment."* That is a better lesson than a demo that just works.

### Telemetry captured during the exchange (all at 0 hops)

| Node | SNR | RSSI |
|---|---|---|
| fermion's sender (`!336890bc`) | 5.5 | -12 |
| Michael's phone KV9G (`!2d21195a`) | 6.0 | -41 |
| Stuff Solar SNST (the pole node) | 7.75 | -55 |
| John-Base (`!7ce82641`) | 1.0 | -102 |

The solar node on the pole is the **strongest** signal on the mesh, which is the range
slide's argument arriving as data rather than assertion. John, down the street, is the
weakest and still perfectly usable at 0 hops.

---

## ★ The instrument lesson, paid for 2026-09-04: the node list is a RECORD, not a STATUS

Michael drove out and asked to be tracked. We polled his node 55 times over 45 minutes.
**Every field came back byte-identical every time** - same coordinates, same altitude, same
`fix_t`, and critically the same `snr 6.75` and `hops 0`.

That last part is the tell. **Live reception jitters SNR.** An SNR that does not move across
45 minutes is not a weak live signal; it is *no live signal at all*. We were re-reading one
cached snapshot from the last time we heard him.

**`--info` reads the node database, which records the last time a node was heard. It is not
a link status.** Reading it repeatedly produces a confident, stable, completely wrong
picture of a live link. This is the same shape as two other traps this week: netbird
reporting `Connected` while no packets flowed, and a node list keeping entries learned on a
different modem preset.

### The instrument that actually answers "can I reach them right now"

An **acknowledged transmission**, and you must read which kind of ack you got:

| Result | What it means |
|---|---|
| `Received an ACK.` | **The destination confirmed.** Round trip proven, both directions, at that moment. |
| `Received an implicit ACK.` | **Someone rebroadcast our packet.** It entered the mesh. The destination said nothing. Reachability is UNPROVEN. |
| `Received a NAK, error reason: ...` | It arrived and was actively refused. Read the reason. |
| (timeout) | Nothing heard at all. |

Measured on the same node an hour apart: explicit ACK at 2 miles when his radio was up,
implicit ACK only after it had power-cycled. **The implicit ack is the interesting one** -
it looks like success in the output and is not.

### Consequences

- **For the talk:** if anyone asks "how do I know my message got there?", this is the
  answer, and it is a better answer than most people have. The app shows delivery state
  too; the CLI just names it more precisely.
- **For the range slide:** we do not yet have a clean own-hardware range number. What we
  have is one explicit ACK at 2.0 miles, which is a real data point and worth exactly that
  much - one point, one direction, one moment.
- **For any future tracking:** poll with acks, not with `--info`.
