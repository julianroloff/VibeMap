import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    MODEL_DIR: str = os.getenv("MODEL_DIR", os.path.join(os.path.dirname(__file__), "models"))
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user1:test@localhost/ml_db")
    
    # Service URLs
    LOCATION_SERVICE_URL: str = os.getenv("LOCATION_SERVICE_URL", "http://localhost:8002")
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mysecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings() 