from pydantic import BaseModel


class Courier(BaseModel):
    courier_id: int
    courier_type: int


class CourierToRegion(BaseModel):
    courier_id: int
    region_id: int
