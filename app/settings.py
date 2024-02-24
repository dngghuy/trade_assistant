import os

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import final
from dotenv import load_dotenv

load_dotenv()


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.prod.env', '.dev.env'),  # first search .dev.env, then .prod.env
        env_file_encoding='utf-8'
    )
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE", "")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "")


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
