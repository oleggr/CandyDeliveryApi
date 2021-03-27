from pydantic import BaseModel, validator


class Region(BaseModel):
    region_id: int
    region_name: str

    @validator('region_id')
    def region_id_validation(cls, v: int):
        if v >= 0 and isinstance(v, int):
            raise ValueError('Id must be positive integer')
        return v
