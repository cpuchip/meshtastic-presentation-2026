"""Log every packet heard from a node, with position and RF quality, to CSV.

The receiving half of a range test. Runs on the FIXED radio (the one at the
house). The mobile radio does not need any special software - anything it
transmits is a sample.

Design notes, all of them paid for on 2026-09-04:

  - LISTEN ONLY. The python API's sendPosition() wedged silently here for ten
    minutes, producing no output while looking alive. Receiving via pubsub is
    proven; do any transmitting with the CLI in a separate step.

  - Log EVERY packet type, not just positions. SNR and RSSI ride on all of them,
    so telemetry and nodeinfo are range samples too. Position packets are the
    ones that also carry a location.

  - Write and flush per row. A range test ends when the car comes back, not when
    the script decides; a buffered file that dies with the process loses the run.

  - Record the packet's own rxTime and the wall clock separately. They disagree
    on this hardware: the nodedb lastHeard field read seven weeks stale while we
    were actively exchanging acks with the node.

Usage:
  python scripts/range-log.py --port COM4 --node '!2d21195a' --out range.csv --seconds 3600
  python scripts/range-log.py --port COM4 --out range-all.csv     # every node
"""

import argparse
import csv
import sys
import time
from datetime import datetime

import meshtastic.serial_interface
from pubsub import pub

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

COLS = ["wall_time", "rx_time", "from_id", "portnum", "lat", "lon", "alt",
        "snr", "rssi", "hop_start", "hop_limit", "hops_used", "seq", "text"]

rows = 0
writer = None
fh = None
TARGET = None


def on_packet(packet, interface):
    global rows
    node = packet.get("fromId")
    if TARGET and node != TARGET:
        return
    dec = packet.get("decoded") or {}
    pos = dec.get("position") or {}
    hs, hl = packet.get("hopStart"), packet.get("hopLimit")

    text = dec.get("text", "")
    seq = ""
    # The range-test module sends "seq N" style payloads; capture the number so
    # gaps in the sequence become measurable packet loss.
    if text.lower().startswith("seq "):
        seq = text.split()[1] if len(text.split()) > 1 else ""

    row = {
        "wall_time": datetime.now().isoformat(timespec="seconds"),
        "rx_time": packet.get("rxTime", ""),
        "from_id": node,
        "portnum": dec.get("portnum", ""),
        "lat": pos.get("latitude", ""),
        "lon": pos.get("longitude", ""),
        "alt": pos.get("altitude", ""),
        "snr": packet.get("rxSnr", ""),
        "rssi": packet.get("rxRssi", ""),
        "hop_start": hs if hs is not None else "",
        "hop_limit": hl if hl is not None else "",
        "hops_used": (hs - hl) if (hs is not None and hl is not None) else "",
        "seq": seq,
        "text": text[:120],
    }
    writer.writerow(row)
    fh.flush()
    rows += 1

    loc = f"{row['lat']:.5f},{row['lon']:.5f}" if row["lat"] != "" else "        no position"
    print(f"{datetime.now():%H:%M:%S}  #{rows:<4} {node}  {row['portnum']:<18} "
          f"{loc}  snr {row['snr']!s:>6}  rssi {row['rssi']!s:>5}  hops {row['hops_used']}",
          flush=True)


ap = argparse.ArgumentParser()
ap.add_argument("--port", default="COM4")
ap.add_argument("--node", default=None, help="only log this node id")
ap.add_argument("--out", default="range.csv")
ap.add_argument("--seconds", type=int, default=3600)
args = ap.parse_args()
TARGET = args.node

fh = open(args.out, "w", newline="", encoding="utf-8")
writer = csv.DictWriter(fh, fieldnames=COLS)
writer.writeheader()
fh.flush()

for topic in ("position", "text", "telemetry", "data", "user"):
    try:
        pub.subscribe(on_packet, f"meshtastic.receive.{topic}")
    except Exception:
        pass

print(f"logging {TARGET or 'ALL nodes'} on {args.port} -> {args.out}  ({args.seconds}s)")
print("every packet is a range sample: SNR and RSSI ride on all of them.")
print("-" * 104, flush=True)

iface = meshtastic.serial_interface.SerialInterface(devPath=args.port)
try:
    time.sleep(args.seconds)
finally:
    iface.close()
    fh.close()
    print("-" * 104)
    print(f"done. {rows} packet(s) logged to {args.out}")
