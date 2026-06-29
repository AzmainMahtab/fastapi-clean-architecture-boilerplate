from dataclasses import dataclass, field

from app.core.pagination import PaginationParams


@dataclass(frozen=True)
class GetUserByUuidQuery:
    uuid: str


@dataclass(frozen=True)
class GetUserByUsernameQuery:
    username: str


@dataclass(frozen=True)
class GetUserByEmailQuery:
    email: str


@dataclass(frozen=True)
class ListUsersQuery:
    status: str | None = None
    include_deleted: bool = False
    pagination: PaginationParams = field(default_factory=PaginationParams)
