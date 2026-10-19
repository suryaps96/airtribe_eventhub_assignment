import logging
import time

logger = logging.getLogger(__name__)
print("Logger level:", logger.getEffectiveLevel())
print("INFO enabled:", logger.isEnabledFor(logging.INFO))

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path}")
        start_time = time.perf_counter()
        response = self.get_response(request)
        duration = time.perf_counter() - start_time
        logger.info(f"Duration: {duration:.6f} seconds")
        logger.info(f"Response: {response.status_code}")
        return response
