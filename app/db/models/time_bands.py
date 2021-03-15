from pydantic import BaseModel


class Band(BaseModel):
    band_id: int
    start: str
    end: str


class WorkingBand(Band):
    courier_id: int


class DeliveryBand(Band):
    order_id: int
