import pytest

from app.modules.rbac.cqrs.command import CreateRoleCommand
from app.modules.rbac.domain.exception import RoleAlreadyExistsError
from app.modules.rbac.use_cases.create_role import CreateRoleUseCase


@pytest.mark.asyncio
async def test_create_role_success(rbac_repo):
    use_case = CreateRoleUseCase(rbac_repo=rbac_repo)
    command = CreateRoleCommand(name="admin", description="Administrator role")

    result = await use_case.execute(command)

    assert result.role.id is not None
    assert result.role.uuid is not None
    assert result.role.name == "admin"
    assert result.role.description == "Administrator role"


@pytest.mark.asyncio
async def test_create_role_duplicate_raises_error(rbac_repo):
    use_case = CreateRoleUseCase(rbac_repo=rbac_repo)
    command = CreateRoleCommand(name="admin")
    await use_case.execute(command)

    with pytest.raises(RoleAlreadyExistsError):
        await use_case.execute(command)
