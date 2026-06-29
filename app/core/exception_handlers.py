from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.response import ErrorEnvelope, ErrorItem
from app.modules.auth.domain.exception import AUTH_EXCEPTIONS, AuthenticationError


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handles ``AppException`` raised by route handlers.

    Maps the exception's ``code`` and ``detail`` into a structured
    ``ErrorEnvelope`` response so the frontend always gets a
    consistent error shape regardless of which domain exception fired.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorEnvelope(
            status="fail", statusCode=exc.status_code, errors=[ErrorItem(code=exc.code, message=exc.detail or None)]
        ).model_dump(exclude_none=True, mode="json"),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Fallback handler for vanilla FastAPI ``HTTPException``.

    These are raised by FastAPI internally (e.g. 405 method not allowed)
    or by third-party dependencies. Wraps them in the same
    ``ErrorEnvelope`` shape for consistency.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorEnvelope(
            status="fail", statusCode=exc.status_code, errors=[ErrorItem(code="HTTP_ERROR", message=exc.detail or None)]
        ).model_dump(exclude_none=True, mode="json"),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handles Pydantic ``RequestValidationError`` (422).

    Converts FastAPI's built-in validation error list into a list of
    ``ErrorItem`` objects with ``VALIDATION_ERROR`` code, the field
    path, and the validation message. This gives the frontend a
    consistent format to bind form-level errors to input fields.
    """
    errors = []
    for e in exc.errors():
        field = ".".join(str(p) for p in e.get("loc", [])[1:]) or None
        errors.append(ErrorItem(code="VALIDATION_ERROR", field=field, message=e.get("msg")))
    return JSONResponse(
        status_code=422,
        content=ErrorEnvelope(status="fail", statusCode=422, errors=errors).model_dump(exclude_none=True, mode="json"),
    )


async def auth_exception_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
    """Handles ``AuthenticationError`` raised outside route handlers.

    Uses the ``AUTH_EXCEPTIONS`` mapping from the auth domain module
    as the single source of truth for error codes and HTTP statuses.
    """
    code, status_code = AUTH_EXCEPTIONS.get(type(exc), ("AUTH_ERROR", 401))
    return JSONResponse(
        status_code=status_code,
        content=ErrorEnvelope(
            status="fail", statusCode=status_code, errors=[ErrorItem(code=code, message=str(exc) or None)]
        ).model_dump(exclude_none=True, mode="json"),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for any unhandled exception (500).

    Prevents stack traces from leaking to the client. Returns a generic
    ``INTERNAL_ERROR`` message in the standard ``ErrorEnvelope`` shape.
    The original exception is still logged by FastAPI's default middleware.
    """
    return JSONResponse(
        status_code=500,
        content=ErrorEnvelope(
            status="error",
            statusCode=500,
            errors=[ErrorItem(code="INTERNAL_ERROR", message="An unexpected error occurred.")],
        ).model_dump(exclude_none=True, mode="json"),
    )
