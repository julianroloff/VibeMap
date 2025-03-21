from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class Location(BaseModel):
    id: int
    userId: int
    latitude: float
    longitude: float
    stress_level: int
    comment: Optional[str] = None
    geom: Optional[str] = None

class LocationWithPrediction(Location):
    predicted_stress_level: int

class PredictionRequest(BaseModel):
    user_id: Optional[int] = None
    locations: List[Location]

class PredictionResponse(BaseModel):
    predictions: List[LocationWithPrediction]

class TrainingRequest(BaseModel):
    force_retrain: bool = True
    user_id: Optional[int] = None
    locations: List[Location] = []

class TrainingResponse(BaseModel):
    success: bool
    message: str
    num_locations: int

class HealthResponse(BaseModel):
    status: str

class ModelMetadataResponse(BaseModel):
    id: int
    model_name: str
    version: str
    accuracy: float
    num_samples: int
    created_at: str 