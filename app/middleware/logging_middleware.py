# Logs all incomming requests and outgoing responces
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware # Base class


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # display - check method and endpoint
        logging.info(f"Request: {request.method} {request.url}")

        # Display time taken for response
        start_time = time.time()
        response = await call_next(request) # Hit the endpoint
        process_time = time.time() - start_time

        logging.info(
            f"Response: {response.status_code} | "
            f"Time: {process_time:.3f}s"
            )
        
        return response
