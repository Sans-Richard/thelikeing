"""Real loopback HTTP checks; all platform access is replaced by a stub."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading
import types
import unittest
from unittest import mock
from urllib.error import HTTPError
from urllib.request import urlopen

PANEL = Path(__file__).resolve().parents[1]
TARGET = dict(problem_id='6adb28021dac5d235bd73b85',
              contest_id='6adac8363ff2fef7e89242fe', problem_name='sinkhorn_norm')


class PanelHTTPTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data_path = Path(self.temp.name) / 'data.sinkhorn_norm.json'
        target = types.ModuleType('target')
        target.DATA_FILE = self.data_path
        target.target_identity = lambda: TARGET.copy()
        self.track = types.ModuleType('track')
        self.track.refresh_data = mock.Mock(return_value=True)
        self.modules = mock.patch.dict(sys.modules, {'target': target, 'track': self.track})
        self.modules.start()
        self.addCleanup(self.modules.stop)
        spec = importlib.util.spec_from_file_location('panel_server_test', PANEL / 'server.py')
        self.server_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.server_module)
        self.server_module.Handler.log_message = lambda *args: None
        self.httpd = self.server_module.ThreadingHTTPServer(('127.0.0.1', 0), self.server_module.Handler)
        self.httpd.daemon_threads = True
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.url = 'http://127.0.0.1:' + str(self.httpd.server_port)

    def stop_server(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=3)

    def write_data(self, **extra):
        value = dict(target=TARGET.copy(), submissions=[], last_account='member2')
        value.update(extra)
        self.data_path.write_text(json.dumps(value), encoding='utf-8')
        return value

    def get(self, path):
        try:
            response = urlopen(self.url + path, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            raw = response.read()
            content_type = response.headers.get('Content-Type', '')
            value = json.loads(raw) if 'application/json' in content_type else raw
            return response.status, value, response.headers

    def test_index_and_favicon_work(self):
        for path in ('/', '/index.html'):
            status, body, headers = self.get(path)
            self.assertEqual(status, 200)
            self.assertIn('SinkhornNorm 提交追踪'.encode(), body)
            for anchor in (b'id="onlyPass"', b'id="scoreChart"', b'id="detail-table"', b'id="srcModal"'):
                self.assertIn(anchor, body)
            self.assertEqual(headers['Cache-Control'], 'no-store')
        self.assertEqual(self.get('/favicon.ico')[0], 204)
        self.track.refresh_data.assert_not_called()

    def test_original_chart_asset_is_served(self):
        asset = self.server_module.BASE/'chart.umd.min.js'
        self.assertTrue(asset.is_file())
        status, body, headers = self.get('/chart.umd.min.js')
        self.assertEqual(status, 200)
        self.assertEqual(body, asset.read_bytes())
        self.assertIn('javascript', headers['Content-Type'])

    def test_empty_local_data_is_valid_and_never_refreshes(self):
        status, body, _ = self.get('/data.json')
        self.assertEqual(status, 200)
        self.assertEqual(body['target'], TARGET)
        self.assertEqual(body['submissions'], [])
        self.assertIsNone(body['panel']['selected_account'])
        self.assertFalse(body['panel']['cache_exists'])
        status, body, _ = self.get('/refresh')
        self.assertEqual((status, body['status']), (200, 'unselected'))
        self.track.refresh_data.assert_not_called()
        self.assertFalse(self.data_path.exists())

    def test_local_data_does_not_trigger_platform_get(self):
        original = self.write_data()
        self.track.refresh_data.side_effect = AssertionError('must remain local')
        status, body, _ = self.get('/data.json')
        self.assertEqual(status, 200)
        self.assertEqual(body['submissions'], original['submissions'])
        self.assertEqual(body['panel']['selected_account'], 'member2')
        self.track.refresh_data.assert_not_called()

    def test_refresh_success_then_cached_preserves_success_metadata(self):
        self.write_data()
        status, body, _ = self.get('/refresh')
        self.assertEqual((status, body['status']), (200, 'updated'))
        self.assertEqual(body['account'], 'member2')
        self.assertIsNotNone(body['last_success_at'])
        last_success = body['last_success_at']
        self.track.refresh_data.assert_called_once_with('member2')
        status, body, _ = self.get('/refresh')
        self.assertEqual((status, body['status']), (200, 'cached'))
        self.assertGreaterEqual(body['retry_after_seconds'], 1)
        self.assertEqual(body['last_success_at'], last_success)
        self.assertEqual(self.track.refresh_data.call_count, 1)
        status, data, _ = self.get('/data.json')
        self.assertEqual(data['panel']['last_success_at'], last_success)
        self.assertFalse(data['panel']['refresh_in_progress'])

    def test_refresh_error_is_http_error_and_cache_remains_readable(self):
        original = self.write_data(submissions=[dict(id='cached', score=12)])
        self.track.refresh_data.side_effect = RuntimeError('session expired (stub)')
        status, body, _ = self.get('/refresh')
        self.assertEqual((status, body['status']), (502, 'error'))
        self.assertIn('session expired', body['message'])
        self.assertIsNone(body['last_success_at'])
        status, data, _ = self.get('/data.json')
        self.assertEqual(status, 200)
        self.assertEqual(data['submissions'], original['submissions'])
        self.assertEqual(data['panel']['last_refresh']['status'], 'error')
        self.assertFalse(data['panel']['refresh_in_progress'])
        self.assertEqual(self.track.refresh_data.call_count, 1)

    def test_refresh_false_is_not_reported_as_success(self):
        self.write_data()
        self.track.refresh_data.return_value = False
        status, body, _ = self.get('/refresh')
        self.assertEqual((status, body['status']), (502, 'error'))
        self.assertIsNone(body['last_success_at'])

    def test_busy_refresh_is_distinct_and_data_stays_local(self):
        self.write_data()
        entered, release = threading.Event(), threading.Event()
        def blocked_refresh(account):
            entered.set()
            if not release.wait(4):
                raise RuntimeError('test release timeout')
            return True
        self.track.refresh_data.side_effect = blocked_refresh
        results = []
        worker = threading.Thread(target=lambda: results.append(self.get('/refresh')), daemon=True)
        worker.start()
        try:
            self.assertTrue(entered.wait(2))
            status, body, _ = self.get('/refresh')
            self.assertEqual((status, body['status']), (202, 'refreshing'))
            self.assertEqual(body['account'], 'member2')
            status, data, _ = self.get('/data.json')
            self.assertEqual(status, 200)
            self.assertTrue(data['panel']['refresh_in_progress'])
            self.assertEqual(data['panel']['refresh_account'], 'member2')
            self.assertEqual(self.track.refresh_data.call_count, 1)
        finally:
            release.set()
            worker.join(timeout=4)
        self.assertFalse(worker.is_alive())
        self.assertEqual(results[0][1]['status'], 'updated')

    def test_all_three_target_fields_are_required_and_isolated(self):
        for field in TARGET:
            with self.subTest(field=field):
                wrong = TARGET.copy()
                wrong[field] = 'other'
                self.write_data(target=wrong)
                for path in ('/data.json', '/refresh'):
                    status, body, _ = self.get(path)
                    self.assertEqual((status, body['status']), (409, 'error'))
        self.track.refresh_data.assert_not_called()

    def test_bad_json_or_schema_is_explicit_http_error(self):
        for text in ('{bad', '[]', json.dumps(dict(target=TARGET, submissions={})),
                     json.dumps(dict(target=TARGET, submissions=[], last_account=7))):
            with self.subTest(text=text):
                self.data_path.write_text(text, encoding='utf-8')
                status, body, _ = self.get('/data.json')
                self.assertEqual((status, body['status']), (409, 'error'))
        self.track.refresh_data.assert_not_called()

    def test_static_paths_are_an_explicit_whitelist(self):
        for path in ('/server.py', '/target.py', '/data.sinkhorn_norm.json', '/data.json.bak',
                     '/.config.json', '/runs/source/kernel.asc', '/../index.html',
                     '/%2e%2e/.config.json', '/index.html/extra', '/old/data.json'):
            with self.subTest(path=path):
                status, body, _ = self.get(path)
                self.assertEqual((status, body['status']), (404, 'error'))
        self.track.refresh_data.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
