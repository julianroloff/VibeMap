from pydantic import BaseModel
from typing import List

class SportParkData(BaseModel):
    id: int
    name: str
    sport: str
    latitude: float
    longitude: float

class SportParkList(BaseModel):
    sport_parks: List[SportParkData]  # Expecting a list, not a single object
