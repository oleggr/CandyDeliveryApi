import time

from sqlalchemy import and_

from app.db.models.time_bands import WorkingBand
from app.db.schema import couriers_table, courier_to_region_table, working_bands_table, CourierType
from app.db.models.couriers import Courier, CourierToRegion, CourierFull, courier_types
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

    @staticmethod
    async def courier_update_validation(new_courier: dict) -> bool:
        if 'courier_type' in new_courier \
                and new_courier['courier_type'] not in courier_types:
            return False

        if 'regions' in new_courier \
                and len(new_courier['regions']) <= 0:
            return False

        if 'working_hours' in new_courier \
                and len(new_courier['working_hours']) <= 0:
            return False

        return True

    async def add_courier(
            self,
            courier: CourierFull
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

    async def get_courier_by_id(
            self,
            courier_id: int
    ) -> [Courier, bool]:
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

    async def get_courier_full_data(
            self,
            courier_id: int
    ):
        courier = await self.get_courier_by_id(courier_id)
        regions = await self.get_courier_regions(courier_id)
        bands = await self.get_courier_working_bands(courier_id)

        return CourierFull(
            courier_id=courier_id,
            courier_type=courier.courier_type,
            regions=regions,
            working_hours=bands
        )

    async def insert_courier(
            self,
            courier_id: int,
            courier_type: CourierType
    ):
        courier = Courier(
            courier_id=courier_id,
            courier_type=courier_type
        )

        await self.execute(
            couriers_table.insert().values({
                'courier_id': courier.courier_id,
                'courier_type': courier.courier_type,
            })
        )

    async def update_courier(
            self,
            courier_id: int,
            update_fields: dict
    ):
        if 'courier_type' in update_fields:
            await self.execute(
                couriers_table.update()
                    .where(couriers_table.c.courier_id == courier_id)
                    .values({'courier_type': update_fields['courier_type']})
            )

        if 'regions' in update_fields:
            await self.execute(
                courier_to_region_table.delete().where(
                    couriers_table.c.courier_id == courier_id
                )
            )

            for region in update_fields['regions']:
                await self.set_courier_to_region_mapping(
                    courier_id,
                    region
                )

        if 'working_hours' in update_fields:
            await self.execute(
                working_bands_table.delete().where(
                    couriers_table.c.courier_id == courier_id
                )
            )

            for band in update_fields['working_hours']:
                await self.set_courier_working_band(
                    courier_id,
                    band
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

        await self.execute(
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

    async def get_courier_regions(
            self,
            courier_id: int
    ):
        regions = []

        session = await self.get_session()
        res = session.query(courier_to_region_table.c.region_id) \
            .filter(courier_to_region_table.c.courier_id.in_([courier_id])) \
            .all()

        for region in res:
            regions.append(region[0])

        return regions

    async def get_courier_working_bands(
            self,
            courier_id: int
    ):
        bands = []

        session = await self.get_session()
        res = session.query(working_bands_table) \
            .filter(working_bands_table.c.courier_id.in_([courier_id])) \
            .all()

        for band in res:
            bands.append(band[2] + '-' + band[3])

        return bands

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

        await self.execute(
            working_bands_table.insert().values({
                'courier_id': working_band.courier_id,
                'start': working_band.start,
                'end': working_band.end
            })
        )
