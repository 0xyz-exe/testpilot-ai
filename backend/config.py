from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    database_url: str = "sqlite:///./testpilot.db"
    secret_key: str = "dev-secret-change-in-production"
    allowed_origins: List[str] = ["http://localhost:3000"]
    artifact_storage_path: str = "./artifacts"
    max_test_timeout: int = 300
    default_test_timeout: int = 30
    max_retries: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings()
