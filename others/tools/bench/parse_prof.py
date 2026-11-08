import csv, glob, sys
tag, out = sys.argv[1], sys.argv[2]
cfgs = sys.argv[3:]
f = sorted(glob.glob(f"{out}/PROF_*/mindstudio_profiler_output/op_summary_*.csv"))
if not f:
    print("no op_summary; see /tmp/%s.log" % tag); sys.exit(1)
rows = list(csv.DictReader(open(f[-1])))
# Each launch emits iters+1 profiled rows (the first is the cold run), and
# distinct shapes can share one kernel symbol, so chunk by the known size
# rather than by symbol.
groups, i = [], 0
for c in cfgs:
    n = int(c.split()[3]) + 1
    groups.append(rows[i:i + n])
    i += n


def g(r, k):
    try: return float(r.get(k, "N/A"))
    except Exception: return 0.0


for c, grp in zip(cfgs, groups):
    p = c.split()
    ts = [g(r, "Task Duration(us)") for r in grp]
    b = min(ts)
    best = grp[ts.index(b)]
    print(f"{tag:>12} {p[0]:>7}x{p[1]:<6} dt={p[2]}: dur={b:8.2f} "
          f"vec={g(best,'aiv_vec_time(us)'):7.2f} scl={g(best,'aiv_scalar_time(us)'):6.2f} "
          f"mte2={g(best,'aiv_mte2_time(us)'):7.2f} mte3={g(best,'aiv_mte3_time(us)'):6.2f} "
          f"n={len(grp)}")
