from pydantic import BaseModel, validator

courier_types = {
    'foot': 1,
    'bike': 1,
    'car': 1,
}


class Courier(BaseModel):
    courier_id: int
    courier_type: str

    @validator('courier_id')
    def courier_id_validation(cls, v: int):
        if not (v >= 0 and isinstance(v, int)):
            raise ValueError('Id must be positive integer')
        return v

    @validator('courier_type')
    def courier_type_validation(cls, v: str):
        if v not in courier_types:
            raise ValueError('Unknown courier type')
        return v


class CourierToRegion(BaseModel):
    courier_id: int
    region_id: int

    @validator('courier_id', 'region_id')
    def id_validation(cls, v: int):
        if not (v >= 0 and isinstance(v, int)):
            raise ValueError('Id must be positive integer')
        return v


class CourierInCreate(Courier):
    regions: list
    working_hours: list

    @validator('regions', 'working_hours')
    def list_validation(cls, v: list):
        if not len(v) > 0:
            raise ValueError('Field can\'t be empty')
        return v
