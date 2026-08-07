from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Peel API"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    APP_URL: str
    DATABASE_URL: str

    SECRET_KEY: str = Field(..., min_length=1)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CLOUD_NAME: str = Field(..., min_length=1)
    CLOUD_API_KEY: str = Field(..., min_length=1)
    CLOUD_API_SECRET: str = Field(..., min_length=1)

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_postgres_url(cls, v: str) -> str:
        if not v.startswith("postgresql+asyncpg://"):
            raise ValueError("DATABASE_URL deve começar com 'postgresql+asyncpg://'")
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()