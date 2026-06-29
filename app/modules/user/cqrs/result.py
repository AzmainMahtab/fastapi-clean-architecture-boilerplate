from dataclasses import dataclass

from app.core.pagination import Page
from app.modules.user.domain.entities import User


@dataclass(frozen=True)
class RegisterUserResult:
    user: User


@dataclass(frozen=True)
class UserActionResult:
    user: User


@dataclass(frozen=True)
class ListUsersResult:
    page: Page[User]
