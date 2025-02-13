from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dependencies import get_db
from models import APILocation
from schemas import SportParkList

from fetchers import fetch_and_save_sport_parks

router = APIRouter()

@router.get("/sport/fetch")
async def fetch_sport_data(db: AsyncSession = Depends(get_db)):
    await fetch_and_save_sport_parks(db)  # Fetch and store data
    return {"message": "Data fetched successfully"}





@router.get("/sport", response_model=SportParkList)
async def get_stored_sport_parks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(APILocation))
    parks = result.scalars().all()

    # Convert ORM objects to plain dictionaries before returning
    serialized_parks = []
    for park in parks:
        serialized_parks.append({
            "id": park.id,
            "name": park.name,
            "sport": park.sport,
            "latitude": park.latitude,
            "longitude": park.longitude,
        })

    return {"sport_parks": serialized_parks}


