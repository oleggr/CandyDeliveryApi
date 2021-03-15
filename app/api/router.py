from fastapi import APIRouter, HTTPException

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

from app.db.services.regions import RegionsService

router = APIRouter()


@router.get("/", )
async def root():
    return "Hello World"


@router.get("/test", )
async def test():
    return "TEST ROUTE!!!!!"


@router.post("/region/{region_id}", )
async def set_region(region_id):
    try:
        await RegionsService().add_region(
            region_id,
            f'test region {region_id}'
        )
        return HTTP_200_OK
    except:
        return HTTP_400_BAD_REQUEST


@router.get("/region/{region_id}", )
async def get_region(region_id):
    try:
        region = await RegionsService().get_region_by_id(region_id)
        return f'Your region has id:{region.region_id} name:{region.region_name}'

    except:
        return HTTP_400_BAD_REQUEST


@router.get("/{user_id}", )
async def user(user_id: int):
    if user_id != 0:
        return f'Your id is: {user_id}'
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
        )
