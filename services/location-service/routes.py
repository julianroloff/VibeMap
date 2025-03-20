from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, func
from models import Location
from schemas import LocationCreate, LocationResponse
from dependencies import get_db, get_current_user
from geoalchemy2.functions import ST_Point
from typing import Optional
from fastapi import Query

router = APIRouter()

#Create new location entry
@router.post("/locations/", response_model=LocationResponse)
async def add_location(
    location: LocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    new_location = Location(
        user_Id = current_user["user_id"], 
        latitude = location.latitude,
        longitude = location.longitude,
        stress_level = location.stress_level,
        comment = location.comment,
        geom = ST_Point(location.longitude, location.latitude)
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return new_location

# Get all locations
@router.get("/locations/")
async def get_locations(user_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Location.id,
            Location.user_Id,
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
            "userId": row.user_Id,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "stress_level": row.stress_level,
            "comment": row.comment,
            "geom": row.geom  # GeoJSON format (string)
        }
        for row in result
    ]

    if user_id is not None:
        print(f"DEBUG: Received user_id: {user_id}")

    print(f"DEBUG: Retrieved locations: {locations}")  # Debug output
    return locations

@router.get("/locations/user/{user_id}")
async def get_user_location(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(
            Location.id,
            Location.user_Id,
            Location.latitude,
            Location.longitude,
            Location.stress_level,
            Location.comment,
            func.ST_AsGeoJSON(Location.geom).label("geom")  # Convert geometry to GeoJSON
        ).where(Location.user_Id == user_id)
    )

    locations = [
        {
            "id": row.id,
            "userId": row.user_Id,
            "latitude": row.latitude,
            "longitude": row.longitude,
            "stress_level": row.stress_level,
            "comment": row.comment,
            "geom": row.geom  # GeoJSON format (string)
        }
        for row in result
    ]

    print(f"DEBUG: Retrieved locations for user {user_id}: {locations}")  # Debug output
    return locations


