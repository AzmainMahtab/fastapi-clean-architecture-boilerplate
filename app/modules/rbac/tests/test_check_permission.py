import pytest

from app.modules.rbac.cqrs.query import CheckUserPermissionQuery
from app.modules.rbac.use_cases.check_permission import CheckPermissionUseCase


@pytest.mark.asyncio
async def test_user_has_permission_false(rbac_repo):
    use_case = CheckPermissionUseCase(rbac_repo=rbac_repo)
    query = CheckUserPermissionQuery(user_id=1, permission_name="user:create")

    result = await use_case.execute(query)

    assert result.has_permission is False


@pytest.mark.asyncio
async def test_user_has_permission_via_role(rbac_repo):
    from app.modules.rbac.cqrs.command import (
        AssignPermissionToRoleCommand,
        AssignRoleCommand,
        CreatePermissionCommand,
        CreateRoleCommand,
    )
    from app.modules.rbac.use_cases.assign_permission import AssignPermissionToRoleUseCase
    from app.modules.rbac.use_cases.assign_role import AssignRoleUseCase
    from app.modules.rbac.use_cases.create_permission import CreatePermissionUseCase
    from app.modules.rbac.use_cases.create_role import CreateRoleUseCase

    uc_role = CreateRoleUseCase(rbac_repo=rbac_repo)
    role_result = await uc_role.execute(CreateRoleCommand(name="admin"))

    uc_perm = CreatePermissionUseCase(rbac_repo=rbac_repo)
    perm_result = await uc_perm.execute(CreatePermissionCommand(name="user:create", resource="user", action="create"))

    uc_assign_perm = AssignPermissionToRoleUseCase(rbac_repo=rbac_repo)
    await uc_assign_perm.execute(
        AssignPermissionToRoleCommand(role_uuid=role_result.role.uuid, permission_uuid=perm_result.permission.uuid)
    )

    uc_assign_role = AssignRoleUseCase(rbac_repo=rbac_repo)
    await uc_assign_role.execute(AssignRoleCommand(user_id=1, role_uuid=role_result.role.uuid))

    use_case = CheckPermissionUseCase(rbac_repo=rbac_repo)
    query = CheckUserPermissionQuery(user_id=1, permission_name="user:create")
    result = await use_case.execute(query)

    assert result.has_permission is True
