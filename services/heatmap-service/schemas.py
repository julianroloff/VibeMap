from pydantic import BaseModel
from typing import List

class HeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    aggregated_stress: float

class HeatmapResponse(BaseModel):
    points: List[HeatmapPoint]