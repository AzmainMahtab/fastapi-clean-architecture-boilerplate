import pytest

from app.modules.rbac.cqrs.command import CreatePermissionCommand
from app.modules.rbac.domain.exception import PermissionAlreadyExistsError
from app.modules.rbac.use_cases.create_permission import CreatePermissionUseCase


@pytest.mark.asyncio
async def test_create_permission_success(rbac_repo):
    use_case = CreatePermissionUseCase(rbac_repo=rbac_repo)
    command = CreatePermissionCommand(name="user:create", resource="user", action="create")

    result = await use_case.execute(command)

    assert result.permission.id is not None
    assert result.permission.uuid is not None
    assert result.permission.name == "user:create"
    assert result.permission.resource == "user"
    assert result.permission.action == "create"


@pytest.mark.asyncio
async def test_create_permission_duplicate_raises_error(rbac_repo):
    use_case = CreatePermissionUseCase(rbac_repo=rbac_repo)
    command = CreatePermissionCommand(name="user:create", resource="user", action="create")
    await use_case.execute(command)

    with pytest.raises(PermissionAlreadyExistsError):
        await use_case.execute(command)
