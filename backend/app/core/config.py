from typing import List, Optional, Any
from pydantic import field_validator, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
import json


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://tasktracker:tasktracker_password_2024@localhost:5432/tasktracker"

    # Redis
    REDIS_URL: str = "redis://:redis_password_2024@localhost:6379/0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars-long-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:5173","http://localhost","http://127.0.0.1","http://127.0.0.1:3000","http://127.0.0.1:5173"]'

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string"""
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["http://localhost:3000", "http://localhost:5173"]

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Tracker"
    VERSION: str = "1.0.0"

    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = "Task Tracker"

    # Sentry
    SENTRY_DSN: Optional[str] = None

    # Files
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx", ".xls", ".xlsx"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # Default admin bootstrap
    DEFAULT_ADMIN_EMAIL: Optional[str] = "admin@example.com"
    DEFAULT_ADMIN_USERNAME: Optional[str] = "admin"
    DEFAULT_ADMIN_PASSWORD: Optional[str] = "Admin123!"
    DEFAULT_ADMIN_FIRST_NAME: Optional[str] = "Admin"
    DEFAULT_ADMIN_LAST_NAME: Optional[str] = "User"


settings = Settings()
