from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from app.modules.user.domain.value_objects import Email, HashedPassword, PhoneNumber


class UserStatus(StrEnum):
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


@dataclass
class User:
    """Domain Entity: The user itself, containing state and behavior."""

    id: int | None = None
    uuid: str | None = None
    email: Email = field(default=None)  # type: ignore
    hashed_password: HashedPassword = field(default=None)  # type: ignore
    phone_number: PhoneNumber = field(default=None)  # type: ignore
    username: str = ""
    first_name: str | None = None
    last_name: str | None = None
    status: UserStatus = UserStatus.PENDING_VERIFICATION

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    def verify(self) -> None:
        """Business behavior: Transition state to active."""
        if self.status != UserStatus.PENDING_VERIFICATION:
            raise ValueError("User is already verified or inactive.")
        self.status = UserStatus.ACTIVE

    def deactivate(self) -> None:
        self.status = UserStatus.INACTIVE

    def suspend(self) -> None:
        self.status = UserStatus.SUSPENDED

    def soft_delete(self, deleted_at: datetime) -> None:
        self.status = UserStatus.INACTIVE
        self.deleted_at = deleted_at

    def restore(self) -> None:
        self.status = UserStatus.PENDING_VERIFICATION
        self.deleted_at = None
