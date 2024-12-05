from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


# 継承元の型がAnyなため、ignoreを指定
class Settings(BaseSettings):  # type: ignore
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    PROJECT_NAME: str = "FastAPI"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    BACKEND_CORS_ORIGINS: list[str] = []
    DYNAMO_DB_POLING_TABLE: str = ""
    DYNAMO_DB_PUSH_TABLE: str = ""
    ANTHROPIC_API_KEY_1: str = ""


settings = Settings()
