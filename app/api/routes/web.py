import json
import time

from fastapi import APIRouter, Request
from starlette import status
from starlette.templating import Jinja2Templates

from app.api.routes.couriers import get_courier, _add_courier, _update_courier
from app.api.routes.orders import complete_order, _assign_orders, _add_orders
from app.db.models.couriers import CourierFull
from app.db.services.orders import OrdersService

router = APIRouter()
templates = Jinja2Templates(directory="static")


@router.get(
    "",
    name='web:menu-page',
    status_code=status.HTTP_200_OK
)
async def get_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@router.get(
    "/main",
    name='web:menu-page',
    status_code=status.HTTP_200_OK
)
async def get_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@router.get(
    "/orders",
    name='web:orders-menu',
    status_code=status.HTTP_200_OK
)
async def get_orders(request: Request):
    return templates.TemplateResponse("orders_menu.html", {"request": request})


@router.get(
    "/orders/complete/menu",
    name='web:orders-complete-menu',
    status_code=status.HTTP_200_OK
)
async def get_complete_orders_menu(request: Request):
    return templates.TemplateResponse("orders_complete_menu.html", {"request": request})


@router.get(
    "/orders/complete",
    name='web:orders-complete',
    status_code=status.HTTP_200_OK
)
async def complete_orders(courier_id, order_id, request: Request):
    complete_time = int(time.time())

    await complete_order(courier_id, order_id, complete_time)

    return templates.TemplateResponse("orders_menu.html", {"request": request})


@router.get(
    "/orders/assign/menu",
    name='web:orders-assign-menu',
    status_code=status.HTTP_200_OK
)
async def get_assign_orders_menu(request: Request):
    return templates.TemplateResponse("orders_assign_menu.html", {"request": request})


@router.get(
    "/orders/assign",
    name='web:orders-assign',
    status_code=status.HTTP_200_OK
)
async def assign_orders(courier_id, request: Request):

    await _assign_orders(courier_id)

    return templates.TemplateResponse("orders_menu.html", {"request": request})


@router.get(
    "/orders/add/menu",
    name='web:orders-assign-menu',
    status_code=status.HTTP_200_OK
)
async def get_add_orders_menu(request: Request):
    return templates.TemplateResponse("orders_add_menu.html", {"request": request})


@router.get(
    "/orders/add",
    name='web:orders-assign',
    status_code=status.HTTP_200_OK
)
async def add_orders(
        order_id,
        weight,
        region,
        delivery_hours,
        request: Request
):
    await _add_orders([
        {
            'order_id': int(order_id),
            'weight': float(weight),
            'region': int(region),
            'delivery_hours': delivery_hours.split(",")
        }
    ])

    return templates.TemplateResponse("orders_menu.html", {"request": request})


@router.get(
    "/orders/region",
    name='web:orders-region',
    status_code=status.HTTP_200_OK
)
async def orders_to_regions(request: Request, region_id=-1):
    orders = await OrdersService().get_orders_by_regions(region_id)
    return templates.TemplateResponse(
        "orders_to_regions.html",
        {
            "request": request,
            "orders": orders,
            "count": len(orders)
        }
    )


@router.get(
    "/couriers",
    name='web:couriers-menu',
    status_code=status.HTTP_200_OK
)
async def get_couriers(request: Request):
    return templates.TemplateResponse("couriers_menu.html", {"request": request})


@router.get(
    "/couriers/add/menu",
    name='web:add-courier-menu',
    status_code=status.HTTP_200_OK
)
async def add_courier(request: Request):
    return templates.TemplateResponse("couriers_add_menu.html", {"request": request})


@router.get(
    "/couriers/add",
    name='web:add-courier',
    status_code=status.HTTP_200_OK
)
async def add_courier(courier_id, courier_type, regions, working_hours, request: Request):
    args = {
        'courier_id': int(courier_id),
        'courier_type': courier_type,
        'regions': regions.split(','),
        'working_hours': working_hours.split(','),
    }

    await _add_courier([args])

    courier = CourierFull(**args)

    return templates.TemplateResponse("couriers_watch.html", {"request": request, 'courier': courier})


@router.get(
    "/couriers/update/menu",
    name='web:update-courier-menu',
    status_code=status.HTTP_200_OK
)
async def get_update_courier_menu(request: Request):
    return templates.TemplateResponse("couriers_update_menu.html", {"request": request})


@router.get(
    "/couriers/update",
    name='web:update-courier',
    status_code=status.HTTP_200_OK
)
async def update_courier(courier_id, courier_type, regions, working_hours, request: Request):
    args = dict()

    args['courier_id'] = courier_id

    if courier_type:
        args['courier_type'] = courier_type

    if regions:
        args['regions'] = regions.split(',')

    if working_hours:
        args['working_hours'] = working_hours.split(',')

    code, courier = await _update_courier(int(courier_id), args)

    return templates.TemplateResponse("couriers_watch.html", {"request": request, 'courier': courier})


@router.get(
    "/couriers/watch/menu",
    name='web:couriers-menu',
    status_code=status.HTTP_200_OK
)
async def get_couriers(request: Request):
    return templates.TemplateResponse("couriers_watch_menu.html", {"request": request})


@router.get(
    "/couriers/watch",
    name='web:couriers-menu',
    status_code=status.HTTP_200_OK
)
async def get_couriers(courier_id: int, request: Request):
    courier = await get_courier(courier_id)
    courier = json.loads(courier.body)
    courier = CourierFull(**courier)

    return templates.TemplateResponse("couriers_watch.html", {"request": request, 'courier': courier})
