from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения"""

    # API
    API_V1_STR: str = "/api/v1"

    # Database
    database_url: str

    # Security
    secret_key: str
    webhook_secret_key: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Игнорировать дополнительные поля из .env


settings = Settings()  # type: ignore[call-arg]
