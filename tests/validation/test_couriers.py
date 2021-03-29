import pytest

from app.db.models.couriers import CourierFull
from app.db.services.couriers import CouriersService


ok_couriers = [
    {
      "courier_id": 1,
      "courier_type": "foot",
      "regions": [1, 2],
      "working_hours": ["10:00-14:00", "20:00-22:00"]
    },
    {
      "courier_id": 2,
      "courier_type": "bike",
      "regions": [2, 3],
      "working_hours": ["09:00-18:00"]
    }
]

not_ok_couriers = [
    {
      "courier_id": 1,
      "regions": [1, 2],
      "working_hours": ["10:00-14:00", "20:00-22:00"]
    },
    {
      "courier_id": 2,
      "courier_type": "bike",
      "working_hours": ["09:00-18:00"]
    },
    {
      "courier_id": 3,
      "courier_type": "foot",
      "regions": [1, 2],
    },
    {
      "courier_id": 4,
      "courier_type": "bike",
      "regions": [],
      "working_hours": ["09:00-18:00"]
    },
    {
      "courier_id": 5,
      "courier_type": "foot",
      "regions": [1, 2],
      "working_hours": []
    },
    {
      "courier_id": 6,
      "courier_type": "bird",
      "regions": [2, 3],
      "working_hours": ["09:00-18:00"]
    },
    {
      "courier_type": "foot",
      "regions": [1, 2],
      "working_hours": ["10:00-14:00", "20:00-22:00"]
    }
]


@pytest.mark.asyncio
@pytest.mark.parametrize('dataset', ok_couriers)
async def test_successful_courier_validation(dataset: dict):
    courier_service = CouriersService()
    assert await courier_service.is_courier_valid(dataset) is True


@pytest.mark.asyncio
@pytest.mark.parametrize('dataset', not_ok_couriers)
async def test_unsuccessful_courier_validation(dataset: dict):
    courier_service = CouriersService()
    assert await courier_service.is_courier_valid(dataset) is False


@pytest.mark.asyncio
@pytest.mark.parametrize('dataset', not_ok_couriers)
async def test_courier_model_validation(dataset: dict):
    with pytest.raises(ValueError):
        CourierFull(**dataset)
