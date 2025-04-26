from cloudwatchpy.batcher import LogBatcher
from cloudwatchpy.models import LogEntry

class DummyClient:
    def __init__(self):
        self.sent = []

    def send(self, entry):
        self.sent.append(entry)

def test_batcher_flush():
    dummy_client = DummyClient()
    batcher = LogBatcher(dummy_client, batch_size=2)

    batcher.add_log(LogEntry("INFO", "Log 1"))
    assert len(dummy_client.sent) == 0  # not yet flushed

    batcher.add_log(LogEntry("INFO", "Log 2"))
    assert len(dummy_client.sent) == 2  # flushed after reaching batch size

    batcher.add_log(LogEntry("INFO", "Log 3"))
    batcher.flush()
    assert len(dummy_client.sent) == 3  # manual flush
