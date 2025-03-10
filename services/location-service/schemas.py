from pydantic import BaseModel
from typing import Optional

class LocationCreate(BaseModel):
    latitude: float
    longitude: float
    stress_level: float
    comment: Optional[str]

class LocationResponse(LocationCreate):
    id:int
    user_Id: int

    class Config:
        from_attributes = True