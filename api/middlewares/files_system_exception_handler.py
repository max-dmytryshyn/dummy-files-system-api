from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from api.constants import FILES_SYSTEM_EXCEPTIONS_CODE_MAPPING
from files_system.exceptions import BaseFileSystemException


class FilesSystemExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except BaseFileSystemException as e:
            return JSONResponse(
                status_code=FILES_SYSTEM_EXCEPTIONS_CODE_MAPPING[type(e)],
                content={"detail": e.message}
            )
