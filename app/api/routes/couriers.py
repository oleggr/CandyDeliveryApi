from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import JSONResponse

from app.db.models.couriers import CourierFull
from app.db.services.couriers import CouriersService
from app.db.services.orders import OrdersService

router = APIRouter()


@router.post(
    "",
    name='couriers:add-couriers',
    status_code=status.HTTP_201_CREATED
)
async def set_couriers(request: Request):
    couriers = await request.json()

    code, msg = await _add_courier(couriers['data'])

    if code == 0:
        return JSONResponse(
            {'validation_error': {'couriers': msg}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if code == 1:
        return JSONResponse(
            {'couriers': msg},
            status_code=status.HTTP_201_CREATED,
        )


async def _add_courier(couriers):
    to_create = []
    unfilled = []
    couriers_service = CouriersService()

    for courier in couriers:
        if not await couriers_service.is_courier_valid(courier):
            unfilled.append({'id': courier['courier_id']})
        else:
            to_create.append({'id': courier['courier_id']})

    if len(unfilled) > 0:
        return 0, unfilled

    else:
        for courier in couriers:
            await couriers_service.add_courier(
                CourierFull(**courier)
            )
        return 1, to_create


@router.patch(
    "/{courier_id}",
    name='couriers:update-courier',
    status_code=status.HTTP_200_OK
)
async def update_courier(courier_id: int, request: Request):
    update_fields = await request.json()
    code, msg = await _update_courier(courier_id, update_fields)

    if code == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if code == 1:
        return JSONResponse(
            msg.dict(),
            status_code=status.HTTP_201_CREATED,
        )


async def _update_courier(courier_id, update_fields):
    couriers_service = CouriersService()
    orders_service = OrdersService()

    if not await couriers_service.courier_update_validation(update_fields) \
            or not await couriers_service.get_courier_by_id(courier_id):
        return 0, ""

    await couriers_service.update_courier(courier_id, update_fields)
    courier = await couriers_service.get_courier_full_data(courier_id)

    await orders_service.unassign_orders(courier)

    return 1, courier


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
