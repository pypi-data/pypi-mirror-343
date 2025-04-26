from cloudwatchpy.config import Config

def test_config_defaults(monkeypatch):
    monkeypatch.setenv("LOG_COMPRESSION", "false")
    monkeypatch.setenv("LOG_BATCH_SIZE", "5")
    from cloudwatchpy.config import Config  # Re-import to avoid stale cache
    assert Config.ENABLE_COMPRESSION is False
    assert Config.LOG_BATCH_SIZE == 5
