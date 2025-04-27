class PyCloudWatchError(Exception):
    """Base exception for pycloudwatch errors."""
    pass


class AWSConfigurationError(PyCloudWatchError):
    """Raised when AWS credentials or configuration are missing or invalid."""
    def __init__(self, message="AWS configuration is incomplete or invalid"):
        super().__init__(message)


class LogStreamCreationError(PyCloudWatchError):
    """Raised when log stream could not be created."""
    def __init__(self, log_group: str, log_stream: str):
        message = f"Failed to create log stream: '{log_stream}' in group '{log_group}'"
        super().__init__(message)


class LogBatchingError(PyCloudWatchError):
    """Raised when batching fails due to incorrect size/format."""
    def __init__(self, reason: str):
        message = f"Log batching failed: {reason}"
        super().__init__(message)


class LogSendError(PyCloudWatchError):
    """Raised when sending logs to AWS fails unexpectedly."""
    def __init__(self, original_exception: Exception):
        message = f"Failed to send log to CloudWatch: {original_exception}"
        super().__init__(message)
