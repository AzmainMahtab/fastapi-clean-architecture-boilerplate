from dataclasses import dataclass

from app.core.pagination import Page
from app.modules.rbac.domain.entities import Permission, Role


@dataclass(frozen=True)
class PermissionActionResult:
    permission: Permission


@dataclass(frozen=True)
class RoleActionResult:
    role: Role


@dataclass(frozen=True)
class ListPermissionsResult:
    page: Page[Permission]


@dataclass(frozen=True)
class ListRolesResult:
    page: Page[Role]


@dataclass(frozen=True)
class UserPermissionsResult:
    permissions: list[Permission]


@dataclass(frozen=True)
class UserRolesResult:
    roles: list[Role]


@dataclass(frozen=True)
class CheckPermissionResult:
    has_permission: bool
