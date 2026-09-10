"""
core/config.py
Centralized configuration loaded from environment variables (.env).
No secrets are hardcoded here.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str = "sqlite:///./lead_analyzer.db"
    MODEL_DIR: str = "ml/models"

    class Config:
        env_file = ".env"


settings = Settings()
