from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    return JSONResponse(status_code=status_code, content={"status": status_code, "message": exc.detail})


async def value_error_handler(request: Request, exc: ValueError):
    status_code = HTTPStatus.BAD_REQUEST
    return JSONResponse(status_code=status_code, content={"status": status_code, "message": str(exc)})


async def exception_handler(request: Request, exc: Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content={"status": status_code, "message": str(exc)})
