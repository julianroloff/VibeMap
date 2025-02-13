from fastapi import APIRouter, Depends
from dependencies import fetch_location_data
import numpy as np
from schemas import HeatmapResponse, HeatmapPoint

router = APIRouter()

# Generate heatmap data
@router.get("/heatmap/", response_model=HeatmapResponse)
async def get_heatmap():
    location_data = await fetch_location_data()

    if not location_data:
        return {"points": []}
    
    # Convert data into numpy array for processing
    locations = np.array([[loc["latitude"], loc["longitude"], loc["stress_level"]] for loc in location_data])

    unique_locations = {}
    for lat, lon, stress in locations:
        key = (lat, lon)
        if key not in unique_locations:
            unique_locations[key] = []
            unique_locations[key].append(stress)

    heatmap_points = [
        HeatmapPoint(latitude = lat, longitude = lon, aggregated_stress = np.mean(stress))
        for (lat, lon), stresses in unique_locations.items()
    ]

    return {"points": heatmap_points}
