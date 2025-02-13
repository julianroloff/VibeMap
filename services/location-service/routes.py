from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, func
from models import Location
from schemas import LocationCreate, LocationResponse
from dependencies import get_db
from geoalchemy2.functions import ST_Point

router = APIRouter()

#Create a new location entry
@router.post("/locations/", response_model=LocationResponse)
async def add_location(location: LocationCreate, db: AsyncSession = Depends(get_db)):
    new_location = Location(
        name = location.name,
        latitude = location.latitude,
        longitude = location.longitude,
        stress_level = location.stress_level,
        geom = ST_Point(location.longitude, location.latitude) # this stores a location as a point in PostGIS
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return new_location

# Get all locations
@router.get("/locations/")
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Location.id,
            Location.name,
            Location.latitude,
            Location.longitude,
            Location.stress_level,
            Location.comment,
            func.ST_AsGeoJSON(Location.geom).label("geom")  # Convert geometry to GeoJSON
        )
    )

    locations = [
        {
            "id": row.id,
            "name": row.name,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "stress_level": row.stress_level,
            "comment": row.comment,
            "geom": row.geom  # GeoJSON format (string)
        }
        for row in result
    ]

    print(f"DEBUG: Retrieved locations: {locations}")  # Debug output
    return locations

