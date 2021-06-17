import io

from fastapi import APIRouter, Request
from fastapi.openapi.models import Response
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse, StreamingResponse, FileResponse
from starlette.templating import Jinja2Templates

from app.db.services.couriers import CouriersService
from app.db.services.orders import OrdersService

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import xlsxwriter

from xhtml2pdf import pisa


router = APIRouter()
templates = Jinja2Templates(directory="static")


@router.get(
    "/reports",
    name='web:couriers-menu',
    status_code=status.HTTP_200_OK
)
async def get_couriers(request: Request):
    return templates.TemplateResponse("reports_menu.html", {"request": request})


@router.get(
    "/report/pdf",
    name='reports:get-full-report',
    status_code=status.HTTP_200_OK
)
async def get_pdf_report():

    # добавить количество записей в отчет и диаграму (времени работы) или график

    couriers_service = CouriersService()
    orders_service = OrdersService()

    couriers = await couriers_service.get_couriers()
    orders = await orders_service.get_orders()
    assignitions = await orders_service.get_assigintions()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("static/report_template.html")

    template_vars = {
        'couriers': couriers,
        'orders': orders,
        'assignitions': assignitions,
        'datetime': dt_string
    }

    html_out = template.render(template_vars)

    resultFile = open(dt_string + '.pdf', "w+b")
    pisa.CreatePDF(html_out, resultFile)
    resultFile.close()

    return FileResponse(dt_string + '.pdf', media_type="application/pdf")


@router.get(
    "/report/exel",
    name='reports:get-full-report',
    status_code=status.HTTP_200_OK
)
async def get_exel_report():
    couriers_service = CouriersService()
    orders_service = OrdersService()

    couriers = await couriers_service.get_couriers()
    orders = await orders_service.get_orders()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    data = []

    data.append(["Курьеры", "", "", ""])
    data.append(['номер курьера', 'тип курьера', 'регионы', 'рабочие часы'])

    for courier in couriers:
        data.append([
            courier.courier_id,
            courier.courier_type,
            ";".join(str(courier.regions)),
            ";".join(courier.working_hours)
        ])

    workbook = xlsxwriter.Workbook(f'{dt_string}.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    for courier_id, courier_type, regions, working_hours in data:
        worksheet.write(row, col, courier_id)
        worksheet.write(row, col + 1, courier_type)
        worksheet.write(row, col + 2, regions)
        worksheet.write(row, col + 3, working_hours)
        row += 1

    data = []
    data.append(["Заказы", "", "", "", "", "", ""])
    data.append([
        'номер заказа',
        'вес',
        'регион',
        'выполнен',
        'время завершения',
        'назначенный курьер',
        'время доставки'
    ])

    for order in orders:
        data.append([
            order.order_id,
            order.weight,
            order.region_id,
            order.is_ready,
            order.complete_time,
            order.assign_id,
            ";".join(order.delivery_hours)
        ])

    # Iterate over the data and write it out row by row.
    for order_id, weight, region_id, is_ready, complete_time, assign_id, delivery_hours in data:
        worksheet.write(row, col, order_id)
        worksheet.write(row, col + 1, weight)
        worksheet.write(row, col + 2, region_id)
        worksheet.write(row, col + 3, is_ready)
        worksheet.write(row, col + 4, complete_time)
        worksheet.write(row, col + 5, assign_id)
        worksheet.write(row, col + 6, delivery_hours)
        row += 1

    new_data = [
        ["курьеры", len(couriers)],
        ["заказы", len(orders)],
    ]

    chart = workbook.add_chart({'type': 'pie'})
    chart.add_series({
        'categories': f'=Sheet1!$A${row + 1}:$A${row + 2}',
        'values': f'=Sheet1!$B${row + 1}:$B${row + 2}',
        'points': [
            {'fill': {'color': 'green'}},
            {'fill': {'color': 'red'}},
        ],
    })
    worksheet.insert_chart('I1', chart)

    for item, val in (new_data):
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, val)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()
    return FileResponse(f'{dt_string}.xlsx', media_type='application/vnd.ms-excel')
