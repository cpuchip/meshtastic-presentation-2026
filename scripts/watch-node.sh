#!/usr/bin/env bash
# Poll one node's position and RF quality on a loop, and log only what changes.
#
# Written 2026-09-04 after the python-API version wedged inside the library call
# and produced nothing for ten minutes. This drives the `meshtastic` CLI instead,
# which has been reliable all session. Slower per sample (a full connect and
# config download each time, ~20-30 s) but it cannot hang silently, and a sample
# every minute is plenty for a car.
#
# Prints a line per poll: position, distance from home, SNR, hops, and whether
# anything moved since last time. A repeated position is itself the signal - it
# means we are no longer hearing fresh fixes.
#
# Usage: scripts/watch-node.sh COM4 '!2d21195a' 60 2400

PORT="${1:-COM4}"
NODE="${2:-!2d21195a}"
EVERY="${3:-60}"
TOTAL="${4:-2400}"

export PATH="$PATH:/c/Users/cpuch/AppData/Roaming/Python/Python314/Scripts"

echo "watching $NODE on $PORT every ${EVERY}s for ${TOTAL}s"
echo "reference: home cluster 37.35552,-92.8776192"
echo "------------------------------------------------------------------------------"

END=$(( $(date +%s) + TOTAL ))
N=0
while [ "$(date +%s)" -lt "$END" ]; do
  N=$((N+1))
  timeout 120 meshtastic --port "$PORT" --info 2>/dev/null | NODE="$NODE" N="$N" python -c "
import sys, re, json, math, os
from datetime import datetime
t = sys.stdin.read()
node = os.environ['NODE']; n = os.environ['N']
m = re.search(r'Nodes in mesh: (\{.*?\n\})\n', t, re.S)
ts = datetime.now().strftime('%H:%M:%S')
if not m:
    print(f'{ts}  #{n}  (could not read nodedb)', flush=True); raise SystemExit
d = json.loads(m.group(1))
v = d.get(node)
if not v:
    print(f'{ts}  #{n}  NOT HEARD - node absent from nodedb', flush=True); raise SystemExit
p = v.get('position', {}) or {}
lat, lon = p.get('latitude'), p.get('longitude')
snr, hops = v.get('snr','?'), v.get('hopsAway','?')
if lat is None:
    print(f'{ts}  #{n}  present, no position   snr={snr} hops={hops}', flush=True); raise SystemExit
dlat = (lat-37.35552)*111.32
dlon = (lon-(-92.8776192))*111.32*math.cos(math.radians(lat))
dist = math.hypot(dlat, dlon)
print(f'{ts}  #{n}  {lat:.5f},{lon:.5f}  {dist:5.2f} km / {dist*0.6214:5.2f} mi  '
      f'alt {p.get(\"altitude\",\"?\")}m  snr {snr} hops {hops}  fix_t {p.get(\"time\")}', flush=True)
"
  sleep "$EVERY"
done
echo "------------------------------------------------------------------------------"
echo "done after $N polls"
