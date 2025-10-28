from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database - defaults to SQLite for easy setup
    database_url: str = "sqlite:///./skillconnect.db"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # App
    app_name: str = "SkillConnect"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()