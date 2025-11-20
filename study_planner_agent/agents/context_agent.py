import logging
from typing import Dict, Any
from tools.memory_tools import save_user_profile, load_user_profile, update_study_preferences, get_user_stats

logger = logging.getLogger(__name__)

class ContextAgent:
    """
    Agent responsible for managing user profiles and memory.
    """
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        logger.info("Context Agent initialized.")

    def get_profile(self, user_id: str) -> Dict[str, Any]:
        return load_user_profile(user_id)

    def save_profile(self, user_id: str, data: Dict[str, Any]) -> bool:
        return save_user_profile(user_id, data)
        
    def get_stats(self, user_id: str) -> Dict[str, Any]:
        return get_user_stats(user_id)
