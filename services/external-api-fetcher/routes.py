from fastapi import APIRouter
from fetchers import fetch_sport_park
from schemas import SportParkList

router = APIRouter()

@router.get("/sport/", response_model=SportParkList)
def fetch_sport_data():
    sport_parks = fetch_sport_park()
    return {"sport_parks": sport_parks}  # Wrap it inside a dictionary
