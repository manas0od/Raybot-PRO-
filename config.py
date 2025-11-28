# config.py — Raybot PRO Configuration

import os

# Load OpenAI key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# SQLite database path
DB_PATH = os.environ.get("RAYBOT_DB", "raybot_v2.sqlite")

# Whisper model name (tiny, base, small, medium, large)
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "tiny")

# Force offline mode (FOR KAGGLE)
# Set:   RAYBOT_OFFLINE=1   to disable all external LLM calls
OFFLINE_ONLY = os.environ.get("RAYBOT_OFFLINE", "0") in ("1", "true", "True")

# App title
APP_TITLE = "Raybot PRO — Multi-Agent Demo"