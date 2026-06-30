import pytest

from app.modules.owner.cqrs.command import CreateOwnerCommand
from app.modules.owner.cqrs.query import GetOwnerByUserIdQuery, GetOwnerByUuidQuery
from app.modules.owner.domain.exception import OwnerNotFoundError
from app.modules.owner.use_cases.create_owner import CreateOwnerUseCase
from app.modules.owner.use_cases.get_owner import GetOwnerUseCase


@pytest.fixture
def existing_owner(owner_repo):
    uc = CreateOwnerUseCase(owner_repo=owner_repo)
    cmd = CreateOwnerCommand(user_id=1, address="123 Main St")
    return uc.execute(cmd)


@pytest.mark.asyncio
async def test_get_owner_by_uuid_success(existing_owner, owner_repo):
    result = await existing_owner
    owner = result.owner
    use_case = GetOwnerUseCase(owner_repo=owner_repo)
    query = GetOwnerByUuidQuery(uuid=owner.uuid)

    found = await use_case.by_uuid(query)

    assert found.id == owner.id
    assert found.user_id == owner.user_id


@pytest.mark.asyncio
async def test_get_owner_by_uuid_not_found(owner_repo):
    use_case = GetOwnerUseCase(owner_repo=owner_repo)
    query = GetOwnerByUuidQuery(uuid="nonexistent")

    with pytest.raises(OwnerNotFoundError):
        await use_case.by_uuid(query)


@pytest.mark.asyncio
async def test_get_owner_by_user_id_success(existing_owner, owner_repo):
    result = await existing_owner
    owner = result.owner
    use_case = GetOwnerUseCase(owner_repo=owner_repo)
    query = GetOwnerByUserIdQuery(user_id=owner.user_id)

    found = await use_case.by_user_id(query)

    assert found.id == owner.id
    assert found.uuid == owner.uuid


@pytest.mark.asyncio
async def test_get_owner_by_user_id_not_found(owner_repo):
    use_case = GetOwnerUseCase(owner_repo=owner_repo)
    query = GetOwnerByUserIdQuery(user_id=999)

    with pytest.raises(OwnerNotFoundError):
        await use_case.by_user_id(query)
