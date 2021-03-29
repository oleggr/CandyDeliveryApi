from pydantic import BaseModel, validator

from app.db.schema import CourierType

courier_types = {
    'foot': 10,
    'bike': 15,
    'car': 50,
}


class Courier(BaseModel):
    courier_id: int
    courier_type: CourierType

    @validator('courier_id')
    def courier_id_validation(cls, v: int):
        if not (v >= 0 and isinstance(v, int)):
            raise ValueError('Id must be positive integer')
        return v

    @validator('courier_type')
    def courier_type_validation(cls, v: CourierType):
        if v not in CourierType:
            raise ValueError('Unknown courier type')
        return str(v)


class CourierToRegion(BaseModel):
    courier_id: int
    region_id: int

    @validator('courier_id', 'region_id')
    def id_validation(cls, v: int):
        if not (v >= 0 and isinstance(v, int)):
            raise ValueError('Id must be positive integer')
        return v


class CourierFull(Courier):
    regions: list
    working_hours: list

    @validator('regions', 'working_hours')
    def list_validation(cls, v: list):
        if not len(v) > 0:
            raise ValueError('Field can\'t be empty')
        return v
