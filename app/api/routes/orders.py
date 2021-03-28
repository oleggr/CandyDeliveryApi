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

    for order in orders['data']:
        if not await OrdersService.is_order_valid(order):
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

            await OrdersService().add_order(
                OrderFull(**order)
            )
            return JSONResponse(
                {'orders': to_create},
                status_code=status.HTTP_201_CREATED,
            )
