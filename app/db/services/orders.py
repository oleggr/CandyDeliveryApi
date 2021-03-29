import time

from sqlalchemy import and_

from app.db.models.couriers import courier_types
from app.db.models.orders import OrderFull, Order, OrderAssign
from app.db.models.time_bands import DeliveryBand
from app.db.schema import orders_table, delivery_bands_table, orders_assign_table
from app.db.services.abstract import AbstractService
from app.db.services.couriers import CouriersService
from app.db.services.regions import RegionsService


class OrdersService(AbstractService):
    default_assign_id = -1
    default_complete_time = 0

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
                and 0.01 <= order['weight'] <= 50
        ):
            return False

        if not (
                'region_id' in order
                and order['region_id'] >= 0
                and isinstance(order['region_id'], int)
        ):
            return False

        if not (
                'delivery_hours' in order
                and len(order['delivery_hours']) > 0
        ):
            return False

        return True

    @staticmethod
    async def order_update_validation(new_order: dict) -> bool:
        if (
                'weight' in new_order
                and not (
                        isinstance(new_order['weight'], float)
                        and 0.01 <= new_order['weight'] <= 50
                )
        ):
            return False

        if (
                'region_id' in new_order
                and not (
                    new_order['region_id'] >= 0
                    and isinstance(new_order['region_id'], int)
                )
        ):
            return False

        if (
                'complete_time' in new_order
                and not isinstance(new_order['complete_time'], int)
        ):
            return False

        if (
                'assign_id' in new_order
                and not (
                    new_order['assign_id'] >= 0
                    and isinstance(new_order['assign_id'], int)
                )
        ):
            return False

        if (
                'delivery_hours' in new_order
                and not len(new_order['delivery_hours']) > 0
        ):
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

    async def update_order(
            self,
            order_id: int,
            update_fields: dict
    ):
        if not (
                await self.order_update_validation(update_fields)
                and await self.get_order_by_id(order_id)
        ):
            raise ValueError('Order update unsuccessful')

        if 'delivery_hours' not in update_fields:
            await self.execute(
                orders_table.update()
                .where(orders_table.c.order_id == order_id)
                .values(update_fields)
            )

        else:
            bands = update_fields['delivery_hours']
            del update_fields['delivery_hours']

            if len(update_fields) > 0:
                await self.execute(
                    orders_table.update()
                    .where(orders_table.c.order_id == order_id)
                    .values(update_fields)
                )

                await self.execute(
                    delivery_bands_table.delete().where(
                        delivery_bands_table.c.order_id == order_id
                    )
                )

                for band in bands:
                    await self.set_order_delivery_band(
                        order_id,
                        band
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

    async def get_delivery_bands(self, order_id: int):
        bands = []

        session = await self.get_session()
        res = session.query(delivery_bands_table) \
            .filter(delivery_bands_table.c.order_id.in_([order_id])) \
            .all()

        for band in res:
            bands.append(band[2] + '-' + band[3])

        return bands

    async def get_order_full_data(self, order_id: int):
        order = await self.get_order_by_id(order_id)
        bands = await self.get_delivery_bands(order_id)

        return OrderFull(
            order_id=order.order_id,
            weight=order.weight,
            region_id=order.region_id,
            is_ready=order.is_ready,
            complete_time=order.complete_time,
            assign_id=order.assign_id,
            delivery_hours=bands,
        )

    async def create_orders_assign(self, courier_id: int):
        assign = OrderAssign(
            courier_id=courier_id,
            assign_time=int(time.time())
        )

        await self.execute(
            orders_assign_table.insert().values({
                'courier_id': assign.courier_id,
                'assign_time': assign.assign_time,
            })
        )

    async def get_orders_assign(self, courier_id: int) -> [OrderAssign, bool]:
        assign_row = await self.select(
            orders_assign_table.select().where(
                and_(
                    orders_assign_table.c.courier_id == courier_id,
                    orders_assign_table.c.is_finished == 0
                )
            )
        )

        if assign_row:
            return OrderAssign(**assign_row)
        else:
            return False

    async def get_unassigned_orders(self) -> list:
        orders = []

        session = await self.get_session()
        res = session.query(orders_table) \
            .filter(orders_table.c.assign_id.in_([self.default_assign_id])) \
            .all()

        for order_row in res:
            order = await self.get_order_full_data(order_row[0])
            orders.append(order)

        return orders

    async def get_unfinished_assigned_orders(self, courier_id: int):
        orders = []

        order_assign = await self.get_orders_assign(courier_id)
        if not order_assign:
            return [[], None]
        assign_id = order_assign.assign_id

        session = await self.get_session()
        res = session.query(orders_table) \
            .filter(orders_table.c.assign_id.in_([assign_id])) \
            .all()

        for order_row in res:
            order = await self.get_order_full_data(order_row[0])
            if order.complete_time == self.default_complete_time:
                orders.append(order.order_id)

        return [orders, order_assign.assign_time]

    async def assign_orders(self, courier_id: int) -> list:
        assigned_orders = []
        couriers_service = CouriersService()

        if not await couriers_service.get_courier_by_id(courier_id):
            raise ValueError('Courier not exist')

        already_assigned = await self.get_unfinished_assigned_orders(courier_id)
        if len(already_assigned[0]) > 0:
            return already_assigned

        orders = await self.get_unassigned_orders()

        if not len(orders) > 0:
            raise ValueError('available orders absent')

        courier = await couriers_service.get_courier_full_data(courier_id)

        await self.create_orders_assign(courier.courier_id)
        order_assign = await self.get_orders_assign(courier.courier_id)

        max_weight = courier_types[courier.courier_type]

        for order in orders:

            delivery_availability = await self.check_delivery_availability(
                order.delivery_hours,
                courier.working_hours
            )

            if (
                    order.weight <= max_weight
                    and order.region_id in courier.regions
                    and delivery_availability
            ):
                assigned_orders.append(order.order_id)
                await self.update_order(
                    order.order_id,
                    {'assign_id': order_assign.assign_id}
                )

        return [assigned_orders, order_assign.assign_time]

    async def check_delivery_availability(
            self,
            delivery_hours: list,
            working_hours: list
    ) -> bool:
        for working_band in working_hours:
            band = working_band.split('-')
            min_w = band[0]
            max_w = band[0]

            for delivery_band in delivery_hours:
                band = delivery_band.split('-')
                min_d = band[0]
                max_d = band[0]

                if min_w <= max_d <= max_w \
                        or min_w <= min_d <= max_w:
                    return True

        return False

    async def update_assign(self, assign_id: int, update_fields: dict):
        await self.execute(
            orders_assign_table.update()
            .where(orders_assign_table.c.assign_id == assign_id)
            .values(update_fields)
        )
