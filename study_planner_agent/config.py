import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Application Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_DIR = os.getenv("DATA_DIR", "./data")
START_DATE = os.getenv("START_DATE", "2025-11-21")

# Constants
DIFFICULTY_MULTIPLIERS = {
    "high": 1.5,
    "medium": 1.0,
    "low": 0.7
}

SESSION_DEFAULTS = {
    "duration": 2,  # hours
    "break_duration": 15,  # minutes
    "max_daily_hours": 5
}

PEAK_HOURS_MAP = {
    "morning": 8,    # 08:00
    "afternoon": 14, # 14:00
    "evening": 18    # 18:00
}
