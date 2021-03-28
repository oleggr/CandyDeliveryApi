from fastapi import APIRouter, HTTPException, Body, Request
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

    for courier in couriers['data']:
        try:
            if not await CouriersService.is_courier_valid(courier):
                unfilled.append({'id': courier['courier_id']})
            else:
                to_create.append({'id': courier['courier_id']})

        except ValueError as e:
            return JSONResponse(
                {'unhandled exception': str(e)},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

    if len(unfilled) > 0:
        return JSONResponse(
            {'validation_error': {'couriers': unfilled}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    else:
        for courier in couriers['data']:
            await CouriersService().add_courier(
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
        courier.json(),
        status_code=status.HTTP_201_CREATED,
    )
