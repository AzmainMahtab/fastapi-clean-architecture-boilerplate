from fastapi import HTTPException


class AppException(HTTPException):
    """HTTP-aware exception with a machine-readable error code.

    Raised by route handlers when a domain exception occurs
    (e.g. user not found, duplicate email). The ``code`` is
    used by ``app_exception_handler`` to build a structured
    ``ErrorEnvelope`` response.

    Attributes:
        code: Machine-readable string like ``"USER_NOT_FOUND"``.
        status_code: HTTP status code.
        detail: Human-readable message.
    """

    def __init__(self, code: str, status_code: int, detail: str = ""):
        self.code = code
        super().__init__(status_code=status_code, detail=detail)
