import logging
import traceback

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.exception import ApplicationError

_logger = logging.getLogger(f"custom.{__name__}")


class HttpRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response | JSONResponse:
        try:
            response: Response = await call_next(request)
        except ApplicationError as exc:
            _logger.info(traceback.format_exc())
            response = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": f"{type(exc)}"},
            )
        except Exception:
            _logger.error(traceback.format_exc())
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "internal server error"},
            )
        return response
