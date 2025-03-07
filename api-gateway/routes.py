from fastapi import APIRouter
import requests

router = APIRouter()

# Service URLs

AUTH_SERVICE_URL = "http://localhost:8001"
LOCATION_SERVICE_URL = "http://localhost:8002"
HEATMAP_SERVICE_URL = "http://localhost:8003"
ML_SERVICE_URL = "http://localhost:8004"
EXTERNAL_API_FETCHER_URL = "http://localhost:8005"

@router.api_route("/auth/{path:path}", methods=["GET", "POST"])
def proxy_auth(path: str):
    return requests.get(f"{AUTH_SERVICE_URL}/{path}").json()

@router.get("/location/{path:path}")
def proxy_location(path: str):
    return requests.get(f"{LOCATION_SERVICE_URL}/{path}").json()

@router.get("/heatmap/{path:path}")
def proxy_heatmap(path: str):
    return requests.get(f"{HEATMAP_SERVICE_URL}/{path}").json()

@router.get("/ml/{path:path}")
def proxy_ml(path: str):
    return requests.get(f"{ML_SERVICE_URL}/{path}").json()

@router.get("external/{path:path}")
def proxy_external(path: str):
    return requests.get(f"{EXTERNAL_API_FETCHER_URL}/{path}").json()




