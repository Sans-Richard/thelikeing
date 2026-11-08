#!/bin/bash
# Clean variant benchmark: builds a kernel in a FRESH dir and profiles configs.
# Usage: ./benchvar.sh <kernel.asc> <tag> "cfg1;cfg2;..."
#   cfg = "rows d dtype iters"
set -euo pipefail
KERNEL="$1"; TAG="$2"; CFGS="$3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
BENCH_DIR="$ROOT/others/bench_run"
DIR=/tmp/bv_$TAG
rm -rf "$DIR"; mkdir -p "$DIR/build"
cp "$BENCH_DIR/CMakeLists.txt" "$BENCH_DIR/data_utils.h" "$BENCH_DIR/main.asc" "$DIR/"
cp "$KERNEL" "$DIR/kernel.asc"
cd "$DIR/build"
cmake .. > cmake.log 2>&1
make -j40 > make.log 2>&1 || { echo "BUILD FAIL $TAG"; tail -5 make.log; exit 1; }
OUT=/tmp/prof_$TAG
rm -rf "$OUT"
ARGS=""
IFS=';' read -ra LIST <<< "$CFGS"
for c in "${LIST[@]}"; do ARGS="$ARGS $c"; done
msprof --output="$OUT" --application="$DIR/build/add_rms_norm_bias_custom$ARGS" > /tmp/$TAG.log 2>&1
python3 - "$TAG" "$CFGS" "$OUT" <<'PYEOF'
import csv, glob, sys
tag, cfgs, out = sys.argv[1], sys.argv[2], sys.argv[3]
f = sorted(glob.glob(f"{out}/PROF_*/mindstudio_profiler_output/op_summary_*.csv"))[-1]
rows = list(csv.DictReader(open(f)))
idx = 0
for c in cfgs.split(';'):
    parts = c.split(); it = int(parts[3])
    ts = []
    for _ in range(it + 1):
        if idx >= len(rows): break
        r = rows[idx]; idx += 1
        ts.append((float(r["Task Duration(us)"]), r))
    b = min(ts, key=lambda x: x[0])[1]
    print(f"{tag:>10} {parts[0]:>7}x{parts[1]:<5} dt={parts[2]}: dur={float(b['Task Duration(us)']):8.2f} vec={float(b['aiv_vec_time(us)']):7.2f} scl={float(b['aiv_scalar_time(us)']):6.2f} mte2={float(b['aiv_mte2_time(us)']):7.2f} mte3={float(b['aiv_mte3_time(us)']):6.2f}")
PYEOF
