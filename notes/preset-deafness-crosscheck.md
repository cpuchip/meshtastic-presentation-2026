# LONG_TURBO deafness — cross-check from fermion, 2026-09-04

> **`meshtastic` seat (fermion) confirming yogachip's bench observation from a
> different instrument: the `reference/firmware` and `reference/meshtastic-docs`
> clones, not a radio.** yogachip saw it on hardware; this is the source side.
> Its files (`notes/channels.md`) are untouched.

## Both claims confirmed

**1. LONG_TURBO is real, and it is 500 kHz.**
`firmware/src/mesh/generated/meshtastic/config.pb.h:346`

```
meshtastic_Config_LoRaConfig_ModemPreset_LONG_TURBO = 9,
```

with the firmware's own comment: *"Long Range - Turbo / This preset performs
similarly to LongFast, but with 500Khz bandwidth."* Parameters at
`firmware/src/mesh/MeshRadio.h:250` — **bw 500 kHz, sf 11, cr 8** (LONG_FAST is
250 kHz). The enum continues past 9 to LITE_FAST 10, LITE_SLOW 11, NARROW_FAST
12, NARROW_SLOW 13… — yogachip's "protobufs now go to 16" holds.

**2. The docs gap is real, and worse than "never mentions it" — they contradict
themselves.**

| Where | LONG_TURBO? |
|---|---|
| `docs/configuration/radio/lora.mdx` — the numbered preset list | **absent** |
| `docs/configuration/radio/lora.mdx:227` — the `lora.modem_preset` value table | **absent** (lists only 8) |
| `docs/about/overview/radio-settings.mdx:91` | **present** — 1.34 kbps, 500 kHz, 150 dB |
| `docs/software/android/user/settings-radio-user.md:62` | **present** — "Similar range to Long Fast but with 500 kHz bandwidth" |

So the page a person configuring their radio would actually open is the one
missing it. Corroborating tell that it is a late addition nobody swept after:
the SHORT_TURBO comment two lines above still claims it is *"the only one with
500kHz bandwidth"* — untrue now that LONG_TURBO exists.

## Why the board was deaf (supported)

Two independent reasons, either alone sufficient:

1. **Incompatible modem config.** 500 kHz vs 250 kHz — the radios cannot
   demodulate each other. Not a decryption problem; a physical-layer one.
2. **Different frequency.** Slot count scales inversely with bandwidth: the US
   902–928 band gives 104 slots at LONG_FAST's 250 kHz, but roughly half that at
   500 kHz. The same slot *index* lands on a different actual frequency.

That matches the symptom exactly — nodedb holding only itself, on a desk with
three working nodes.

## What is NOT established

**What set that board to LONG_TURBO is unresolved, and I am not asserting a
mechanism either.** Note only that it makes the anomaly sharper, not softer:
`lora.mdx:37` says *"Default is `unset` which equates to `LONG_FAST`"* — so a
factory-fresh board should not have come up on LONG_TURBO. Vendor pre-flash,
carried-over config, and a 2.7.26 behavior change are all live hypotheses with
no evidence separating them. **Do not offer a cause from the stage.**

Limit of this instrument: the clones are `--depth 1` from **2026-08-28** and are
not pinned to 2.7.26. They prove LONG_TURBO's existence, parameters, and the docs
gap; they cannot speak to what changed *in* 2.7.26.

## The stage action (this is the payload)

This is a **second, independent** mechanism for "my brand-new radio sees nobody,"
different from the channel-name one. The channel mechanism is about being unable
to *read*; this one is about being unable to *hear*. A newcomer cannot tell them
apart — both look like a dead radio.

So the setup preflight is **two settings, not one**:

> **Region = US. Preset = LongFast.**
> Check both before deciding the mesh is dead.

`slides/slides.md` §"Setup: the whole thing" step 3 currently says region only.
Adding the preset closes the second failure mode for the cost of three words —
and it is now the *first* thing to check when someone at the expo says "mine
isn't finding anything." Worth having in the Q&A pocket too.

## Adjacent, and yogachip is right to have rejected it

The claim that "region US moves you off LongFast because LongFast is not
US-compliant" is backwards. The region caveat attaches to the **500 kHz**
presets, not to LongFast: `firmware/test/test_admin_radio/test_main.cpp:537`
asserts *"LONG_TURBO should be invalid for EU_868"*, and the SHORT_TURBO comment
says the 500 kHz width *"is not legal to use in all regions."* LongFast at
250 kHz is the documented US default. Good rejection.
