from pydantic import BaseModel


class Order(BaseModel):
    order_id: int
    weight: float
    region_id: int
    is_ready: bool
    complete_time: int


class OrderAssign(BaseModel):
    assign_id: int
    courier_id: int
    order_id: int
    assign_time: int
