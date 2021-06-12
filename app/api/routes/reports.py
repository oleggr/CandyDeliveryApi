import io

from fastapi import APIRouter
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


@router.get(
    "/report",
    name='reports:get-full-report',
    status_code=status.HTTP_200_OK
)
async def get_report():

    # добавить количество записей в отчет и диаграму (времени работы) или график

    couriers_service = CouriersService()
    orders_service = OrdersService()

    couriers = await couriers_service.get_couriers()
    orders = await orders_service.get_orders()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("static/report_template.html")

    template_vars = {
        'couriers': couriers,
        'orders': orders,
        'datetime': dt_string
    }

    html_out = template.render(template_vars)

    resultFile = open(dt_string + '.pdf', "w+b")
    pisa.CreatePDF(html_out, resultFile)
    resultFile.close()

    return FileResponse(dt_string + '.pdf', media_type="application/pdf")


@router.get(
    "/exel_report",
    name='reports:get-full-report',
    status_code=status.HTTP_200_OK
)
async def get_report():
    couriers_service = CouriersService()
    orders_service = OrdersService()

    couriers = await couriers_service.get_couriers()
    orders = await orders_service.get_orders()

    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    data = []

    data.append(["Курьеры", ""])
    data.append(["Параметр", "Значение"])

    for courier in couriers:
        data.append(['номер курьера', courier.courier_id])
        data.append(['тип курьера', courier.courier_type])
        data.append(['регионы', ";".join(str(courier.regions))])
        data.append(['рабочие часы', ";".join(courier.working_hours)])
        data.append(["", ""])

    data.append(["Заказы", ""])
    data.append(["Параметр", "Значение"])

    for order in orders:
        data.append(['номер заказа', order.order_id])
        data.append(['вес', order.weight])
        data.append(['регион', order.region_id])
        data.append(['выполнен', order.is_ready])
        data.append(['время завершения', order.complete_time])
        data.append(['назначенный курьер', order.assign_id])
        data.append(['время доставки', ";".join(order.delivery_hours)])
        data.append(["", ""])

    workbook = xlsxwriter.Workbook(f'{dt_string}.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for item, val in (data):
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, val)
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
    worksheet.insert_chart('D1', chart)

    for item, val in (new_data):
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, val)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()
    return FileResponse(f'{dt_string}.xlsx', media_type='application/vnd.ms-excel')
