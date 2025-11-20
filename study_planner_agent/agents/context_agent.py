import logging
from typing import Dict, Any, Optional
import json
import os

logger = logging.getLogger(__name__)

class ContextAgent:
    """
    Agent maintains user profiles and memory.
    """
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.users_dir = os.path.join(data_dir, "users")
        logger.info("Context Agent initialized.")

    def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieves user context/profile.
        """
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                return json.load(f)
        return {}

    def update_user_context(self, user_id: str, data: Dict[str, Any]):
        """
        Updates user context.
        """
        user_file = os.path.join(self.users_dir, f"{user_id}.json")
        # Merge or overwrite logic here
        with open(user_file, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Updated context for user {user_id}")
