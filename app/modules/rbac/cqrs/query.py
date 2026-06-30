from dataclasses import dataclass, field

from app.core.pagination import PaginationParams


@dataclass(frozen=True)
class GetPermissionByUuidQuery:
    uuid: str


@dataclass(frozen=True)
class GetPermissionByNameQuery:
    name: str


@dataclass(frozen=True)
class ListPermissionsQuery:
    pagination: PaginationParams = field(default_factory=PaginationParams)


@dataclass(frozen=True)
class GetRoleByUuidQuery:
    uuid: str


@dataclass(frozen=True)
class GetRoleByNameQuery:
    name: str


@dataclass(frozen=True)
class ListRolesQuery:
    pagination: PaginationParams = field(default_factory=PaginationParams)


@dataclass(frozen=True)
class GetUserPermissionsQuery:
    user_id: int


@dataclass(frozen=True)
class GetUserRolesQuery:
    user_id: int


@dataclass(frozen=True)
class CheckUserPermissionQuery:
    user_id: int
    permission_name: str
