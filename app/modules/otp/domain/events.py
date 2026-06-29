from dataclasses import dataclass

from app.modules.otp.domain.value_objects import OtpType


@dataclass(frozen=True)
class OtpGeneratedEvent:
    """Domain Event: Fired when an OTP has been generated for a user."""

    user_uuid: str
    otp_type: OtpType
    otp_uuid: str


@dataclass(frozen=True)
class OtpValidatedEvent:
    """Domain Event: Fired when an OTP has been successfully validated."""

    user_uuid: str
    otp_type: OtpType
    otp_uuid: str
