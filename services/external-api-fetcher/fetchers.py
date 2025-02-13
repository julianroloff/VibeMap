import requests
from config import SPORT_PARK_API_URL
from pyproj import Transformer

# Transformer to convert RD coordinates (EPSG:28992) to Latitude/Longitude (EPSG:4326)
transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326", always_xy=True)

# Fetch sport park data
def fetch_sport_park():
    url = f"{SPORT_PARK_API_URL}openbaresportplek/"  # Ensure single slash
    response = requests.get(url)

    print(f"DEBUG: Requesting URL: {url}")  # Log the correct URL
    print(f"DEBUG: Response Status Code: {response.status_code}")
    print(f"DEBUG: Response JSON: {response.json()}")

    if response.status_code == 200:
        data = response.json()
        sport_parks = []

        for park in data.get("_embedded", {}).get("openbaresportplek", []):
            rd_x, rd_y = park["geometry"].get("coordinates", [None, None])
            if rd_x is not None and rd_y is not None:
                lon, lat = transformer.transform(rd_x, rd_y)  # Convert RD to Latitude/Longitude
            else:
                lon, lat = None, None  # Handle missing coordinates

            sport_parks.append({
                "id": park.get("id"),
                "name": park.get("naam"),
                "sport": park.get("sportvoorziening"),
                "latitude": lat,
                "longitude": lon
            })
        
        return sport_parks if sport_parks else []  # Return an empty list if no data
    
    return []  # Return an empty list instead of None
