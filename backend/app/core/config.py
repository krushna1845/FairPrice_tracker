# ══════════════════════════════════════════════════════════════
#  core/config.py  —  App Configuration & Environment Variables
#
#  Reads values from the .env file automatically.
#  Use `settings.VARIABLE_NAME` anywhere in the app to access them.
#
#  Example:
#    from app.core.config import settings
#    print(settings.APP_NAME)   →  "Market Buddy API"
# ══════════════════════════════════════════════════════════════

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # ── App Info ───────────────────────────────────────────────
    APP_NAME: str = "Market Buddy API"
    DEBUG: bool = False

    # ── Database ───────────────────────────────────────────────
    # Full PostgreSQL connection string
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/marketbuddy"

    # ── JWT Authentication ─────────────────────────────────────
    SECRET_KEY: str = "change-this-to-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # ── CORS ───────────────────────────────────────────────────
    # List of frontend URLs that are allowed to call this API
    CORS_ORIGINS: List[str] = [
        "https://market-buddy-kappa.vercel.app",  # Production frontend
        "http://localhost:3000",                  # Local React dev server
        "http://localhost:5173",                  # Local Vite dev server
        "http://localhost:8080",                  # Local Vite dev server (current)
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # ── Redis ──────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379"

    class Config:
        # Automatically reads from the .env file
        env_file = ".env"


# Create a single shared instance used throughout the app
settings = Settings()
