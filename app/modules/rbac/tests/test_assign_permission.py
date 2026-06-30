import pytest
import pytest_asyncio

from app.modules.rbac.cqrs.command import AssignPermissionToRoleCommand, CreatePermissionCommand, CreateRoleCommand
from app.modules.rbac.domain.exception import PermissionNotFoundError, RoleNotFoundError
from app.modules.rbac.use_cases.assign_permission import AssignPermissionToRoleUseCase
from app.modules.rbac.use_cases.create_permission import CreatePermissionUseCase
from app.modules.rbac.use_cases.create_role import CreateRoleUseCase


@pytest_asyncio.fixture
async def role_and_permission(rbac_repo):
    uc_role = CreateRoleUseCase(rbac_repo=rbac_repo)
    role_result = await uc_role.execute(CreateRoleCommand(name="manager"))

    uc_perm = CreatePermissionUseCase(rbac_repo=rbac_repo)
    perm_result = await uc_perm.execute(CreatePermissionCommand(name="car:read", resource="car", action="read"))

    return role_result.role, perm_result.permission


@pytest.mark.asyncio
async def test_assign_permission_to_role_success(role_and_permission, rbac_repo):
    role, permission = role_and_permission
    use_case = AssignPermissionToRoleUseCase(rbac_repo=rbac_repo)
    command = AssignPermissionToRoleCommand(role_uuid=role.uuid, permission_uuid=permission.uuid)

    await use_case.execute(command)

    perms = await rbac_repo.get_role_permissions(role.id)
    assert len(perms) == 1
    assert perms[0].name == "car:read"


@pytest.mark.asyncio
async def test_assign_permission_role_not_found(rbac_repo):
    use_case = AssignPermissionToRoleUseCase(rbac_repo=rbac_repo)
    command = AssignPermissionToRoleCommand(role_uuid="nonexistent", permission_uuid="nonexistent")

    with pytest.raises(RoleNotFoundError):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_assign_permission_not_found(role_and_permission, rbac_repo):
    role, _ = role_and_permission
    use_case = AssignPermissionToRoleUseCase(rbac_repo=rbac_repo)
    command = AssignPermissionToRoleCommand(role_uuid=role.uuid, permission_uuid="nonexistent")

    with pytest.raises(PermissionNotFoundError):
        await use_case.execute(command)
