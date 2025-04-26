import logging
import socket
import traceback
import requests
import threading
import time
import queue
import atexit
import json
import os

DEFAULT_BUFFER_CAPACITY = 1000
DEFAULT_FLUSH_INTERVAL = 1
DEFAULT_CHECK_INTERVAL = 0.1
DEFAULT_BATCH_SIZE = 50
DEFAULT_DROP_EXTRA_EVENTS = True
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 0.5

class LogViewHandler(logging.Handler):
    def __init__(self, source_token: str, host="",
                 buffer_capacity=DEFAULT_BUFFER_CAPACITY,
                 flush_interval=DEFAULT_FLUSH_INTERVAL,
                 check_interval=DEFAULT_CHECK_INTERVAL,
                 batch_size=DEFAULT_BATCH_SIZE,
                 drop_extra_events=DEFAULT_DROP_EXTRA_EVENTS,
                 fallback_file=None,
                 level=logging.NOTSET):
        super().__init__(level)
        self.source_token = source_token
        self.host = host.rstrip("/")
        self.batch_size = batch_size
        self.pipe = queue.Queue(maxsize=buffer_capacity)
        self.flush_interval = flush_interval
        self.check_interval = check_interval
        self.drop_extra_events = drop_extra_events
        self.formatter = logging.Formatter("%(asctime)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.fallback_file = fallback_file
        self.dropcount = 0
        self.session = requests.Session()
        self.stop_event = threading.Event()

        # Flush thread management
        self.flush_thread = None
        self.flush_thread_started = False
        self.flush_thread_lock = threading.Lock()

        atexit.register(self.close)

    def ensure_flush_thread_alive(self):
        if not self.flush_thread_started:
            with self.flush_thread_lock:
                if not self.flush_thread_started:
                    self.flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
                    self.flush_thread.start()
                    self.flush_thread_started = True

    def emit(self, record):
        try:
            self.ensure_flush_thread_alive()

            log_data = {
                "time": self.formatter.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "hostname": socket.gethostname(),
                "source_token": self.source_token,
                "pathname": record.pathname,
                "filename": record.filename,
                "func_name": record.funcName,
                "lineno": record.lineno,
                "thread": record.threadName,
                "process": record.processName,
                "module": record.module,
                "created": record.created,
                "exception": ""
            }

            if record.exc_info:
                log_data["exception"] = ''.join(traceback.format_exception(*record.exc_info))

            self.pipe.put(log_data, block=not self.drop_extra_events)

            if self.pipe.qsize() >= self.batch_size:
                self._flush()

        except queue.Full:
            self.dropcount += 1
        except Exception as e:
            if self.fallback_file:
                self._write_fallback({"error": str(e)})
            else:
                raise e

    def _flush_loop(self):
        last_flush = time.monotonic()

        while not self.stop_event.is_set():
            now = time.monotonic()
            if now - last_flush >= self.flush_interval:
                self._flush()
                last_flush = now
            time.sleep(self.check_interval)

    def _flush(self):
        logs = []
        while not self.pipe.empty() and len(logs) < self.batch_size:
            try:
                logs.append(self.pipe.get_nowait())
            except queue.Empty:
                break

        if logs:
            self._send_with_retries(logs)

    def _send_with_retries(self, logs):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                headers = {
                    "Authorization": f"Bearer {self.source_token}"
                }
                res = self.session.post(f"{self.host}/api/logs/ingest", json=logs, timeout=3, headers=headers)

                if res.ok:
                    return
                else:
                    raise Exception(f"Response {res.status_code}: {res.text}")
            except Exception as e:
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_BACKOFF_BASE * (2 ** (attempt - 1)))
                else:
                    if self.fallback_file:
                        self._write_fallback(logs)

    def _write_fallback(self, logs):
        try:
            os.makedirs(os.path.dirname(self.fallback_file), exist_ok=True)
            with open(self.fallback_file, "a", encoding="utf-8") as f:
                if isinstance(logs, list):
                    for entry in logs:
                        f.write(json.dumps(entry) + "\n")
                else:
                    f.write(json.dumps(logs) + "\n")
        except Exception as e:
            raise e

    def close(self):
        if self.flush_thread_started and not self.stop_event.is_set():
            self.stop_event.set()
            self.flush_thread.join(timeout=2)
            self._flush()
        super().close()
