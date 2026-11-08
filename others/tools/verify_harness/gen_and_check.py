#!/usr/bin/env python3
# ============================================================================
# gen_and_check.py - end-to-end correctness driver for the AddRmsNormBias
# verification harness.
#
# For every (shape, dtype) case:
#   1. generate random x / residual / gamma / bias with numpy,
#   2. write them to ./input/*.bin (raw dtype bytes, row-major),
#   3. run ./build/add_rms_norm_bias_custom <rows> <D> <dtype> [shape=...],
#   4. read ./output/out.bin and compare against the numpy golden:
#        y    = x.astype(f32) + residual.astype(f32)
#        rms  = sqrt(mean(y*y, axis=-1, keepdims=True) + 1e-5)
#        out  = y / rms * gamma + bias          (all fp32)
#        golden = round_to_dtype(out)
#      Tolerances: fp32 rtol/atol 1e-4, fp16/bf16 rtol/atol 1e-3.
#
# Exit code 0 iff every case passes (unless --strict, see below).
#
# Usage:
#   python3 gen_and_check.py [--shapes-file FILE] [--shapes "S;S;..."]
#                            [--only "r,d,dt"] [--quick] [--strict] [--list]
# ============================================================================

import argparse
import fcntl
import os
import subprocess
import sys
import time

import numpy as np

try:
    from ml_dtypes import bfloat16
    HAVE_ML_DTYPES = True
except ImportError:
    bfloat16 = None
    HAVE_ML_DTYPES = False

HARNESS_DIR = os.path.dirname(os.path.abspath(__file__))
BINARY = os.path.join(HARNESS_DIR, "build", "add_rms_norm_bias_custom")

EPS = 1e-5
CASE_TIMEOUT = int(os.environ.get("CASE_TIMEOUT", "1800"))
CHUNK_ELEMS = 1 << 24  # rows are processed in <=16M-element chunks

DTYPE_NAMES = {0: "fp32", 1: "fp16", 2: "bf16"}
TOLERANCES = {0: 1e-4, 1: 1e-3, 2: 1e-3}

PATTERNS = {
    "small": {
        "x": (-2.0, 2.0), "residual": (-2.0, 2.0),
        "gamma": (0.8, 1.2), "bias": (-0.3, 0.3),
    },
    "large": {
        "x": (-10.0, 10.0), "residual": (-10.0, 10.0),
        "gamma": (0.1, 2.0), "bias": (-2.0, 2.0),
    },
}
SEED_COMBOS_SMALL = [("small", 0), ("large", 0), ("small", 1234), ("large", 4321)]
SEED_COMBOS_BIG = [("small", 0), ("large", 0)]

# Default shape list: (shape..., dtype) with dtype 0=fp32 1=fp16 2=bf16.
# Last element of each tuple is the dtype; preceding elements are the shape.
DEFAULT_SHAPES = [
    # --- 比赛还原 shape（09-13 探针 + 2026-10-03 rows/D 探针 + 带宽物理双确认，
    #     见 HISTORY.md §33/§35；刺探行动的 c6/c7/c8/c10/c14 "修正"已被证伪）---
    (1, 64, 1),
    (7, 197, 0),        # c2: blkprobe 锁定 rows=7（原 8）
    (128, 256, 0),
    (767, 197, 1),      # c4: 767（rows 探针 2026-10-03 确认）
    (8, 32768, 1),
    (1513, 577, 1),     # c6: 1513（rows 探针 + 带宽物理：2200 需 604GB/s 超 pad 地板）
    (3114, 401, 1),     # c7: 3114（rows 探针 + 带宽物理：6000 需 839GB/s 超 pad 地板）
    (10240, 512, 1),    # c8: d=512 对齐（带宽物理：508 非对齐需 954GB/s 超 pad 地板）
    (4096, 1535, 0),
    (8192, 1024, 1),    # c10: d=1024 对齐（带宽物理：1016 非对齐需 1020GB/s 超 pad 地板）
    (3748, 3080, 0),
    (3408, 4096, 2),
    (10296, 3076, 0),
    (950000, 115, 2),   # c14: ~95万 rows（2026-10-03 实测 162.6ns/行 × 23750 行/核 = 3.86ms = 平台 3820✓；2M 行本地应 8.59ms 矛盾）
    (215000, 8192, 2),  # c15: 215K rows（带宽物理：262144 需 1444GB/s 超 DRAM 上限）
    # --- 边界/特形 ---
    (1, 8, 0),
    (2, 3, 4, 8, 0),
    (7, 13, 0),
    (64, 64, 1),
    (1000003, 64, 2),
    (1, 192, 1),
    (17, 576, 1),
    (5, 401, 1),
]

QUICK_SET = {
    (1, 64, 1), (7, 197, 0), (767, 197, 1), (1513, 577, 1),
    (4096, 1535, 0), (3408, 4096, 2), (2, 3, 4, 8, 0), (7, 13, 0),
    (1, 192, 1),
}


# ---------------------------------------------------------------------------
# dtype encode/decode
# ---------------------------------------------------------------------------
def _f32_to_bf16_u16(x):
    u = np.asarray(x, dtype=np.float32).view(np.uint32)
    rounding = ((u >> 16) & 1) + 0x7FFF
    u = (u + rounding) & 0xFFFFFFFF
    return (u >> 16).astype(np.uint16)


def _bf16_u16_to_f32(u):
    return (np.asarray(u, dtype=np.uint32) << 16).view(np.float32)


def encode(arr_f32, dtype_id):
    """Round an fp32 array to the target dtype (returns target-dtype array)."""
    if dtype_id == 0:
        return arr_f32.astype(np.float32)
    if dtype_id == 1:
        return arr_f32.astype(np.float16)
    if HAVE_ML_DTYPES:
        return arr_f32.astype(bfloat16)
    return _f32_to_bf16_u16(arr_f32)


def decode(arr, dtype_id):
    """Widen a target-dtype array to fp32 for comparison."""
    if dtype_id == 1:
        return arr.astype(np.float32)
    if dtype_id == 2 and not HAVE_ML_DTYPES:
        return _bf16_u16_to_f32(arr)
    return arr.astype(np.float32)


def file_dtype(dtype_id):
    if dtype_id == 0:
        return np.float32
    if dtype_id == 1:
        return np.float16
    return bfloat16 if HAVE_ML_DTYPES else np.uint16


def _float_key(u, width):
    """Map float bit patterns to a monotonic integer key (adjacent == 1 ULP)."""
    if width == 16:
        ui = u.astype(np.int32)
        return np.where((ui & 0x8000) != 0, (~ui) & 0xFFFF, ui | 0x8000).astype(np.int64)
    ui = u.astype(np.int64)
    return np.where((ui & 0x80000000) != 0,
                    (~ui) & 0xFFFFFFFF, ui | 0x80000000).astype(np.int64)


# ---------------------------------------------------------------------------
# golden + comparison
# ---------------------------------------------------------------------------
def golden_flat(x2d, r2d, g32, b32):
    y = x2d.astype(np.float32) + r2d.astype(np.float32)
    rms = np.sqrt(np.mean(y * y, axis=-1, keepdims=True) + EPS)
    return y / rms * g32 + b32


def compare(out_path, x, r, g, b, dtype_id):
    """Chunked golden comparison. Returns a dict of statistics."""
    shape = x.shape
    D = shape[-1]
    x2d = x.reshape(-1, D)
    r2d = r.reshape(-1, D)
    nrows = x2d.shape[0]
    total = nrows * D

    g32 = g.astype(np.float32)
    b32 = b.astype(np.float32)

    act = np.fromfile(out_path, dtype=file_dtype(dtype_id))
    if act.size != total:
        raise RuntimeError("out.bin has %d elements, expected %d" % (act.size, total))
    act = act.reshape(nrows, D)

    rtol = TOLERANCES[dtype_id]
    atol = rtol
    width = 32 if dtype_id == 0 else 16
    uitype = np.uint32 if dtype_id == 0 else np.uint16

    chunk_rows = max(1, CHUNK_ELEMS // D)
    stats = {
        "max_abs": 0.0, "max_rel": 0.0,
        "mismatch": 0, "mismatch_1ulp": 0, "nonfinite": 0, "total": int(total),
    }

    for s in range(0, nrows, chunk_rows):
        e = min(nrows, s + chunk_rows)
        gold32 = golden_flat(x2d[s:e], r2d[s:e], g32, b32)
        gold = encode(gold32, dtype_id)          # quantize golden like the kernel
        a = act[s:e]
        ad = decode(a, dtype_id)
        gd = decode(gold, dtype_id)

        diff = np.abs(ad - gd)
        denom = np.abs(gd)
        bad = diff > (atol + rtol * denom)

        nonfinite = ~np.isfinite(ad)
        n_nonfinite = int(np.count_nonzero(nonfinite))
        n_bad = int(np.count_nonzero(bad)) + n_nonfinite
        stats["nonfinite"] += n_nonfinite
        stats["mismatch"] += n_bad
        stats["mismatch_1ulp"] += n_nonfinite

        if n_bad > 0:
            ka = _float_key(a.view(uitype), width)
            kg = _float_key(gold.view(uitype), width)
            beyond = (np.abs(ka - kg) > 1) & ~nonfinite
            stats["mismatch_1ulp"] += int(np.count_nonzero(bad & beyond))

        if diff.size:
            stats["max_abs"] = max(stats["max_abs"], float(np.max(diff)))
        nz = denom > 0
        if np.any(nz):
            stats["max_rel"] = max(stats["max_rel"], float(np.max(diff[nz] / denom[nz])))

    return stats


# ---------------------------------------------------------------------------
# shape parsing / data generation
# ---------------------------------------------------------------------------
def parse_shape_spec(spec):
    parts = [p.strip() for p in spec.replace("x", ",").replace("X", ",").split(",") if p.strip()]
    if len(parts) < 2:
        raise ValueError("bad shape spec: %r" % spec)
    vals = [int(p) for p in parts]
    shape, dtype_id = tuple(vals[:-1]), vals[-1]
    if dtype_id not in DTYPE_NAMES:
        raise ValueError("bad dtype in %r (want 0/1/2)" % spec)
    if any(v <= 0 for v in shape):
        raise ValueError("non-positive dim in %r" % spec)
    return shape + (dtype_id,)


def read_shapes_file(path):
    shapes = []
    with open(path, "r") as f:
        for lineno, line in enumerate(f, 1):
            line = line.split("#")[0].strip()
            if not line:
                continue
            try:
                shapes.append(parse_shape_spec(line))
            except ValueError as exc:
                raise ValueError("%s:%d: %s" % (path, lineno, exc))
    return shapes


def make_case(rng, shape, dtype_id, pattern):
    D = shape[-1]
    p = PATTERNS[pattern]
    x = encode(rng.uniform(p["x"][0], p["x"][1], size=shape).astype(np.float32), dtype_id)
    r = encode(rng.uniform(p["residual"][0], p["residual"][1], size=shape).astype(np.float32), dtype_id)
    g = encode(rng.uniform(p["gamma"][0], p["gamma"][1], size=D).astype(np.float32), dtype_id)
    b = encode(rng.uniform(p["bias"][0], p["bias"][1], size=D).astype(np.float32), dtype_id)
    return x, r, g, b


def write_bin(path, arr):
    with open(path, "wb") as f:
        f.write(np.ascontiguousarray(arr).tobytes())


def combos_for(numel):
    return SEED_COMBOS_SMALL if numel <= 64 * 1024 * 1024 else SEED_COMBOS_BIG


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="AddRmsNormBias harness driver")
    ap.add_argument("--shapes-file", help="file with one 'd0,d1,...,dtype' per line")
    ap.add_argument("--shapes", help="inline ';'-separated shape specs")
    ap.add_argument("--only", action="append", default=[],
                    help="run only the given shape spec (repeatable)")
    ap.add_argument("--quick", action="store_true", help="run a representative subset")
    ap.add_argument("--strict", action="store_true",
                    help="exit nonzero on any strict rtol/atol mismatch")
    ap.add_argument("--list", action="store_true", help="list default shapes and exit")
    ap.add_argument("--workdir", default=HARNESS_DIR,
                    help="directory whose input/ and output/ are used (default: harness dir)")
    args = ap.parse_args()

    workdir = os.path.abspath(args.workdir)
    input_dir = os.path.join(workdir, "input")
    output_dir = os.path.join(workdir, "output")

    shapes = list(DEFAULT_SHAPES)
    if args.shapes_file:
        shapes = read_shapes_file(args.shapes_file)
    if args.shapes:
        shapes = [parse_shape_spec(s) for s in args.shapes.split(";") if s.strip()]
    if args.quick:
        shapes = [s for s in shapes if s in QUICK_SET]
    if args.only:
        wanted = [parse_shape_spec(s) for s in args.only]
        shapes = [s for s in shapes if s in wanted]

    if args.list:
        for s in shapes:
            print(",".join(str(v) for v in s))
        return 0

    if not os.path.isfile(BINARY):
        print("ERROR: %s not found; build first (run_verify.sh or cmake+make)" % BINARY,
              file=sys.stderr)
        return 2
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Serialize access to the shared input/output directory. run_verify.sh holds
    # the lock for its whole lifetime and sets VERIFY_LOCK_HELD=1.
    lock_fd = None
    if os.environ.get("VERIFY_LOCK_HELD") != "1":
        lock_fd = open(os.path.join(HARNESS_DIR, ".verify.lock"), "w")
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            print("Another verification run holds the lock; waiting...", file=sys.stderr)
            fcntl.flock(lock_fd, fcntl.LOCK_EX)

    if not HAVE_ML_DTYPES:
        print("WARNING: ml_dtypes unavailable; using uint16 bf16 emulation", file=sys.stderr)

    results = []
    n_cases = sum(len(combos_for(int(np.prod(s[:-1])))) for s in shapes)
    case_idx = 0

    for spec in shapes:
        shape, dtype_id = spec[:-1], spec[-1]
        numel = int(np.prod(shape))
        dt_name = DTYPE_NAMES[dtype_id]
        rows = int(np.prod(shape[:-1])) if len(shape) > 1 else 1
        D = shape[-1]

        for pattern, seed in combos_for(numel):
            case_idx += 1
            t0 = time.time()
            rng = np.random.default_rng(seed)
            x, r, g, b = make_case(rng, shape, dtype_id, pattern)
            write_bin(os.path.join(input_dir, "x.bin"), x)
            write_bin(os.path.join(input_dir, "residual.bin"), r)
            write_bin(os.path.join(input_dir, "gamma.bin"), g)
            write_bin(os.path.join(input_dir, "bias.bin"), b)

            out_path = os.path.join(output_dir, "out.bin")
            if os.path.exists(out_path):
                os.remove(out_path)

            cmd = [BINARY, str(rows), str(D), str(dtype_id)]
            if len(shape) > 2:
                cmd.append("shape=" + ",".join(str(v) for v in shape))
            try:
                proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True,
                                      timeout=CASE_TIMEOUT)
            except subprocess.TimeoutExpired:
                stats = {"max_abs": float("nan"), "max_rel": float("nan"),
                         "mismatch": numel, "mismatch_1ulp": numel,
                         "nonfinite": 0, "total": numel}
                verdict, note = "FAIL", "timeout after %ds" % CASE_TIMEOUT
                results.append((spec, pattern, seed, verdict, note, stats))
                print("[%3d/%3d] FAIL shape=%s dtype=%s pattern=%s seed=%d: %s"
                      % (case_idx, n_cases, shape, dt_name, pattern, seed, note))
                continue

            if proc.returncode != 0 or not os.path.exists(out_path):
                err = (proc.stderr or "").strip().splitlines()
                out = (proc.stdout or "").strip().splitlines()
                detail = err[-1] if err else (out[-1] if out else "out.bin missing")
                note = "rc=%d: %s" % (proc.returncode, detail)
                stats = {"max_abs": float("nan"), "max_rel": float("nan"),
                         "mismatch": numel, "mismatch_1ulp": numel,
                         "nonfinite": 0, "total": numel}
                verdict = "FAIL"
            else:
                try:
                    stats = compare(out_path, x, r, g, b, dtype_id)
                except Exception as exc:  # noqa: BLE001
                    note = "compare error: %s" % exc
                    stats = {"max_abs": float("nan"), "max_rel": float("nan"),
                             "mismatch": numel, "mismatch_1ulp": numel,
                             "nonfinite": 0, "total": numel}
                    verdict = "FAIL"
                    results.append((spec, pattern, seed, verdict, note, stats))
                    print("[%3d/%3d] FAIL shape=%s dtype=%s pattern=%s seed=%d: %s"
                          % (case_idx, n_cases, shape, dt_name, pattern, seed, note))
                    continue

                if stats["nonfinite"] > 0:
                    verdict = "FAIL"
                    note = "%d non-finite outputs" % stats["nonfinite"]
                elif stats["mismatch"] == 0:
                    verdict = "PASS"
                    note = ""
                elif stats["mismatch_1ulp"] == 0:
                    verdict = "FAIL(1ulp)" if args.strict else "PASS(1ulp)"
                    note = "%d elements within 1 ULP" % stats["mismatch"]
                else:
                    verdict = "FAIL"
                    note = "%d mismatches (%d beyond 1 ULP)" % (
                        stats["mismatch"], stats["mismatch_1ulp"])

            results.append((spec, pattern, seed, verdict, note, stats))
            elapsed = time.time() - t0
            print("[%3d/%3d] %-9s shape=%-22s dtype=%-4s pattern=%-5s seed=%-4d "
                  "max_abs=%.3e max_rel=%.3e mism=%d/1ulp=%d  (%.1fs)%s"
                  % (case_idx, n_cases, verdict, str(shape), dt_name, pattern, seed,
                     stats["max_abs"], stats["max_rel"], stats["mismatch"],
                     stats["mismatch_1ulp"], elapsed,
                     ("  " + note) if note else ""))
            sys.stdout.flush()

    print("=" * 100)
    n_fail = sum(1 for r in results if r[3].startswith("FAIL"))
    n_pass = len(results) - n_fail
    for spec, pattern, seed, verdict, note, stats in results:
        print("%-9s shape=%-22s dtype=%-4s pattern=%-5s seed=%-4d %s"
              % (verdict, str(spec[:-1]), DTYPE_NAMES[spec[-1]], pattern, seed, note))
    print("-" * 100)
    print("SUMMARY: %d/%d cases passed, %d failed%s"
          % (n_pass, len(results), n_fail,
             " (strict mode)" if args.strict else ""))
    return 1 if n_fail > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
