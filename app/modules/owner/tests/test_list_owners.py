import pytest

from app.core.pagination import PaginationParams
from app.modules.owner.cqrs.command import CreateOwnerCommand
from app.modules.owner.cqrs.query import ListOwnersQuery
from app.modules.owner.use_cases.create_owner import CreateOwnerUseCase
from app.modules.owner.use_cases.list_owners import ListOwnersUseCase


@pytest.mark.asyncio
async def test_list_owners_empty(owner_repo):
    use_case = ListOwnersUseCase(owner_repo=owner_repo)
    query = ListOwnersQuery(pagination=PaginationParams(offset=0, limit=10))

    result = await use_case.execute(query)

    assert result.page.items == []
    assert result.page.total == 0


@pytest.mark.asyncio
async def test_list_owners_paginated(owner_repo):
    uc_create = CreateOwnerUseCase(owner_repo=owner_repo)
    for i in range(5):
        await uc_create.execute(CreateOwnerCommand(user_id=i + 1, address=f"Address {i}"))

    use_case = ListOwnersUseCase(owner_repo=owner_repo)
    query = ListOwnersQuery(pagination=PaginationParams(offset=0, limit=2))

    result = await use_case.execute(query)

    assert len(result.page.items) == 2
    assert result.page.total == 5
    assert result.page.offset == 0
    assert result.page.limit == 2


@pytest.mark.asyncio
async def test_list_owners_offset(owner_repo):
    uc_create = CreateOwnerUseCase(owner_repo=owner_repo)
    for i in range(5):
        await uc_create.execute(CreateOwnerCommand(user_id=i + 1, address=f"Address {i}"))

    use_case = ListOwnersUseCase(owner_repo=owner_repo)
    query = ListOwnersQuery(pagination=PaginationParams(offset=3, limit=10))

    result = await use_case.execute(query)

    assert len(result.page.items) == 2
    assert result.page.total == 5
