import pytest

from app.core.pagination import PaginationParams
from app.modules.car.cqrs.command import CreateCarCommand
from app.modules.car.cqrs.query import ListCarsByOwnerQuery, ListCarsQuery
from app.modules.car.use_cases.create_car import CreateCarUseCase
from app.modules.car.use_cases.list_cars import ListCarsUseCase


@pytest.mark.asyncio
async def test_list_all_cars_empty(car_repo):
    use_case = ListCarsUseCase(car_repo=car_repo)
    query = ListCarsQuery(pagination=PaginationParams(offset=0, limit=10))

    result = await use_case.all_cars(query)

    assert result.page.items == []
    assert result.page.total == 0


@pytest.mark.asyncio
async def test_list_all_cars_paginated(car_repo):
    uc_create = CreateCarUseCase(car_repo=car_repo)
    for i in range(5):
        await uc_create.execute(
            CreateCarCommand(
                owner_id=1, make="Toyota", model=f"Model {i}", year=2023, color="Blue", license_plate=f"PLATE-{i}"
            )
        )

    use_case = ListCarsUseCase(car_repo=car_repo)
    query = ListCarsQuery(pagination=PaginationParams(offset=0, limit=2))

    result = await use_case.all_cars(query)

    assert len(result.page.items) == 2
    assert result.page.total == 5


@pytest.mark.asyncio
async def test_list_cars_by_owner_empty(car_repo):
    use_case = ListCarsUseCase(car_repo=car_repo)
    query = ListCarsByOwnerQuery(owner_id=1, pagination=PaginationParams(offset=0, limit=10))

    result = await use_case.by_owner(query)

    assert result.page.items == []
    assert result.page.total == 0


@pytest.mark.asyncio
async def test_list_cars_by_owner_with_cars(car_repo):
    uc_create = CreateCarUseCase(car_repo=car_repo)
    # Owner 1 has 3 cars
    for i in range(3):
        await uc_create.execute(
            CreateCarCommand(
                owner_id=1, make="Toyota", model=f"Model {i}", year=2023, color="Blue", license_plate=f"P1-{i}"
            )
        )
    # Owner 2 has 2 cars
    for i in range(2):
        await uc_create.execute(
            CreateCarCommand(
                owner_id=2, make="Honda", model=f"Model {i}", year=2022, color="Red", license_plate=f"P2-{i}"
            )
        )

    use_case = ListCarsUseCase(car_repo=car_repo)
    query = ListCarsByOwnerQuery(owner_id=1, pagination=PaginationParams(offset=0, limit=10))

    result = await use_case.by_owner(query)

    assert len(result.page.items) == 3
    assert result.page.total == 3
    for car in result.page.items:
        assert car.owner_id == 1


@pytest.mark.asyncio
async def test_list_cars_by_owner_paginated(car_repo):
    uc_create = CreateCarUseCase(car_repo=car_repo)
    for i in range(5):
        await uc_create.execute(
            CreateCarCommand(
                owner_id=1, make="Toyota", model=f"Model {i}", year=2023, color="Blue", license_plate=f"P1-{i}"
            )
        )

    use_case = ListCarsUseCase(car_repo=car_repo)
    query = ListCarsByOwnerQuery(owner_id=1, pagination=PaginationParams(offset=2, limit=2))

    result = await use_case.by_owner(query)

    assert len(result.page.items) == 2
    assert result.page.total == 5
    assert result.page.offset == 2
