"""Pinned SinkhornNorm target. No credentials belong in this module."""
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
PROBLEM_ID = '6adb28021dac5d235bd73b85'
CONTEST_ID = '6adac8363ff2fef7e89242fe'
PROBLEM_NAME = 'sinkhorn_norm'
PROBLEM_URL = 'https://cannjudge.cn/public/op_challenge_xinan_final/sinkhorn_norm'
PROJECT_DIR = ROOT / 'sinkhorn_norm_problem_2360_template'
DATA_FILE = BASE / 'data.sinkhorn_norm.json'
TEMPLATE_FILE = BASE / 'template.sinkhorn_norm.json'
RUNS_DIR = BASE / 'runs_sinkhorn'
STOP_FILES = (ROOT / 'STOP.json', PROJECT_DIR / 'STOP.json', BASE / 'STOP.sinkhorn_norm.json')
LOCK_FILE = ROOT / 'others/scoreboard_and_submit/.submission.lock'
POST_CLOCK_FILE = ROOT / 'others/scoreboard_and_submit/.last_submission.json'
END_TIME = '2026-11-07T04:00:00.000Z'

def target_identity():
    return dict(problem_id=PROBLEM_ID, contest_id=CONTEST_ID, problem_name=PROBLEM_NAME)
