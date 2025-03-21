from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Create lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Nothing to do here
    yield
    # Shutdown: Nothing to do here

app = FastAPI(title="ML Service", lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(
    router, 
    prefix="/ml", 
    tags=["ML"]
)

# Public health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
