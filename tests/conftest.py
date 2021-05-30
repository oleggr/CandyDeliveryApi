import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
async def client():
    return TestClient(app)
