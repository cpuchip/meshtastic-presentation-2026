# Asset sources

## Device images (`images/`)

Copied 2026-08-28 from the official Meshtastic docs repository
(https://github.com/meshtastic/meshtastic, GPL-3.0), path
`static/img/hardware/`. Product photos originate with the vendors (Heltec,
Seeed Studio, RAKwireless, LILYGO); used here for a free educational
presentation with attribution.

| File | Origin path in docs repo |
|---|---|
| meshtastic-logo.webp | static/img/hardware/meshtastic-logo.webp |
| heltec-v4.webp | static/img/hardware/heltec/heltec-V4.webp |
| heltec-v3.webp | static/img/hardware/HTIT-WB32LA(F)_V3.webp |
| sensecap-t1000e.webp | static/img/hardware/seeed/T1000-E.webp |
| sensecap-solar-node.webp | static/img/hardware/seeed/sensecap_solar_node.webp |
| wio-tracker-l1.webp | static/img/hardware/seeed/wio_tracker_l1.webp |
| rak-wisblock.webp | static/img/hardware/rak4631_5005.webp |
| lilygo-t-deck.webp | static/img/hardware/LILYGO-T-DECK.webp |
| lilygo-t-echo.webp | static/img/hardware/t-echo-lilygo.webp |
| lilygo-t-beam.webp | static/img/hardware/t-beam-meshtastic.webp |
| station-g2.webp | static/img/hardware/station-series/station-g2-front.webp |
| rak-wismesh-pocket.webp | static/img/hardware/rak/pocket-v2.webp |
| rak-wismesh-repeater.webp | static/img/hardware/rak/wismesh-repeater.webp |
| rak-wismesh-tap.webp | static/img/hardware/rak/wismesh-tap.webp |
| elecrow-thinknode-m1.webp | static/img/hardware/elecrow/Thinknode-m1_for_Meshtastic.webp |
| muzi-r1-neo.webp | static/img/hardware/muzi/muziworks-r1-neo.webp |
| nano-g2-ultra.webp | static/img/hardware/nano_g2_ultra.webp |
| canary-one.webp | static/img/hardware/canary-one/perspective.webp |
| heltec-meshpocket.webp | static/img/hardware/heltec/meshpocket.webp |

## Diagrams (`diagrams/`)

Original SVGs drawn for this talk (ours, no external source). Theme-aware:
lines and text use `currentColor` so they inherit the slide theme; accents are
LCARS orange #FF9C00, blue #47A3FF, green #3FB950, red #E5534B — all chosen to
read on both dark and light backgrounds.

- `how-it-works.svg` — phone ⇄ node (Bluetooth) ⇄ node (LoRa, miles) ⇄ phone
- `mesh-hops.svg` — blocked direct path vs. two hops through a hilltop node
- `height-wins.svg` — desk / window / 35-ft pole / hilltop range comparison

## Event

- `expo-saturday-schedule-2026.png` — downloaded 2026-08-28 from
  ozarkshomesteading.com's image CDN (img1.wsimg.com), the published Final
  Saturday Schedule 2026. Reference/verification use.

## Still needed

- [ ] Photo of Michael's own 35-ft pole node + P1-Pro (take on site — the
      lived-story slide should show OUR hardware, not a catalog shot)
- [ ] Mesh-topology diagram in the site theme (draw as SVG during the
      cpuchip.net adaptation; don't borrow one)
- [ ] Screenshots of the phone app pairing/channel-QR flow for slide 14 backup

## Our own photographs (not third-party, no attribution needed)

- `images/solar-node-pole.webp` - Michael's SenseCAP Solar Node **SNST_cb53** on his
  35-foot flagpole, photographed 2026-09-04. Ours to use anywhere, including the
  cpuchip.net presentations tab. EXIF rotation was baked in rather than left as an
  orientation tag, because not every slide renderer or print pipeline honours the tag and
  a sideways flagpole is not recoverable from the podium. Resized to 1400x1867.
