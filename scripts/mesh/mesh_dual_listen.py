"""Listen on BOTH radios at once; optionally transmit a tagged broadcast.

Broadcast on the primary channel avoids the PKI/NO_CHANNEL path that directed
messages take, so this measures the physical layer: did the other radio HEAR it.

  python mesh_dual_listen.py <seconds> [--tx COM15] [--tag TAG]

Prints every packet each radio receives, tagged by the port that heard it.
"""
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

import meshtastic.serial_interface
from meshtastic.protobuf import config_pb2
from pubsub import pub

secs = float(sys.argv[1]) if len(sys.argv) > 1 else 90.0
tx_port = None
tag = f"T{int(time.time()) % 10000}"
args = sys.argv[2:]
for i, a in enumerate(args):
    if a == "--tx":
        tx_port = args[i + 1]
    if a == "--tag":
        tag = args[i + 1]

PORTS = ["COM14", "COM15"]
ifaces = {}
label = {}
heard = {p: [] for p in PORTS}


def on_receive(packet, interface):
    port = label.get(id(interface), "?")
    d = packet.get("decoded", {}) or {}
    portnum = d.get("portnum", "?")
    txt = d.get("text")
    frm = packet.get("fromId")
    snr = packet.get("rxSnr")
    hops = packet.get("hopStart")
    rec = (time.strftime("%H:%M:%S"), frm, portnum, txt, snr, hops)
    heard[port].append(rec)
    extra = f" text={txt!r}" if txt else ""
    print(f"  [{rec[0]}] {port} <- {frm} {portnum} snr={snr} hops={hops}{extra}",
          flush=True)


pub.subscribe(on_receive, "meshtastic.receive")

for p in PORTS:
    try:
        it = meshtastic.serial_interface.SerialInterface(devPath=p)
        ifaces[p] = it
        label[id(it)] = p
        lora = it.localNode.localConfig.lora
        pre = config_pb2.Config.LoRaConfig.ModemPreset.Name(lora.modem_preset)
        print(f"listening {p}: !{it.myInfo.my_node_num:08x} preset={pre} bw={lora.bandwidth}")
    except Exception as e:
        print(f"{p} OPEN FAILED {type(e).__name__}: {e}")

if tx_port and tx_port in ifaces:
    msg = f"linktest {tag}"
    print(f"\nTX from {tx_port}: {msg!r} (broadcast, primary channel)")
    ifaces[tx_port].sendText(msg)

print(f"\n--- listening {secs:.0f}s ---", flush=True)
t0 = time.time()
while time.time() - t0 < secs:
    time.sleep(1)

print("\n=== SUMMARY ===")
for p in PORTS:
    pre = "?"
    if p in ifaces:
        pre = config_pb2.Config.LoRaConfig.ModemPreset.Name(
            ifaces[p].localNode.localConfig.lora.modem_preset)
    print(f"{p} ({pre}): {len(heard[p])} packets received")
    for r in heard[p]:
        print(f"   {r[0]} from={r[1]} {r[2]} text={r[3]!r} snr={r[4]}")
    if tx_port:
        hit = [r for r in heard[p] if r[3] and tag in str(r[3])]
        print(f"   -> saw the {tag} broadcast: {'YES' if hit else 'NO'}")

for it in ifaces.values():
    try:
        it.close()
    except Exception:
        pass
