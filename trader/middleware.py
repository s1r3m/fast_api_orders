import asyncio
import random
from http import HTTPStatus
from typing import Callable

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware


class ValidationErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        # Substitute default 422 Validation error with 400.
        try:
            return await call_next(request)
        except (RequestValidationError, ValidationError) as exc:
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content={"details": "Invalid input", "errors": exc.errors()},
            )


class DelayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        # Add a random delay between 0.1 and 1 seconds.
        await asyncio.sleep(random.uniform(0.1, 1))
        response = await call_next(request)
        return response
