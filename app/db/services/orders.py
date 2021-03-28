from sqlalchemy import and_

from app.db.models.orders import OrderFull, Order
from app.db.models.time_bands import DeliveryBand
from app.db.schema import orders_table, delivery_bands_table
from app.db.services.abstract import AbstractService
from app.db.services.regions import RegionsService


class OrdersService(AbstractService):
    @classmethod
    async def is_order_valid(cls, order: dict):
        if not (
                'order_id' in order
                and order['order_id'] >= 0
                and isinstance(order['order_id'], int)
        ):
            return False

        if not (
                'weight' in order
                and isinstance(order['weight'], float)
                and 0.01 <= order['weight'] <= 50
        ):
            return False

        if not ('region' in order
                and order['region'] >= 0
                and isinstance(order['region'], int)
        ):
            return False

        if not ('delivery_hours' in order
                and len(order['delivery_hours']) > 0):
            return False

        return True

    async def add_order(self, order: OrderFull):
        if await self.get_order_by_id(order.order_id):
            return

        regions_service = RegionsService()
        if not await regions_service.get_region_by_id(order.region_id):
            await regions_service.add_region(order.region_id)

        for band in order.delivery_hours:
            await self.set_order_delivery_band(order.order_id, band)

        await self.execute(
            orders_table.insert().values({
                'order_id': order.order_id,
                'weight': order.weight,
                'region_id': order.region_id,
                'is_ready': False
            })
        )

    async def get_order_by_id(self, order_id: int) -> [Order, bool]:
        order_row = await self.select(
            orders_table.select().where(
                and_(
                    orders_table.c.order_id == order_id,
                )
            )
        )

        if order_row:
            return Order(**order_row)
        else:
            return False

    async def set_order_delivery_band(self, order_id: int, band: str):
        band = band.split('-')
        start = band[0]
        end = band[1]

        delivery_band = DeliveryBand(
            order_id=order_id,
            start=start,
            end=end
        )

        await self.execute(
            delivery_bands_table.insert().values({
                'order_id': delivery_band.order_id,
                'start': delivery_band.start,
                'end': delivery_band.end
            })
        )
