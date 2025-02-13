from fastapi import FastAPI
from routes import router

app = FastAPI(title="External API Fetcher")

app.include_router(router, prefix="/external", tags=["External Data"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)