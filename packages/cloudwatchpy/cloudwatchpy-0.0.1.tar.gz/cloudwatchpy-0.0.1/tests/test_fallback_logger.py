import os
from cloudwatchpy.logger import PyCloudLogger
from cloudwatchpy.fallback_logger import LOG_FILE

def test_fallback_logger(monkeypatch):
    # Ensure AWS config is missing to trigger fallback
    monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY", raising=False)
    monkeypatch.delenv("CLOUDWATCH_LOG_GROUP", raising=False)
    monkeypatch.delenv("CLOUDWATCH_LOG_STREAM", raising=False)

    # Remove old log file if it exists
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    # Create logger
    logger = PyCloudLogger("test_logger")

    # Should not be using CloudWatch
    assert logger.use_cloudwatch is False

    # Log something
    test_message = "Testing fallback logger"
    logger.info(test_message)

    # Ensure log file was created
    assert os.path.exists(LOG_FILE)

    # Read log content and check the message
    with open(LOG_FILE, "r") as f:
        content = f.read()
        assert test_message in content
        assert '"level": "INFO"' in content or "INFO" in content

    # Cleanup
    os.remove(LOG_FILE)
