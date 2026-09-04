"""Follow one node's position reports live off a serial radio.

Written 2026-09-04 to track KV9G while Michael drove. Prints one line per fix:
time, coordinates, distance and bearing from a reference point, movement since
the previous fix, and the RF quality of the packet that carried it.

Why a script instead of `meshtastic --listen`: --listen prints the full debug
firehose, and the position packets are buried in it. This subscribes to the
position topic directly.

Note on precision: if the channel sets positionPrecision below full, the
coordinates are deliberately quantised before transmission. Movement then shows
up as jumps between grid cells rather than a smooth track. That is the sender
protecting their location, not a broken GPS.

Usage:
  python scripts/track-node.py --port COM4 --node '!2d21195a' --seconds 900
  python scripts/track-node.py --port COM4            # follow every node
"""

import argparse
import math
import sys
import time
from datetime import datetime

import meshtastic.serial_interface
from pubsub import pub

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# The home cluster, from nodes parked at the house.
REF_LAT, REF_LON = 37.35552, -92.8776192
POINTS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

last = {}   # node id -> (lat, lon, monotonic time)
count = 0


def vector(lat1, lon1, lat2, lon2):
    """Great-circle-ish distance in km and bearing in degrees. Flat-earth is
    fine at these ranges and avoids pretending to more accuracy than the
    quantised input has."""
    dlat = (lat2 - lat1) * 111.32
    dlon = (lon2 - lon1) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dlat, dlon), (math.degrees(math.atan2(dlon, dlat)) + 360) % 360


def compass(bearing):
    return POINTS[round(bearing / 22.5) % 16]


def on_position(packet, interface):
    global count
    node = packet.get("fromId")
    if TARGET and node != TARGET:
        return
    pos = (packet.get("decoded") or {}).get("position") or {}
    lat, lon = pos.get("latitude"), pos.get("longitude")
    if lat is None or lon is None:
        return

    count += 1
    dist, brg = vector(REF_LAT, REF_LON, lat, lon)
    line = (f"{datetime.now():%H:%M:%S}  {node}  {lat:.5f},{lon:.5f}"
            f"  {dist:5.2f} km / {dist*0.6214:5.2f} mi {compass(brg)}"
            f"  alt {pos.get('altitude','?')}m")

    prev = last.get(node)
    if prev:
        moved, mbrg = vector(prev[0], prev[1], lat, lon)
        dt = time.monotonic() - prev[2]
        line += f"  | moved {moved*1000:6.0f} m {compass(mbrg)} in {dt:4.0f}s"
        if dt > 0 and moved > 0:
            line += f" ({moved/(dt/3600):4.1f} km/h)"
    else:
        line += "  | first fix"

    snr, rssi = packet.get("rxSnr"), packet.get("rxRssi")
    if snr is not None:
        line += f"  [snr {snr} rssi {rssi} hops {packet.get('hopStart',0) - packet.get('hopLimit',0)}]"

    print(line, flush=True)
    last[node] = (lat, lon, time.monotonic())


def on_text(packet, interface):
    node = packet.get("fromId")
    txt = (packet.get("decoded") or {}).get("text", "")
    print(f"{datetime.now():%H:%M:%S}  {node}  TEXT: {txt}", flush=True)


ap = argparse.ArgumentParser()
ap.add_argument("--port", default="COM4")
ap.add_argument("--node", default=None, help="node id to follow, e.g. '!2d21195a'")
ap.add_argument("--seconds", type=int, default=900)
args = ap.parse_args()
TARGET = args.node

pub.subscribe(on_position, "meshtastic.receive.position")
pub.subscribe(on_text, "meshtastic.receive.text")

print(f"tracking {TARGET or 'ALL nodes'} on {args.port} for {args.seconds}s")
print(f"reference point (home cluster): {REF_LAT}, {REF_LON}")
print("-" * 100, flush=True)

iface = meshtastic.serial_interface.SerialInterface(devPath=args.port)
try:
    time.sleep(args.seconds)
finally:
    iface.close()
    print("-" * 100)
    print(f"done. {count} position fix(es) captured.")
