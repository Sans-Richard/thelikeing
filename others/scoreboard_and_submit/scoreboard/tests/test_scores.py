"""Offline score provenance regressions; no authentication/network/device use."""
import contextlib
from copy import deepcopy
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

STAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(STAGE if (STAGE/'track.py').is_file() else STAGE.parent))
import track


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.client = SimpleNamespace(account_id='member1', account_name='Member 1',
                                      user_id='u1', session=mock.Mock())
        self.before = '2026-10-23T12:00:00+00:00'
        self.after = '2026-10-23T13:00:00+00:00'

    def entry(self, sid='s1', owner='u1', **extra):
        value = dict(id=sid, user_id=owner, create_time='2026-10-23T11:00:00Z',
                     status='Pass', cases=[])
        value.update(extra)
        return value

    def row(self, sid='s1', owner='u1', score=32.5, rank=17, team='team1', **extra):
        value = dict(submission_id=sid, user_id=owner, score=score, rank=rank,
                     status='Pass', create_time='2026-10-23T11:00:00Z',
                     team=dict(_id=team, team_id='external-'+team, ID=22, team_name='My team'))
        value.update(extra)
        return value

    def data(self, *entries, **extra):
        value = dict(target=dict(problem_id=track.PROBLEM_ID), submissions=list(entries))
        value.update(extra)
        return value

    def ranking(self, *rows):
        return dict(rows=list(rows), testcases=[], raw_pages=[])

    def response(self, **values):
        result = dict(rows=[], pages=1, current=1, total=0, size=100, testcases=[])
        result.update(values)
        return mock.Mock(json=mock.Mock(return_value=result))

    def test_fetch_all_leaderboard_pages_uses_current_problem_url(self):
        self.client.session.get.side_effect = [
            self.response(rows=[self.row('s1')], pages=2, total=2),
            self.response(rows=[self.row('s2', owner='u2')], pages=2, current=2, total=2),
        ]
        result = track.fetch_rankings(self.client)
        self.assertEqual([r['submission_id'] for r in result['rows']], ['s1', 's2'])
        self.assertEqual(len(result['raw_pages']), 2)
        self.assertEqual(self.client.session.get.call_args_list, [
            mock.call(track.RANKING_URL, params=dict(page=1, size=100), timeout=20),
            mock.call(track.RANKING_URL, params=dict(page=2, size=100), timeout=20),
        ])
        self.client.session.post.assert_not_called()

    def test_duplicate_sid_across_pages_rejects_unstable_snapshot(self):
        self.client.session.get.side_effect = [
            self.response(rows=[self.row()], pages=2),
            self.response(rows=[self.row()], pages=2, current=2),
        ]
        with self.assertRaisesRegex(RuntimeError, 'pagination'):
            track.fetch_rankings(self.client)

    def test_changed_page_count_rejects_unstable_snapshot(self):
        self.client.session.get.side_effect = [self.response(pages=2), self.response(pages=3)]
        with self.assertRaisesRegex(RuntimeError, 'pagination'):
            track.fetch_rankings(self.client)

    def test_malformed_page_count_is_rejected_without_unbounded_requests(self):
        for pages in (True, '2', -1, 1001, None):
            with self.subTest(pages=pages):
                self.client.session.get.return_value = self.response(pages=pages)
                self.client.session.get.reset_mock()
                with self.assertRaisesRegex(RuntimeError, 'page count'):
                    track.fetch_rankings(self.client)
                self.assertEqual(self.client.session.get.call_count, 1)

    def test_missing_sid_or_testcase_metadata_is_rejected(self):
        for kwargs in (dict(rows=[dict(score=31)]), dict(testcases=None)):
            with self.subTest(kwargs=kwargs):
                self.client.session.get.return_value = self.response(**kwargs)
                with self.assertRaises(RuntimeError):
                    track.fetch_rankings(self.client)

    def test_sid_and_owner_must_both_match(self):
        data = self.data(self.entry())
        with self.assertRaisesRegex(RuntimeError, 'owner mismatch'):
            track.apply_rankings(data, self.ranking(self.row(owner='u2')), self.client, self.before)
        self.assertNotIn('first_score_observation', data['submissions'][0])

    def test_same_source_does_not_copy_teammates_score_into_another_sid(self):
        data = self.data(self.entry('s1', source='identical'), self.entry('s2', owner='u2', source='identical'))
        track.apply_rankings(data, self.ranking(self.row('s1')), self.client, self.before)
        self.assertEqual(data['submissions'][0]['current_score'], 32.5)
        self.assertIsNone(data['submissions'][1]['current_score'])
        self.assertNotIn('first_score_observation', data['submissions'][1])

    def test_first_observation_is_frozen_while_current_changes(self):
        data = self.data(self.entry())
        track.apply_rankings(data, self.ranking(self.row()), self.client, self.before)
        first = deepcopy(data['submissions'][0]['first_score_observation'])
        track.apply_rankings(data, self.ranking(self.row(score=31.1, rank=19)), self.client, self.after)
        entry = data['submissions'][0]
        self.assertEqual(entry['first_score_observation'], first)
        self.assertEqual(entry['score'], 32.5)
        self.assertEqual(entry['ranking'], 17)
        self.assertEqual(entry['current_score'], 31.1)
        self.assertEqual(entry['last_score_observation']['observed_at'], self.after)
        self.assertEqual(entry['score_kind'], 'first_observed')

    def test_zero_is_valid_official_score_and_first_observation(self):
        data = self.data(self.entry())
        track.apply_rankings(data, self.ranking(self.row(score=0)), self.client, self.before)
        self.assertEqual(data['team_score'], 0)
        self.assertEqual(data['leaderboard_scores'], [0])
        self.assertEqual(data['submissions'][0]['score'], 0)
        self.assertEqual(data['submissions'][0]['current_score'], 0)

    def test_nonrepresentative_history_keeps_first_but_clears_current(self):
        data = self.data(self.entry('s1'), self.entry('s2'))
        track.apply_rankings(data, self.ranking(self.row('s1')), self.client, self.before)
        track.apply_rankings(data, self.ranking(self.row('s2', score=41)), self.client, self.after)
        old, new = data['submissions']
        self.assertEqual(old['score'], 32.5)
        self.assertIsNone(old['current_score'])
        self.assertIsNone(old['current_ranking'])
        self.assertIsNone(old['current_score_observed_at'])
        self.assertEqual(new['current_score'], 41)

    def test_failed_ranking_clears_stale_current_without_deleting_history(self):
        data = self.data(self.entry())
        track.apply_rankings(data, self.ranking(self.row()), self.client, self.before)
        observations = deepcopy(data['score_observations'])
        track.apply_rankings(data, None, self.client, self.after)
        self.assertIsNone(data['team_score'])
        self.assertIsNone(data['team_rank'])
        self.assertEqual(data['leaderboard_scores'], [])
        self.assertIsNone(data['submissions'][0]['current_score'])
        self.assertEqual(data['submissions'][0]['score'], 32.5)
        self.assertEqual(data['score_observations'], observations)

    def test_repeated_refresh_deduplicates_curve_points_but_updates_freshness(self):
        data = self.data(self.entry())
        ranking = self.ranking(self.row())
        track.apply_rankings(data, ranking, self.client, self.before)
        track.apply_rankings(data, ranking, self.client, self.after)
        self.assertEqual(len(data['score_observations']), 1)
        self.assertEqual(data['score_observations'][0]['observed_at'], self.before)
        self.assertEqual(data['score_observations'][0]['last_seen_at'], self.after)

    def test_different_sid_with_same_score_creates_new_observation(self):
        data = self.data(self.entry('s1'), self.entry('s2'))
        track.apply_rankings(data, self.ranking(self.row('s1')), self.client, self.before)
        track.apply_rankings(data, self.ranking(self.row('s2')), self.client, self.after)
        self.assertEqual([o['submission_id'] for o in data['score_observations']], ['s1', 's2'])

    def test_known_team_cannot_silently_rebind_to_another_team(self):
        data = self.data(self.entry(), team=dict(team_object_id='trusted-team'))
        with self.assertRaisesRegex(RuntimeError, 'team identity'):
            track.apply_rankings(data, self.ranking(self.row(team='other-team')), self.client, self.before)
        self.assertEqual(data['team']['team_object_id'], 'trusted-team')

    def test_multiple_team_representatives_are_rejected(self):
        data = self.data(self.entry(), team=dict(team_object_id='team1'))
        with self.assertRaisesRegex(RuntimeError, 'Multiple representative'):
            track.apply_rankings(data, self.ranking(self.row(), self.row('s2', owner='u2')),
                                 self.client, self.before)

    def test_unrelated_leaderboard_row_cannot_establish_our_team(self):
        data = self.data(self.entry())
        track.apply_rankings(data, self.ranking(self.row('foreign', owner='u2')), self.client, self.before)
        self.assertIsNone(data['team_score'])
        self.assertNotIn('team', data)
        self.assertEqual(data['score_observations'], [])

    def test_teammates_representative_can_update_verified_team_only(self):
        data = self.data(self.entry(), team=dict(team_object_id='team1'))
        track.apply_rankings(data, self.ranking(self.row('teammate', owner='u2', score=55)), self.client, self.before)
        self.assertEqual(data['team_score'], 55)
        self.assertIsNone(data['submissions'][0]['current_score'])
        self.assertEqual(data['score_observations'][0]['submission_id'], 'teammate')

    def test_theory_score_is_not_a_kernel_score(self):
        entry = self.entry()
        track.present_entry(entry, dict(theory_score=0, files=[]), self.client)
        self.assertIsNone(entry['score'])
        self.assertIsNone(entry['score_kind'])

    def test_genuine_detail_zero_is_not_overwritten_by_first_observation(self):
        entry = self.entry()
        track.present_entry(entry, dict(score=0), self.client)
        data = self.data(entry)
        track.apply_rankings(data, self.ranking(self.row(score=12)), self.client, self.before)
        self.assertEqual(entry['score'], 0)
        self.assertEqual(entry['score_kind'], 'submission_detail')
        self.assertEqual(entry['current_score'], 12)

    def test_detail_score_note_does_not_claim_its_total_is_missing(self):
        entry = self.entry()
        track.present_entry(entry, dict(score=0), self.client)
        track.apply_rankings(self.data(entry), self.ranking(self.row()), self.client, self.before)
        self.assertNotIn('未保存总分', entry['score_note'])

    def test_null_legacy_first_observation_can_be_initialized(self):
        entry = self.entry(first_score_observation=None)
        track.apply_rankings(self.data(entry), self.ranking(self.row()), self.client, self.before)
        self.assertEqual(entry['first_score_observation']['score'], 32.5)

    def run_refresh(self, data, ranking=None, details=None, account='member1', fail_ranking=False):
        details = details or {}
        with tempfile.TemporaryDirectory(prefix='panel-score-test-', dir=STAGE) as temporary:
            base = Path(temporary)/'scoreboard'
            base.mkdir()
            (base.parent/'scoreboard-view').mkdir()
            writes = {}
            def save(path, value):
                writes[Path(path).relative_to(base.parent).as_posix()] = deepcopy(value)
            with contextlib.ExitStack() as stack:
                patches = dict(
                    client_for=mock.Mock(return_value=self.client),
                    live_metadata=mock.Mock(return_value=(dict(score_mode=1, ranking_submission_mode='latest'), {})),
                    user_submissions=mock.Mock(return_value=[dict(_id=sid) for sid in details]),
                    validate_result=mock.Mock(), record_result=mock.Mock(),
                    load_data=mock.Mock(return_value=data),
                    lock=lambda *a, **kw: contextlib.nullcontext(),
                    write_json=mock.Mock(side_effect=save),
                )
                for name, value in patches.items():
                    stack.enter_context(mock.patch.object(track.workflow, name, value))
                stack.enter_context(mock.patch.object(track.workflow.cfg, 'BASE', base))
                stack.enter_context(mock.patch.object(track, 'DATA_FILE', base/'data.sinkhorn_norm.json'))
                stack.enter_context(mock.patch.object(track, 'fetch_rankings',
                    side_effect=RuntimeError('offline') if fail_ranking else None,
                    return_value=ranking if ranking is not None else self.ranking()))
                self.client.get_submission = mock.Mock(side_effect=lambda sid:details[sid])
                result = track.refresh_data(account)
                self.client.session.post.assert_not_called()
                return result, writes, patches

    def test_refresh_account_with_zero_submissions_still_sets_last_account(self):
        data = self.data(last_account='member2')
        result, writes, patches = self.run_refresh(data)
        self.assertTrue(result)
        self.assertEqual(data['last_account'], 'member1')
        self.assertEqual(data['submissions'], [])
        patches['client_for'].assert_called_once_with('member1', cached_only=True)
        self.assertIn('scoreboard/data.sinkhorn_norm.json', writes)

    def test_refresh_falls_back_only_to_explicit_saved_account(self):
        data = self.data(last_account='member1')
        result, _, patches = self.run_refresh(data, account=None)
        self.assertTrue(result)
        patches['client_for'].assert_called_once_with('member1', cached_only=True)

    def test_refresh_without_account_does_not_authenticate(self):
        result, writes, patches = self.run_refresh(self.data(), account=None)
        self.assertFalse(result)
        patches['client_for'].assert_not_called()
        self.assertEqual(writes, {})

    def test_refresh_hidden_tbest_is_never_filled_from_detail_or_stale_numbers(self):
        entry = self.entry(cases=[dict(testcase_id='visible', status='Pass', best_time=99),
                                 dict(testcase_id='hidden', status='Hidden', best_time=777)])
        data = self.data(entry)
        ranking = self.ranking(self.row())
        ranking['testcases'] = [dict(_id='visible', tbest=2.14),
                                dict(_id='hidden', tbest=123, hidden=True)]
        _, writes, _ = self.run_refresh(data, ranking)
        self.assertEqual(data['global_best_times'], [2.14, None])
        self.assertEqual(len([key for key in writes if 'ranking_observations/' in key]), 1)
        self.assertEqual(data['scoring']['mode'], 'official_problem_ranking')
        self.assertIsNone(data['scoring']['theoretical_score'])

    def test_refresh_ranking_failure_removes_old_current_and_emits_warning(self):
        entry = self.entry(current_score=55, current_ranking=3)
        data = self.data(entry, team=dict(team_object_id='team1'), team_score=55, team_rank=3)
        _, writes, _ = self.run_refresh(data, fail_ranking=True)
        self.assertIsNone(data['team_score'])
        self.assertIsNone(entry['current_score'])
        self.assertIn('官方榜单暂不可用', data['panel_warnings'][0])
        self.assertFalse(any('ranking_observations/' in key for key in writes))

    def test_refresh_missing_detail_total_and_failed_ranking_keep_frozen_first_observation(self):
        entry = self.entry()
        data = self.data(entry)
        track.apply_rankings(data, self.ranking(self.row()), self.client, self.before)
        frozen = deepcopy(entry['first_score_observation'])
        self.run_refresh(data, details={'s1': dict(files=[], theory_score=0)}, fail_ranking=True)
        self.assertEqual(entry['first_score_observation'], frozen)
        self.assertEqual(entry['score'], 32.5)
        self.assertEqual(entry['score_kind'], 'first_observed')
        self.assertIn(self.before, entry['score_note'])
        self.assertIsNone(entry['current_score'])


if __name__ == '__main__':
    unittest.main()
