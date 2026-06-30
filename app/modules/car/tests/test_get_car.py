import pytest

from app.modules.car.cqrs.command import CreateCarCommand
from app.modules.car.cqrs.query import GetCarByUuidQuery
from app.modules.car.domain.exception import CarNotFoundError
from app.modules.car.use_cases.create_car import CreateCarUseCase
from app.modules.car.use_cases.get_car import GetCarUseCase


@pytest.fixture
def existing_car(car_repo):
    uc = CreateCarUseCase(car_repo=car_repo)
    cmd = CreateCarCommand(owner_id=1, make="Toyota", model="Camry", year=2023, color="Blue", license_plate="ABC-123")
    return uc.execute(cmd)


@pytest.mark.asyncio
async def test_get_car_by_uuid_success(existing_car, car_repo):
    result = await existing_car
    car = result.car
    use_case = GetCarUseCase(car_repo=car_repo)
    query = GetCarByUuidQuery(uuid=car.uuid)

    found = await use_case.by_uuid(query)

    assert found.id == car.id
    assert found.make == car.make


@pytest.mark.asyncio
async def test_get_car_by_uuid_not_found(car_repo):
    use_case = GetCarUseCase(car_repo=car_repo)
    query = GetCarByUuidQuery(uuid="nonexistent")

    with pytest.raises(CarNotFoundError):
        await use_case.by_uuid(query)
