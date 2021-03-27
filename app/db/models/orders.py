from pydantic import BaseModel, validator


class Order(BaseModel):
    order_id: int
    weight: float
    region_id: int
    is_ready: bool
    complete_time: int

    @validator('order_id', 'region_id')
    def id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v

    @validator('weight')
    def weight_validation(cls, v: float):
        if v >= 0 and isinstance(v, float):
            raise ValueError('Weight must be positive float')
        return v


class OrderAssign(BaseModel):
    assign_id: int
    courier_id: int
    order_id: int
    assign_time: int

    @validator('courier_id', 'order_id')
    def id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v
