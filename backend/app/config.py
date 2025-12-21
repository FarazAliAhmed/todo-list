"""
Configuration module for the FastAPI backend.
Loads environment variables and provides configuration settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/todo_db"

    # JWT Configuration - accepts JWT_SECRET or BETTER_AUTH_SECRET
    jwt_secret: str = "your-secret-key-change-in-production"
    better_auth_secret: str = ""  # Alternative secret name
    jwt_algorithm: str = "HS256"
    jwt_expiration_days: int = 7

    # CORS - comma-separated string that will be split into a list
    cors_origins: str = "http://localhost:3000"

    # API Configuration
    api_prefix: str = "/api"

    # OpenAI Configuration
    openai_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def effective_jwt_secret(self) -> str:
        """Get the effective JWT secret - prefer better_auth_secret if set."""
        if self.better_auth_secret:
            return self.better_auth_secret
        return self.jwt_secret


settings = Settings()
