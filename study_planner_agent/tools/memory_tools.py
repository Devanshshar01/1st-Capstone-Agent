import json
import os
from typing import Dict, Any, List, Optional
from config import DATA_DIR

def save_user_profile(user_id: str, profile_data: Dict[str, Any]) -> bool:
    """
    Create/update user profile.
    """
    filepath = os.path.join(DATA_DIR, "users", f"{user_id}.json")
    try:
        with open(filepath, 'w') as f:
            json.dump(profile_data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False

def load_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Retrieve complete user data.
    """
    filepath = os.path.join(DATA_DIR, "users", f"{user_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def update_study_preferences(user_id: str, preference_updates: Dict[str, Any]) -> bool:
    """
    Modify specific preferences.
    """
    profile = load_user_profile(user_id)
    if "preferences" not in profile:
        profile["preferences"] = {}
    
    profile["preferences"].update(preference_updates)
    return save_user_profile(user_id, profile)

def get_conversation_context(session_id: str, last_n: int = 10) -> List[Dict[str, Any]]:
    """
    Retrieve conversation history.
    """
    # Mock implementation
    return []

def store_session_memory(session_id: str, interaction_data: Dict[str, Any]) -> bool:
    """
    Save agent interactions.
    """
    # Mock implementation
    return True

def get_user_stats(user_id: str) -> Dict[str, Any]:
    """
    Calculate user statistics.
    """
    return {
        "total_sessions": 12,
        "total_hours": 24.5,
        "current_streak": 3
    }
