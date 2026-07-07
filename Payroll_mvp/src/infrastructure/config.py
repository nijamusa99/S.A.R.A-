import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    llm_model: str = os.getenv("LLM_MODEL", "llama3.1:8b")
    withholding_rate: float = 0.11

    class Config:
        env_file = ".env"

settings = Settings()