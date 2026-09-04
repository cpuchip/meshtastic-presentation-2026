# Channels, frequency, and encryption - the part beginners get wrong

*Written 2026-09-04 for the Expo talk. Every rule here is checked against the official
Meshtastic docs (linked inline), not against forum folklore. This is the section Michael
flagged as his weak spot, so it goes deeper than the talk needs on purpose: the extra is
for Q&A, not for slides.*

---

## The one idea that makes all of it make sense

There are **two separate layers**, and almost every beginner problem is someone confusing
them:

| Layer | The question it answers | What controls it |
|---|---|---|
| **1. Radio** | *Can our radios physically hear each other?* | Region + modem preset + frequency slot |
| **2. Channel** | *Can we read what we hear?* | Channel name + PSK (the key) |

Layer 1 is the room. Layer 2 is the language spoken in it.

You can be in the same room and not understand each other (same frequency, different key).
You cannot understand each other from different rooms no matter what language you speak
(different frequency). **Frequency first, always.** If layer 1 is wrong, nothing else you
change will help, and this is where people burn a weekend.

---

## Layer 1: are we even on the same frequency?

Three things have to match, and only the first is obvious.

### a. Region

`US` here. Sets the legal band (902-928 MHz ISM) and the power limits. Ships as `UNSET`,
and a node with an unset region **will not transmit at all** - it just shows a message on
screen. That is the #1 "my brand new node does nothing" cause.

### b. Modem preset

Default is **LONG_FAST** (protobuf enum 0). It bundles bandwidth, spreading factor and
coding rate. **Two nodes on different presets are deaf to each other, full stop.**

Leave it on LONG_FAST. The whole public mesh is there, and the slower presets buy range
you will not notice while costing airtime everyone shares.

### The preset list has grown, and the docs lag (checked 2026-09-04)

The LoRa config docs page still lists **nine** presets and does not mention `LONG_TURBO`
at all. The protobufs now go to **17** (0-16). Sources disagree by version, so count on
none of them:

| Where | Knows presets up to |
|---|---|
| meshtastic.org LoRa config page | 9 (no LONG_TURBO) |
| `meshtastic` python package 2.7.11 (our CLI) | 13 (`NARROW_SLOW`) |
| current protobufs | 16 (`MEDIUM_TURBO`) |

Newer entries: `LONG_TURBO` (9) "performs similarly to LongFast, but with 500Khz
bandwidth"; `LITE_FAST`/`LITE_SLOW`/`NARROW_FAST`/`NARROW_SLOW` (10-13, EU band
compliance); `TINY_FAST`/`TINY_SLOW` (14-15, 20 kHz, amateur-radio compliance, needs a
TCXO); `MEDIUM_TURBO` (16). `LONG_SLOW` is deprecated as of 2.7 and `VERY_LONG_SLOW` as
of 2.5.

### ⚠ A live example from our own bench, 2026-09-04

A **brand new Seeed XIAO S3** flashed to 2.7.26 came up on **`LONG_TURBO` (500 kHz)**
while every other node here runs **`LONG_FAST` (250 kHz)**. Its node database held exactly
**one** entry: itself. It had heard nobody, and nobody had heard it, sitting on the same
desk as three working nodes.

That is layer 1 failing, in the room, with nothing wrong with any radio. It is the best
demo we have for this section: **same house, same channel name, same key, zero contact.**

**In actual megahertz** (Michael read these off the radios; the arithmetic below reproduces
both exactly). US region runs 902-928 MHz, and the centre frequency is
`freqStart + bw/2000 + slot x bw/1000`, with `numChannels = floor(26 / (bw/1000))`:

| Preset | Bandwidth | Slots | Slot | Centre | Occupies |
|---|---|---|---|---|---|
| `LONG_FAST` | 250 kHz | 104 | 19 | **906.875 MHz** | 906.750 - 907.000 |
| `LONG_TURBO` | 500 kHz | 52 | 13 | **908.750 MHz** | 908.500 - 909.000 |

**1.5 MHz of clear air between the two bands. They do not overlap at all.** This is not
"weak signal" or "hard to hear" - it is a different radio channel. Worth putting the two
numbers on the slide, because "different frequency" is abstract and *906.875 vs 908.750*
is not.

**Resolved 2026-09-04, with the confidence stated honestly.** The question was only ever
"LONG_FAST is protobuf enum 0 and the documented default, so a factory-fresh board should
have come up on LongFast - what wrote LONG_TURBO instead?" Michael's answer: **the board
came that way from the vendor.**

That is coherent and it closes the loop, because **a flash without a full erase preserves
the existing configuration.** So Seeed's preloaded settings survived the update to 2.7.26
untouched. Nothing wrote LONG_TURBO during the flash; it was simply never overwritten.

Confidence: this rests on Michael's recollection of the board as shipped, not on a
measurement of a second sealed unit. Good enough to stop investigating, not good enough to
state as a general fact about XIAO S3 boards.

### ⚠ The tension this exposes, and it is worth a sentence on stage

We tell people **"do not tick full erase"** so their identity keys survive an update. True,
and it prevents the DM breakage above. But the same behaviour is why this board arrived on
a preset nobody chose: **whatever the vendor shipped, survives.**

So the two pieces of advice belong together:

> "Update without a full erase, so you keep your keys. And then check your region and
> preset anyway, because whatever the factory set is still in there."

**A claim we checked and rejected:** a search result asserted that setting region US moves
a node off LongFast because "LongFast's bandwidth is not US-compliant." Both the LoRa docs
page and the LongFast blog post contradict it, and it is backwards: 250 kHz is
unremarkable in the US ISM band, while the **500 kHz** presets (`SHORT_TURBO`,
`LONG_TURBO`, `MEDIUM_TURBO`) are the ones carrying region-legality caveats. Do not repeat
it.

### c. Frequency slot - and here is the trap

The band is divided into numbered slots. Which slot your node uses is set by:

> "a hash of the **PRIMARY** channel's name sets the LoRa frequency slot, which determines
> the actual frequency you are transmitting on in the band."
> ([channels docs](https://meshtastic.org/docs/configuration/radio/channels/))

Read that twice, because it is genuinely surprising:

> ### Renaming your primary channel moves you to a different frequency.

Not a different "chat room". A different **frequency**. Your radio and your neighbour's
radio stop hearing each other at the physical layer, and no amount of key-swapping fixes
it.

The stock default primary channel has an **empty name**, and on US/LONG_FAST that hashes
to **slot 20**. (Verified on our own demo node: `channelNum: 20`, `usePreset: true`, name
`""`.)

**So:** if you want a private family channel *and* you want to stay on the public mesh,
**do not rename the primary.** Add a *secondary* channel instead. Secondary channel names
do not touch the frequency; only the primary's does.

If you deliberately want your own frequency, you can set the slot explicitly rather than
letting the name hash pick it (`lora.channelNum`). When it is 0/unset the device "reverts
to the older channel name hash-based algorithm."

---

## Layer 2: can we read each other?

A channel is a name plus a key.

- **8 channels**, indexed 0-7. Index 0 is **PRIMARY** and cannot be disabled. The others
  are **SECONDARY**. Active channels have to be consecutive: no disabled gaps in between.
- **Name:** max 12 bytes. Empty string means the default primary. Both name and key must
  match for two nodes to talk on that channel.
- **PSK:** 0 bytes (no crypto), 16 bytes (AES128) or 32 bytes (AES256). Payloads use
  AES256-CTR, a different key per channel.
- The default primary key is the single byte `0x01`, base64 **`AQ==`**. It is published in
  the docs and baked into every device on earth.

**LongFast is not private and was never meant to be.** Everyone has the key. Treat it as a
public square: fine for hello, coordination, and finding people, wrong for anything you
would not say out loud at the expo.

### Sharing a channel

Share the channel URL / QR from the app. That is the whole handshake. Anyone who scans it
gets the name and the key and is on the channel. Which is also the warning: **the QR is
the key.** Do not put a private channel's QR on a slide, a handout, or a photo.

---

## Michael's question: do messages still get through if we are on the same frequency but not the same channel?

**Yes. And this is the nicest thing about the protocol.**

> "The packet header remains unencrypted, while payloads are encrypted. This design choice
> allows nodes to relay packets they cannot decrypt."
> ([encryption docs](https://meshtastic.org/docs/overview/encryption/))

So a node that cannot read your traffic still **carries** it. It sees a packet, decrements
the hop limit, and rebroadcasts on behalf of a stranger whose message is gibberish to it.

Two consequences worth saying out loud in the talk:

1. **Your private family channel rides the public mesh.** You get the reach of every
   stranger's node without any of them being able to read a word. Strangers' radios are
   working for you right now.
2. **Being on the mesh is a contribution, not just a consumption.** A node sitting in a
   window is helping neighbours it has never decrypted a byte from.

The default rebroadcast mode is **`ALL`**: "rebroadcast ALL messages from its primary mesh
as well as other meshes with the same modem settings." Leave it there. The alternatives:

| Mode | What it does |
|---|---|
| `ALL` | **default.** Carries everything on your modem settings, decryptable or not |
| `LOCAL_ONLY` | Ignores foreign meshes and anything it cannot decrypt |
| `KNOWN_ONLY` | LOCAL_ONLY, plus ignores nodes not in its known list |
| `ALL_SKIP_DECODING` | Same as ALL but never decodes. Repeater role only |
| `CORE_PORTNUMS_ONLY` | Drops non-standard traffic (TAK, RangeTest, PaxCounter...) |
| `NONE` | No rebroadcast. Only for SENSOR / TRACKER / TAK_TRACKER roles |

Setting `LOCAL_ONLY` to "keep my mesh clean" is the move that quietly makes you a worse
neighbour. Unless you have a reason, leave it on ALL.

### Roles, quickly

Stay on **CLIENT**. Use **CLIENT_MUTE** if you genuinely do not want to relay (a phone-side
node in a pocket, say).

**Do not set ROUTER or REPEATER** because it sounds more powerful. Those are infrastructure
roles for nodes with height and a power budget, and a badly placed router hurts the mesh by
rebroadcasting from a hole. That is a pole node's job, not a desk node's.

---

## So: keep LongFast, or not?

**Keep it, and add to it.** The recommended shape for a homesteader:

- **Primary: leave it exactly as shipped.** Empty name, default key, LONG_FAST, region US.
  This is your reach and your neighbours. Renaming it is what silently removes you from the
  local mesh.
- **Secondary: your family channel.** Name it, generate a **random** key (not `default`,
  not a `simple` one - those are publicly known too), share it by QR to the people you
  trust. Encrypted, private, and it still rides everyone else's nodes.

Reasons you would move off the default primary, all of them advanced:

- You are running a deliberately separate network and accept being invisible to the public
  mesh (this is what a regional group does when it names a primary).
- Local LongFast congestion is genuinely bad. Out here it is not.
- You are a licensed ham using `overrideFrequency` for out-of-band work.

---

## Why the local mesh looked empty (the LZMesh case)

This is the worked example for the talk, and it is ours.

Our demo node runs the stock primary: empty name, default key, US/LONG_FAST, slot 20.

**SETTLED 2026-09-04** by the `meshtastic` seat, from LZMesh's own published setup page:
they keep **channel 0 blank** with the stock key and put `LZMesh` at **index 1 as a
secondary**. Their page calls channel 1 the "Primary LZMesh network", which means
main/most-used, not Meshtastic's index-0 PRIMARY. Full evidence:
[lzmesh-channel-finding.md](lzmesh-channel-finding.md).

**So the good branch is the true one.** A factory-fresh radio here is already on LZMesh's
frequency and hears their nodes without any change. Adding their channel only lets you
*read* that traffic. One QR scan, not a frequency problem. This also explains the
stranger's RAK4631 our node heard at zero hops on stock LongFast.

Better still, **LZMesh is a worked local example of our own headline advice**: never
rename the primary, add a secondary. The sixty-node network west of us is set up exactly
the way we are telling the room to set up.

Two riders if we send people to their QR:
- **Scanning it replaces existing channels** (their own warning). Save custom ones first.
- **Their page also publishes MQTT settings.** MQTT backhauls over the internet, which
  cuts against the off-grid thesis. Advanced topic, not first-node material.

The lesson still holds and is worth the slide: **an empty node list is usually a settings
mismatch, not a dead mesh.** Our XIAO S3 on LONG_TURBO above is the sharper example, since
that one really is a frequency-layer miss.

---

## The 60-second version for the audience

1. Set region to **US**. Without it the radio will not transmit.
2. Leave the preset on **LongFast** and leave the primary channel **unnamed**. That is what
   puts you on the mesh with everyone else.
3. For privacy, **add a second channel** with a random key and share it by QR. Never rename
   the primary to do this.
4. Your private messages still travel through strangers' radios. They carry them; they
   cannot read them.
5. If your node list is empty, you are almost certainly on a different frequency or preset,
   not alone in the world.

---

## Sources

- Channels: https://meshtastic.org/docs/configuration/radio/channels/
- LoRa config: https://meshtastic.org/docs/configuration/radio/lora/
- Encryption: https://meshtastic.org/docs/overview/encryption/
- Mesh algorithm: https://meshtastic.org/docs/overview/mesh-algo/
- Device config (roles, rebroadcast): https://meshtastic.org/docs/configuration/radio/device/

## Open

- [x] ~~Ask LZMesh whether `CHAOS JLN Main` is their primary or a secondary.~~ **Settled
      2026-09-04**: their primary is blank; `LZMesh` is a secondary. See
      [lzmesh-channel-finding.md](lzmesh-channel-finding.md).
- [x] ~~What set the new XIAO S3 to `LONG_TURBO`?~~ **Closed 2026-09-04: it shipped that way; a flash without full erase preserved it.**

---

## The key-mismatch gotcha: when DMs break after an update

*Hit live on our own bench 2026-09-04, then researched. This one belongs on the setup
slide because it is caused by the very step we tell people to do.*

### The symptom

Broadcasts work fine. **Direct messages to one specific node silently fail.** Ask for an
acknowledgement and the radio answers:

```
Received a NAK, error reason: NO_CHANNEL
```

**Note the error name misdirects.** `NO_CHANNEL` is Routing.Error 6, and Meshtastic has
dedicated PKC errors (`PKI_FAILED` 34, `PKI_UNKNOWN_PUBKEY` 35, `PKI_SEND_FAIL_PUBLIC_KEY`
39) which you do **not** get. So the error reads like a channel problem and is actually a
key problem. Do not let the label steer the diagnosis; we nearly did.

### The cause

Direct messages are encrypted to the recipient's **public key** (PKC), not to the channel
key. Every node stores the public keys of nodes it has met.

**A full erase during a firmware flash wipes the device's key pair.** The node comes back
with the *same node ID* and a *brand new key*. Everyone who met it before still holds the
old public key, so their DMs are encrypted to a key it no longer has. It cannot decrypt
them, and it NAKs.

Maintainer guidance is blunt ([firmware discussion
#5122](https://github.com/meshtastic/firmware/discussions/5122)):

> "If you don't want to wipe the keys don't do a full erase."

### The nasty part: it is a recovery deadlock

From [firmware issue #10371](https://github.com/meshtastic/firmware/issues/10371): the
node cannot tell its peers to fix it, **because direct messaging is exactly what is
broken.** On a public mesh with many peers holding the stale key, there is no systematic
recovery today. Every peer has to clear it by hand.

### What to actually do

**Prevention, and this is the real advice:**

- **Do not tick "full erase" for routine firmware updates.** A normal update keeps your
  keys and this never happens.
- If you must full-erase, **back up the public and private keys first** from the phone
  app's Security settings, and restore them after. Users report this is far less work than
  chasing down every peer afterwards.

**Cure, once it has happened - and which side matters:**

> **★ Refined 2026-09-04 by measurement.** After both sides cleared the node, our DM
> **ACKed**. But the public key *we* held for KV9G came back **byte-identical** to the one
> we had before (`y9m2DDyD83e0kavLB8t1/N39…`). So our copy was never the stale one.
>
> **The stale copy was on the receiving side** - his phone's stored key for *our* node.
> That is why our DM NAKed with NO_CHANNEL: he could not decrypt it. Clearing it here was
> belt-and-braces; **clearing it there was the fix.**
>
> Which sharpens why this is a deadlock: **the node that must act is the one that cannot be
> reached.** You cannot DM someone to tell them their key for you is stale, because that DM
> is the broken thing. Broadcast still works, so a channel message is the only way to ask.

- **The receiver must forget the sender.** Clearing on the sending side alone will not fix
  it. Clear both if you cannot tell which way round it is.
  - Phone app: long-press the node, remove it.
  - CLI: `meshtastic --port COM4 --remove-node '!2d21195a'`
- Then wait for the node to re-announce. **Default `nodeInfoBroadcastSecs` is 10800, three
  hours**, so it is not instant. Sending any message from the other node makes it announce
  immediately, which is much faster than waiting.

### For the stage

One sentence on the setup slide, at the "update it" step:

> "When you update, do not tick full erase. It wipes your radio's identity, and your
> direct messages to everyone who already knows you stop working until both of you delete
> each other and start over."

That is a real, checkable, avoidable footgun, and it lands on the exact step where they
will meet it.

---

## Position privacy: the mesh deliberately blurs where you are

*Confirmed bit-exactly on our own data 2026-09-04, after it fooled us for an afternoon.*

Meshtastic reduces the precision of the position it shares, per channel. It masks the low
bits of the integer latitude/longitude and adds half a cell, so what goes out is the
**centre of a grid cell**, not your house:

```
published = (value & (0xFFFFFFFF << (32 - bits))) + (1 << (31 - bits))
```

Our primary channel runs `positionPrecision: 13`, which is the default here.

| | latitude | longitude |
|---|---|---|
| Michael's actual house | 37.32970 | -92.89390 |
| **What the mesh publishes** | **37.35552** | **-92.87762** |

Masking `373297000` at 13 bits gives `373555200` **exactly**. The published point sits
**3.22 km / 2.00 mi** from the real one, and a 13-bit cell is **2.45 km (1.52 mi)** tall.

### Why this fooled us, and why it will fool the room

**Every node at the house reports the identical coordinate** - the Indicator, the solar
node, the T1000-E, and John-Base down the street. They are all in one cell, so they all
publish one point. We read that as "the home cluster", used it as a reference, and computed
two miles of nonsense from it.

**The tell we missed:** John lives down the street and reported coordinates identical to
the house, to seven decimal places. Real GPS never agrees like that. Identical positions
across several nodes means quantisation, not a location.

### For the talk - this is a good slide, not a footnote

People assume a GPS tracker on a public channel broadcasts their address. **It does not,
by default.** It broadcasts a ~1.5 mile square. That is a genuine privacy feature that
nobody explains, and it answers a question this audience will actually have.

And the flip side, which is the honest half: **on your own private channel you can raise
the precision**, and then it really is your address. So the rule to say out loud:

> "Your public position is a blurred square about a mile and a half across. Your private
> family channel can carry your exact position. Know which one you are sharing on."

### ⚠ Consequence for range testing

**You cannot measure range from public-channel positions.** The quantisation is 2.45 km,
which is larger than most of the range you are trying to measure. Every sample inside one
cell reports the same coordinate.

A range test needs full-precision position, which means running it **on a private channel
with `positionPrecision` raised**, and saying so in the writeup. See
[range-test.md](range-test.md).
