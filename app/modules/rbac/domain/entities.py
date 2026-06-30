from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Permission:
    """Domain Entity: A granular permission representing an action on a resource.

    Format: ``resource:action`` (e.g. ``user:create``, ``car:delete``).
    """

    id: int | None = None
    uuid: str | None = None
    name: str = ""  # e.g. "user:create"
    description: str | None = None
    resource: str = ""  # e.g. "user"
    action: str = ""  # e.g. "create"

    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class Role:
    """Domain Entity: A named collection of permissions assigned to users."""

    id: int | None = None
    uuid: str | None = None
    name: str = ""  # e.g. "admin"
    description: str | None = None
    permissions: list[Permission] = field(default_factory=list)

    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class UserRoleAssignment:
    """Domain Entity: A role assigned to a user with audit metadata."""

    role: Role
    assigned_by: int | None = None
    assigned_at: datetime | None = None


@dataclass
class RolePermissionAssignment:
    """Domain Entity: A permission assigned to a role with audit metadata."""

    permission: Permission
    assigned_by: int | None = None
    assigned_at: datetime | None = None
