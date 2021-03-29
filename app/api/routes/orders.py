from datetime import datetime
from fastapi import APIRouter, Request
from starlette import status
from starlette.responses import JSONResponse

from app.db.models.orders import OrderFull
from app.db.services.orders import OrdersService

router = APIRouter()


@router.post(
    "",
    name='orders:add-orders',
    status_code=status.HTTP_201_CREATED
)
async def set_orders(request: Request):
    orders = await request.json()
    to_create = []
    unfilled = []

    orders_service = OrdersService()

    for order in orders['data']:
        if not await orders_service.is_order_valid(order):
            unfilled.append({'id': order['order_id']})
        else:
            to_create.append({'id': order['order_id']})

    if len(unfilled) > 0:
        return JSONResponse(
            {'validation_error': {'orders': unfilled}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    else:
        for order in orders['data']:
            print('ORDER BAAA: ', order)

            await orders_service.add_order(
                OrderFull(**order)
            )
            return JSONResponse(
                {'orders': to_create},
                status_code=status.HTTP_201_CREATED,
            )


@router.post(
    "/assign",
    name='orders:assign-orders',
    status_code=status.HTTP_200_OK
)
async def assign_orders(request: Request):
    assigned = []
    response = await request.json()
    courier_id = response['courier_id']

    orders_service = OrdersService()

    try:
        orders = await orders_service.assign_orders(courier_id)

        for order in orders[0]:
            assigned.append({'id': order})

        assign_time = datetime.fromtimestamp(orders[1])

        return JSONResponse(
            {
                'orders': assigned,
                'assign_time': assign_time.isoformat()
            },
            status_code=status.HTTP_200_OK,
        )
    except ValueError as e:
        return JSONResponse(
            {'value error': str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post(
    "/complete",
    name='orders:complete-orders',
    status_code=status.HTTP_200_OK
)
async def complete_orders(request: Request):
    pass
