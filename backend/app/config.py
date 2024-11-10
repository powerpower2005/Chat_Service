from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class CORSSettings(BaseSettings):
    origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]

class Settings(BaseSettings):
    # Database settings
    db_name: str = "chat_db"
    mongodb_url: str = "mongodb://mongodb:27017"
    mongodb_database: str = "chatapp"
    redis_url: str = "redis://localhost:6379"
    
    # API server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Security settings
    secret_key: str = "your-secure-secret-key-here"
    access_token_expire_minutes: int = 60
    jwt_algorithm: str = "HS256"
    
    # CORS settings
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    
    cors_settings: CORSSettings = CORSSettings()
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

settings = Settings()