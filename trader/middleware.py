import asyncio
import random
from typing import Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class DelayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        await asyncio.sleep(random.uniform(0.1, 1))
        response = await call_next(request)
        return response
