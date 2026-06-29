from dataclasses import dataclass

from app.modules.user.domain.entities import User


@dataclass(frozen=True)
class LoginResult:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class RefreshTokenResult:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class LogoutResult:
    message: str = "Logged out successfully."


@dataclass(frozen=True)
class UserProfileResult:
    user: User


@dataclass(frozen=True)
class SendActivationOtpResult:
    message: str = "Activation OTP sent to your email."


@dataclass(frozen=True)
class ActivateAccountResult:
    message: str = "Account activated successfully."
