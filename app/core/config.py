"""
Application Configuration
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Diary Orchestrator Agent"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    AWS_REGION: str = "us-east-1"
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
