import pytest
import pytest_asyncio

from app.modules.rbac.cqrs.command import AssignRoleCommand, CreateRoleCommand
from app.modules.rbac.domain.exception import RoleAlreadyAssignedError, RoleNotFoundError
from app.modules.rbac.use_cases.assign_role import AssignRoleUseCase
from app.modules.rbac.use_cases.create_role import CreateRoleUseCase


@pytest_asyncio.fixture
async def existing_role(rbac_repo):
    uc = CreateRoleUseCase(rbac_repo=rbac_repo)
    result = await uc.execute(CreateRoleCommand(name="admin"))
    return result.role


@pytest.mark.asyncio
async def test_assign_role_to_user_success(existing_role, rbac_repo):
    role = existing_role
    use_case = AssignRoleUseCase(rbac_repo=rbac_repo)
    command = AssignRoleCommand(user_id=1, role_uuid=role.uuid)

    await use_case.execute(command)

    has_role = await rbac_repo.user_has_role(1, "admin")
    assert has_role is True


@pytest.mark.asyncio
async def test_assign_role_not_found(rbac_repo):
    use_case = AssignRoleUseCase(rbac_repo=rbac_repo)
    command = AssignRoleCommand(user_id=1, role_uuid="nonexistent")

    with pytest.raises(RoleNotFoundError):
        await use_case.execute(command)


@pytest.mark.asyncio
async def test_assign_role_already_assigned(existing_role, rbac_repo):
    role = existing_role
    use_case = AssignRoleUseCase(rbac_repo=rbac_repo)
    command = AssignRoleCommand(user_id=1, role_uuid=role.uuid)
    await use_case.execute(command)

    with pytest.raises(RoleAlreadyAssignedError):
        await use_case.execute(command)
