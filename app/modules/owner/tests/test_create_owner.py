import pytest

from app.modules.owner.cqrs.command import CreateOwnerCommand
from app.modules.owner.domain.exception import OwnerAlreadyExistsError
from app.modules.owner.use_cases.create_owner import CreateOwnerUseCase


@pytest.mark.asyncio
async def test_create_owner_success(owner_repo):
    use_case = CreateOwnerUseCase(owner_repo=owner_repo)
    command = CreateOwnerCommand(user_id=1, address="123 Main St", date_of_birth=None)

    result = await use_case.execute(command)

    assert result.owner.id is not None
    assert result.owner.uuid is not None
    assert result.owner.user_id == 1
    assert result.owner.address == "123 Main St"


@pytest.mark.asyncio
async def test_create_owner_duplicate_user_id_raises_error(owner_repo):
    use_case = CreateOwnerUseCase(owner_repo=owner_repo)
    command = CreateOwnerCommand(user_id=1, address="123 Main St")
    await use_case.execute(command)

    with pytest.raises(OwnerAlreadyExistsError):
        command2 = CreateOwnerCommand(user_id=1, address="456 Oak Ave")
        await use_case.execute(command2)
