from cloudwatchpy.logger import PyCloudLogger
import os

class MockCloudWatchClient:
    def __init__(self, *args, **kwargs):
        self.logs = []

    def send(self, log_entry: dict):
        self.logs.append(log_entry)

def test_cloudwatch_logger(monkeypatch):
    # Simulate AWS config
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "dummy")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "dummy")
    monkeypatch.setenv("CLOUDWATCH_LOG_GROUP", "test-group")
    monkeypatch.setenv("CLOUDWATCH_LOG_STREAM", "test-stream")

    # Patch the CloudWatchClient in the logger module
    monkeypatch.setattr("pycloudwatch.logger.CloudWatchClient", MockCloudWatchClient)

    logger = PyCloudLogger("test_cloud_logger")

    assert logger.use_cloudwatch is True
    logger.info("Test log", context={"key": "value"})

    # Verify the mock received the log
    mock_client = logger.backend
    assert len(mock_client.logs) == 1
    assert mock_client.logs[0]["message"] == "Test log"
    assert mock_client.logs[0]["context"]["key"] == "value"
