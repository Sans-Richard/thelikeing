#!/usr/bin/env python3
"""提交前本地性能分析：对 15 个（或指定子集）case 逐个跑 msOpProf 可视化报告。

产出：
- report_work/<ts>/case01.html ... case15.html  每个 case 一个 fast 报告（details+cache）
- report_work/<ts>/summary.json                 每个 case 的耗时/流水线/缓存命中汇总

用法：
  python3 collect_reports.py                          # 全量 15 case
  python3 collect_reports.py --cases "1,4,13"         # 只跑指定子集
  python3 collect_reports.py --out /path/to/dir       # 指定输出目录
"""
import argparse
import fcntl
import hashlib
import json
import math
import os
import signal
import shutil
import subprocess
import sys
import time

from pathlib import Path
_ENJOY = Path(__file__).resolve().parents[3]           # enjoy_ur_time/
ROOT = str(_ENJOY)
PROJECT_DIR = str(_ENJOY / 'addrmsnormbias_problem_1742_template')
BENCH_DIR = str(_ENJOY / 'others' / 'bench_run')
SKILL_SCRIPTS = os.path.expanduser(
    '~/.config/opencode/skills/tool-perf-report/scripts')
_SCOREBOARD = _ENJOY / 'others' / 'scoreboard_and_submit' / 'scoreboard'
REPORTS_BASE = str(_SCOREBOARD / 'reports')
DEFAULT_OUT = str(_SCOREBOARD / 'report_work')

# (rows, d, dtype)   dtype: 0=fp32 1=fp16 2=bf16
CASES = [
    (1, 64, 1), (8, 197, 0), (128, 256, 0), (768, 197, 1), (8, 32768, 1),
    (1513, 577, 1), (3114, 401, 1), (10240, 512, 1), (4096, 1535, 0), (8192, 1024, 1),
    (3748, 3080, 0), (3408, 4096, 2), (10296, 3076, 0), (950000, 115, 2), (215000, 8192, 2),
]

CASES_PER_MINUTE = 3  # ~20s/case


def digest(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def prepare_operator(out_dir, use_project_kernel):
    """Build an immutable source snapshot; never profile bench_run's old binary."""
    operator = os.path.join(out_dir, 'operator')
    os.makedirs(operator, exist_ok=False)
    source = os.path.join(PROJECT_DIR if use_project_kernel else BENCH_DIR, 'kernel.asc')
    shutil.copyfile(source, os.path.join(operator, 'kernel.asc'))
    for name in ('main.asc', 'data_utils.h', 'CMakeLists.txt'):
        shutil.copyfile(os.path.join(BENCH_DIR, name), os.path.join(operator, name))
    provenance = {
        'source_path': source, 'source_sha256': digest(os.path.join(operator, 'kernel.asc')),
        'inputs': {n: digest(os.path.join(operator, n)) for n in
                   ('kernel.asc', 'main.asc', 'data_utils.h', 'CMakeLists.txt')},
        'ascend_home_path': os.environ.get('ASCEND_HOME_PATH'),
    }
    build = os.path.join(operator, 'build')
    commands = [['cmake', '-S', operator, '-B', build],
                ['cmake', '--build', build, '-j8']]
    with open(os.path.join(out_dir, 'build.log'), 'w') as log:
        for command in commands:
            subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=600)
    executable = os.path.join(build, 'add_rms_norm_bias_custom')
    if not os.path.isfile(executable):
        raise RuntimeError('fresh build did not produce the benchmark executable')
    provenance.update(executable=executable, binary_sha256=digest(executable),
                      build_commands=commands)
    with open(os.path.join(out_dir, 'build_provenance.json'), 'w') as f:
        json.dump(provenance, f, ensure_ascii=False, indent=2)
    print('Fresh build source SHA256: ' + provenance['source_sha256'], flush=True)
    return operator, provenance


def run_one(case_idx, out_dir, operator, provenance):
    rows, d, dtype = CASES[case_idx]
    case_tag = f'case{case_idx + 1:02d}'
    tag = f'{rows}x{d}_dt{dtype}'
    collection = os.path.join(out_dir, f'collection_{case_tag}')
    app_arg = f'{rows} {d} {dtype} 1'
    env = dict(os.environ)

    # 单 case 采集 + fast 渲染
    cmd = [
        sys.executable, os.path.join(SKILL_SCRIPTS, 'run_pipeline.py'),
        '--operator-path', operator,
        '--app', 'build/add_rms_norm_bias_custom',
        '--app-cwd', operator,
        '--app-arg', app_arg,
        '--output', collection,
        '--preset', 'fast',
        '--build-config', 'kernel_sha256=' + provenance['source_sha256'],
    ]
    print(f'[{case_tag}] {tag} collecting...', flush=True)
    t0 = time.time()
    # Serialize device use with all optimization/verification workers.
    with open('/tmp/npu.lock', 'a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, env=env, start_new_session=True)
        try:
            stdout, stderr = process.communicate(timeout=600)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                stdout, stderr = process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                stdout, stderr = process.communicate()
            with open(os.path.join(out_dir, case_tag + '.log'), 'w') as log:
                log.write(stdout + '\n' + stderr)
            raise RuntimeError(case_tag + ' collection timed out; process group stopped')
        except BaseException:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.communicate()
            raise
    r = subprocess.CompletedProcess(cmd, process.returncode, stdout, stderr)
    with open(os.path.join(out_dir, case_tag + '.log'), 'w') as log:
        log.write(stdout + '\n' + stderr)
    dt = time.time() - t0
    if r.returncode != 0:
        print(f'  ERROR rc={r.returncode} in {dt:.0f}s')
        print((r.stdout or '')[-800:])
        print((r.stderr or '')[-800:])
        return None, dt

    state_path = os.path.join(collection, '_internal', 'run_state.json')
    with open(state_path) as f:
        state = json.load(f)
    if state.get('status') != 'completed':
        raise RuntimeError(case_tag + ': collection is not completed: ' + str(state))
    if not os.path.isfile(os.path.join(collection, 'collection_manifest.json')):
        raise RuntimeError(case_tag + ': collection manifest missing')

    # 定位报告 html
    html = os.path.join(collection, 'report.html')
    if not os.path.exists(html):
        html = _find_report_html(collection)
    if not html:
        print(f'  ERROR: report.html not found in {collection}')
        return None, dt

    dst_html = os.path.join(out_dir, f'{case_tag}.html')
    shutil.copy2(html, dst_html)
    print(f'  OK {dt:.0f}s -> {case_tag}.html')
    return validate_report(collection, case_tag, tag, dst_html, provenance), dt


def validate_report(collection, case_tag, tag, dst_html, provenance):
    summary = _summarize(collection, case_tag, tag, dst_html)
    duration = summary.get('duration_us')
    if not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
        raise RuntimeError(case_tag + ': missing or invalid duration in report payload')
    if not summary.get('pipeline') or not summary.get('blocks'):
        raise RuntimeError(case_tag + ': missing pipeline or core data')
    summary.update(source_sha256=provenance['source_sha256'],
                   binary_sha256=provenance['binary_sha256'])
    # The skill's self_check is a package/full-feature integration test: it
    # requires Source/Timeline/Roofline even for fast captures. Validate the
    # requested fast contract here instead, retaining explicit scope in JSON.
    with open(os.path.join(collection, 'report_payload.json')) as f:
        payload = json.load(f)
    cache = payload.get('views', {}).get('cache', {})
    if not cache.get('summary') or not isinstance(summary.get('l2_hit'), (int, float)):
        raise RuntimeError(case_tag + ': missing cache data in fast report')
    with open(os.path.join(collection, 'report_index.json')) as f:
        index = json.load(f)
    if not os.path.isfile(dst_html) or os.path.getsize(dst_html) < 1000:
        raise RuntimeError(case_tag + ': empty HTML report')
    with open(os.path.join(os.path.dirname(dst_html), case_tag + '_validation.json'), 'w') as f:
        json.dump({'passed': True, 'scope': 'fast details/cache, completed collection, source/binary provenance',
                   'full_feature_self_check': 'not applicable to fast preset',
                   'report_index': index, 'source_sha256': provenance['source_sha256']},
                  f, ensure_ascii=False, indent=2)
    return summary


def _find_report_html(collection):
    for root, _dirs, files in os.walk(collection):
        for f in files:
            if f == 'report.html':
                return os.path.join(root, f)
    return None


def _summarize(collection, case_tag, tag, html):
    payload = os.path.join(collection, 'report_payload.json')
    summary = {
        'case': case_tag, 'tag': tag, 'html': os.path.basename(html),
        'duration_us': None, 'pipeline': {}, 'l2_hit': None,
    }
    if not os.path.exists(payload):
        return summary
    try:
        with open(payload) as f:
            d = json.load(f)
        views = d.get('views', {})
        det = views.get('details', {})
        basic = det.get('basic', {})
        if basic.get('available'):
            summary['duration_us'] = basic.get('duration_us')
            summary['blocks'] = basic.get('blocks')
        compute = det.get('compute', {})
        blocks = compute.get('blocks') or []
        if blocks:
            engines = blocks[0].get('engines') or []
            if engines:
                pipes = engines[0].get('pipeline') or []
                summary['pipeline'] = {p.get('name'): p.get('value') for p in pipes}
        cache = views.get('cache', {})
        csum = cache.get('summary') or []
        for item in csum:
            key = item.get('key') or ''
            if 'L2 Cache Read' in key and 'hit rate' in key:
                summary['l2_hit'] = item.get('mean')
                break
        advice = det.get('advice', {})
        if advice.get('available'):
            summary['advice'] = advice.get('items')
    except Exception as e:
        summary['parse_error'] = str(e)
    return summary


def main():
    def terminated(signum, frame):
        raise SystemExit('collection terminated; cleaning active profiler')
    signal.signal(signal.SIGTERM, terminated)
    ap = argparse.ArgumentParser()
    ap.add_argument('--cases', default='all',
                    help='case 子集，逗号分隔 1..15；默认 all')
    ap.add_argument('--out', default=DEFAULT_OUT)
    ap.add_argument('--sync-kernel', action='store_true', default=True,
                    help='使用工程 kernel.asc 快照，在报告目录全新编译（默认）')
    ap.add_argument('--no-sync-kernel', dest='sync_kernel', action='store_false')
    args = ap.parse_args()

    if args.cases.strip().lower() == 'all':
        idxs = list(range(15))
    else:
        idxs = [int(x) for x in args.cases.split(',') if x.strip()]
        bad = [i for i in idxs if not (1 <= i <= 15)]
        if bad:
            print(f'ERROR: case 编号越界: {bad}（应为 1..15）')
            sys.exit(1)
        idxs = [i - 1 for i in idxs]

    os.umask(0o027)
    ts = time.strftime('%Y%m%d_%H%M%S') + '_' + str(time.time_ns() % 1000000).zfill(6)
    out_dir = os.path.join(args.out, ts)
    os.makedirs(out_dir, exist_ok=False)

    # 估算
    est = len(idxs) * 22 / 60
    print(f'计划采集 {len(idxs)} 个 case（{idxs}），估算 {est:.1f} 分钟')
    print(f'输出: {out_dir}')

    operator, provenance = prepare_operator(out_dir, args.sync_kernel)

    summaries = []
    total = time.time()
    for i, ci in enumerate(idxs, 1):
        s, dt = run_one(ci, out_dir, operator, provenance)
        if s:
            summaries.append(s)
        else:
            raise RuntimeError('采集失败，停止后续采集与提交: case' + str(ci + 1))
        print(f'  进度 {i}/{len(idxs)}，累计 {(time.time()-total)/60:.1f} 分钟', flush=True)

    with open(os.path.join(out_dir, 'summary.json'), 'w') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    if digest(provenance['source_path']) != provenance['source_sha256']:
        raise RuntimeError('采集期间源码已改变，报告不能绑定到当前源码')
    if len(summaries) != len(idxs):
        raise RuntimeError('采集未覆盖所有请求 case')

    print(f'\n完成。{len(summaries)}/{len(idxs)} 成功，总耗时 {(time.time()-total)/60:.1f} 分钟')
    print(f'summary: {os.path.join(out_dir, "summary.json")}')


if __name__ == '__main__':
    main()
