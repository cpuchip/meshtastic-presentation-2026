# Range test - how to get a real number off our own hardware

*Built 2026-09-04 because the range slide currently asserts range without measuring it,
and because a first attempt produced a confident wrong answer from stale data.*

Everything the talk says about range right now is borrowed from other people. One drive
with this setup fixes that, and "here is my own mesh, measured on Thursday" is worth more
to that room than any number off a spec sheet.

---

## Which direction are we measuring?

Be explicit, because they are not the same thing and the answer differs:

| Test | What it proves | How |
|---|---|---|
| **Base hears mobile** (pull) | one direction | mobile transmits, base logs SNR/RSSI + mobile's position |
| **Mobile hears base** (push) | the other direction | base transmits, phone app shows what arrives |
| **Round trip** | **both**, at that instant | acknowledged message, and you must read *which* ack |

The dots on the map are the **pull** direction only. Say that out loud rather than letting
a map imply more than it measured.

---

## Method A - no config change on the mobile radio (start here)

The mobile node already broadcasts position. Every packet it sends carries SNR and RSSI,
so every packet is a sample. Nothing to set up in the car.

**On the base radio (the one at the house), before driving:**

```
python scripts/range-log.py --port COM4 --node '!2d21195a' --out range.csv --seconds 5400
```

Drive. Come back. Then:

```
python scripts/range-map.py --csv range.csv --home 37.3297,-92.8939 --out range-map.html
```

`--home` is the **base radio's real coordinates**. Get this right: an earlier attempt
measured everything from `37.35552,-92.87762`, a value several nodes report identically
because it is coarse or defaulted, and every distance computed from it was wrong.

## Method B - the range-test module (adds packet loss)

Method A cannot measure loss, because a packet that never arrives leaves no trace. The
built-in module sends a numbered packet on a fixed cadence, so gaps in the sequence *are*
the loss measurement.

**Mobile node = sender:**
```
meshtastic --port <mobile> --set range_test.enabled true --set range_test.sender 60
```

**Base node = receiver:**
```
meshtastic --port COM4 --set range_test.enabled true --set range_test.sender 0 --set range_test.save true
```

`range-log.py` already parses `seq N` payloads into a `seq` column, so the same CSV gives
loss as well as signal.

**Turn the sender back off afterwards** (`--set range_test.sender 0`). A node beaconing
every 60 s forever is airtime everyone in range pays for.

---

## ⚠ FIRST: raise the position precision, or the test is meaningless

**The public channel publishes a quantized position**, not a real one. At the default
`positionPrecision: 13` that is a **5.84 km (3.63 mi) x 4.64 km (2.88 mi)** cell, and every node inside it
reports the identical coordinate. That is larger than most of the range being measured, so
a range test built on public positions produces one repeated point.

This is exactly what wrecked the 2026-09-04 attempt: the "home cluster" coordinate several
nodes shared was the center of a privacy cell 2.00 mi from the actual house. Mechanism and
proof in [channels.md](channels.md).

**So before driving**, put the position on a channel with full precision - the private
`Stuff` channel is the natural place - and confirm the coordinates you receive actually
differ from the published public ones. If the mobile node's reported position matches the
old cell-center value, you are still reading quantized data.

## Reading the result honestly

- **A dot means the base heard the mobile node.** It does not prove the reverse.
- **Distance comes from the mobile node's own reported position.** If that is coarse or
  stale, the distance inherits the error. On 2026-09-04 a position went 27 minutes without
  updating while we treated it as current, and separately was quantized to a 5.84 km cell
  while we treated it as a location. Both failures produced confident wrong numbers.
- **SNR is the number that matters**, not distance. Two miles across a field and two miles
  through oak ridges are different experiments. Note the terrain.
- **Watch for `hops_used > 0`.** That sample arrived *via a relay*, so it measures the mesh,
  not the link. For a point-to-point range figure, keep only `hops_used = 0`.

## Before trusting any of it

Confirm the mobile node's position is actually *updating*. Two reads a few minutes apart
that return an identical `fix_t` mean the GPS is not producing new fixes, and every
distance downstream is fiction. This is the failure that cost us the first attempt.

## For the talk

A map of our own county with real dots on it is a better range slide than any claim, and
the caveats above are the honest version of "your mileage varies". If the drive does not
happen before Saturday, say what we actually have: one acknowledged round trip, distance
unverified, and the honest reasons why.
