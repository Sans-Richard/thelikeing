"""Offline regression tests for the SinkhornNorm migration.

No test authenticates, sends network traffic, compiles, or uses an NPU.
The platform SDK's source packager is loaded as pure local Python only.
Run: python -m unittest discover -s tests -v
"""
import contextlib
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

STAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGE))
import sinkhorn_workflow as workflow


def load_packager():
    # The migration workspace contains a read-only copy of the production SDK.
    candidate = STAGE.parent / 'project_files.py'
    if not candidate.is_file():
        candidate = Path.home() / '.config/opencode/skills/cannjudge-submit/project_files.py'
    spec = importlib.util.spec_from_file_location('migration_test_packager', candidate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PACKAGER = load_packager()


class MigrationTests(unittest.TestCase):
    def setUp(self):
        # Keep temporary atomic renames inside the explicitly writable workspace.
        self.temporary = tempfile.TemporaryDirectory(prefix='sinkhorn-migration-test-',
                                                    dir=Path(__file__).parent)
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        base = root / 'others/scoreboard_and_submit/scoreboard'
        project = root / 'sinkhorn_norm_problem_2360_template'
        base.mkdir(parents=True)
        project.mkdir()
        self.cfg = SimpleNamespace(
            ROOT=root, BASE=base, PROJECT_DIR=project,
            PROBLEM_ID='final-problem', CONTEST_ID='final-contest',
            PROBLEM_NAME='sinkhorn_norm', PROBLEM_URL='https://cannjudge.cn/public/final/sinkhorn_norm',
            DATA_FILE=base/'data.sinkhorn_norm.json', TEMPLATE_FILE=base/'template.sinkhorn_norm.json',
            RUNS_DIR=base/'runs_sinkhorn', STOP_FILES=(root/'STOP.json',),
            LOCK_FILE=base/'.submission.lock', POST_CLOCK_FILE=base/'.last_submission.json',
            END_TIME='2099-01-01T00:00:00Z',
        )
        self.cfg.target_identity = lambda: dict(
            problem_id=self.cfg.PROBLEM_ID, contest_id=self.cfg.CONTEST_ID,
            problem_name=self.cfg.PROBLEM_NAME)
        self.template = {'files': [
            {'path':'kernel.asc', 'content':'// official empty kernel\n', 'editable':True},
            {'path':'main.asc', 'content':'// official main\n', 'editable':False},
            {'path':'judge.asc', 'content':'// official judge\n', 'editable':False},
            {'path':'data_utils.h', 'content':'// official data\n', 'editable':False},
            {'path':'run.sh', 'content':'#!/bin/bash\nexit 0\n', 'editable':False},
        ]}
        for item in self.template['files']:
            (project/item['path']).write_text(item['content'], encoding='utf-8')
        (project/'kernel.asc').write_text('// candidate computes SinkhornNorm\n', encoding='utf-8')
        (project/'.cannjudge-project.json').write_text(json.dumps({
            'problem_id':self.cfg.PROBLEM_ID, 'code_template':'npu_kernel_dev'}), encoding='utf-8')
        self.cfg.TEMPLATE_FILE.write_text(json.dumps(self.template), encoding='utf-8')
        self.client = SimpleNamespace(account_id='member2', account_name='Member 2',
                                      user_id='user-2', session=mock.Mock())
        self.client_constructor = mock.Mock(side_effect=AssertionError('network client created'))
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(workflow, 'cfg', self.cfg).start()
        mock.patch.object(workflow, 'lock', lambda *args, **kwargs: contextlib.nullcontext()).start()
        mock.patch.object(workflow, 'sdk_modules', lambda: (
            self.client_constructor, PACKAGER.collect_kernel_files, PACKAGER.template_files)).start()
        # No test is allowed to fall through to real authentication or device execution.
        self.login = mock.patch.object(workflow, 'client_for', return_value=self.client).start()
        self.device = mock.patch.object(workflow, 'official_sample_check').start()
        self.popen = mock.patch.object(workflow.subprocess, 'Popen',
                                      side_effect=AssertionError('external process started')).start()

    def problem(self):
        return dict(_id=self.cfg.PROBLEM_ID, contest_id=self.cfg.CONTEST_ID,
                    name=self.cfg.PROBLEM_NAME, code_template='npu_kernel_dev',
                    start_time='2020-01-01T00:00:00Z', end_time=self.cfg.END_TIME)

    def result(self, count=1, **extra):
        result = dict(_id='submission-1', problem_id=self.cfg.PROBLEM_ID,
                      user_id=self.client.user_id, status='Pass', score=92.5,
                      result=[dict(testcase_id='case-'+str(i), testcase_status='Pass',
                                   time=i+1, best_time=i+0.5, precision_ratio=1.0)
                              for i in range(count)])
        result.update(extra)
        return result

    def job(self, state='prepared', **extra):
        run = self.cfg.RUNS_DIR/'job-1'
        run.mkdir(parents=True, exist_ok=True)
        job = dict(target=self.cfg.target_identity(), account_id=self.client.account_id,
                   user_id=self.client.user_id, state=state, submission_id=None,
                   source_sha256='test-hash', post_started=100.0,
                   editable_paths=['kernel.asc'])
        job.update(extra)
        workflow.write_json(run/'job.json', job)
        return run, job

    def test_dry_run_is_offline_and_does_not_authenticate_or_write_results(self):
        report = workflow.dry_run()
        self.assertEqual([f['path'] for f in report['files']], ['kernel.asc'])
        self.assertEqual(report['network_requests'], 0)
        self.assertEqual(report['submission_requests'], 0)
        self.assertEqual(report['device_runs'], 0)
        self.assertFalse(report['account_selected'])
        self.login.assert_not_called()
        self.client_constructor.assert_not_called()
        self.client.session.get.assert_not_called()
        self.client.session.post.assert_not_called()
        self.popen.assert_not_called()
        self.device.assert_not_called()
        self.assertFalse(self.cfg.DATA_FILE.exists())
        self.assertFalse(self.cfg.POST_CLOCK_FILE.exists())

    def test_target_rejects_each_old_or_incorrect_identity_field(self):
        workflow.check_target(self.problem())
        for key in ('_id', 'contest_id', 'name', 'code_template'):
            with self.subTest(key=key):
                problem = self.problem()
                problem[key] = 'old-initial-round'
                with self.assertRaises(RuntimeError):
                    workflow.check_target(problem)

    def test_old_project_manifest_is_rejected(self):
        (self.cfg.PROJECT_DIR/'.cannjudge-project.json').write_text(
            '{"problem_id":"old-initial-problem"}', encoding='utf-8')
        with self.assertRaises(ValueError):
            workflow.dry_run()

    def test_modified_protected_file_is_rejected(self):
        (self.cfg.PROJECT_DIR/'judge.asc').write_text('// changed judge\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            workflow.dry_run()

    def test_valid_helper_is_allowed_but_framework_is_not_uploaded(self):
        (self.cfg.PROJECT_DIR/'helper.h').write_text('// legal helper\n', encoding='utf-8')
        paths = [item['path'] for item in workflow.packaged_files(self.template)]
        self.assertEqual(paths, ['helper.h', 'kernel.asc'])

    def test_old_result_store_cannot_be_loaded_as_finals_data(self):
        old = self.cfg.BASE/'data.json'
        old.write_text('{"submissions":[{"id":"old"}]}', encoding='utf-8')
        self.assertEqual(workflow.load_data()['submissions'], [])
        workflow.write_json(self.cfg.DATA_FILE, dict(target={'problem_id':'old'}, submissions=[]))
        with self.assertRaises(RuntimeError):
            workflow.load_data()
        self.assertIn('old', old.read_text(encoding='utf-8'))

    def test_unknown_post_is_single_request_with_durable_journal_before_send(self):
        run, job = self.job()
        payload = dict(problemId=self.cfg.PROBLEM_ID, userId=self.client.user_id,
                       files=[dict(path='kernel.asc', content='candidate')])

        def timeout_after_accepting(*args, **kwargs):
            disk = json.loads((run/'job.json').read_text(encoding='utf-8'))
            self.assertEqual(disk['state'], 'posting')
            self.assertTrue(self.cfg.POST_CLOCK_FILE.is_file())
            self.assertFalse(kwargs['allow_redirects'])
            self.assertEqual(kwargs['json'], payload)
            raise TimeoutError('simulated lost response')

        self.client.session.post.side_effect = timeout_after_accepting
        with self.assertRaisesRegex(RuntimeError, 'uncertain'):
            workflow.post_once(self.client, payload, run, job)
        self.assertEqual(self.client.session.post.call_count, 1)
        disk = json.loads((run/'job.json').read_text(encoding='utf-8'))
        self.assertEqual(disk['state'], 'post_uncertain')
        self.assertIsNone(disk['submission_id'])
        with self.assertRaisesRegex(RuntimeError, 'Unfinished'):
            workflow.guard_new_submission(now=10000)
        self.assertEqual(self.client.session.post.call_count, 1)

    def test_missing_submission_id_is_uncertain_and_not_retried(self):
        run, job = self.job()
        response = mock.Mock(status_code=200)
        response.json.return_value = {'data':{}}
        self.client.session.post.return_value = response
        with self.assertRaisesRegex(RuntimeError, 'uncertain'):
            workflow.post_once(self.client, {}, run, job)
        self.assertEqual(self.client.session.post.call_count, 1)
        self.assertEqual(json.loads((run/'job.json').read_text())['state'], 'post_uncertain')

    def test_valid_post_records_id_and_pending_request_blocks_all_accounts(self):
        run, job = self.job()
        response = mock.Mock(status_code=200)
        response.json.return_value = {'data':{'submissionId':'submission-1'}}
        self.client.session.post.return_value = response
        self.assertEqual(workflow.post_once(self.client, {}, run, job), 'submission-1')
        disk = json.loads((run/'job.json').read_text())
        self.assertEqual((disk['state'], disk['submission_id']), ('pending', 'submission-1'))
        self.client.account_id = 'member3'
        with self.assertRaisesRegex(RuntimeError, 'Unfinished'):
            workflow.guard_new_submission(now=10000)

    def test_post_accepts_201_and_records_explicit_4xx_rejection(self):
        run, job = self.job()
        response = mock.Mock(status_code=201)
        response.json.return_value = {'data':{'submissionId':'submission-1'}}
        self.client.session.post.return_value = response
        self.assertEqual(workflow.post_once(self.client, {}, run, job), 'submission-1')
        run, job = self.job()
        response = mock.Mock(status_code=403)
        response.json.return_value = {'message':'forbidden'}
        self.client.session.post.return_value = response
        with self.assertRaisesRegex(RuntimeError, 'rejected'):
            workflow.post_once(self.client, {}, run, job)
        self.assertEqual(json.loads((run/'job.json').read_text())['state'], 'post_rejected')
        workflow.guard_new_submission(now=job['post_started']+60)
        self.assertEqual(self.client.session.post.call_count, 2)

    def test_post_redirect_server_error_and_invalid_json_remain_uncertain(self):
        for status in (302, 307, 500, 200):
            with self.subTest(status=status):
                run, job = self.job()
                response = mock.Mock(status_code=status)
                if status == 200:
                    response.json.side_effect = ValueError('invalid JSON')
                else:
                    response.json.return_value = {'message':'not a confirmed success'}
                self.client.session.post.reset_mock()
                self.client.session.post.return_value = response
                with self.assertRaisesRegex(RuntimeError, 'uncertain'):
                    workflow.post_once(self.client, {}, run, job)
                self.assertEqual(self.client.session.post.call_count, 1)
                self.assertEqual(json.loads((run/'job.json').read_text())['state'], 'post_uncertain')

    def test_interval_stop_and_unfinished_journals_fail_closed(self):
        workflow.write_json(self.cfg.POST_CLOCK_FILE, {'time':1000})
        with self.assertRaisesRegex(RuntimeError, '60-second'):
            workflow.guard_new_submission(now=1059.9)
        workflow.guard_new_submission(now=1060)
        self.cfg.STOP_FILES[0].write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(RuntimeError, 'STOP'):
            workflow.guard_new_submission(now=2000)
        self.cfg.STOP_FILES[0].unlink()
        for state in ('posting', 'post_uncertain', 'pending'):
            with self.subTest(state=state):
                self.job(state)
                with self.assertRaisesRegex(RuntimeError, 'Unfinished'):
                    workflow.guard_new_submission(now=2000)
        self.job('validation_failed')
        workflow.guard_new_submission(now=2000)

    def test_case_lengths_are_not_fixed_and_score_is_platform_supplied(self):
        for count in (0, 1, 15, 17, 32):
            with self.subTest(count=count):
                entry = workflow.record_result(self.client, 'submission-1', self.result(count))
                self.assertEqual(len(entry['cases']), count)
                self.assertEqual(entry['score'], 92.5)
                data = workflow.load_data()
                self.assertEqual(len(data['global_best_times']), count)
                self.assertEqual(len(data['submissions']), 1)
        no_score = self.result(17)
        del no_score['score']
        entry = workflow.record_result(self.client, 'submission-1', no_score)
        self.assertIsNone(entry['score'])

    def test_result_rejects_wrong_problem_or_user_before_writing(self):
        for field, wrong in (('problem_id', 'old-problem'), ('user_id', 'other-user')):
            with self.subTest(field=field):
                with self.assertRaises(RuntimeError):
                    workflow.record_result(self.client, 'submission-1', self.result(**{field:wrong}))
                self.assertFalse(self.cfg.DATA_FILE.exists())
        result = self.result()
        del result['problem_id']
        del result['user_id']
        with self.assertRaises(RuntimeError):
            workflow.record_result(self.client, 'submission-1', result)

    def test_result_rejects_different_submission_id(self):
        with self.assertRaisesRegex(RuntimeError, 'Submission ID'):
            workflow.record_result(self.client, 'submission-1', self.result(_id='submission-2'))
        self.assertFalse(self.cfg.DATA_FILE.exists())

    def test_resume_known_submission_never_posts_and_rejects_another_account(self):
        run, job = self.job('pending', submission_id='submission-1')
        self.client.get_submission = mock.Mock(return_value=self.result(17))
        self.client.wait_for_result = mock.Mock(side_effect=AssertionError('terminal result polled'))
        entry = workflow.resume('member2', 'submission-1')
        self.assertEqual(len(entry['cases']), 17)
        self.client.session.post.assert_not_called()
        self.client.wait_for_result.assert_not_called()
        with self.assertRaisesRegex(RuntimeError, 'original account'):
            workflow.resume('member3', 'submission-1')

    def test_resume_rejects_a_journal_from_another_target(self):
        self.job('pending', submission_id='submission-1', target={'problem_id':'old-initial'})
        self.client.get_submission = mock.Mock()
        with self.assertRaises(RuntimeError):
            workflow.resume('member2', 'submission-1')
        self.client.get_submission.assert_not_called()

    def test_reconcile_uses_editable_paths_and_ignores_platform_file_metadata(self):
        files = [dict(path='kernel.asc',content='candidate')]
        run, job = self.job('post_uncertain', source_sha256=workflow.source_digest(files))
        items = [dict(_id='submission-1', create_time='1970-01-01T00:01:42Z')]
        mock.patch.object(workflow, 'user_submissions', return_value=items).start()
        platform_files = [dict(path='main.asc',content='official frame',editable=False),
                          dict(path='kernel.asc',content='candidate',editable=True,
                               language='cpp', _id='platform-file-id')]
        self.client.get_submission = mock.Mock(return_value=self.result(files=platform_files))
        answer = workflow.reconcile('member2', run.name)
        self.assertEqual(answer['submission_id'], 'submission-1')
        self.assertEqual(json.loads((run/'job.json').read_text())['state'], 'pending')
        self.client.session.post.assert_not_called()

    def test_reconcile_zero_or_multiple_matches_cannot_clear_unknown(self):
        files = [dict(path='kernel.asc',content='candidate')]
        run, job = self.job('post_uncertain', source_sha256=workflow.source_digest(files))
        self.client.get_submission = mock.Mock(return_value=self.result(files=files))
        for items in ([], [dict(_id='submission-1',create_time='1970-01-01T00:01:42Z'),
                           dict(_id='submission-2',create_time='1970-01-01T00:01:43Z')]):
            with self.subTest(matches=len(items)):
                with mock.patch.object(workflow, 'user_submissions', return_value=items):
                    with self.assertRaisesRegex(RuntimeError, 'remains blocked'):
                        workflow.reconcile('member2', run.name)
                disk = json.loads((run/'job.json').read_text())
                self.assertEqual(disk['state'], 'post_uncertain')
                self.assertIsNone(disk['submission_id'])
        self.client.session.post.assert_not_called()

    def test_blocked_submission_cannot_authenticate_or_post_again(self):
        self.job('post_uncertain')
        with self.assertRaisesRegex(RuntimeError, 'Unfinished'):
            workflow.submit('member3')
        self.login.assert_not_called()
        self.client.session.post.assert_not_called()

    def test_non_list_quota_response_is_rejected(self):
        response = mock.Mock()
        response.json.return_value = {'error':'not a submission list'}
        self.client.session.get.return_value = response
        with self.assertRaisesRegex(RuntimeError, 'quota'):
            workflow.user_submissions(self.client)
        self.client.session.post.assert_not_called()

    def test_mixed_problem_history_is_filtered_even_if_server_ignores_query(self):
        response=mock.Mock()
        own=dict(_id='new',problem_id=self.cfg.PROBLEM_ID,user_id=self.client.user_id)
        response.json.return_value=[
            dict(_id='old',problem_id='prelim',user_id=self.client.user_id),
            own,
            dict(_id='different-version',problem_id='old-final-version',user_id=self.client.user_id)]
        self.client.session.get.return_value=response
        self.assertEqual(workflow.user_submissions(self.client),[own])
        self.client.session.post.assert_not_called()

    def test_history_with_missing_problem_or_wrong_owner_is_rejected(self):
        response=mock.Mock()
        self.client.session.get.return_value=response
        for records in ([dict(_id='unknown',user_id=self.client.user_id)],
                        [dict(_id='other',problem_id=self.cfg.PROBLEM_ID,user_id='other-user')]):
            response.json.return_value=records
            with self.assertRaises(RuntimeError):
                workflow.user_submissions(self.client)
        self.client.session.post.assert_not_called()

    def test_snapshot_binds_source_and_does_not_follow_later_working_edits(self):
        files = workflow.packaged_files(self.template)
        run, job, fixed = workflow.snapshot(self.client, self.template, files)
        expected = workflow.source_digest(files)
        (self.cfg.PROJECT_DIR/'kernel.asc').write_text('// later edit', encoding='utf-8')
        self.assertEqual(job['source_sha256'], expected)
        self.assertEqual(workflow.source_digest(fixed), expected)
        self.assertNotEqual(fixed[0]['content'], (self.cfg.PROJECT_DIR/'kernel.asc').read_text())
        self.assertEqual((run/'source/main.asc').read_text(), '// official main\n')
        self.assertFalse(self.cfg.POST_CLOCK_FILE.exists())

    def test_sample_failure_prevents_any_submission_post(self):
        mock.patch.object(workflow, 'live_metadata', return_value=(self.problem(), self.template)).start()
        mock.patch.object(workflow, 'user_submissions', return_value=[]).start()
        self.device.side_effect = RuntimeError('sample failed')
        with self.assertRaisesRegex(RuntimeError, 'sample failed'):
            workflow.submit('member2')
        self.client.session.post.assert_not_called()
        job = next(workflow.journals())[1]
        self.assertEqual(job['state'], 'validation_failed')


    def test_unbound_refresh_preserves_existing_source_and_run_binding(self):
        run, job = self.job('pending', submission_id='submission-1',
                            source_sha256='validated-candidate-sha')
        workflow.record_result(self.client, 'submission-1', self.result(15), run, job)
        refreshed = workflow.record_result(self.client, 'submission-1', self.result(15, score=96))
        self.assertEqual(refreshed['source_sha256'], 'validated-candidate-sha')
        saved = workflow.load_data()['submissions'][0]
        self.assertEqual(saved['source_sha256'], 'validated-candidate-sha')
        self.assertEqual(saved['run_path'], str(run))
        self.assertEqual(saved['score'], 96)
        imported = workflow.record_result(self.client, 'submission-2',
                                           self.result(_id='submission-2'))
        self.assertIsNone(imported['source_sha256'])

    def test_existing_record_identity_cannot_be_reassigned_during_refresh(self):
        workflow.record_result(self.client, 'submission-1', self.result())
        before = self.cfg.DATA_FILE.read_bytes()
        self.client.account_id = 'member3'
        with self.assertRaisesRegex(RuntimeError, 'identity mismatch'):
            workflow.record_result(self.client, 'submission-1', self.result())
        self.assertEqual(self.cfg.DATA_FILE.read_bytes(), before)



if __name__ == '__main__':
    unittest.main(verbosity=2)
