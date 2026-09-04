"""Inventory the Meshtastic radios on this box: identity + LoRa config + nodedb.

Read-only. Prints nothing secret except channel PSK presence (never the key).
Usage: python mesh_inventory.py COM14 COM15
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import meshtastic
import meshtastic.serial_interface
from meshtastic.protobuf import config_pb2


def preset_name(v):
    try:
        return config_pb2.Config.LoRaConfig.ModemPreset.Name(v)
    except Exception:
        return f"<{v}>"


def region_name(v):
    try:
        return config_pb2.Config.LoRaConfig.RegionCode.Name(v)
    except Exception:
        return f"<{v}>"


def inspect(port):
    print(f"\n{'=' * 60}\nPORT {port}\n{'=' * 60}")
    iface = None
    try:
        iface = meshtastic.serial_interface.SerialInterface(devPath=port)
        info = iface.myInfo
        node = iface.localNode
        my_num = getattr(info, "my_node_num", None)

        me = iface.nodes.get(f"!{my_num:08x}") if my_num else None
        user = (me or {}).get("user", {})
        print(f"  long name   : {user.get('longName')}")
        print(f"  short name  : {user.get('shortName')}")
        print(f"  node id     : {user.get('id')}  (num {my_num})")
        print(f"  hw model    : {user.get('hwModel')}")
        meta = getattr(iface, "metadata", None)
        if meta is not None:
            print(f"  firmware    : {getattr(meta, 'firmware_version', '?')}")

        lora = node.localConfig.lora
        print(f"  region      : {region_name(lora.region)}")
        print(f"  MODEM PRESET: {preset_name(lora.modem_preset)}")
        print(f"  use_preset  : {lora.use_preset}")
        print(f"  bandwidth   : {lora.bandwidth}  sf: {lora.spread_factor}  cr: {lora.coding_rate}")
        print(f"  freq slot   : {lora.channel_num}  (0 = auto/hashed)")
        print(f"  hop limit   : {lora.hop_limit}")

        print("  channels:")
        for ch in node.channels:
            if ch.role == 0:  # DISABLED
                continue
            role = {1: "PRIMARY", 2: "SECONDARY"}.get(ch.role, str(ch.role))
            name = ch.settings.name or "(blank)"
            psk = ch.settings.psk
            if len(psk) == 0:
                pskdesc = "none"
            elif len(psk) == 1:
                pskdesc = f"default (single byte 0x{psk[0]:02x})"
            else:
                pskdesc = f"{len(psk)}-byte key"
            print(f"    [{ch.index}] {role:9s} name={name!r} psk={pskdesc}")

        print(f"  nodedb ({len(iface.nodes)} entries):")
        for nid, n in sorted(iface.nodes.items()):
            u = n.get("user", {})
            mine = "  <-- THIS RADIO" if my_num and nid == f"!{my_num:08x}" else ""
            hops = n.get("hopsAway", "?")
            snr = n.get("snr", "?")
            print(f"    {nid} {str(u.get('shortName')):>6s} "
                  f"{str(u.get('longName'))[:28]:28s} hops={hops} snr={snr}{mine}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")
    finally:
        if iface is not None:
            try:
                iface.close()
            except Exception:
                pass


if __name__ == "__main__":
    ports = sys.argv[1:] or ["COM14", "COM15"]
    for p in ports:
        inspect(p)
    print("\ndone")
