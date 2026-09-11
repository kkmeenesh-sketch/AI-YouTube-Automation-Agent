"""
Configuration Management for AI YouTube Automation Agent

This module handles all configuration settings, environment variables,
and application-wide settings.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# Base Paths
# ============================================
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
LOGS_DIR = BASE_DIR / os.getenv("LOGS_DIR", "logs")
TEMP_DIR = BASE_DIR / os.getenv("TEMP_DIR", "temp")
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_DIR", "output")

# Create necessary directories
for directory in [DATA_DIR, LOGS_DIR, TEMP_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================
# Application Settings
# ============================================
APP_NAME = os.getenv("APP_NAME", "AI YouTube Automation Agent")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ============================================
# OpenAI Configuration
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))

# ============================================
# YouTube API Configuration
# ============================================
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
YOUTUBE_REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "http://localhost:8080/oauth2callback")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID", "")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
YOUTUBE_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

# YouTube Upload Settings
YOUTUBE_PRIVACY_STATUS = os.getenv("VIDEO_PRIVACY_STATUS", "private")
YOUTUBE_DEFAULT_LANGUAGE = os.getenv("VIDEO_DEFAULT_LANGUAGE", "en")
YOUTUBE_UPLOAD_TIMEOUT = int(os.getenv("VIDEO_UPLOAD_TIMEOUT", "600"))
YOUTUBE_MAX_RETRIES = int(os.getenv("VIDEO_MAX_RETRIES", "3"))

# ============================================
# Google Cloud Configuration
# ============================================
GOOGLE_CLOUD_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")

# ============================================
# Speech-to-Text Configuration
# ============================================
SPEECH_TO_TEXT_PROVIDER = os.getenv("SPEECH_TO_TEXT_PROVIDER", "google").lower()
GOOGLE_SPEECH_API_KEY = os.getenv("GOOGLE_SPEECH_API_KEY", "")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")

# Supported providers
SUPPORTED_STT_PROVIDERS = ["google", "assemblyai"]

# ============================================
# Video Generation Configuration
# ============================================
VIDEO_GENERATION_PROVIDER = os.getenv("VIDEO_GENERATION_PROVIDER", "google_vertex_ai").lower()
VIDEO_GENERATION_API_KEY = os.getenv("VIDEO_GENERATION_API_KEY", "")

# Supported providers (to be confirmed)
SUPPORTED_VIDEO_GENERATORS = [
    "google_vertex_ai",
    "d_id",
    "synthesia",
    "runway_ml",
    "custom"
]

# ============================================
# Thumbnail Generation Configuration
# ============================================
THUMBNAIL_GENERATOR = os.getenv("THUMBNAIL_GENERATOR", "dall_e").lower()
DALL_E_MODEL = os.getenv("DALL_E_MODEL", "dall-e-3")
THUMBNAIL_SIZE = os.getenv("THUMBNAIL_SIZE", "1280x720")
GENERATE_THUMBNAIL = os.getenv("GENERATE_THUMBNAIL", "True").lower() == "true"

# ============================================
# Database Configuration
# ============================================
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/automation.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# ============================================
# Scheduler Configuration
# ============================================
SCHEDULER_ENABLED = os.getenv("SCHEDULER_ENABLED", "True").lower() == "true"
SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "UTC")

# ============================================
# API Rate Limiting
# ============================================
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "100"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

# ============================================
# Proxy Configuration
# ============================================
HTTP_PROXY: Optional[str] = os.getenv("HTTP_PROXY", None)
HTTPS_PROXY: Optional[str] = os.getenv("HTTPS_PROXY", None)

PROXIES = {}
if HTTP_PROXY:
    PROXIES["http"] = HTTP_PROXY
if HTTPS_PROXY:
    PROXIES["https"] = HTTPS_PROXY

# ============================================
# Validation Functions
# ============================================
def validate_required_config() -> list:
    """
    Validate that all required configuration variables are set.
    
    Returns:
        list: List of missing configuration keys
    """
    required_keys = [
        ("OPENAI_API_KEY", OPENAI_API_KEY),
        ("YOUTUBE_CLIENT_ID", YOUTUBE_CLIENT_ID),
        ("YOUTUBE_CLIENT_SECRET", YOUTUBE_CLIENT_SECRET),
        ("YOUTUBE_CHANNEL_ID", YOUTUBE_CHANNEL_ID),
    ]
    
    missing = [key for key, value in required_keys if not value]
    return missing


def validate_stt_provider() -> bool:
    """Validate Speech-to-Text provider is supported."""
    return SPEECH_TO_TEXT_PROVIDER in SUPPORTED_STT_PROVIDERS


def validate_video_generator() -> bool:
    """Validate video generation provider is supported."""
    return VIDEO_GENERATION_PROVIDER in SUPPORTED_VIDEO_GENERATORS


# ============================================
# Configuration Summary
# ============================================
CONFIG_SUMMARY = {
    "app": {
        "name": APP_NAME,
        "version": APP_VERSION,
        "debug": DEBUG_MODE,
        "log_level": LOG_LEVEL,
    },
    "paths": {
        "base": str(BASE_DIR),
        "data": str(DATA_DIR),
        "logs": str(LOGS_DIR),
        "temp": str(TEMP_DIR),
        "output": str(OUTPUT_DIR),
    },
    "apis": {
        "openai_model": OPENAI_MODEL,
        "speech_provider": SPEECH_TO_TEXT_PROVIDER,
        "video_provider": VIDEO_GENERATION_PROVIDER,
        "thumbnail_generator": THUMBNAIL_GENERATOR,
    },
    "youtube": {
        "privacy_status": YOUTUBE_PRIVACY_STATUS,
        "language": YOUTUBE_DEFAULT_LANGUAGE,
        "upload_timeout": YOUTUBE_UPLOAD_TIMEOUT,
    },
    "features": {
        "scheduler_enabled": SCHEDULER_ENABLED,
        "rate_limit_enabled": RATE_LIMIT_ENABLED,
        "generate_thumbnail": GENERATE_THUMBNAIL,
    },
}


def print_config_summary():
    """Print configuration summary for debugging."""
    import json
    print("\n" + "="*50)
    print("Configuration Summary")
    print("="*50)
    print(json.dumps(CONFIG_SUMMARY, indent=2))
    print("="*50 + "\n")


if __name__ == "__main__":
    print_config_summary()
    missing = validate_required_config()
    if missing:
        print(f"⚠️  Missing configuration: {', '.join(missing)}")
    else:
        print("✅ All required configuration present")
