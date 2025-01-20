import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Log request details
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Client: {request.client.host if request.client else 'Unknown'}")
        
        # Process the request and get response
        response = await call_next(request)
        
        # Log response status
        logger.info(f"Response Status: {response.status_code}")
        
        return response

class ResponseTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log if response time exceeds threshold (e.g., 1 second)
        if process_time > 1:
            logger.warning(
                f"Slow response detected: {request.method} {request.url} took {process_time:.2f} seconds"
            )
        
        return response 