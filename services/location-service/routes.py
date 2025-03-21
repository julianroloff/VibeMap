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
import httpx

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

    # Trigger training
    async with httpx.AsyncClient() as client:
        locations_result = await db.execute(select(Location))  # Get all locations
        all_locations = locations_result.scalars().all()

        # Cleaned payload without geom
        location_payloads = [
            {
                "id": loc.id,
                "userId": loc.user_Id,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "stress_level": int(loc.stress_level),
                "comment": loc.comment
            }
            for loc in all_locations
        ]

        train_payload = {
            "force_retrain": True,
            "locations": location_payloads
        }

        await client.post("http://localhost:8004/ml/train", json=train_payload)

    return new_location

@router.get("/locations/")
async def get_locations(user_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Location))
    locations = result.scalars().all()

    location_payloads = [
        {
            "id": loc.id,
            "userId": loc.user_Id,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "stress_level": int(loc.stress_level),
            "comment": loc.comment,
            # "geom": to_shape(loc.geom).wkt  # Optional if you want to send geometry as WKT
        }
        for loc in locations
    ]

    # If user_id is provided → personalized prediction
    if user_id is not None:
        async with httpx.AsyncClient() as client:
            predict_payload = {
                "user_id": user_id,
                "locations": location_payloads
            }

            response = await client.post("http://localhost:8004/ml/predict", json=predict_payload)
            if response.status_code == 200:
                return response.json()["predictions"]
            else:
                raise HTTPException(status_code=500, detail="Prediction failed")

    # Otherwise return original location data
    return location_payloads


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


