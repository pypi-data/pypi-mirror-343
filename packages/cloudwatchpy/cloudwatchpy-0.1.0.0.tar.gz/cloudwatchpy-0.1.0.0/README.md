# 📡 pycloudwatch

Structured Python logger with AWS CloudWatch support and a fallback to local JSON logging.

---

## 🔥 Features

- ✅ Seamless AWS CloudWatch Logs integration (via `boto3`)
- ✅ Automatic fallback to `RotatingFileHandler` when CloudWatch config is missing
- ✅ ASGI middleware for FastAPI, Starlette, etc.
- ✅ Log batching with thread-safe flushes
- ✅ JSON-structured logs, optionally compressible
- ✅ Plug-and-play logger interface

---

## 🚀 Installation

```bash
pip install pycloudwatch
```

---

## 🛠 Environment Configuration

| Variable | Description |
|----------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | AWS region (default: `us-east-1`) |
| `CLOUDWATCH_LOG_GROUP` | Name of CloudWatch log group |
| `CLOUDWATCH_LOG_STREAM` | Name of CloudWatch log stream |
| `LOG_BATCH_SIZE` | Batch flush size (default: 10) |
| `LOG_COMPRESSION` | Enable GZIP compression (true/false) |

If any of these are missing, logs will fallback to local `logs/app.log`.

---

## 🧱 Basic Usage

```python
from pycloudwatch.logger import PyCloudLogger

logger = PyCloudLogger("my_app")

logger.info("Server started", context={"port": 8000})
logger.error("Failed to connect to DB", context={"error": "Timeout"})
```

---

## 🧩 ASGI Middleware (FastAPI Example)

```python
from fastapi import FastAPI
from pycloudwatch.middleware import CloudWatchMiddleware

app = FastAPI()
app.add_middleware(CloudWatchMiddleware)
```

---

## 📦 Batching Logs (Advanced)

```python
from pycloudwatch.batcher import LogBatcher
from pycloudwatch.models import LogEntry
from pycloudwatch.logger import PyCloudLogger

logger = PyCloudLogger("batcher-demo")
batcher = LogBatcher(logger.backend, batch_size=5)

for i in range(10):
    batcher.add_log(LogEntry("INFO", f"Batch Log {i+1}", {"iteration": i+1}))

batcher.flush()
```

---

## 🧪 Testing

To run tests:

```bash
pytest tests/
```

Mocks for AWS SDK via `moto` will be included in the test suite.

---

## 💡 Roadmap

- [ ] WSGI middleware support
- [ ] Automatic periodic flush using timer
- [ ] Integration with external S3/Kinesis log exporters
- [ ] OpenTelemetry context propagation

---

## 📜 License

MIT © 2025 [Irfan Ahmad](https://github.com/Irfan-Ahmad-byte)

---

## 🧠 Inspired by

- [`crypsol_logger`](https://github.com/crypsol/crypsol_logger) (Rust)
- `structlog`, `loguru`, and `logging.handlers` (Python logging ecosystem)
