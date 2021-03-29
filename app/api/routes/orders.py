from datetime import datetime
import dateutil.parser

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
    name='orders:complete-order',
    status_code=status.HTTP_200_OK
)
async def complete_orders(request: Request):
    error_message = ''
    response = await request.json()

    courier_id = response['courier_id']
    order_id = response['order_id']
    complete_time = int(
        dateutil.parser
        .parse(response['complete_time'])
        .timestamp()
    )

    orders_service = OrdersService()

    order = await orders_service.get_order_by_id(order_id)
    order_assign = await orders_service.get_orders_assign(courier_id)

    if not orders_service.get_order_by_id(order_id):
        error_message = 'order not found'
    elif order.assign_id != order_assign.assign_id:
        error_message = 'order assigned to another courier'
    elif order.assign_id == orders_service.default_assign_id:
        error_message = 'order is unassigned'

    if error_message != '':
        return JSONResponse(
            {'value error': error_message},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        new_fields = {
            'is_ready': 1,
            'complete_time': complete_time
        }

        assigned_orders = await orders_service.get_unfinished_assigned_orders(courier_id)
        if not len(assigned_orders[0]) > 0:
            await orders_service.update_assign(
                order_assign.assign_id,
                {
                    'is_finished': 1
                }
            )

        await orders_service.update_order(
            order.order_id,
            new_fields
        )

        return JSONResponse(
            {'order_id': order.order_id},
            status_code=status.HTTP_200_OK,
        )
    except ValueError as e:
        return JSONResponse(
            {'value error': str(e)},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
