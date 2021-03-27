from pydantic import BaseModel, validator
from app.db.services.couriers import CouriersService


class Courier(BaseModel):
    courier_id: int
    courier_type: str

    @validator('courier_id')
    def courier_id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v

    @validator('courier_type')
    def courier_type_validation(cls, v: str):
        if v in CouriersService.courier_types.items():
            raise ValueError('Unknown courier type')
        return v


class CourierToRegion(BaseModel):
    courier_id: int
    region_id: int

    @validator('region_id')
    def region_id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v
