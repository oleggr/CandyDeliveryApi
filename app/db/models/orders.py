from pydantic import BaseModel, validator, Field


class Order(BaseModel):
    order_id: int
    weight: float
    region_id: int = Field(None, alias='region')
    is_ready: bool = False
    complete_time: int = None
    assign_id: int = None

    @validator('order_id', 'region_id')
    def id_validation(cls, v: int):
        if not(v >= 0 and isinstance(v, int)):
            raise ValueError('Id must be positive integer')
        return v

    @validator('weight')
    def weight_validation(cls, v: float):
        if not (v >= 0 and isinstance(v, float)):
            raise ValueError('Weight must be positive float')
        return v


class OrderAssign(BaseModel):
    assign_id: int
    courier_id: int
    order_id: int
    assign_time: int

    @validator('courier_id', 'order_id')
    def id_validation(cls, v: int):
        if not (v >= 0 and isinstance(v, int)):
            raise ValueError('Id must be positive integer')
        return v


class OrderFull(Order):
    delivery_hours: list

    @validator('delivery_hours')
    def list_validation(cls, v: list):
        if not len(v) > 0:
            raise ValueError('Field can\'t be empty')
        return v

