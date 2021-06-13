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

    code, msg = await _add_orders(orders['data'])

    if code == 0:
        return JSONResponse(
            {'validation_error': {'orders': msg}},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if code == 1:
        return JSONResponse(
            {'orders': msg},
            status_code=status.HTTP_201_CREATED,
        )


async def _add_orders(orders):
    to_create = []
    unfilled = []

    orders_service = OrdersService()

    for order in orders:
        if 'region' in order:
            order['region_id'] = order['region']
            del order['region']

        if not await orders_service.is_order_valid(order):
            unfilled.append({'id': order['order_id']})
        else:
            to_create.append({'id': order['order_id']})

    if len(unfilled) > 0:
        return 0, unfilled
    else:
        for order in orders:
            await orders_service.add_order(
                OrderFull(**order)
            )
        return 1, to_create


@router.post(
    "/assign",
    name='orders:assign-orders',
    status_code=status.HTTP_200_OK
)
async def assign_orders(request: Request):
    response = await request.json()
    courier_id = response['courier_id']

    code, msg = await _assign_orders(courier_id)

    if code == 0:
        return JSONResponse(
            {'value error': msg},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if code == 1:
        return JSONResponse(
            {
                'orders': msg[0],
                'assign_time': msg[1]
            },
            status_code=status.HTTP_200_OK,
        )


async def _assign_orders(courier_id):
    assigned = []
    orders_service = OrdersService()

    try:
        orders = await orders_service.assign_orders(courier_id)

        for order in orders[0]:
            assigned.append({'id': order})

        assign_time = datetime.fromtimestamp(orders[1])

        return 1, [assigned, assign_time.isoformat()]
    except ValueError as e:
        return 0, str(e)


@router.post(
    "/complete",
    name='orders:complete-order',
    status_code=status.HTTP_200_OK
)
async def complete_orders(request: Request):
    response = await request.json()

    courier_id = response['courier_id']
    order_id = response['order_id']
    complete_time = int(
        dateutil.parser
        .parse(response['complete_time'])
        .timestamp()
    )

    code, msg = await complete_order(courier_id, order_id, complete_time)

    if code == 0:
        return JSONResponse(
            {'value error': msg},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if code == 1:
        return JSONResponse(
            {'order_id': msg},
            status_code=status.HTTP_200_OK,
        )


async def complete_order(courier_id, order_id, complete_time):
    error_message = ''
    orders_service = OrdersService()

    order = await orders_service.get_order_by_id(order_id)
    order_assign = await orders_service.get_orders_assign(courier_id)

    if not orders_service.get_order_by_id(order_id):
        error_message = 'order not found'
    elif order.assign_id == orders_service.default_assign_id:
        error_message = 'order is unassigned'
    elif order.assign_id != order_assign.assign_id:
        error_message = 'order assigned to another courier'

    if error_message != '':
        return 0, error_message

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

        return 1, order.order_id

    except ValueError as e:
        return 0, str(e)
