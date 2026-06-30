import pytest

from app.modules.car.cqrs.command import CreateCarCommand
from app.modules.car.use_cases.create_car import CreateCarUseCase


@pytest.mark.asyncio
async def test_create_car_success(car_repo):
    use_case = CreateCarUseCase(car_repo=car_repo)
    command = CreateCarCommand(owner_id=1, make="Toyota", model="Camry", year=2023, color="Blue", license_plate="ABC-123")

    result = await use_case.execute(command)

    assert result.car.id is not None
    assert result.car.uuid is not None
    assert result.car.owner_id == 1
    assert result.car.make == "Toyota"
    assert result.car.model == "Camry"
    assert result.car.year == 2023
    assert result.car.color == "Blue"
    assert result.car.license_plate == "ABC-123"
