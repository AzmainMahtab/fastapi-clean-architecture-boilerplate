from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.rbac.domain.interfaces import IRbacRepository
from app.modules.rbac.infrastructure.persistence.repository import SQLAlchemyRbacRepository
from app.modules.rbac.use_cases.assign_permission import AssignPermissionToRoleUseCase
from app.modules.rbac.use_cases.assign_role import AssignRoleUseCase
from app.modules.rbac.use_cases.check_permission import CheckPermissionUseCase
from app.modules.rbac.use_cases.create_permission import CreatePermissionUseCase
from app.modules.rbac.use_cases.create_role import CreateRoleUseCase
from app.modules.rbac.use_cases.get_role import GetRoleUseCase
from app.modules.rbac.use_cases.get_user_permissions import GetUserPermissionsUseCase
from app.modules.rbac.use_cases.get_user_roles import GetUserRolesUseCase
from app.modules.rbac.use_cases.list_permissions import ListPermissionsUseCase
from app.modules.rbac.use_cases.list_roles import ListRolesUseCase
from app.modules.rbac.use_cases.revoke_permission import RevokePermissionFromRoleUseCase
from app.modules.rbac.use_cases.revoke_role import RevokeRoleUseCase


async def get_rbac_repo(db: AsyncSession = Depends(get_db)) -> IRbacRepository:
    return SQLAlchemyRbacRepository(db)


async def get_create_permission_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> CreatePermissionUseCase:
    return CreatePermissionUseCase(rbac_repo=repo)


async def get_create_role_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> CreateRoleUseCase:
    return CreateRoleUseCase(rbac_repo=repo)


async def get_list_permissions_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> ListPermissionsUseCase:
    return ListPermissionsUseCase(rbac_repo=repo)


async def get_list_roles_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> ListRolesUseCase:
    return ListRolesUseCase(rbac_repo=repo)


async def get_assign_permission_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> AssignPermissionToRoleUseCase:
    return AssignPermissionToRoleUseCase(rbac_repo=repo)


async def get_revoke_permission_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> RevokePermissionFromRoleUseCase:
    return RevokePermissionFromRoleUseCase(rbac_repo=repo)


async def get_assign_role_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> AssignRoleUseCase:
    return AssignRoleUseCase(rbac_repo=repo)


async def get_revoke_role_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> RevokeRoleUseCase:
    return RevokeRoleUseCase(rbac_repo=repo)


async def get_get_role_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> GetRoleUseCase:
    return GetRoleUseCase(rbac_repo=repo)


async def get_get_user_permissions_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> GetUserPermissionsUseCase:
    return GetUserPermissionsUseCase(rbac_repo=repo)


async def get_get_user_roles_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> GetUserRolesUseCase:
    return GetUserRolesUseCase(rbac_repo=repo)


async def get_check_permission_use_case(repo: IRbacRepository = Depends(get_rbac_repo)) -> CheckPermissionUseCase:
    return CheckPermissionUseCase(rbac_repo=repo)
