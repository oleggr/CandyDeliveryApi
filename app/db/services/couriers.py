import time

from sqlalchemy import and_

from app.db.models.time_bands import WorkingBand
from app.db.schema import couriers_table, courier_to_region_table, working_bands_table
from app.db.models.couriers import Courier, CourierToRegion, CourierInCreate, courier_types
from app.db.services.abstract import AbstractService
from app.db.services.regions import RegionsService


class CouriersService(AbstractService):

    @staticmethod
    async def is_courier_valid(courier: dict) -> bool:
        if not ('courier_id' in courier
                and courier['courier_id'] >= 0
                and isinstance(courier['courier_id'], int)
        ):
            return False

        if not ('courier_type' in courier
                and courier['courier_type'] in courier_types):
            return False

        if not ('regions' in courier
                and len(courier['regions']) > 0):
            return False

        if not ('working_hours' in courier
                and len(courier['working_hours']) > 0):
            return False

        return True

    async def add_courier(
            self,
            courier: CourierInCreate
    ):
        if await self.get_courier_by_id(courier.courier_id):
            return

        regions_service = RegionsService()

        for region in courier.regions:
            if not await regions_service.get_region_by_id(region):
                await regions_service.add_region(region)
            if not await self.get_courier_to_region_mapping(
                    courier.courier_id,
                    region
            ):
                await self.set_courier_to_region_mapping(
                    courier.courier_id,
                    region
                )

        for band in courier.working_hours:
            await self.set_courier_working_band(courier.courier_id, band)

        await self.insert_courier(courier.courier_id, courier.courier_type)

    async def get_courier_by_id(self, courier_id: int) -> [Courier, bool]:
        courier_row = await self.select(
            couriers_table.select().where(
                and_(
                    couriers_table.c.courier_id == courier_id,
                )
            )
        )

        if courier_row:
            return Courier(**courier_row)
        else:
            return False

    async def insert_courier(
            self,
            courier_id: int,
            courier_type: str
    ):
        courier = Courier(
            courier_id=courier_id,
            courier_type=courier_type
        )

        await self.insert(
            couriers_table.insert().values({
                'courier_id': courier.courier_id,
                'courier_type': courier.courier_type,
            })
        )

    async def set_courier_to_region_mapping(
            self,
            courier_id: int,
            region_id: int
    ):
        courier = CourierToRegion(
            courier_id=courier_id,
            region_id=region_id
        )

        await self.insert(
            courier_to_region_table.insert().values({
                'courier_id': courier.courier_id,
                'region_id': courier.region_id,
            })
        )

    async def get_courier_to_region_mapping(
            self,
            courier_id: int,
            region_id: int
    ):
        courier_to_region_row = await self.select(
            courier_to_region_table.select().where(
                and_(
                    courier_to_region_table.c.courier_id == courier_id,
                    courier_to_region_table.c.region_id == region_id
                )
            )
        )

        if courier_to_region_row:
            return CourierToRegion(**courier_to_region_row)
        else:
            return False

    async def set_courier_working_band(
            self,
            courier_id: int,
            band: str
    ):
        band = band.split('-')
        start = band[0]
        end = band[1]

        working_band = WorkingBand(
            courier_id=courier_id,
            start=start,
            end=end
        )

        await self.insert(
            working_bands_table.insert().values({
                'courier_id': working_band.courier_id,
                'start': working_band.start,
                'end': working_band.end
            })
        )
