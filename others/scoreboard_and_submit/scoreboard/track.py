#!/usr/bin/env python3
"""GET-only SinkhornNorm data adapter for the original dashboard UI."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import sinkhorn_workflow as workflow
from target import DATA_FILE, PROBLEM_ID, CONTEST_ID

CST = timezone(timedelta(hours=8))
RANKING_URL = 'https://cannjudge.cn/api/problems/'+PROBLEM_ID+'/ranking'

def platform_number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else None

def first_number(record, names):
    for name in names:
        number = platform_number(record.get(name))
        if number is not None:
            return number
    return None

def fetch_rankings(client):
    """The problem leaderboard is paginated and includes hidden-case totals."""
    rows, pages_raw, testcases = [], [], None
    page, pages = 1, 1
    while page <= pages:
        response = client.session.get(RANKING_URL, params=dict(page=page, size=100), timeout=20)
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or not isinstance(result.get('rows'), list):
            raise RuntimeError('Unexpected problem ranking response')
        count = result.get('pages')
        if not isinstance(count, int) or isinstance(count, bool) or not 0 <= count <= 1000:
            raise RuntimeError('Invalid ranking page count')
        if page > 1 and count != pages:
            raise RuntimeError('Leaderboard pagination changed; refresh again')
        pages = count
        if not all(isinstance(row, dict) and row.get('submission_id') for row in result['rows']):
            raise RuntimeError('Invalid ranking row')
        if testcases is None:
            testcases = result.get('testcases')
            if not isinstance(testcases, list):
                raise RuntimeError('Missing leaderboard testcases')
        pages_raw.append(result)
        rows.extend(result['rows'])
        page += 1
    ids = [row['submission_id'] for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError('Leaderboard changed during pagination; refresh again')
    return dict(rows=rows, testcases=testcases, raw_pages=pages_raw)

def apply_rankings(data, ranking, client, observed_at):
    """Bind current official scores to exact SIDs; never re-score hidden cases."""
    rows = ranking['rows'] if ranking else []
    by_sid = {row['submission_id']: row for row in rows}
    own_ids = {s['id'] for s in data['submissions'] if str(s.get('user_id')) == str(client.user_id)}
    owned = [row for row in rows if row['submission_id'] in own_ids
             and str(row.get('user_id')) == str(client.user_id)]
    known_team = data.get('team') or {}
    team_id = known_team.get('team_object_id')
    for row in owned:
        team = row.get('team') or {}
        if team.get('_id'):
            if team_id and team_id != team['_id']:
                raise RuntimeError('Leaderboard team identity differs from the saved team')
            team_id = team['_id']
            data['team'] = dict(team_object_id=team_id, team_id=team.get('team_id'),
                ID=team.get('ID'), name=team.get('team_name'), verified_by_submission_id=row['submission_id'])
    team_rows = [row for row in rows if team_id and (row.get('team') or {}).get('_id') == team_id]
    if len(team_rows) > 1:
        raise RuntimeError('Multiple representative submissions for the same team')
    team_row = team_rows[0] if team_rows else None
    data['team_score'] = platform_number(team_row.get('score')) if team_row else None
    data['team_rank'] = first_number(team_row, ('rank',)) if team_row else None
    data['leaderboard_scores'] = sorted((number for row in rows
        if (number := platform_number(row.get('score'))) is not None), reverse=True)
    for entry in data['submissions']:
        row = by_sid.get(entry['id'])
        # Both submission and owner must match. A teammate's representative
        # score must never be copied to another submission with the same code.
        if row and str(row.get('user_id')) != str(entry.get('user_id')):
            raise RuntimeError('Leaderboard submission owner mismatch')
        entry['current_score'] = platform_number(row.get('score')) if row else None
        entry['current_ranking'] = first_number(row, ('rank',)) if row else None
        entry['current_score_observed_at'] = observed_at if row else None
        if row and entry['current_score'] is not None:
            observation = dict(score=entry['current_score'], rank=entry['current_ranking'],
                observed_at=observed_at, source='official_problem_ranking')
            if platform_number((entry.get('first_score_observation') or {}).get('score')) is None:
                entry['first_score_observation'] = observation.copy()
            entry['last_score_observation'] = observation
        first = entry.get('first_score_observation') or {}
        if entry.get('score_kind') != 'submission_detail' and platform_number(first.get('score')) is not None:
            entry['score'] = first['score']
            entry['ranking'] = first.get('rank')
            entry['score_kind'] = 'first_observed'
        entry['score_note'] = ('首次采集官方成绩（'+str(first.get('observed_at', ''))+
            '），不是提交瞬时成绩；历史 TBest 快照不可追溯。' if entry.get('score_kind') == 'first_observed'
            else '平台提交详情返回的总分。' if entry.get('score_kind') == 'submission_detail'
            else '历史提交未保存总分，平台未提供历史完整总分；10 个隐藏点不可推算。')
        entry['current_score_note'] = ('官方题目榜单当前代表提交；采集于 '+observed_at if row else
            '当前题目榜单不再列出此历史提交；未将队伍最新成绩复制到本行。')
    observations = data.setdefault('score_observations', [])
    if team_row and data['team_score'] is not None:
        observation = dict(submission_id=team_row['submission_id'], score=data['team_score'],
            rank=data['team_rank'], observed_at=observed_at,
            create_time=team_row.get('create_time'), status=team_row.get('status'),
            source='official_problem_ranking')
        # Preserve the first observation of each actual change. Repeated
        # refreshes update freshness without adding duplicate chart points.
        last = observations[-1] if observations else {}
        changed = any(last.get(k) != observation.get(k) for k in ('submission_id', 'score', 'rank', 'status'))
        if changed:
            observations.append(observation)
        else:
            last['last_seen_at'] = observed_at
    return team_row

def kernel_source(detail):
    files = [item for item in (detail.get('files') or [])
             if isinstance(item, dict) and item.get('path') == 'kernel.asc'
             and isinstance(item.get('content'), str)]
    if len(files) > 1:
        raise RuntimeError('Platform result contains duplicate kernel.asc files')
    return files[0]['content'] if files else None

def present_entry(entry, detail, client):
    entry['label'] = datetime.fromisoformat(entry['create_time'].replace('Z', '+00:00')).astimezone(CST).strftime('%m-%d %H:%M')
    user = detail.get('user') or {}
    entry['submitter'] = user.get('nickname') if isinstance(user, dict) else None
    entry['submitter'] = entry['submitter'] or client.account_name
    entry['platform_submission_id'] = detail.get('ID')
    # Only genuine detail totals qualify as submission-detail scores. First
    # observed ranking snapshots are restored separately, with provenance.
    entry['score'] = first_number(detail, ('score', 'total_score'))
    entry['score_kind'] = 'submission_detail' if entry['score'] is not None else None
    entry['current_score'] = first_number(detail, ('current_score',))
    entry['ranking'] = first_number(detail, ('ranking',))
    entry['current_ranking'] = first_number(detail, ('current_ranking',))
    source = kernel_source(detail)
    if source is not None:
        if entry.get('source') and entry['source'] != source:
            raise RuntimeError('Platform source differs from the saved source for this submission')
        entry['source'] = source
        entry['kernel_sha256'] = hashlib.sha256(source.encode('utf-8')).hexdigest()
    return entry

def refresh_data(account=None):
    # Serialize CLI and HTTP refreshes too, while record_result retains its
    # shorter data-file lock shared with the submission workflow.
    with workflow.lock(workflow.cfg.BASE/'.panel.refresh.lock'):
        return _refresh_data(account)

def _refresh_data(account=None):
    account = account or workflow.load_data().get('last_account')
    if not account:
        return False
    client = workflow.client_for(account, cached_only=True)
    problem, _ = workflow.live_metadata(client)
    details = {}
    for item in workflow.user_submissions(client):
        detail = client.get_submission(item['_id'])
        workflow.validate_result(detail, client)
        workflow.record_result(client, item['_id'], detail)
        details[item['_id']] = detail

    ranking = None
    stats_warning = None
    try:
        ranking = fetch_rankings(client)
    except Exception as error:
        stats_warning = '官方榜单暂不可用（'+type(error).__name__+'），未推算分数或排名。'

    observed_at = datetime.now(timezone.utc).isoformat()
    with workflow.lock(workflow.cfg.BASE/'.data.sinkhorn.lock'):
        data = workflow.load_data()
        for entry in data['submissions']:
            if entry['id'] in details:
                present_entry(entry, details[entry['id']], client)
        data['case_count'] = max((len(entry.get('cases') or []) for entry in data['submissions']), default=0)
        completed = sorted((entry for entry in data['submissions']
                            if entry.get('status') == 'Pass' and entry.get('cases')),
                           key=lambda entry: entry['create_time'], reverse=True)
        data['global_best_times'] = [
            (case.get('best_time') if platform_number(case.get('best_time')) is not None
             and case['best_time'] > 0 and case.get('status') != 'Hidden' else None)
            for case in completed[0]['cases']] if completed else []
        apply_rankings(data, ranking, client, observed_at)
        if ranking is not None:
            best_by_id = {workflow.object_id(t.get('_id') or t.get('id')):
                (platform_number(t.get('tbest')) if not t.get('hidden')
                 and platform_number(t.get('tbest')) is not None and t['tbest'] > 0 else None)
                for t in ranking['testcases'] if isinstance(t, dict)}
            if completed:
                data['global_best_times'] = [best_by_id.get(c.get('testcase_id')) for c in completed[0]['cases']]
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            evidence = workflow.cfg.BASE/'ranking_observations'/(stamp+'.json')
            workflow.write_json(evidence, dict(target=data['target'], observed_at=observed_at,
                endpoint=RANKING_URL, pages=ranking['raw_pages']))
            data['ranking_observed_at'] = observed_at
            data['ranking_evidence'] = str(evidence.relative_to(workflow.cfg.BASE))
        data['last_account'] = client.account_id
        data['updated_at'] = observed_at
        data['panel_warnings'] = ([stats_warning] if stats_warning else []) + [
            '复赛按最新提交排名；历史完整成绩未公开。提交时列的已采集数值为首次观测，曲线按实际采集时间记录。']
        data['scoring'] = dict(mode='official_problem_ranking', theoretical_score=None,
            score_mode=problem.get('score_mode'), ranking_submission_mode=problem.get('ranking_submission_mode'),
            case_formula='100/(1+ln(time/TBest)/ln(1.5))', aggregate='all_testcases_mean',
            source=RANKING_URL, note='Official server totals include hidden cases. No partial-case reconstruction.')
        workflow.write_json(DATA_FILE, data)
        # These are the old dashboard entry points, now containing only new
        # problem data. The original UI can also be opened from its mirror.
        workflow.write_json(workflow.cfg.BASE/'data.json', data)
        mirror = workflow.cfg.BASE.parent/'scoreboard-view'
        if mirror.is_dir():
            public_data = json.loads(json.dumps(data, ensure_ascii=False, allow_nan=False))
            for entry in public_data['submissions']:
                entry.pop('source', None)
                entry.pop('run_path', None)
            workflow.write_json(mirror/'data.json', public_data)
    return True

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--account', required=True)
    args = parser.parse_args()
    try:
        refresh_data(args.account)
        print(json.dumps(dict(problem_id=PROBLEM_ID, contest_id=CONTEST_ID, data_file=str(DATA_FILE)), indent=2))
    except Exception as error:
        parser.exit(1, 'Stopped: '+str(error)+'\n')

if __name__ == '__main__':
    main()
