from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.pagination import PaginatedResponse


class CreatePermissionRequest(BaseModel):
    name: str = Field(description="Permission name in resource:action format (e.g. user:create).", max_length=100)
    description: str | None = Field(default=None, description="Optional description of the permission.")
    resource: str = Field(description="Resource this permission applies to (e.g. user).", max_length=50)
    action: str = Field(description="Action on the resource (e.g. create, read, update, delete).", max_length=50)


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str = Field(description="Permission UUID.")
    name: str = Field(description="Permission name (resource:action).")
    description: str | None = Field(default=None, description="Permission description.")
    resource: str = Field(description="Target resource.")
    action: str = Field(description="Allowed action.")
    created_at: datetime | None = Field(default=None, description="Timestamp of creation.")
    updated_at: datetime | None = Field(default=None, description="Timestamp of last update.")

    @classmethod
    def from_entity(cls, permission) -> PermissionResponse:
        return cls(
            uuid=permission.uuid or "",
            name=permission.name,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            created_at=permission.created_at,
            updated_at=permission.updated_at,
        )


class CreateRoleRequest(BaseModel):
    name: str = Field(description="Unique role name (e.g. admin, manager, user).", max_length=50)
    description: str | None = Field(default=None, description="Optional description of the role.")


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: str = Field(description="Role UUID.")
    name: str = Field(description="Role name.")
    description: str | None = Field(default=None, description="Role description.")
    permissions: list[PermissionResponse] = Field(default_factory=list, description="Permissions assigned to this role.")
    created_at: datetime | None = Field(default=None, description="Timestamp of creation.")
    updated_at: datetime | None = Field(default=None, description="Timestamp of last update.")

    @classmethod
    def from_entity(cls, role) -> RoleResponse:
        return cls(
            uuid=role.uuid or "",
            name=role.name,
            description=role.description,
            permissions=[PermissionResponse.from_entity(p) for p in role.permissions],
            created_at=role.created_at,
            updated_at=role.updated_at,
        )


class AssignRoleRequest(BaseModel):
    user_id: int = Field(description="ID of the user to assign the role to.")


class RevokeRoleRequest(BaseModel):
    user_id: int = Field(description="ID of the user to revoke the role from.")


class AssignPermissionRequest(BaseModel):
    permission_uuid: str = Field(description="UUID of the permission to assign.")


class RevokePermissionRequest(BaseModel):
    permission_uuid: str = Field(description="UUID of the permission to revoke.")


class UserPermissionsResponse(BaseModel):
    user_id: int = Field(description="User ID.")
    permissions: list[str] = Field(default_factory=list, description="List of permission names.")


class UserRolesResponse(BaseModel):
    user_id: int = Field(description="User ID.")
    roles: list[str] = Field(default_factory=list, description="List of role names.")


PermissionListResponse = PaginatedResponse[PermissionResponse]
RoleListResponse = PaginatedResponse[RoleResponse]
