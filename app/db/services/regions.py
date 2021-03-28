from sqlalchemy import and_

from app.db.schema import regions_table
from app.db.models.regions import Region
from app.db.services.abstract import AbstractService


class RegionsService(AbstractService):

    async def add_region(self, region_id: int, region_name: str = ''):
        region = Region(
            region_id=region_id,
            region_name=region_name
        )

        query = regions_table.insert().values({
            'region_id': region.region_id,
            'region_name': region.region_name,
        })

        await self.insert(query)

    async def get_region_by_id(self, region_id: int) -> [Region, bool]:
        query = regions_table.select().where(
            and_(
                regions_table.c.region_id == region_id,
            )
        )
        region_row = await self.select(query)

        if region_row:
            return Region(**region_row)
        else:
            return False
