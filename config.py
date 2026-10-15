"""
RescueVision AI - Configuration Module
Manages environment variables, security configurations, database paths, and upload settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load .env file from the base directory
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default-insecure-dev-key-change-in-prod")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Instance & Database setup
    INSTANCE_DIR = (BASE_DIR / "instance").resolve()
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

    db_env = os.getenv("DATABASE_URL")
    db_file = (INSTANCE_DIR / "rescuevision.db").resolve()

    if not db_env or "instance/rescuevision.db" in db_env:
        DATABASE_URL = f"sqlite:///{db_file.as_posix()}"
    elif db_env.startswith("postgres://"):
        DATABASE_URL = db_env.replace("postgres://", "postgresql://", 1)
    elif db_env.startswith("sqlite:///") and not db_env.startswith("sqlite:////"):
        # Resolve relative SQLite path to absolute posix path
        rel_path = db_env.replace("sqlite:///", "")
        abs_path = (BASE_DIR / rel_path).resolve()
        DATABASE_URL = f"sqlite:///{abs_path.as_posix()}"
    else:
        DATABASE_URL = db_env

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    } if not DATABASE_URL.startswith("sqlite") else {}

    # File uploads
    UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER", "uploads")
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "10")) * 1024 * 1024
    ALLOWED_EXTENSIONS = set(
        ext.strip().lower()
        for ext in os.getenv("ALLOWED_EXTENSIONS", "png,jpg,jpeg,webp").split(",")
    )

    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))

    # Admin credentials
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "RescueAdmin2026!")

    # External APIs
    ENABLE_USGS_EARTHQUAKES = os.getenv("ENABLE_USGS_EARTHQUAKES", "True").lower() in ("true", "1", "yes")
    ENABLE_OPEN_METEO_FLOODS = os.getenv("ENABLE_OPEN_METEO_FLOODS", "True").lower() in ("true", "1", "yes")
    ENABLE_NASA_EONET = os.getenv("ENABLE_NASA_EONET", "True").lower() in ("true", "1", "yes")
    ALERT_CACHE_HOURS = int(os.getenv("ALERT_CACHE_HOURS", "2"))

    # AI / LLM Configuration
    AI_PROVIDER = os.getenv("AI_PROVIDER", "demo_fallback").lower()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


class TestConfig(Config):
    """Configuration for automated test suite."""
    TESTING = True
    DEBUG = False
    # Use in-memory SQLite database for high speed & isolation during automated tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key-rescuevision"
