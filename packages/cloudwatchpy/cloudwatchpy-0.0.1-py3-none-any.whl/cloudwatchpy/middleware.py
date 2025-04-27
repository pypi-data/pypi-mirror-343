import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .logger import PyCloudLogger

class CloudWatchMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, logger_name: str = "pycloudwatch"):
        super().__init__(app)
        self.logger = PyCloudLogger(logger_name)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        end_time = time.time()

        duration = round((end_time - start_time) * 1000, 2)

        log_data = {
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query),
            "client": request.client.host if request.client else None,
            "status_code": response.status_code,
            "duration_ms": duration,
        }

        self.logger.info("HTTP Request", context=log_data)
        return response
