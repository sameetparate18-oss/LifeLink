from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import secrets


class Settings(BaseSettings):

    # =========================================================
    # PROJECT INFORMATION
    # =========================================================

    PROJECT_NAME: str = "LifeLink AI"

    PROJECT_DESCRIPTION: str = (
        "AI Powered Emergency Blood & Organ Donation System"
    )

    VERSION: str = "3.0.0"

    API_V1_PREFIX: str = "/api/v1"

    DEBUG: bool = True

    ENVIRONMENT: str = "development"

    # =========================================================
    # SERVER CONFIGURATION
    # =========================================================

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    RELOAD: bool = True

    # =========================================================
    # DATABASE CONFIGURATION
    # =========================================================

    DATABASE_URL: str = (
        "postgresql://postgres:password@localhost/lifelink_db"
    )

    DATABASE_POOL_SIZE: int = 20

    DATABASE_MAX_OVERFLOW: int = 30

    DATABASE_ECHO: bool = False

    # =========================================================
    # SECURITY CONFIGURATION
    # =========================================================

    SECRET_KEY: str = secrets.token_urlsafe(64)

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    PASSWORD_MIN_LENGTH: int = 8

    # =========================================================
    # JWT / AUTH SETTINGS
    # =========================================================

    TOKEN_TYPE: str = "Bearer"

    AUTH_HEADER_NAME: str = "Authorization"

    # =========================================================
    # CORS SETTINGS
    # =========================================================

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]

    ALLOW_CREDENTIALS: bool = True

    ALLOW_METHODS: List[str] = ["*"]

    ALLOW_HEADERS: List[str] = ["*"]

    # =========================================================
    # AI ENGINE SETTINGS
    # =========================================================

    AI_MODEL_NAME: str = "LifeLink-NeuralNet-v3"

    AI_MODEL_VERSION: str = "3.1"

    AI_PREDICTION_THRESHOLD: float = 0.85

    AI_MATCHING_ENABLED: bool = True

    AI_EMERGENCY_PRIORITY_ENABLED: bool = True

    # =========================================================
    # BLOOD & ORGAN DONATION SETTINGS
    # =========================================================

    MAX_DONOR_DISTANCE_KM: int = 50

    MAX_EMERGENCY_PRIORITY: int = 10

    BLOOD_ASSIGNMENT_ENABLED: bool = True

    ORGAN_ASSIGNMENT_ENABLED: bool = True

    AUTO_MATCHING_ENABLED: bool = True

    # =========================================================
    # GAMIFICATION SYSTEM
    # =========================================================

    ENABLE_REWARD_SYSTEM: bool = True

    REWARD_POINTS_BLOOD_DONATION: int = 10

    REWARD_POINTS_ORGAN_DONATION: int = 20

    REWARD_POINTS_EMERGENCY_HELP: int = 30

    # =========================================================
    # ALERT SYSTEM
    # =========================================================

    ENABLE_SMS_ALERTS: bool = False

    ENABLE_EMAIL_ALERTS: bool = False

    ENABLE_PUSH_NOTIFICATIONS: bool = True

    ALERT_COOLDOWN_SECONDS: int = 60

    # =========================================================
    # RATE LIMITING
    # =========================================================

    RATE_LIMIT_ENABLED: bool = True

    REQUESTS_PER_MINUTE: int = 100

    # =========================================================
    # FILE UPLOAD SETTINGS
    # =========================================================

    MAX_UPLOAD_SIZE_MB: int = 10

    ALLOWED_FILE_TYPES: List[str] = [
        "jpg",
        "jpeg",
        "png",
        "pdf"
    ]

    # =========================================================
    # LOGGING SETTINGS
    # =========================================================

    LOG_LEVEL: str = "INFO"

    LOG_FILE: str = "lifelink.log"

    ENABLE_ACCESS_LOGS: bool = True

    # =========================================================
    # CACHE SETTINGS
    # =========================================================

    CACHE_ENABLED: bool = True

    CACHE_EXPIRATION_SECONDS: int = 300

    # =========================================================
    # STREAMLIT FRONTEND SETTINGS
    # =========================================================

    FRONTEND_TITLE: str = "LifeLink AI Dashboard"

    FRONTEND_THEME: str = "dark"

    FRONTEND_ANIMATIONS: bool = True

    # =========================================================
    # HEALTH MONITORING
    # =========================================================

    HEALTH_CHECK_ENABLED: bool = True

    SYSTEM_MONITOR_INTERVAL: int = 30

    # =========================================================
    # ENVIRONMENT FILE
    # =========================================================

    class Config:

        env_file = ".env"

        case_sensitive = True

        extra = "ignore"


# =========================================================
# CACHED SETTINGS INSTANCE
# =========================================================

@lru_cache()
def get_settings():

    return Settings()


settings = get_settings()