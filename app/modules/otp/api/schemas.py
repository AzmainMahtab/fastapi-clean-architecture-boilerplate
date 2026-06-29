from pydantic import BaseModel, Field

from app.modules.otp.cqrs.command import ValidateOtpCommand
from app.modules.otp.domain.value_objects import OtpType


class ValidateOtpRequest(BaseModel):
    """Request body for the ``/auth/otp/validate`` endpoint.

    Attributes:
        user_uuid: The authenticated user's UUID.
        otp_type: The type of OTP being validated (e.g. ``login-otp``).
        code: The 6-digit OTP code provided by the user.
    """

    user_uuid: str = Field(description="The authenticated user's UUID.")
    otp_type: OtpType = Field(description="Type of OTP (login-otp, password-reset-otp, etc.).")
    code: str = Field(min_length=4, max_length=8, pattern=r"^\d{4,8}$", description="The numeric OTP code.")

    def to_command(self) -> ValidateOtpCommand:
        return ValidateOtpCommand(user_uuid=self.user_uuid, otp_type=self.otp_type, code=self.code)


class ValidateOtpResponse(BaseModel):
    """Response body returned after successful OTP validation.

    Attributes:
        success: Always ``true`` on successful validation.
    """

    success: bool = True
