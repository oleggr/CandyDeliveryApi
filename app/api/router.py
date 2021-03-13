from fastapi import APIRouter, HTTPException

from starlette.status import HTTP_400_BAD_REQUEST


router = APIRouter()


@router.get("/",)
async def root():
    return "Hello World"


@router.get("/test",)
async def test():
    return "TEST ROUTE!!!!!"


@router.get("/{user_id}",)
async def user(user_id: int):
    if user_id != 0:
        return f'Your id is: {user_id}'
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
        )
