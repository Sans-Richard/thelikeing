"""One-request submission workflow for the pinned finals target.

dry_run uses a verified local template cache only: no login/network/NPU/POST.
doctor and result tracking use GET only and never refresh credentials by POST.
The explicit submit command uses the existing selected-account authentication.
"""
import contextlib
from datetime import datetime, timezone, timedelta
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
try:
    import fcntl
except ImportError:
    fcntl = None

import target as cfg

SDK = Path.home() / '.config/opencode/skills/cannjudge-submit'
CST = timezone(timedelta(hours=8))
TERMINAL = {'Pass','Fail','Accepted','Wrong Answer','Compile Error','Runtime Error',
            'Time Limit Exceeded','Memory Limit Exceeded','System Error'}

def sdk_modules():
    sys.path.insert(0, str(SDK))
    from cannjudge_cli import CANNJudgeClient
    from project_files import collect_kernel_files, template_files
    return CANNJudgeClient, collect_kernel_files, template_files

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.'+path.name+'-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

@contextlib.contextmanager
def lock(path):
    if fcntl is None:
        raise RuntimeError('The production workflow requires Linux flock')
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a+') as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError('Workflow/resource is already in use: '+str(path)) from None
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)

def load_data():
    if not cfg.DATA_FILE.exists():
        return dict(target=cfg.target_identity(), submissions=[], pending_submissions=[],
                    global_best_times=[], leaderboard_scores=[], team=None, account_quotas={})
    data = json.loads(cfg.DATA_FILE.read_text(encoding='utf-8'))
    if data.get('target') != cfg.target_identity():
        raise RuntimeError('Result store belongs to a different problem; refusing to mix data')
    return data

def source_digest(files):
    normalized = sorted((dict(path=item['path'],content=item['content']) for item in files),
                        key=lambda item:item['path'])
    if len({item['path'] for item in normalized}) != len(normalized):
        raise RuntimeError('Duplicate source paths')
    return hashlib.sha256(json.dumps(normalized, ensure_ascii=False,
        sort_keys=True, separators=(',',':')).encode('utf-8')).hexdigest()

def check_target(problem):
    if (problem.get('_id') != cfg.PROBLEM_ID or
        problem.get('contest_id') != cfg.CONTEST_ID or
        problem.get('name') != cfg.PROBLEM_NAME or
        problem.get('code_template') != 'npu_kernel_dev'):
        raise RuntimeError('Live problem does not match the pinned SinkhornNorm target')

def live_metadata(client):
    problem = client.resolve_problem(cfg.PROBLEM_URL)
    check_target(problem)
    return problem, client.get_template(cfg.PROBLEM_ID)

def packaged_files(template, project=None):
    _, collect, template_files = sdk_modules()
    project = Path(project or cfg.PROJECT_DIR)
    for name in template_files(template):
        path = project / name
        if not path.is_file() or path.is_symlink():
            raise RuntimeError('Missing or linked official project file: '+name)
    return collect(str(project), template, cfg.PROBLEM_ID)

def summary(files):
    return dict(target=cfg.target_identity(), url=cfg.PROBLEM_URL,
        project=str(cfg.PROJECT_DIR), files=[dict(path=f['path'],
        sha256=hashlib.sha256(f['content'].encode()).hexdigest(),
        bytes=len(f['content'].encode())) for f in files], source_sha256=source_digest(files))

def dry_run():
    template = json.loads(cfg.TEMPLATE_FILE.read_text(encoding='utf-8'))
    result = summary(packaged_files(template))
    result.update(mode='dry-run', network_requests=0, submission_requests=0,
                  device_runs=0, account_selected=False)
    return result

def client_for(account, cached_only=False):
    if not account:
        raise RuntimeError('An explicit --account memberN is required')
    sys.path.insert(0, str(cfg.ROOT / 'others/tools'))
    import accounts
    if not cached_only:
        return accounts.account_client(account)
    # GET-only commands never invoke automatic credential login/renewal.
    profile = accounts.select_account(account)
    identity = json.dumps([profile.get(k,'') for k in ('email','password','ciphertext','user_id')])
    digest = hashlib.sha256(identity.encode()).hexdigest()[:24]
    cache = Path.home()/'.cannjudge/accounts'/profile['id']/(digest+'.json')
    client_class, _, _ = sdk_modules()
    candidates = [cache]
    if profile.get('legacy_session') and profile.get('user_id'):
        candidates.append(Path(profile['legacy_session']).expanduser())
    for path in candidates:
        client = client_class(session_file=path)
        try:
            valid = client.load_session()
        except Exception:
            valid = False
        if not valid:
            continue
        if profile.get('user_id') and str(client.user_id) != str(profile['user_id']):
            raise RuntimeError('Selected account/session identity mismatch')
        client.account_id = profile['id']
        client.account_name = profile.get('name') or profile['id']
        return client
    raise RuntimeError('Selected account has no valid cached session; log in explicitly first')

def user_submissions(client):
    response = client.session.get('https://cannjudge.cn/api/submissions/user/'+str(client.user_id),
        params=dict(problemId=cfg.PROBLEM_ID,userId=client.user_id),timeout=30)
    response.raise_for_status()
    result = response.json()
    if not isinstance(result,list):
        raise RuntimeError('Cannot confirm submission list/quota; stopped')
    # The live endpoint currently ignores problemId and returns mixed-problem
    # history (observed 2026-10-23). Enforce ownership/target locally as well.
    selected=[]
    for item in result:
        if not isinstance(item,dict) or not item.get('_id'):
            raise RuntimeError('Malformed submission list item')
        problem=item.get('problem_id') or item.get('problemId') or item.get('problem')
        owner=item.get('user_id') or item.get('userId') or item.get('user')
        if not problem:
            raise RuntimeError('Cannot confirm problem identity in submission history')
        if owner and object_id(owner)!=str(client.user_id):
            raise RuntimeError('Submission list contains a different owner')
        if object_id(problem)==cfg.PROBLEM_ID:
            selected.append(item)
    return selected

def doctor(account=None):
    client = client_for(account, cached_only=True) if account else sdk_modules()[0]()
    problem, template = live_metadata(client)
    result = summary(packaged_files(template))
    result.update(mode='doctor', end_time=problem.get('end_time'),
        cann_version=problem.get('cann_version'), soc_version=problem.get('soc_version'),
        submission_requests=0, stop_files=[str(p) for p in cfg.STOP_FILES if p.exists()],
        unresolved_jobs=[p.parent.name for p,j in journals() if j.get('state') in {'posting','post_uncertain','pending'}])
    if account:
        submissions = user_submissions(client)
        result['account'] = dict(id=client.account_id,name=client.account_name,user_id=client.user_id)
        result['submission_count_for_problem'] = len(submissions)
        today=datetime.now(timezone.utc).astimezone(CST).date()
        result['quota']=dict(used_today_for_problem=sum(
            datetime.fromisoformat(s['create_time'].replace('Z','+00:00')).astimezone(CST).date()==today
            for s in submissions),server_limit=None,
            note='Server limit is not published in the inspected metadata; no prelim quota is inherited')
    return result

def journals():
    for path in sorted(cfg.RUNS_DIR.glob('*/job.json')):
        yield path, json.loads(path.read_text(encoding='utf-8'))

def guard_new_submission(now=None):
    if any(p.exists() for p in cfg.STOP_FILES):
        raise RuntimeError('STOP is present; submission stopped')
    for path, job in journals():
        if job.get('state') in {'posting','post_uncertain','pending'}:
            raise RuntimeError('Unfinished request '+path.parent.name+'; use --resume or --reconcile')
    if cfg.POST_CLOCK_FILE.exists():
        previous = json.loads(cfg.POST_CLOCK_FILE.read_text())
        if (now if now is not None else time.time()) - previous['time'] < 60:
            raise RuntimeError('The shared 60-second submission interval has not elapsed')

def snapshot(client, template, files):
    _, _, template_files = sdk_modules()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    job_id = stamp+'_'+source_digest(files)[:12]
    run = cfg.RUNS_DIR/job_id
    source = run/'source'
    source.mkdir(parents=True, exist_ok=False)
    names = set(template_files(template)) | {f['path'] for f in files}
    for name in names:
        (source/name).write_bytes((cfg.PROJECT_DIR/name).read_bytes())
    write_json(source/'.cannjudge-project.json', dict(version=1,
        problem_id=cfg.PROBLEM_ID,code_template='npu_kernel_dev'))
    fixed = packaged_files(template, source)
    if source_digest(fixed) != source_digest(files):
        raise RuntimeError('Working source changed while preparing snapshot')
    job = dict(target=cfg.target_identity(),account_id=client.account_id,
        user_id=client.user_id,state='prepared',source_sha256=source_digest(fixed),
        editable_paths=[item['path'] for item in fixed],
        created_at=datetime.now(timezone.utc).isoformat(), submission_id=None,
        source_files={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in names})
    write_json(run/'job.json',job)
    return run,job,fixed

def official_sample_check(run, job):
    # The official run.sh is copied unchanged and runs inside the fixed snapshot.
    source = run/'source'
    command = ['bash','-lc',
        'source /home/developer/Ascend/cann-9.0.0/set_env.sh && exec bash run.sh npu']
    with lock('/tmp/npu.lock'), open(run/'check.log','w',encoding='utf-8') as log:
        process = subprocess.Popen(command,cwd=source,stdout=log,stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            code = process.wait(timeout=900)
        except BaseException:
            os.killpg(process.pid,signal.SIGTERM)
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid,signal.SIGKILL)
                process.wait()
            raise
    if code:
        raise RuntimeError('Official sample/build failed; see '+str(run/'check.log'))
    for name, digest in job['source_files'].items():
        if hashlib.sha256((source/name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Source changed during sample validation')
    write_json(run/'check.json',dict(passed=True,mode='npu',
        source_sha256=job['source_sha256'],scope='official public sample only'))

def post_once(client, payload, run, job):
    # Caller holds the cross-account, cross-process submission lock.
    job.update(state='posting',post_started=time.time())
    write_json(run/'job.json',job)  # Durable BEFORE issuing the only POST.
    write_json(cfg.POST_CLOCK_FILE,dict(time=job['post_started'],job=run.name))
    try:
        response = client.session.post('https://cannjudge.cn/api/submissions/submit',
            json=payload,timeout=30,allow_redirects=False)
        if response.status_code in {400,401,403,404,409,413,422,429}:
            # A complete API error response establishes a definite rejection.
            rejection=response.json()
            if isinstance(rejection,dict):
                safe_rejection={k:str(rejection[k])[:1600] for k in ('message','error','code','detail','retryAfter','retry_after','resetAt','limit') if k in rejection}
                safe_headers={k:response.headers[k] for k in ('Date','Retry-After','X-RateLimit-Limit','X-RateLimit-Remaining','X-RateLimit-Reset','RateLimit-Limit','RateLimit-Remaining','RateLimit-Reset') if k in response.headers}
                job.update(state='post_rejected',http_status=response.status_code,rejection=safe_rejection,rejection_headers=safe_headers)
                write_json(run/'job.json',job)
                raise RuntimeError('Server rejected the submission: HTTP '+str(response.status_code))
        response.raise_for_status()
        if not 200 <= response.status_code < 300:
            raise RuntimeError('Unexpected submission response')
        submission_id = response.json().get('data',{}).get('submissionId')
        if not isinstance(submission_id,str) or not submission_id:
            raise RuntimeError('Submission response has no ID')
    except BaseException as error:
        if job.get('state')=='post_rejected':
            raise RuntimeError('Server rejected the submission: HTTP '+str(job['http_status'])+'; no automatic retry') from None
        job.update(state='post_uncertain',error_type=type(error).__name__)
        write_json(run/'job.json',job)
        raise RuntimeError('POST outcome uncertain; do not retry. Use --reconcile '+run.name) from None
    job.update(state='pending',submission_id=submission_id)
    write_json(run/'job.json',job)
    return submission_id

def object_id(value):
    return str(value.get('_id','')) if isinstance(value,dict) else str(value or '')

def validate_result(result, client, known_job=None):
    problem = result.get('problem_id') or result.get('problemId') or result.get('problem')
    owner = result.get('user_id') or result.get('userId') or result.get('user')
    if problem and object_id(problem) != cfg.PROBLEM_ID:
        raise RuntimeError('Submission result belongs to a different problem')
    if owner and object_id(owner) != str(client.user_id):
        raise RuntimeError('Submission result belongs to a different user')
    if not known_job and (not problem or not owner):
        raise RuntimeError('Cannot verify ownership/target for an untracked submission')

def record_result(client, sid, result, run=None, job=None):
    validate_result(result,client,job)
    if result.get('_id') and str(result['_id'])!=sid:
        raise RuntimeError('Submission ID does not match the result')
    if run:
        write_json(run/'result.json',result)
    cases = []
    for item in result.get('result') or []:
        cases.append(dict(testcase_id=object_id(item.get('testcase_id')),
            status=item.get('testcase_status',item.get('status','Unknown')),
            time=item.get('time'),best_time=item.get('best_time'),
            precision=item.get('precision_ratio'),msg=item.get('msg')))
    score = result.get('score',result.get('total_score'))
    if not isinstance(score,(int,float)) or not math.isfinite(score):
        score = None  # No old formula, hidden-case inference, or invented zero.
    entry = dict(id=sid,problem_id=cfg.PROBLEM_ID,account_id=client.account_id,
        user_id=client.user_id,status=result.get('status','Unknown'),valid=result.get('valid'),cases=cases,
        score=score,current_score=score,current_ranking=None,
        create_time=result.get('create_time',datetime.now(timezone.utc).isoformat()),
        source_sha256=job.get('source_sha256') if job else None,ai_analysis=None)
    if run:
        entry['run_path']=str(run)
    with lock(cfg.BASE/'.data.sinkhorn.lock'):
        data=load_data()
        previous=next((s for s in data['submissions'] if s['id']==sid),None)
        if previous:
            if any(str(previous.get(key)) != str(entry[key])
                   for key in ('problem_id', 'account_id', 'user_id')):
                raise RuntimeError('Existing submission identity mismatch')
            if job is None:
                # A GET refresh supplies no new source evidence. Retain the
                # binding established for this same submission by its job.
                entry['source_sha256'] = previous.get('source_sha256')
            previous.update(entry)
        else:
            data['submissions'].append(entry)
        data['submissions'].sort(key=lambda s:s['create_time'])
        data['global_best_times']=[c['best_time'] for c in cases]
        data['last_account']=client.account_id
        data['pending_submissions']=[s for s in data['submissions'] if s['status'] not in TERMINAL]
        write_json(cfg.DATA_FILE,data)
    if job:
        job['state']='complete' if result.get('status') in TERMINAL else 'pending'
        write_json(run/'job.json',job)
    return entry

def resume(account,sid,max_wait=300):
    client=client_for(account,cached_only=True)
    matches=[(p.parent,j) for p,j in journals() if j.get('submission_id')==sid]
    run,job=matches[0] if len(matches)==1 else (None,None)
    if job and (job['account_id']!=account or str(job['user_id'])!=str(client.user_id)
                or job['target']!=cfg.target_identity()):
        raise RuntimeError('Resume must use the original account')
    initial=client.get_submission(sid)
    validate_result(initial,client,job)
    result=client.wait_for_result(sid,max_wait=max_wait,interval=5) if initial.get('status') not in TERMINAL else initial
    return record_result(client,sid,result,run,job)

def reconcile(account,job_id):
    if Path(job_id).name!=job_id or job_id in {'.','..'}:
        raise RuntimeError('Invalid job ID')
    run=cfg.RUNS_DIR/job_id
    with lock(cfg.LOCK_FILE):
        job=json.loads((run/'job.json').read_text())
        client=client_for(account,cached_only=True)
        if job['account_id']!=account or str(job['user_id'])!=str(client.user_id) or job['target']!=cfg.target_identity():
            raise RuntimeError('Reconcile account/target mismatch')
        if job.get('submission_id'):
            return dict(submission_id=job['submission_id'],next_action='--resume')
        matches=[]
        for item in user_submissions(client):
            created=datetime.fromisoformat(item['create_time'].replace('Z','+00:00')).timestamp()
            if created < job['post_started']-5 or created > job['post_started']+300:
                continue
            detail=client.get_submission(item['_id'])
            validate_result(detail,client,job)
            if detail.get('_id') and str(detail['_id'])!=str(item['_id']):
                raise RuntimeError('Reconcile response ID mismatch; request remains blocked')
            files=detail.get('files')
            paths=set(job['editable_paths'])
            fixed=[f for f in files if f.get('path') in paths] if isinstance(files,list) else []
            if fixed and {f['path'] for f in fixed}==paths and source_digest(fixed)==job['source_sha256']:
                matches.append(item['_id'])
        if len(matches)!=1:
            raise RuntimeError('Reconcile found '+str(len(matches))+' matches; request remains blocked')
        job.update(submission_id=matches[0],state='pending')
        write_json(run/'job.json',job)
        return dict(submission_id=matches[0],next_action='--resume')

def submit(account,daily_limit=None,repeat=False):
    with lock(cfg.LOCK_FILE):
        guard_new_submission()
        client=client_for(account)
        problem,template=live_metadata(client)
        end=datetime.fromisoformat(problem.get('end_time',cfg.END_TIME).replace('Z','+00:00'))
        start=datetime.fromisoformat(problem['start_time'].replace('Z','+00:00'))
        now=datetime.now(timezone.utc)
        if not start<=now<end:
            raise RuntimeError('The problem is not open for submissions')
        submissions=user_submissions(client)
        today=now.astimezone(CST).date()
        used=sum(datetime.fromisoformat(s['create_time'].replace('Z','+00:00')).astimezone(CST).date()==today for s in submissions)
        if daily_limit is not None and (daily_limit<1 or used>=daily_limit):
            raise RuntimeError('Selected account has reached the explicit local daily limit')
        files=packaged_files(template)
        _,_,template_files=sdk_modules()
        official=template_files(template)
        if next(f['content'] for f in files if f['path']=='kernel.asc')==official['kernel.asc']['content']:
            raise RuntimeError('The official empty kernel is still present')
        data=load_data()
        if not repeat and any(s.get('source_sha256')==source_digest(files) for s in data['submissions']):
            raise RuntimeError('Identical source was already submitted; --repeat requires a deliberate repeat experiment')
        run,job,fixed=snapshot(client,template,files)
        print('Snapshot: '+str(run),flush=True)
        try:
            official_sample_check(run,job)
        except BaseException:
            job['state']='validation_failed'
            write_json(run/'job.json',job)
            raise
        # Recheck STOP, interval and live deadline after potentially lengthy build.
        guard_new_submission()
        if datetime.now(timezone.utc)>=end:
            raise RuntimeError('Deadline elapsed during validation')
        sid=post_once(client,dict(problemId=cfg.PROBLEM_ID,userId=client.user_id,files=fixed),run,job)
    print('Submission ID: '+sid,flush=True)
    return resume(account,sid)
