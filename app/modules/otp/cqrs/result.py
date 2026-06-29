from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GenerateOtpResult:
    otp_uuid: str
    expires_at: datetime
    code: str = ""


@dataclass(frozen=True)
class ValidateOtpResult:
    success: bool = True
    otp_uuid: str = ""
