import requests
from config import LOCATION_SERVICE_URL

async def fetch_location_data():
    response = requests.get(f"{LOCATION_SERVICE_URL}/location/locations/")
    if response.status_code == 200:
        return response.json()
    return []


