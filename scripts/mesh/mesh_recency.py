"""Zero-hop nodes with LAST-HEARD recency.

nodedb presence is a HISTORICAL record: an entry can survive a preset change,
so "in the DB" never means "reachable now". This prints age since last heard so
live links can be told from fossils.
"""
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")

import meshtastic.serial_interface
from meshtastic.protobuf import config_pb2


def preset_name(v):
    try:
        return config_pb2.Config.LoRaConfig.ModemPreset.Name(v)
    except Exception:
        return f"<{v}>"


def age(ts, now):
    if not ts:
        return "never"
    d = now - ts
    if d < 90:
        return f"{int(d)}s ago"
    if d < 5400:
        return f"{d / 60:.1f}m ago"
    if d < 172800:
        return f"{d / 3600:.1f}h ago"
    return f"{d / 86400:.1f}d ago"


for port in sys.argv[1:] or ["COM14", "COM15"]:
    iface = None
    try:
        iface = meshtastic.serial_interface.SerialInterface(devPath=port)
        now = time.time()
        lora = iface.localNode.localConfig.lora
        my = iface.myInfo.my_node_num
        print(f"\n=== {port}  preset={preset_name(lora.modem_preset)} "
              f"bw={lora.bandwidth}  me=!{my:08x} ===")
        rows = []
        for nid, n in iface.nodes.items():
            if nid == f"!{my:08x}":
                continue
            hops = n.get("hopsAway")
            lh = n.get("lastHeard")
            rows.append((lh or 0, nid, n.get("user", {}).get("longName"), hops, n.get("snr")))
        rows.sort(reverse=True)
        fresh = [r for r in rows if r[0] and (now - r[0]) < 3600]
        print(f"  {len(rows)} peers; {len(fresh)} heard within the last hour")
        print("  --- 12 most recently heard ---")
        for lh, nid, ln, hops, snr in rows[:12]:
            print(f"    {nid} {str(ln)[:30]:30s} hops={str(hops):>4s} "
                  f"snr={str(snr):>6s}  {age(lh, now)}")
    except Exception as e:
        print(f"{port} ERROR {type(e).__name__}: {e}")
    finally:
        if iface:
            try:
                iface.close()
            except Exception:
                pass
