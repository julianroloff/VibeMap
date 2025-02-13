from pydantic import BaseModel
from typing import Optional

class LocationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    stress_level: float

class LocationResponse(LocationCreate):
    id:int

    class Config:
        from_attributes = True