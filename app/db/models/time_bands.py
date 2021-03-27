import time

from pydantic import BaseModel, validator


class Band(BaseModel):
    band_id: int
    start: str
    end: str

    @validator('start', 'end')
    def time_format_validation(cls, v: str):
        try:
            time.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Wrong time format')


class WorkingBand(Band):
    courier_id: int

    @validator('courier_id')
    def courier_id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v


class DeliveryBand(Band):
    order_id: int

    @validator('order_id')
    def order_id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v
