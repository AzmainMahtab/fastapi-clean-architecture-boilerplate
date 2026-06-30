from app.modules.rbac.domain.entities import Permission, Role
from app.modules.rbac.infrastructure.persistence.models import PermissionModel, RoleModel


def map_permission_to_domain(orm: PermissionModel) -> Permission:
    return Permission(
        id=orm.id,
        uuid=str(orm.uuid) if orm.uuid else None,
        name=orm.name,
        description=orm.description,
        resource=orm.resource,
        action=orm.action,
        created_at=orm.created_at,
        updated_at=orm.updated_at,
    )


def map_permission_to_persistence(entity: Permission) -> PermissionModel:
    return PermissionModel(
        id=entity.id,
        uuid=entity.uuid,
        name=entity.name,
        description=entity.description,
        resource=entity.resource,
        action=entity.action,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def map_role_to_domain(orm: RoleModel, include_permissions: bool = True) -> Role:
    permissions = []
    if include_permissions and orm.permissions:
        permissions = [map_permission_to_domain(p) for p in orm.permissions]
    return Role(
        id=orm.id,
        uuid=str(orm.uuid) if orm.uuid else None,
        name=orm.name,
        description=orm.description,
        permissions=permissions,
        created_at=orm.created_at,
        updated_at=orm.updated_at,
    )


def map_role_to_persistence(entity: Role) -> RoleModel:
    return RoleModel(
        id=entity.id,
        uuid=entity.uuid,
        name=entity.name,
        description=entity.description,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
