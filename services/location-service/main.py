from fastapi import FastAPI
from routes import router
from dependencies import engine, Base

app = FastAPI(title="Location Service")

app.include_router(router, prefix="/location", tags=["Location"])

# Create Database Table on Startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)