"""Actively ping one node on a schedule, and log everything that comes back.

Written 2026-09-04 to keep reaching KV9G while Michael drove out of range and
his radio power-cycled. One serial connection does both jobs: a serial port
cannot be shared, so a separate listener and pinger will fight over it.

Why active pings and not just listening: a passive listener cannot tell
"he is out of range" from "he simply has not transmitted yet." An acknowledged
direct message is a round trip, so a reply proves the link works in BOTH
directions at that moment. That is the honest instrument for a range test.

Each ping is a position request, which is cheap and asks for exactly the thing
worth knowing. Anything heard in between - position, text, telemetry, or the
node reappearing at all - is logged too.

Usage:
  python scripts/ping-node.py --port COM4 --node '!2d21195a' --every 90 --seconds 1800
"""

import argparse
import math
import sys
import threading
import time
from datetime import datetime

import meshtastic.serial_interface
from pubsub import pub

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REF_LAT, REF_LON = 37.35552, -92.8776192
POINTS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

heard = {"count": 0, "last": None}


def stamp():
    return f"{datetime.now():%H:%M:%S}"


def vector(lat1, lon1, lat2, lon2):
    dlat = (lat2 - lat1) * 111.32
    dlon = (lon2 - lon1) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dlat, dlon), (math.degrees(math.atan2(dlon, dlat)) + 360) % 360


def compass(b):
    return POINTS[round(b / 22.5) % 16]


def rf(packet):
    snr, rssi = packet.get("rxSnr"), packet.get("rxRssi")
    if snr is None:
        return ""
    hops = packet.get("hopStart", 0) - packet.get("hopLimit", 0)
    return f"  [snr {snr} rssi {rssi} hops {hops}]"


def on_any(packet, interface):
    node = packet.get("fromId")
    if node != TARGET:
        return
    heard["count"] += 1
    heard["last"] = time.monotonic()
    dec = packet.get("decoded") or {}
    kind = dec.get("portnum", "?")

    if kind == "POSITION_APP":
        p = dec.get("position") or {}
        lat, lon = p.get("latitude"), p.get("longitude")
        if lat is not None:
            d, b = vector(REF_LAT, REF_LON, lat, lon)
            print(f"{stamp()}  ◄ POSITION  {lat:.5f},{lon:.5f}  "
                  f"{d:5.2f} km / {d*0.6214:5.2f} mi {compass(b)}  "
                  f"alt {p.get('altitude','?')}m{rf(packet)}", flush=True)
            return
    if kind == "TEXT_MESSAGE_APP":
        print(f"{stamp()}  ◄ TEXT  {dec.get('text','')}{rf(packet)}", flush=True)
        return
    print(f"{stamp()}  ◄ {kind}{rf(packet)}", flush=True)


ap = argparse.ArgumentParser()
ap.add_argument("--port", default="COM4")
ap.add_argument("--node", required=True)
ap.add_argument("--every", type=int, default=90, help="seconds between pings")
ap.add_argument("--seconds", type=int, default=1800)
args = ap.parse_args()
TARGET = args.node

for topic in ("position", "text", "telemetry", "data"):
    try:
        pub.subscribe(on_any, f"meshtastic.receive.{topic}")
    except Exception:
        pass

print(f"pinging {TARGET} on {args.port} every {args.every}s for {args.seconds}s")
print("◄ = heard from him.  ► = we transmitted.  Silence between pings is normal.")
print("-" * 96, flush=True)

iface = meshtastic.serial_interface.SerialInterface(devPath=args.port)
stop = threading.Event()
deadline = time.monotonic() + args.seconds
n = 0
try:
    while not stop.wait(0) and time.monotonic() < deadline:
        n += 1
        try:
            iface.sendPosition(destinationId=TARGET, wantResponse=True)
            print(f"{stamp()}  ► ping #{n} sent (position request)", flush=True)
        except Exception as e:
            print(f"{stamp()}  ► ping #{n} FAILED to send: {e}", flush=True)
        # sleep in slices so the receive callbacks stay responsive
        end = min(time.monotonic() + args.every, deadline)
        while time.monotonic() < end:
            time.sleep(1)
finally:
    iface.close()
    print("-" * 96)
    last = heard["last"]
    ago = f"{time.monotonic()-last:.0f}s ago" if last else "never"
    print(f"done. {n} ping(s) sent, {heard['count']} packet(s) heard from {TARGET} (last: {ago}).")
