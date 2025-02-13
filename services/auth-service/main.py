from fastapi import FastAPI
from routes import router

app = FastAPI(title="Authentication Service")

app.include_router(router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)