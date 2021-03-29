from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import JSONResponse

from app.db.models.couriers import CourierFull
from app.db.services.couriers import CouriersService


router = APIRouter()


@router.post(
    "",
    name='couriers:add-couriers',
    status_code=status.HTTP_201_CREATED
)
async def set_couriers(request: Request):
    couriers = await request.json()
    to_create = []
    unfilled = []
    couriers_service = CouriersService()

    for courier in couriers['data']:
        if not await couriers_service.is_courier_valid(courier):
            unfilled.append({'id': courier['courier_id']})
        else:
            to_create.append({'id': courier['courier_id']})

    if len(unfilled) > 0:
        return JSONResponse(
            {'validation_error': {'couriers': unfilled}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    else:
        for courier in couriers['data']:
            await couriers_service.add_courier(
                CourierFull(**courier)
            )
        return JSONResponse(
            {'couriers': to_create},
            status_code=status.HTTP_201_CREATED,
        )


@router.patch(
    "/{courier_id}",
    name='couriers:update-courier',
    status_code=status.HTTP_200_OK
)
async def update_courier(courier_id: int, request: Request):
    update_fields = await request.json()

    if not await CouriersService.courier_update_validation(update_fields) \
            or not await CouriersService().get_courier_by_id(courier_id):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    await CouriersService().update_courier(courier_id, update_fields)
    courier = await CouriersService().get_courier_full_data(courier_id)

    return JSONResponse(
        courier.dict(),
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/{courier_id}",
    name='couriers:get-courier',
    status_code=status.HTTP_200_OK
)
async def get_courier(courier_id: int):
    courier = await CouriersService().get_courier_full_data(courier_id)
    courier = courier.dict()

    return JSONResponse(
        courier,
        status_code=status.HTTP_201_CREATED,
    )
