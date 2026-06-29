from dataclasses import dataclass
from datetime import datetime

from app.modules.otp.domain.value_objects import OtpType


@dataclass
class OneTimePassword:
    id: int | None = None
    uuid: str | None = None
    user_uuid: str = ""
    otp_type: OtpType = OtpType.LOGIN
    code_hash: str = ""
    is_used: bool = False
    expires_at: datetime | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return True
        from datetime import datetime as dt

        return dt.now(self.expires_at.tzinfo) > self.expires_at

    def mark_used(self) -> None:
        self.is_used = True
