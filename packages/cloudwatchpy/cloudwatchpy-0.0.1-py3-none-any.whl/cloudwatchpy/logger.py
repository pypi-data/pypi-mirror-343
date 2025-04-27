from typing import Optional, Dict
from .config import Config
from .models import LogEntry
from .fallback_logger import get_fallback_logger

try:
    from .client import CloudWatchClient
except ImportError:
    CloudWatchClient = None  # fallback if client fails to import

class PyCloudLogger:
    def __init__(self, name: str):
        self.name = name

        if Config.is_cloudwatch_enabled() and CloudWatchClient:
            self.backend = CloudWatchClient(
                log_group=Config.LOG_GROUP,
                region=Config.AWS_REGION,
                compress=Config.ENABLE_COMPRESSION
            )
            self.use_cloudwatch = True
        else:
            print("CloudWatch client not available or CloudWatch is disabled. Using fallback logger.")
            print("Log group:", Config.LOG_GROUP, "Log stream:", Config.LOG_STREAM, "Region:", Config.AWS_REGION)
            self.backend = get_fallback_logger(name)
            self.use_cloudwatch = False

    def info(self, message: str, context: Optional[Dict] = None):
        self._log("INFO", message, context)

    def warning(self, message: str, context: Optional[Dict] = None):
        self._log("WARNING", message, context)

    def error(self, message: str, context: Optional[Dict] = None):
        self._log("ERROR", message, context)

    def debug(self, message: str, context: Optional[Dict] = None):
        self._log("DEBUG", message, context)

    def _log(self, level: str, message: str, context: Optional[Dict]):
        if self.use_cloudwatch:
            log_entry = LogEntry(level, message, context)
            self.backend.send(log_entry)
        else:
            log_func = getattr(self.backend, level.lower(), self.backend.info)
            log_func(message)
