class AuthenticationError(Exception):
    """Base exception for all authentication failures.

    All auth exceptions inherit from this class so callers can catch
    them broadly when needed.
    """


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided email/password combination is incorrect."""


class TokenExpiredError(AuthenticationError):
    """Raised when a JWT token has exceeded its expiration time."""


class TokenBlacklistedError(AuthenticationError):
    """Raised when a refresh token has been revoked (via logout or rotation)."""


class InvalidTokenError(AuthenticationError):
    """Raised when a token is malformed, signed with the wrong key, or of the wrong type."""


class AccountSuspendedError(AuthenticationError):
    """Raised when the user's account status is ``SUSPENDED`` and login is denied."""


class UserNotFoundError(AuthenticationError):
    """Raised when a user referenced in a token no longer exists."""


class AccountInactiveError(AuthenticationError):
    """Raised when the user's account status is ``INACTIVE`` and access is denied."""


class AccountAlreadyActiveError(AuthenticationError):
    """Raised when attempting to activate an account that is already active."""


# Map domain exceptions to machine-readable codes and HTTP statuses.
# Single source of truth — imported by both router and exception handlers.
AUTH_EXCEPTIONS: dict[type[AuthenticationError], tuple[str, int]] = {
    InvalidCredentialsError: ("INVALID_CREDENTIALS", 401),
    AccountSuspendedError: ("ACCOUNT_SUSPENDED", 403),
    AccountInactiveError: ("ACCOUNT_INACTIVE", 403),
    TokenExpiredError: ("TOKEN_EXPIRED", 401),
    TokenBlacklistedError: ("TOKEN_BLACKLISTED", 401),
    InvalidTokenError: ("INVALID_TOKEN", 401),
    UserNotFoundError: ("USER_NOT_FOUND", 404),
    AccountAlreadyActiveError: ("ACCOUNT_ALREADY_ACTIVE", 409),
}
