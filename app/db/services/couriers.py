from sqlalchemy import and_

from app.db.schema import couriers_table
from app.db.schema import courier_to_region_table
from app.db.models.couriers import Courier
from app.db.models.couriers import CourierToRegion
from app.db.services.abstract import AbstractService


class CouriersService(AbstractService):

    courier_types = {
        'foot': 1,
        'bike': 1,
        'car': 1,
    }

    async def add_courier(
            self,
            courier_id: int,
            courier_type: str,
            regions: list,
            working_hours: list
    ):
        courier = Courier(
            courier_id=courier_id,
            courier_type=courier_type
        )

        query = couriers_table.insert().values({
            'courier_id': courier.courier_id,
            'courier_type': courier.courier_type,
        })

        await self.insert(query)

    async def get_courier_by_id(self, courier_id: int) -> Courier:
        query = couriers_table.select().where(
            and_(
                couriers_table.c.courier_id == courier_id,
            )
        )
        courier_row = await self.select(query)
        return Courier(**courier_row)
