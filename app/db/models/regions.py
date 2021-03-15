from pydantic import BaseModel


class Region(BaseModel):
    region_id: int
    region_name: str
