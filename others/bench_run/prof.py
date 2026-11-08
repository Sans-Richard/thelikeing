#!/usr/bin/env python3
"""Run a list of (rows,d,dtype,iters) configs under msprof and print device times.

Usage: python3 prof.py "4096 1535 0 3" "4096 1536 0 3" ...
Older msprof output dirs are reused unless --clean is passed first.
"""
import csv
import glob
import os
import subprocess
import sys
import shutil

BENCH = os.path.dirname(os.path.abspath(__file__))
BIN = f"{BENCH}/build/add_rms_norm_bias_custom"
OUT = "/tmp/prof_cur"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    configs = []
    for a in args:
        parts = a.split()
        configs.append((int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]) if len(parts) > 3 else 3))

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    cmd = [BIN] + [f"{r} {d} {dt} {it}" for (r, d, dt, it) in configs]
    # binary expects args in groups: rows D dtype [iters]  (each take 4 argv slots)
    argv = []
    for (r, d, dt, it) in configs:
        argv += [str(r), str(d), str(dt), str(it)]
    logs = os.path.join(OUT, "run.log")
    os.makedirs(OUT, exist_ok=True)
    with open(logs, "w") as f:
        subprocess.run(["msprof", f"--output={OUT}", "--application=" + " ".join([f'"{BIN}"'] + argv)],
                       stdout=f, stderr=f)
    csvs = glob.glob(f"{OUT}/PROF_*/mindstudio_profiler_output/op_summary_*.csv")
    if not csvs:
        print("no op_summary found; see", logs)
        return
    rows = list(csv.DictReader(open(sorted(csvs)[-1])))
    # Each config: warmup + iters launches in order.
    idx = 0
    print(f"{'config':>24} | {'min':>8} | {'avg':>8} | {'vec':>7} {'scalar':>7} {'mte2':>7} {'mte3':>7} | name")
    for (r, d, dt, it) in configs:
        times = []
        for _ in range(it + 1):
            if idx >= len(rows):
                break
            row = rows[idx]
            idx += 1
            times.append(float(row["Task Duration(us)"]))
        if times:
            mini = min(times)
            ai = sum(times) / len(times)
            # pipe metrics from the min-time launch
            best_row = None
            for k in range(idx - len(times), idx):
                if float(rows[k]["Task Duration(us)"]) == mini:
                    best_row = rows[k]
            met = ""
            if best_row:
                met = (f"{float(best_row['aiv_vec_time(us)']):7.2f} {float(best_row['aiv_scalar_time(us)']):7.2f} "
                       f"{float(best_row['aiv_mte2_time(us)']):7.2f} {float(best_row['aiv_mte3_time(us)']):7.2f}")
            print(f"{r:>7}x{d:<5} dt={dt} it={it:<3} | {mini:8.2f} | {ai:8.2f} | {met} | {rows[idx-1]['Op Name'][:40]}")


if __name__ == "__main__":
    main()
