"""Active link test: send a DM with wantAck and wait for the routing ACK.

An ACK proves a ROUND TRIP (they heard us, we heard them) — unlike nodedb
presence, which is only history. Absence of ACK is weaker evidence than its
presence, so always pair a negative with a positive control on the same radio.

  python mesh_linktest.py COM15 '!d5faaa85' "text"
"""
import sys
import threading
import time

sys.stdout.reconfigure(encoding="utf-8")

import meshtastic.serial_interface
from meshtastic.protobuf import config_pb2

port, dest = sys.argv[1], sys.argv[2]
text = sys.argv[3] if len(sys.argv) > 3 else "link test"
TIMEOUT = float(sys.argv[4]) if len(sys.argv) > 4 else 45.0

got = threading.Event()
result = {}


def on_response(packet):
    d = packet.get("decoded", {})
    routing = d.get("routing", {})
    result["error"] = routing.get("errorReason", "NONE")
    result["from"] = packet.get("fromId")
    result["rx_snr"] = packet.get("rxSnr")
    result["hops"] = packet.get("hopStart")
    got.set()


iface = meshtastic.serial_interface.SerialInterface(devPath=port)
lora = iface.localNode.localConfig.lora
preset = config_pb2.Config.LoRaConfig.ModemPreset.Name(lora.modem_preset)
me = iface.myInfo.my_node_num
print(f"radio  : {port}  !{me:08x}  preset={preset} bw={lora.bandwidth}")
print(f"target : {dest}")
print(f"text   : {text!r}")

t0 = time.time()
iface.sendText(text, destinationId=dest, wantAck=True, onResponse=on_response)
print(f"sent, waiting up to {TIMEOUT:.0f}s for routing ACK ...")
ok = got.wait(TIMEOUT)
dt = time.time() - t0

if ok and result.get("error") in (None, "NONE", 0):
    print(f"RESULT: ACK in {dt:.1f}s from {result.get('from')} "
          f"snr={result.get('rx_snr')} -> ROUND TRIP CONFIRMED")
elif ok:
    print(f"RESULT: NAK after {dt:.1f}s error={result.get('error')} -> delivery FAILED")
else:
    print(f"RESULT: NO ACK within {TIMEOUT:.0f}s -> no round trip (deaf, absent, or out of range)")

try:
    iface.close()
except Exception:
    pass
