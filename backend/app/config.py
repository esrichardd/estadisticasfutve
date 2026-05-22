from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Base de datos
    database_url: str

    # Entorno (development | production)
    environment: str = "development"

    # CORS — orígenes permitidos para el frontend
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Instancia global — el resto del código importa esto directamente:
#   from app.config import settings
settings = Settings()
