import threading
import time
from typing import Dict, List
from .client import CloudWatchClient
from .models import LogEntry

class LogBatcher:
    def __init__(self, cloudwatch_client: CloudWatchClient, batch_size: int = 10):
        self.client = cloudwatch_client
        self.batch_size = batch_size
        self.buffer: List[Dict] = []
        self.lock = threading.Lock()

    def add_log(self, log_entry: LogEntry):
        with self.lock:
            self.buffer.append(log_entry.to_dict())
            if len(self.buffer) >= self.batch_size:
                self._flush_locked()

    def flush(self):
        with self.lock:
            self._flush_locked()

    def _flush_locked(self):
        if not self.buffer:
            return
        for entry in self.buffer:
            self.client.send(entry)
        self.buffer.clear()
