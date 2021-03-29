import pytest

from app.db.models.orders import OrderFull
from app.db.services.orders import OrdersService

ok_orders = [
    {
        "order_id": 1,
        "weight": 0.23,
        "region_id": 12,
        "delivery_hours": ["09:00-18:00"]
    },
    {
        "order_id": 2,
        "weight": 25,
        "region_id": 2,
        "delivery_hours": ["00:00-01:00", "12:12-13:13"]
    }
]

not_ok_orders = [
    {
        "order_id": 1,
        "weight": 0.0001,
        "region_id": 12,
        "delivery_hours": ["09:00-18:00"]
    },
    {
        "order_id": 2,
        "weight": 25,
        "region_id": 2,
    },
    {
        "order_id": 3,
        "weight": 12,
        "delivery_hours": ["09:00-18:00"]
    },
    {
        "order_id": 4,
        "region_id": 12,
        "delivery_hours": ["09:00-18:00"]
    },
    {
        "weight": 3,
        "region_id": 12,
        "delivery_hours": ["09:00-18:00"]
    },
    {
        "order_id": 5,
        "weight": 51,
        "region_id": 12,
        "delivery_hours": ["09:00-18:00"]
    },
]


@pytest.mark.asyncio
@pytest.mark.parametrize('dataset', ok_orders)
async def test_successful_order_validation(dataset: dict):
    orders_service = OrdersService()
    assert await orders_service.is_order_valid(dataset) is True


@pytest.mark.asyncio
@pytest.mark.parametrize('dataset', not_ok_orders)
async def test_unsuccessful_order_validation(dataset: dict):
    orders_service = OrdersService()
    assert await orders_service.is_order_valid(dataset) is False


@pytest.mark.asyncio
@pytest.mark.parametrize('dataset', not_ok_orders)
async def test_order_model_validation(dataset: dict):
    with pytest.raises(ValueError):
        OrderFull(**dataset)
