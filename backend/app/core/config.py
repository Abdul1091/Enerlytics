from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Enerlytics API"
    APP_DESCRIPTION: str = (
        "Backend service for the Enerlytics platform."
    )
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD_HASH: str


settings = Settings()

class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.test",
        extra="ignore",
    )