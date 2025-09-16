from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@db:5432/wealthtech_db"
    tenant_id: int = 1
    embeddings_provider: str = "local"
    summarizer: str = "extractive"
    
    class Config:
        env_file = ".env"

settings = Settings()
