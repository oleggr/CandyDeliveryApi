import asyncio
import asynctest
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.models.regions import Region


def test_first():
    a = 1
    assert a == 1


async def test_hello(
        app: FastAPI,
        client: AsyncClient
):
    response = await client.get(app.url_path_for('hello-world'))
    print('-->', response.json())


# def test_add_region(
#         app: FastAPI, client: AsyncClient,  test_region: Region
# ):
    # await client.post(
    #     app.url_path_for('region:add-region'),

    # )

    # print('\n>> ', app.url_path_for('hello-world'))

    # print()
    # for elem in app.routes:
    #     print('>>', elem.url_path_for(elem.name))
