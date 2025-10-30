"""
Core configuration for SHIELD Backend Application
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "SHIELD Security Analysis API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "shield-secret-key-change-in-production")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:5500",  # Live Server default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5500",
        "file://",  # For local HTML files
    ]
    
    # Future Integration Points
    # Phase 1: AI Model Configuration
    AI_MODEL_PATH: str = os.getenv("AI_MODEL_PATH", "./models/")
    AI_MODEL_TIMEOUT: int = int(os.getenv("AI_MODEL_TIMEOUT", "30"))
    
    # Phase 2: Honeypot Configuration
    HONEYPOT_ENABLED: bool = os.getenv("HONEYPOT_ENABLED", "false").lower() == "true"
    HONEYPOT_SESSION_TIMEOUT: int = int(os.getenv("HONEYPOT_SESSION_TIMEOUT", "1800"))  # 30 minutes
    HONEYPOT_LOG_PATH: str = os.getenv("HONEYPOT_LOG_PATH", "./logs/honeypot/")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "shield.log")
    
    class Config:
        env_file = ".env"


settings = Settings()