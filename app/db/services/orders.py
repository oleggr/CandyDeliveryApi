from sqlalchemy import and_

from app.db.schema import orders_table
from app.db.models.couriers import Courier
from app.db.models.couriers import CourierToRegion
from app.db.services.abstract import AbstractService


class OrdersService(AbstractService):
    pass
