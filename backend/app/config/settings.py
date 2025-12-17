from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True

    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # Neon Database
    NEON_HOST: str
    NEON_PORT: int
    NEON_USER: str
    NEON_PASSWORD: str
    NEON_DB: str

    # LLM - Choose ONE
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7

    # Paths
    TEXTBOOK_PATH: str = "../docs"
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()