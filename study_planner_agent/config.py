import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration Constants
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
DATA_DIR = os.getenv("DATA_DIR", "./data")

# Validation
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in environment variables.")

# Ensure data directories exist
USERS_DIR = os.path.join(DATA_DIR, "users")
SCHEDULES_DIR = os.path.join(DATA_DIR, "schedules")

os.makedirs(USERS_DIR, exist_ok=True)
os.makedirs(SCHEDULES_DIR, exist_ok=True)

# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("agent.log")
    ]
)

logger = logging.getLogger("StudyPlannerAgent")
logger.info("Configuration loaded successfully.")
