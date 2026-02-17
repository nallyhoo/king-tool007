
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Union
from slowapi import Limiter
from slowapi.util import get_remote_address

class Settings(BaseSettings):
    PROJECT_NAME: str = "Video Manager"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./videomanager.db"

    # JWT
    SECRET_KEY: str = "a_very_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Rate Limiting
    RATELIMIT_DEFAULT: str = "100/minute"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATELIMIT_DEFAULT])
