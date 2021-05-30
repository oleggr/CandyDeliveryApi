from fastapi.testclient import TestClient


def test_successful_orders_post(client: TestClient):
    json_orders = \
        {
            "data": [
                {
                    "order_id": 1,
                    "weight": 0.23,
                    "region": 12,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 2,
                    "weight": 15,
                    "region": 1,
                    "delivery_hours": ["09:00-18:00"]
                },
                {
                    "order_id": 3,
                    "weight": 0.01,
                    "region": 22,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                },
                {
                    "order_id": 4,
                    "weight": 0.01,
                    "region": 22,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                },
                {
                    "order_id": 5,
                    "weight": 16,
                    "region": 22,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                },
                {
                    "order_id": 6,
                    "weight": 14.8,
                    "region": 22,
                    "delivery_hours": ["09:00-12:00", "16:00-21:30"]
                },
            ]
        }
    response = client.post('/orders', json=json_orders)
    assert response.status_code == 201
    assert response.json() == {'orders': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}]}
