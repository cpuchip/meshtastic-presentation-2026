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

**Arm 3, the negative control.** Hold up the third radio first.

```
meshtastic --port COM10 --sendtext "You should not see this one."
```

Then show the phone. Nothing arrives.

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
