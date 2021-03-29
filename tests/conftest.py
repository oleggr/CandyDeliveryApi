from random import random

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from fastapi import FastAPI

from app.db.models.regions import Region

#
# @pytest.fixture
# def mariadb():
#     tmp_name = '.'.join([uuid.uuid4().hex, 'pytest'])
#     tmp_url = DbConfig.get_conn_string(tmp_name)
#
#     create_database(tmp_url)
#
#     try:
#         yield tmp_url
#     finally:
#         drop_database(tmp_url)
#
#
# @pytest.fixture(autouse=True)
# async def apply_migrations(mariadb: None) -> None:
#     alembic.config.main(argv=["upgrade", "head"])
#     yield
#     alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture
async def app() -> FastAPI:
# def app(apply_migrations: None) -> FastAPI:
    from app.main import get_application

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def test_region():
    return Region(
        region_id=random(),
        region_name='test region'
    )
