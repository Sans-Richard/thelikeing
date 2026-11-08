#!/bin/bash
# Build a kernel variant in a FRESH dir and profile configs.
# Usage: vrun.sh <kernel.asc> <tag> "rows d dtype iters" ["..." ...]
set -uo pipefail
KERNEL="$1"; TAG="$2"; shift 2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
BENCH_DIR="$ROOT/others/bench_run"
DIR=/tmp/vr_$TAG
BIN="$DIR/build/add_rms_norm_bias_custom"
if [ ! -x "$BIN" ]; then
  rm -rf "$DIR"; mkdir -p "$DIR/build"
  cp "$BENCH_DIR/CMakeLists.txt" "$BENCH_DIR/data_utils.h" "$BENCH_DIR/main.asc" "$DIR/"
  cp "$KERNEL" "$DIR/kernel.asc"
  ( cd "$DIR/build" && cmake .. >cmake.log 2>&1 && make -j40 >make.log 2>&1 ) || { echo "BUILD FAIL $TAG"; grep -E "error" "$DIR/build/make.log" | head -8; exit 1; }
fi
OUT=/tmp/prof_$TAG; rm -rf "$OUT"
ARGS=""; for c in "$@"; do ARGS="$ARGS $c"; done
msprof --output="$OUT" --application="$BIN$ARGS" >/tmp/$TAG.log 2>&1
python3 "$SCRIPT_DIR/parse_prof.py" "$TAG" "$OUT" "$@"
