import io
import json

from fastapi import APIRouter, Request, requests
from fastapi.openapi.models import Response
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse, StreamingResponse, FileResponse
from starlette.templating import Jinja2Templates

from app.api.routes.couriers import get_courier
from app.db.models.couriers import CourierFull

router = APIRouter()
templates = Jinja2Templates(directory="static")


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
    "/couriers",
    name='web:couriers-menu',
    status_code=status.HTTP_200_OK
)
async def get_couriers(request: Request):
    return templates.TemplateResponse("couriers_menu.html", {"request": request})


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
