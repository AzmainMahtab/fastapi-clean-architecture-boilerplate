class OtpError(Exception):
    """Base exception for OTP domain errors."""


class InvalidOtpError(OtpError):
    """Raised when the provided OTP code does not match the stored hash."""


class OtpExpiredError(OtpError):
    """Raised when the OTP has exceeded its validity window."""


class OtpAlreadyUsedError(OtpError):
    """Raised when the OTP has already been consumed."""
