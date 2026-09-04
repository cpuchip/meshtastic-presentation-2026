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

Default is **LONG_FAST**. It bundles bandwidth, spreading factor and coding rate. Nine
presets exist, from `SHORT_TURBO` to `VERY_LONG_SLOW`. Two nodes on different presets are
deaf to each other, full stop.

Leave it on LONG_FAST. The whole public mesh is there, and the slower presets buy range
you will not notice while costing airtime everyone shares.

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

Our demo node runs the stock primary: empty name, default key, US/LONG_FAST, slot 20. The
regional network (LZMesh, SWMO) shows most nodes on a **named** channel, `CHAOS JLN Main`.

If that name is their **primary**, then by the hash rule they are on a **different
frequency slot** than a stock node, and a factory-fresh radio in Marshfield cannot hear
them at all - not "cannot decrypt them", cannot *hear* them. If it is a **secondary**
channel on a stock primary, the radios do hear each other and just cannot read that
traffic.

**We should ask in their Discord which it is before Saturday**, because the answer changes
what we tell the room to do. Do not guess this on stage.

Either way the lesson for a beginner holds and is worth the slide: **an empty node list is
usually a settings mismatch, not a dead mesh.**

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

- [ ] **Ask LZMesh whether `CHAOS JLN Main` is their primary or a secondary.** Changes the
      advice we give the room. Their Discord: https://discord.lzarc.com
