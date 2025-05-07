"""
config.py
환경 설정
"""

import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Voice Kiosk RAG API"
    APP_VERSION: str = "0.1.0"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "chroma_db")
    
    # MySQL 설정
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "mylio")

    class Config:
        env_file = ".env"


settings = Settings()