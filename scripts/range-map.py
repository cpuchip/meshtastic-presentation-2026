"""Turn a range-log CSV into a self-contained interactive map plus a summary.

Reads the CSV from range-log.py and writes one HTML file: every sample plotted
at the mobile node's reported position, coloured by SNR, with the fixed node
marked and a line to the furthest confirmed contact.

The HTML is self-contained apart from the map tiles, which need internet to
draw. That is fine for building the slide at home and wrong for the pavilion,
so it also prints a text summary that stands on its own with no network.

Honest limits, stated on the map itself rather than buried here:
  - Distance is computed from the MOBILE node's own reported position. If that
    position is stale or coarse, the distance inherits the error.
  - A sample proves the fixed node HEARD the mobile one. It does not prove the
    reverse; only an acknowledged message proves both directions.

Usage:
  python scripts/range-map.py --csv range.csv --home 37.3297,-92.8939 --out range-map.html
"""

import argparse
import csv
import json
import math
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--csv", default="range.csv")
ap.add_argument("--home", required=True, help="lat,lon of the FIXED radio")
ap.add_argument("--out", default="range-map.html")
ap.add_argument("--title", default="Meshtastic range test")
args = ap.parse_args()

HLAT, HLON = [float(x) for x in args.home.split(",")]


def dist_km(lat, lon):
    dlat = (lat - HLAT) * 111.32
    dlon = (lon - HLON) * 111.32 * math.cos(math.radians((lat + HLAT) / 2))
    return math.hypot(dlat, dlon)


pts, no_pos, ports = [], 0, Counter()
with open(args.csv, encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        ports[r["portnum"]] += 1
        if not r["lat"]:
            no_pos += 1
            continue
        lat, lon = float(r["lat"]), float(r["lon"])
        pts.append({
            "lat": lat, "lon": lon,
            "d": round(dist_km(lat, lon), 3),
            "snr": float(r["snr"]) if r["snr"] else None,
            "rssi": int(r["rssi"]) if r["rssi"] else None,
            "hops": r["hops_used"], "t": r["wall_time"], "port": r["portnum"],
        })

if not pts:
    print(f"No positioned samples in {args.csv}.")
    print(f"  {sum(ports.values())} packet(s) total, {no_pos} without a position.")
    print("  Packet types seen:", dict(ports))
    print("\nA range test needs the mobile node to be BROADCASTING ITS POSITION.")
    print("Check that its GPS has a fix and that position broadcast is on.")
    raise SystemExit(1)

pts.sort(key=lambda p: p["t"])
far = max(pts, key=lambda p: p["d"])

print(f"{len(pts)} positioned sample(s), {no_pos} without position")
print(f"furthest contact : {far['d']:.2f} km / {far['d']*0.6214:.2f} mi "
      f"(snr {far['snr']}, rssi {far['rssi']}) at {far['t']}")
print(f"distance range   : {min(p['d'] for p in pts):.2f} - {far['d']:.2f} km")
snrs = [p["snr"] for p in pts if p["snr"] is not None]
if snrs:
    print(f"snr range        : {min(snrs)} to {max(snrs)}")
print("packet types     :", dict(ports))

html = """<!doctype html><meta charset="utf-8"><title>__TITLE__</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
 html,body{margin:0;height:100%;font:14px system-ui,sans-serif}
 #map{height:100%}
 .box{position:absolute;top:10px;right:10px;z-index:1000;background:#fff;
      padding:10px 12px;border:1px solid #333;max-width:300px;line-height:1.4}
 .box h3{margin:0 0 6px;font-size:14px}
 .cav{margin-top:8px;padding-top:8px;border-top:1px solid #ccc;font-size:12px;color:#444}
</style>
<div id="map"></div>
<div class="box">
  <h3>__TITLE__</h3>
  <b>__N__</b> samples &middot; furthest <b>__FAR__ mi</b><br>
  Colour = SNR: <span style="color:#0a0">good</span> /
  <span style="color:#c80">fair</span> / <span style="color:#c00">weak</span>
  <div class="cav">
    Distance is from the mobile node's <i>own reported position</i>; if that is
    coarse or stale, the distance inherits the error. A dot means the base
    <i>heard</i> the mobile node. Only an acknowledged message proves both
    directions.
  </div>
</div>
<script>
const home = [__HLAT__, __HLON__], pts = __PTS__;
const map = L.map('map').setView(home, 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  {maxZoom:19, attribution:'&copy; OpenStreetMap'}).addTo(map);
L.circleMarker(home,{radius:9,color:'#000',fillColor:'#fff',fillOpacity:1,weight:3})
 .addTo(map).bindPopup('Base radio');
function col(s){ if(s===null) return '#888'; if(s>=5) return '#0a0'; if(s>=0) return '#c80'; return '#c00'; }
const bounds=[home];
for(const p of pts){
  bounds.push([p.lat,p.lon]);
  L.circleMarker([p.lat,p.lon],{radius:5,color:col(p.snr),fillColor:col(p.snr),
    fillOpacity:.85,weight:1}).addTo(map)
   .bindPopup(`<b>${p.d.toFixed(2)} km</b> (${(p.d*0.6214).toFixed(2)} mi)<br>
     snr ${p.snr} &middot; rssi ${p.rssi} &middot; hops ${p.hops}<br>${p.t}<br><i>${p.port}</i>`);
}
const far = pts.reduce((a,b)=>b.d>a.d?b:a);
L.polyline([home,[far.lat,far.lon]],{color:'#000',dashArray:'6,6',weight:2}).addTo(map);
map.fitBounds(bounds,{padding:[40,40]});
</script>"""

html = (html.replace("__TITLE__", args.title)
            .replace("__N__", str(len(pts)))
            .replace("__FAR__", f"{far['d']*0.6214:.2f}")
            .replace("__HLAT__", str(HLAT)).replace("__HLON__", str(HLON))
            .replace("__PTS__", json.dumps(pts)))

with open(args.out, "w", encoding="utf-8") as fh:
    fh.write(html)
print(f"\nwrote {args.out} - open it in a browser (tiles need internet)")
