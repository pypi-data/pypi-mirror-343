import datetime
import boto3
import json
import time
from threading import Lock
from botocore.exceptions import ClientError

from cloudwatchpy.models import LogEntry
# from .compressor import compress_data_if_enabled  # Reserved for S3 or raw HTTP APIs

class CloudWatchClient:
    def __init__(self, log_group, region="us-east-1", compress=True):
        self.log_group = log_group
        self.log_stream = "log_stream"
        self.compress = compress
        self.client = boto3.client("logs", region_name=region)
        self.sequence_token = None
        self.lock = Lock()  # For thread-safe token updates

    def _ensure_log_group_stream(self):
        # Create log group if it doesn't exist
        try:
            self.client.create_log_group(logGroupName=self.log_group)
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                raise e

        # Create log stream if it doesn't exist
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group,
                logStreamName=self.log_stream
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceAlreadyExistsException":
                self._fetch_token()
            else:
                raise e

    def _fetch_token(self):
        # Retrieve the sequence token for the log stream
        response = self.client.describe_log_streams(
            logGroupName=self.log_group,
            logStreamNamePrefix=self.log_stream
        )
        streams = response.get("logStreams", [])
        if streams:
            self.sequence_token = streams[0].get("uploadSequenceToken")

    def send(self, log_entry: LogEntry):
        # Prepare message in expected format
        timestamp = int(time.time() * 1000)  # Current time in milliseconds
        self.log_stream = f"{datetime.datetime.now(datetime.timezone.utc).date()}-{log_entry.level}"
        
        # Ensure log group and stream exist
        self._ensure_log_group_stream()
        
        log_entry = log_entry.to_dict()
        message = json.dumps(log_entry)

        event = {
            "timestamp": timestamp,
            "message": message,
        }

        # Thread-safe block
        with self.lock:
            kwargs = {
                "logGroupName": self.log_group,
                "logStreamName": self.log_stream,
                "logEvents": [event],
            }
            if self.sequence_token:
                kwargs["sequenceToken"] = self.sequence_token

            try:
                response = self.client.put_log_events(**kwargs)
                self.sequence_token = response["nextSequenceToken"]
            except self.client.exceptions.InvalidSequenceTokenException:
                self._fetch_token()
                self.send(log_entry)  # Retry once
            except Exception as e:
                print(f"Error sending log to CloudWatch: {e}")
