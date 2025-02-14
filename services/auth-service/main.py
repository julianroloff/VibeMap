from fastapi import FastAPI
from routes import router
from dependencies import engine, Base

app = FastAPI(title="Authentication Service")

app.include_router(router, prefix="/auth", tags=["Auth"])

# Create Database Table on Startup (Corrected)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
