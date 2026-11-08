#!/usr/bin/env python3
"""Loopback-only SinkhornNorm panel; platform refreshes are explicit GETs."""
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from pathlib import Path
import sys
import threading
import time
from urllib.parse import urlparse

from target import DATA_FILE, target_identity

BASE = Path(__file__).resolve().parent
REFRESH_MIN_INTERVAL = 10
_lock = threading.Lock()
_last_success_clock = None
_last_success_at = None
_last_success_account = None
_refreshing_account = None
_last_refresh = None


class DataError(RuntimeError):
    pass


def load_local_data():
    """Read only the isolated result store; never contact CANNJudge."""
    if not Path(DATA_FILE).exists():
        return dict(target=target_identity(), submissions=[], pending_submissions=[],
                    global_best_times=[], leaderboard_scores=[], team=None,
                    account_quotas={})
    try:
        data = json.loads(Path(DATA_FILE).read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise DataError('无法读取本地新题记录：' + str(error)) from error
    if not isinstance(data, dict) or data.get('target') != target_identity():
        raise DataError('本地记录的 problem_id、contest_id 或 problem_name 与 SinkhornNorm 不符')
    if not isinstance(data.get('submissions'), list):
        raise DataError('本地记录中的 submissions 必须为列表')
    account = data.get('last_account')
    if account is not None and not isinstance(account, str):
        raise DataError('本地记录中的 last_account 无效')
    return data


def panel_state(data):
    return dict(selected_account=data.get('last_account') or None,
                last_success_at=_last_success_at,
                last_success_account=_last_success_account,
                refresh_in_progress=_lock.locked(),
                refresh_account=_refreshing_account,
                last_refresh=_last_refresh,
                cache_exists=Path(DATA_FILE).is_file())


def refresh_result(status, message, account=None, **extra):
    return dict(status=status, message=message, account=account,
                last_success_at=_last_success_at,
                last_success_account=_last_success_account, **extra)


def do_refresh():
    """Refresh the selected cached account; return a body and HTTP status."""
    global _last_success_clock, _last_success_at, _last_success_account
    global _refreshing_account, _last_refresh
    data = load_local_data()
    account = data.get('last_account') or None
    if not account:
        return refresh_result('unselected', '尚未选择刷新账号；当前仅显示本地记录。'), 200
    if not _lock.acquire(blocking=False):
        return refresh_result('refreshing', '已有平台刷新正在进行；当前显示本地缓存。',
                              _refreshing_account or account), 202
    try:
        now = time.monotonic()
        if (_last_success_clock is not None and account == _last_success_account
                and now - _last_success_clock < REFRESH_MIN_INTERVAL):
            remaining = max(1, int(REFRESH_MIN_INTERVAL - (now - _last_success_clock) + 0.999))
            return refresh_result('cached', '距离上次成功刷新过近；使用本地缓存。',
                                  account, retry_after_seconds=remaining), 200
        _refreshing_account = account
        try:
            from track import refresh_data
            if not refresh_data(account):
                raise RuntimeError('刷新未完成')
        except Exception as error:
            _last_refresh = refresh_result('error', '平台刷新失败：' + str(error), account)
            return _last_refresh, 502
        _last_success_clock = time.monotonic()
        _last_success_at = datetime.now(timezone.utc).isoformat()
        _last_success_account = account
        _last_refresh = refresh_result('updated', '平台记录已更新。', account)
        return _last_refresh, 200
    finally:
        _refreshing_account = None
        _lock.release()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/refresh':
            try:
                body, status = do_refresh()
            except DataError as error:
                body, status = dict(status='error', message=str(error)), 409
            self._json(body, status)
            return
        if path == '/data.json':
            try:
                data = load_local_data()
                data['panel'] = panel_state(data)
            except DataError as error:
                self._json(dict(status='error', message=str(error)), 409)
                return
            self._json(data)
            return
        if path in ('/', '/index.html'):
            try:
                body = (BASE / 'index.html').read_bytes()
            except OSError:
                self._json(dict(status='error', message='面板页面不可用'), 500)
                return
            self._send(body, 'text/html; charset=utf-8')
            return
        if path == '/chart.umd.min.js':
            self._send((BASE/'chart.umd.min.js').read_bytes(), 'application/javascript; charset=utf-8')
            return
        report = re.fullmatch(r'/reports/([a-f0-9]{24})/(summary\.json|case\d{2}\.html)', path)
        if report:
            try:
                data = load_local_data()
                submission_id, name = report.groups()
                allowed = any(entry.get('id') == submission_id and
                              entry.get('problem_id') == target_identity()['problem_id']
                              for entry in data['submissions'])
                folder = BASE/'reports'/submission_id
                source = folder/name
                if allowed and source.is_file() and source.resolve().is_relative_to(folder.resolve()):
                    self._send(source.read_bytes(), 'application/json; charset=utf-8'
                               if name.endswith('.json') else 'text/html; charset=utf-8')
                    return
            except DataError as error:
                self._json(dict(status='error', message=str(error)), 409)
                return
        if path == '/favicon.ico':
            self._send(b'', 'image/x-icon', 204)
            return
        # Only the routes above are public. No source, old data, or config files.
        self._json(dict(status='error', message='未找到此面板路径'), 404)

    def _json(self, body, status=200):
        self._send(json.dumps(body, ensure_ascii=False, allow_nan=False).encode('utf-8'),
                   'application/json; charset=utf-8', status)

    def _send(self, body, content_type, status=200):
        try:
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, fmt, *args):
        sys.stderr.write('[%s] %s\n' % (time.strftime('%H:%M:%S'), fmt % args))


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    print(f'Serving SinkhornNorm panel at http://127.0.0.1:{port}/', flush=True)
    print('GET /refresh updates the selected cached account; /data.json is local only.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
