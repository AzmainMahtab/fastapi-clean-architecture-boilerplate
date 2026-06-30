from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PermissionCreatedEvent:
    permission_uuid: str
    name: str
    created_at: datetime


@dataclass(frozen=True)
class RoleCreatedEvent:
    role_uuid: str
    name: str
    created_at: datetime


@dataclass(frozen=True)
class RoleAssignedEvent:
    user_id: int
    role_uuid: str
    assigned_at: datetime


@dataclass(frozen=True)
class RoleRevokedEvent:
    user_id: int
    role_uuid: str
    revoked_at: datetime


@dataclass(frozen=True)
class PermissionAssignedToRoleEvent:
    role_uuid: str
    permission_uuid: str
    assigned_at: datetime


@dataclass(frozen=True)
class PermissionRevokedFromRoleEvent:
    role_uuid: str
    permission_uuid: str
    revoked_at: datetime
