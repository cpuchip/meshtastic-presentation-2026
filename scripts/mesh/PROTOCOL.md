# Cross-preset link test — fermion ↔ yogachip

Michael's question: *four radios, two per box, one LONG_TURBO and one LONG_FAST
on each — can we communicate over each link?* This is the protocol, plus what
fermion has already measured.

`pip install meshtastic` first (fermion is on lib 2.7.11).

## fermion's radios — MEASURED 2026-09-04

| Port | Node | Hardware | Preset | BW | Primary channel |
|---|---|---|---|---|---|
| COM14 | `!903c20aa` StuffleJuice (SJ) | Seeed Wio Tracker L1 | **LONG_TURBO** | 500 kHz | `(blank)`, default PSK |
| COM15 | `!336890bc` KV9G-HWT-90bc (9Gbc) | Heltec Wireless Tracker | **LONG_FAST** | 250 kHz | `(blank)`, default PSK |

Both on firmware **2.7.26.54e0d8d**, region **US**, `use_preset=true`, slot auto.
COM14 also carries a secondary `HamStudy` (32-byte key).

### The finding that reframes the test

**COM14 (LONG_TURBO) has heard nothing in 110 days.** Its 36-node database is
entirely fossil. COM15 (LONG_FAST) has 94 peers but only **3 heard within the
hour** — every LZ-region name in it (CHAOSNode LZ, KF0LZX Roof, Trinity LZ…) was
last heard **399–402 days ago**.

> **A Meshtastic node list is a HISTORY, not a live view.** Entries survive
> preset changes and persist for a year. "95 nodes" felt like a live network and
> was four live contacts. Check last-heard before believing a node list — ours,
> or an audience member's.

## Results so far

| Test | Method | Result |
|---|---|---|
| LF → live neighbour, directed | `mesh_linktest.py COM15 '!d5faaa85'` | **NAK `NO_CHANNEL`** in 19.4 s — directed messages take the PKI path; not a clean physical-layer answer. Use broadcast instead. |
| LF broadcast → LT radio (cross-preset) | `mesh_dual_listen.py 120 --tx COM15` | LT did **not** hear it |
| Positive control | — | **MISSING** — see below |

⚠ **The cross-preset negative is not yet evidence.** In that 120 s window
*neither* radio heard any outside traffic at all, so "LT didn't hear it" cannot
be distinguished from "LT hears nothing regardless" — which, given 110 days of
silence, is entirely possible. **An assertion that cannot fail for the reason it
claims to test is not a check.** The positive control is the whole experiment.

## The 2×2 — what yogachip needs to run

Identify yogachip's two radios first:

```sh
python scripts/mesh/mesh_inventory.py           # auto-detects COM14/COM15; pass your own ports
python scripts/mesh/mesh_recency.py             # live vs fossil
```

Report back: **port, node id, preset, bandwidth, primary channel name** for each.

Then, with fermion listening on both radios simultaneously:

| # | Transmitter | Expected on fermion COM15 (LF) | Expected on fermion COM14 (LT) |
|---|---|---|---|
| 1 | yogachip **LONG_FAST** broadcast | **HEARD** ← positive control | not heard |
| 2 | yogachip **LONG_TURBO** broadcast | not heard | **HEARD** ← positive control |

Test 1 and test 2 each supply the positive control the other direction lacks.
Run them **separately**, tagged, so a hit is attributable:

```sh
python scripts/mesh/mesh_dual_listen.py 180 --tx <your-LF-port> --tag YOGALF1
# wait for it to finish, then
python scripts/mesh/mesh_dual_listen.py 180 --tx <your-LT-port> --tag YOGALT1
```

Fermion runs `mesh_dual_listen.py 180` (no `--tx`) across the same window and
reports which tag landed on which radio.

**Both radios must be powered and their preset confirmed before the run** — a
"no" from a radio that is off looks exactly like a "no" from physics.

## Why it matters for the talk

If tests 1 and 2 land and the cross pairs stay silent, we have a demonstrated,
first-hand version of the preset lesson: **two radios in one room, one setting
different, no contact.** That is a live demo worth doing on stage — it needs no
internet and it explains the single most common "my new radio doesn't work."

Companion write-up: `../../notes/preset-deafness-crosscheck.md`.
