from dataclasses import dataclass

from app.modules.otp.domain.value_objects import OtpType


@dataclass(frozen=True)
class GenerateOtpCommand:
    user_uuid: str
    otp_type: OtpType


@dataclass(frozen=True)
class ValidateOtpCommand:
    user_uuid: str
    otp_type: OtpType
    code: str
