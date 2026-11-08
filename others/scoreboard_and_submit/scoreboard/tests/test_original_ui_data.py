"""Offline tests of the new data adapter used by the restored original UI."""
import contextlib
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

STAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(STAGE if (STAGE/'track.py').is_file() else STAGE.parent))
import track

class OriginalUIDataTests(unittest.TestCase):
    def test_missing_platform_scores_remain_unknown(self):
        entry = dict(id='new', create_time='2026-10-23T11:07:25Z')
        detail = dict(user=dict(nickname='member name'), files=[dict(path='kernel.asc', content='new source')])
        track.present_entry(entry, detail, SimpleNamespace(account_name='fallback'))
        self.assertEqual(entry['label'], '10-23 19:07')
        self.assertEqual(entry['submitter'], 'member name')
        self.assertIsNone(entry['score'])
        self.assertIsNone(entry['current_score'])
        self.assertIsNone(entry['current_ranking'])
        self.assertEqual(entry['source'], 'new source')

    def test_platform_zero_is_a_real_zero_and_is_not_reused_as_current(self):
        entry = dict(id='new', create_time='2026-10-23T11:07:25Z')
        track.present_entry(entry, dict(score=0, files=None), SimpleNamespace(account_name='member1'))
        self.assertEqual(entry['score'], 0)
        self.assertIsNone(entry['current_score'])
        self.assertEqual(entry['submitter'], 'member1')

    def test_duplicate_or_changed_submission_source_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, 'duplicate'):
            track.kernel_source(dict(files=[dict(path='kernel.asc', content='a'), dict(path='kernel.asc', content='b')]))
        entry = dict(id='new', create_time='2026-10-23T11:07:25Z', source='old verified')
        with self.assertRaisesRegex(RuntimeError, 'differs'):
            track.present_entry(entry, dict(files=[dict(path='kernel.asc', content='changed')]), SimpleNamespace(account_name='member1'))

    def test_non_finite_and_boolean_values_are_not_scores(self):
        for value in (float('nan'), float('inf'), True, '93.5', None):
            self.assertIsNone(track.platform_number(value))
        self.assertEqual(track.platform_number(12.3), 12.3)

    def test_refresh_writes_only_new_data_and_keeps_hidden_times_unknown(self):
        with tempfile.TemporaryDirectory(prefix='panel-ui-test-', dir=STAGE) as temporary:
            base = Path(temporary)/'scoreboard'
            base.mkdir()
            (base.parent/'scoreboard-view').mkdir()
            client = SimpleNamespace(account_id='member1', account_name='member1',
                                     user_id='owner1', session=mock.Mock())
            # A real official response includes pagination and a testcase list;
            # keep zero total as a genuine official result, not a missing value.
            ranking = dict(rows=[], testcases=[dict(_id='visible', tbest=2.0),
                                               dict(_id='hidden', hidden=True)],
                           pages=1, current=1, total=0, size=100)
            client.session.get.return_value = mock.Mock(json=mock.Mock(return_value=ranking))
            case = dict(testcase_id='visible', time=4.0, best_time=2.0, status='Pass')
            hidden = dict(testcase_id='hidden', time=None, best_time=None, status='Hidden')
            data = dict(target=dict(problem_id='new-problem'), last_account='member1',
                        submissions=[dict(id='new', user_id='owner1', status='Pass', cases=[case, hidden],
                                          create_time='2026-10-23T11:07:25Z', source_sha256='bound-job-hash')])
            detail = dict(user=dict(nickname='member1'), files=[dict(path='kernel.asc', content='new submitted kernel')])
            writes = {}
            with mock.patch.object(track.workflow, 'client_for', return_value=client), \
                 mock.patch.object(track.workflow, 'live_metadata', return_value=(dict(score_mode=1, ranking_submission_mode='latest'), {})), \
                 mock.patch.object(track.workflow, 'user_submissions', return_value=[dict(_id='new')]), \
                 mock.patch.object(track.workflow, 'validate_result'), \
                 mock.patch.object(track.workflow, 'record_result'), \
                 mock.patch.object(track.workflow, 'load_data', return_value=data), \
                 mock.patch.object(track.workflow, 'lock', lambda _:contextlib.nullcontext()), \
                 mock.patch.object(track.workflow.cfg, 'BASE', base), \
                 mock.patch.object(track.workflow, 'write_json', side_effect=lambda p,v:writes.update({str(p):v})), \
                 mock.patch.object(track, 'DATA_FILE', base/'data.sinkhorn_norm.json'):
                client.get_submission = mock.Mock(return_value=detail)
                self.assertTrue(track.refresh_data('member1'))
            self.assertEqual(data['global_best_times'], [2.0, None])
            self.assertEqual(data['case_count'], 2)
            self.assertEqual(data['submissions'][0]['source_sha256'], 'bound-job-hash')
            self.assertIsNone(data['submissions'][0]['score'])
            self.assertIsNone(data['team_score'])
            self.assertIsNone(data['team_rank'])
            self.assertEqual(len(writes), 4)
            mirror = writes[str(base.parent/'scoreboard-view/data.json')]
            self.assertNotIn('source', mirror['submissions'][0])
            self.assertIn('kernel_sha256', data['submissions'][0])
            self.assertEqual(Path(data['ranking_evidence']).parts[0], 'ranking_observations')
            client.session.get.assert_called_once_with(track.RANKING_URL, params=dict(page=1, size=100), timeout=20)
            client.session.post.assert_not_called()

if __name__ == '__main__':
    unittest.main()
