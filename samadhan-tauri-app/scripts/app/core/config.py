from typing import List
from pydantic_settings import BaseSettings
import secrets
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Samadhan API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for Samadhan Application"
    API_V1_STR: str = "/api/v1"
    
    # API Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 5000
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DB_HOST: str = "127.0.0.1"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "samadhandb"
    SQLALCHEMY_DATABASE_URI: str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:1420",  # Tauri dev server
        "http://localhost:5000",  # FastAPI server
        "tauri://localhost",      # Tauri app
    ]
    
    # Redis (for caching)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 