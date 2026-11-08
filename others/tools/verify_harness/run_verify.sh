#!/bin/bash
# ============================================================================
# run_verify.sh - build and run the AddRmsNormBias verification harness.
#
#   ./run_verify.sh [gen_and_check.py args...]
#
# Env:
#   KERNEL_SRC     kernel to test (default: /tmp/opt1/kernel.asc if it exists,
#                  else the known-good template kernel)
#   CLEAN_BUILD=1  wipe ./build before configuring
#   CASE_TIMEOUT   per-case timeout in seconds (default 1800)
#
# Everything is written under this directory only.
# ============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENJOY_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
TEMPLATE_DIR="$ENJOY_DIR/addrmsnormbias_problem_1742_template"

if [ -z "${ASCEND_HOME_PATH:-}" ] && [ -f /home/developer/Ascend/cann-9.0.0/set_env.sh ]; then
    # shellcheck disable=SC1091
    source /home/developer/Ascend/cann-9.0.0/set_env.sh
fi

if [ -z "${ASCEND_HOME_PATH:-}" ]; then
    echo "ERROR: ASCEND_HOME_PATH not set and CANN set_env.sh not found" >&2
    exit 1
fi

if [ -z "${KERNEL_SRC:-}" ]; then
    if [ -f "$TEMPLATE_DIR/temp.asc" ]; then
        KERNEL_SRC="$TEMPLATE_DIR/temp.asc"
    else
        KERNEL_SRC="$TEMPLATE_DIR/kernel.asc"
    fi
fi

if [ ! -f "$KERNEL_SRC" ]; then
    echo "ERROR: kernel source not found: $KERNEL_SRC" >&2
    exit 1
fi

# Serialize runs sharing this directory (multiple agents/tools may use it at the
# same time; concurrent runs would race on ./input, ./output and ./build).
if command -v flock >/dev/null 2>&1; then
    exec 9>"$SCRIPT_DIR/.verify.lock"
    flock 9
    export VERIFY_LOCK_HELD=1
fi

echo "=== [1/3] Stage harness files (kernel: $KERNEL_SRC) ==="
cp "$KERNEL_SRC" "$SCRIPT_DIR/kernel.asc"
[ -f "$SCRIPT_DIR/CMakeLists.txt" ] || cp "$TEMPLATE_DIR/CMakeLists.txt" "$SCRIPT_DIR/CMakeLists.txt"
[ -f "$SCRIPT_DIR/data_utils.h" ] || cp "$TEMPLATE_DIR/data_utils.h" "$SCRIPT_DIR/data_utils.h"
# The copied CMakeLists builds main.asc -> keep it as a symlink to verify_main.asc.
ln -sf verify_main.asc "$SCRIPT_DIR/main.asc"
mkdir -p "$SCRIPT_DIR/input" "$SCRIPT_DIR/output"

echo "=== [2/3] Build ==="
if [ "${CLEAN_BUILD:-0}" = "1" ]; then
    rm -rf "$SCRIPT_DIR/build"
fi
mkdir -p "$SCRIPT_DIR/build"
if ! cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build" >"$SCRIPT_DIR/build/cmake_configure.log" 2>&1; then
    cat "$SCRIPT_DIR/build/cmake_configure.log" >&2
    exit 1
fi
cmake --build "$SCRIPT_DIR/build" -j"$(nproc)"

echo "=== [3/3] Generate, run and verify ==="
if [ -n "${WORK_DIR:-}" ]; then
    exec python3 "$SCRIPT_DIR/gen_and_check.py" --workdir "$WORK_DIR" "$@"
else
    exec python3 "$SCRIPT_DIR/gen_and_check.py" "$@"
fi
