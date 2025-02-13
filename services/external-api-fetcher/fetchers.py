import requests
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from config import SPORT_PARK_API_URL
from pyproj import Transformer
from models import APILocation
from dependencies import get_db

# Transform coordinates from RD New (EPSG:28992) to WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326", always_xy=True)

async def fetch_and_save_sport_parks(db: AsyncSession):
    """Fetches sport park data and saves it to the database"""
    url = f"{SPORT_PARK_API_URL}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        sport_parks = []

        for park in data.get("_embedded", {}).get("park", []):  # Fix key to "park"
            name = park.get("omschrijving")  # Fix key to "omschrijving"
            sport = park.get("objectsubtype")  # Fix key to "objectsubtype"
            
            # Extract first coordinate from MultiPolygon
            try:
                rd_x, rd_y = park["geometry"]["coordinates"][0][0][0]  # Get first point
                lon, lat = transformer.transform(rd_x, rd_y)  # Convert to lat/lon
            except (KeyError, IndexError, TypeError):
                continue  # Skip if coordinates are missing

            # Avoid duplicates
            existing = (await db.execute(select(APILocation).filter(APILocation.id == park.get("id")))).scalars().first()
            if existing:
                continue

            new_park = APILocation(
                id=park.get("id"),
                name=name,
                sport=sport,
                latitude=lat,
                longitude=lon,
                geom=f"POINT({lon} {lat})"
            )
            db.add(new_park)
            sport_parks.append(new_park)

        await db.commit()
        return sport_parks

    return []
